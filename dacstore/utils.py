import pandas as pd
import requests
from io import StringIO

from .config import drop_cols, cleaning_dict, translation_columns, translation_answers

survey_id = 1837044
api_url = f"https://api.surveyhero.com/v1/surveys/{survey_id}/responses"


# a function that translates ascii regex to python regex


def strip_df(df):
    """strip leading and trailing whitespaces from all columns and headers"""
    df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    df.columns = df.columns.str.strip()
    return df


def strip_double_whitespaces(df):
    df.columns = df.columns.str.replace(r"\s+", " ", regex=True)
    return df


def value_counts(df, normalize=True):
    """Count values in colums"""
    counts = {}
    for c in df:
        counts[c] = df[c].value_counts(normalize=normalize).to_dict()
    return counts


def to_results(counts, categories, labels=None, fact=100):
    results = {}
    for question, data in counts.items():
        label = question
        if labels:
            label = labels.get(question) or question
        results[label] = [data.get(k, 0.0) * 100 for k in categories]
    return results


def get_data(
    source=None, user=None, password=None, postprocess=True, translate=True, drop=True
):
    """read csv from file or surveyhero api"""
    if source is None:
        # get data from surveyhero api
        # params = {"format": "csv", "status": "completed"}
        params = {"format": "csv"}
        r = requests.get(api_url, params=params, auth=(user, password))
        print(r.status_code)
        print(f"API request status code: {r.status_code}")
        source = StringIO(
            r.content.decode("utf-8").replace(
                "Direct Air Capture (DAC)\n", "Direct Air Capture (DAC)"
            )
        )

    print(f"reading from: {source}")

    df = pd.read_csv(
        source,
        index_col="ID",
        date_format="%d.%m.%Y %H:%M:%S",
        parse_dates=[1, 2],
        skipinitialspace=True,
    )

    df = strip_df(df)
    df = strip_double_whitespaces(df)
    df = df.replace(cleaning_dict)

    if translate:
        df = df.rename(columns=translation_columns)
        df = df.replace(translation_answers)

    if drop is True:
        df = df.drop(columns=drop_cols)

    if postprocess is True:
        df["completion_time"] = df["Last updated on"] - df["Started on"]

    df = strip_df(df)

    return df


def to_excel(df, filename):
    """Auto adjust column width and save to Excel file"""
    # create a pandas.ExcelWriter object
    writer = pd.ExcelWriter(filename, engine="xlsxwriter")

    # write the data frame to Excel
    df.to_excel(writer, index=False)

    # get the XlsxWriter workbook and worksheet objects
    # workbook = writer.book
    worksheet = writer.sheets["Sheet1"]

    # adjust the column widths based on the content
    for i, col in enumerate(df.columns):
        width = max(df[col].apply(lambda x: len(str(x))).max(), len(col))
        worksheet.set_column(i, i, width)

    # save the Excel file
    writer.close()
