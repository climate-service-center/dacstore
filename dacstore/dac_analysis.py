import pandas as pd


from dac_config import replacer, drop_cols, rename_cols


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


def get_df(filename):
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
    df = df.rename(columns=rename_cols)
    df = df.drop(columns=drop_cols)
    # replace words with values (laker scale)
    df = df.replace(replacer)
    df = add_completion_time(df)
    return df
