import pandas as pd


from dac_config import replacer, drop_cols, rename_cols, cleaning_dict, translation_columns, translation_answers


def strip_df(df):
    """strip leading and trailing whitespaces from all columns and headers"""
    df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    df.columns = df.columns.str.strip()
    return df


def add_completion_time(df):
    """compute completion time"""
    tformat = "%d.%m.%Y %H:%M:%S"
    df["completion_time"] = pd.to_datetime(
        df["Last updated on"], format=tformat, errors="coerce"
    ) - pd.to_datetime(df["Started on"], format=tformat, errors="coerce")
    return df.drop(columns=["Started on", "Last updated on"])


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
        results[label] = [data[k] * 100 for k in categories]
    return results


def get_df(filename, drop=True, translate=True):
    """open csv file and do some cleaning"""
    df = pd.read_csv(
        filename,
        index_col=0,
        parse_dates=True,
        date_format="%d.%m.%Y %H:%M:%S",
        sep=",",
        skipinitialspace=True,
    )
    df = strip_df(df)
    # df = df.rename(columns=rename_cols)
    df = df.replace(cleaning_dict)
    if translate:
        df = df.rename(columns=translation_columns)
        df = df.replace(translation_answers)
    if drop is True:
        df = df.drop(columns=drop_cols)
    # replace words with values (laker scale)
    # df = df.replace(replacer)
    df = add_completion_time(df)
    df = strip_df(df)
    return df
