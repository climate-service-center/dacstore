# Author: Lars Buntemeyer and Rodrigo Valencia (a little bit).
# Insitute: Climate Service Center Germany (GERICS).

import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor


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
    """Set no knowledge answers to neutral answers"""
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


def invert_agreement(df):
    return df.apply(lambda x: 5 - (x - 1))


def fix_risk_agreement(df):
    """Fix risk agreement values to get a consistent risk scale"""
    risk_fix = [
        "DAC ist sicher.",
        "CO2-Speicherung ist sicher.",
    ]
    df.loc[df.index, risk_fix] = invert_agreement(df[risk_fix])
    return df


def fix_cost_agreement(df):
    """Fix cost agreement values to get a consistent risk scale"""
    cost_fix = [
        "100 € für die Entnahme von 1 Tonne CO2 zu zahlen, ist ein angemessener Preis.",
    ]
    df.loc[df.index, cost_fix] = invert_agreement(df[cost_fix])
    return df


def fix_agreement(df):
    """Fix agreement values to get a consistent scale"""
    df = fix_risk_agreement(df)
    # df = fix_cost_agreement(df)
    return df


def multicollinearity(X):
    """Check for multicollinearity

    Multicollinearity occurs when independent variables in a regression model are correlated.
    This correlation is a problem because independent variables should be independent.

    """
    # Check for multicollinearity using VIF
    X = sm.add_constant(X)  # Add a constant to the model (intercept)
    vif_data = pd.DataFrame()
    vif_data["feature"] = X.columns
    vif_data["VIF"] = [
        variance_inflation_factor(X.values, i) for i in range(X.shape[1])
    ]
    return vif_data


def cronbach_alpha(df):
    """Calculate Cronbach's alpha

    Cronbach's alpha is a measure of internal consistency, that is,
    how closely related a set of items are as a group.

    """
    df = df.copy().dropna()
    # Number of items (questions)
    N = df.shape[1]
    # Variance of each item
    item_variances = df.var(axis=0, ddof=1)
    # Total variance of the sum of all items
    total_variance = df.sum(axis=1).var(ddof=1)
    # Cronbach's alpha calculation
    alpha = (N / (N - 1)) * (1 - (item_variances.sum() / total_variance))
    return alpha
