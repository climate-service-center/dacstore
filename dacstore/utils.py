import pandas as pd
import requests
from io import StringIO

from .config import drop_cols, cleaning_dict, translation_columns, translation_answers

survey_id = 1837044
api_url = f"https://api.surveyhero.com/v1/surveys/{survey_id}/responses"


report_cols = [
    "{id}",
    "Status",
    "Started on",
    "Geschlecht",
    "Altersgruppe",
    # "Höchster Bildungsabschluss",
    # "Beruf",
    "completion_time",
    "Bei dieser Frage ignorieren Sie bitte die folgenden Optionen und wählen Sie 'Stimme nicht zu'.",
    "valid",
]

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


def get_data(source=None, user=None, password=None, translate=True, drop=True):
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

    df["completion_time"] = df["Last updated on"] - df["Started on"]

    df = strip_df(df)

    return df


def report_to_excel(df, filename):
    """Auto adjust column width and save to Excel file"""
    # Create a pandas.ExcelWriter object
    # if engine == "openpyxl":
    from openpyxl.utils import get_column_letter
    from openpyxl.styles import PatternFill

    df = df.astype({"completion_time": str, "{id}": str})
    writer = pd.ExcelWriter(filename, engine="openpyxl")
    df = df[report_cols]
    df.to_excel(writer, index=True, sheet_name="Sheet1")

    # Get the XlsxWriter workbook and worksheet objectsk
    worksheet = writer.sheets["Sheet1"]

    # Adjust the column widths based on the content
    for i, col in enumerate(df.columns):
        # Calculate the maximum width for the column
        max_width = max(df[col].astype(str).map(len).max(), len(col))
        # Set the column width
        print(max_width)
        # worksheet.set_column(i+1, i+1, max_width)
        worksheet.column_dimensions[get_column_letter(i + 2)].width = max_width

    # writer.close()

    # workbook = load_workbook(filename=filename)
    # sheet = workbook["Sheet1"]
    sheet = worksheet

    colnames = ["valid", "Geschlecht"]

    col_indices = {
        cell.value: n
        for n, cell in enumerate(list(sheet.rows)[0])
        if cell.value in colnames
    }

    for row in sheet.iter_rows(min_row=1, max_row=None, min_col=None, max_col=None):
        if row[col_indices["valid"]].value != "valid":
            for cell in row:
                cell.fill = PatternFill(
                    start_color="FF001F", end_color="FF001F", fill_type="solid"
                )

    # workbook.save(filename=filename)
    writer.close()
