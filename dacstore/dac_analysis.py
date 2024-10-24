# Author: Lars Buntemeyer and Rodrigo Valencia (a little bit).
# Insitute: Climate Service Center Germany (GERICS).

import pandas as pd


from .config import (
    drop_cols,
    cleaning_dict,
    translation_columns,
    translation_answers,
    no_replacer,
)


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


def to_results(counts, categories=None, labels=None, fact=100):
    results = {}
    for question, data in counts.items():
        label = question
        if labels:
            label = labels.get(question) or question
        cats = categories or list(data.keys())
        print(cats)
        results[label] = [data.get(k, 0.0) * 100 for k in cats]
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


def compute_group_averages(df, groups):
    """Compute group averages from different groups and columns"""
    for k, v in groups.items():
        df[k] = df[v].mean(axis=1)
    return df


def set_dependent_questions(df):
    print("setting dependent question values...")
    depends = {
        "Haben Sie schon von Technologien zur Entnahme von Kohlendioxid (CO2) aus der Luft (auf Englisch Direct Air Capture (DAC)) gehört?": "Wie gut sind ihre Kenntnisse dieser Technologien?",
        "Haben Sie schon von Kohlendioxid (CO2)-Speicherung gehört?": "Wie gut sind ihre Kenntnisse der CO2-Speicherungstechnologien?",
    }
    # return depends
    for k, v in depends.items():
        df.loc[df[k] == "Nein", v] = no_replacer
    return df


def set_no_knowledge_to_neutral(df):
    distance = [
        "DAC Anlage",
        "CO2-Speicherung im Boden",
        "CO2-Speicherung im Meeresboden",
    ]
    dont_care = "Stimme weder zu noch lehne ich ab"
    neutral = "Neutral"
    dont_know = "Weiß nicht"
    cols = [c for c in df.columns if dont_know in df[c].unique()]
    for c in cols:
        if c in distance:
            # replace dont_know with "Nirgendwo in Deutschland"
            df.loc[df[c] == dont_know, c] = "Nirgendwo in Deutschland"
        elif dont_care in df[c].unique():
            # replace dont_know with "Stimme weder zu noch lehne ich ab"
            df.loc[df[c] == dont_know, c] = dont_care
        elif neutral in df[c].unique():
            # replace dont_know with "Neutral"
            df.loc[df[c] == dont_know, c] = neutral
    return df
