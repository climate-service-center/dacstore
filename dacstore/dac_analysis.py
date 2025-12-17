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
    """Strip leading/trailing whitespace from all string columns and headers.

    Parameters
    ----------
    df : pandas.DataFrame
        Input DataFrame possibly containing string columns with extraneous spaces.

    Returns
    -------
    pandas.DataFrame
        Cleaned DataFrame with stripped string values and column names.
    """
    df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    df.columns = df.columns.str.strip()
    return df


def add_completion_time(df):
    """Compute survey completion time from start and end timestamps.

    Expects columns "Started on" and "Last updated on" with format
    `%d.%m.%Y %H:%M:%S`. Adds a `completion_time` timedelta column and drops
    the original timestamp columns.

    Parameters
    ----------
    df : pandas.DataFrame
        Input survey DataFrame.

    Returns
    -------
    pandas.DataFrame
        DataFrame with `completion_time` and without the original timestamp columns.
    """
    tformat = "%d.%m.%Y %H:%M:%S"
    df["completion_time"] = pd.to_datetime(
        df["Last updated on"], format=tformat, errors="coerce"
    ) - pd.to_datetime(df["Started on"], format=tformat, errors="coerce")
    return df.drop(columns=["Started on", "Last updated on"])


def value_counts(df, normalize=True):
    """Count per-column value frequencies.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame whose columns will be tallied.
    normalize : bool, optional
        If True, return relative frequencies; else absolute counts. Default True.

    Returns
    -------
    dict[str, dict]
        Mapping column name -> value counts (or proportions).
    """
    counts = {}
    for c in df:
        counts[c] = df[c].value_counts(normalize=normalize).to_dict()
    return counts


def to_results(counts, categories=None, labels=None, fact=100):
    """Convert counts to ordered Likert result rows.

    Parameters
    ----------
    counts : dict
        Mapping of question -> value frequency dict.
    categories : list[str], optional
        Ordered category labels to align values.
    labels : dict[str, str], optional
        Mapping of original question text to shorter display labels.
    fact : float, optional
        Scaling factor (e.g., 100 to convert proportions to percentages). Default 100.

    Returns
    -------
    dict[str, list[float]]
        Mapping display label -> ordered list of values per category.
    """
    results = {}
    for question, data in counts.items():
        label = question
        if labels:
            label = labels.get(question) or question
        cats = categories or list(data.keys())
        results[label] = [data.get(k, 0.0) * 100 for k in cats]
    return results


def get_df(filename, drop=True, translate=True):
    """Load CSV and apply standard cleaning, translation, and pruning.

    Parameters
    ----------
    filename : str or pathlib.Path
        Path to the CSV file.
    drop : bool, optional
        Whether to drop columns defined in `config.drop_cols`. Default True.
    translate : bool, optional
        Whether to translate headers and answer labels using `config` maps. Default True.

    Returns
    -------
    pandas.DataFrame
        Cleaned and prepared survey DataFrame.
    """
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
    """Compute row-wise averages for specified column groups.

    Parameters
    ----------
    df : pandas.DataFrame
        Input survey DataFrame.
    groups : dict[str, list[str]]
        Mapping of new column name -> list of existing column names to average.

    Returns
    -------
    pandas.DataFrame
        DataFrame with new average columns added.
    """
    for k, v in groups.items():
        df[k] = df[v].mean(axis=1)
    return df


def set_dependent_questions(df):
    """Impose dependency rules: set knowledge responses based on awareness.

    If a respondent answered "No" to awareness questions, corresponding
    knowledge items are set to a predefined "no knowledge" value (`no_replacer`).

    Parameters
    ----------
    df : pandas.DataFrame
        Survey DataFrame.

    Returns
    -------
    pandas.DataFrame
        Updated DataFrame with dependent values set.
    """
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
    """Map "Don't know" to context-appropriate neutral or distance choices.

    Parameters
    ----------
    df : pandas.DataFrame
        Survey DataFrame possibly containing "Weiß nicht" responses.

    Returns
    -------
    pandas.DataFrame
        Updated DataFrame with neutralized values.
    """
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
    """Invert a 1–5 agreement scale to maintain consistent direction.

    Parameters
    ----------
    df : pandas.DataFrame
        Numeric 1–5 Likert items to invert.

    Returns
    -------
    pandas.DataFrame
        Inverted scale values.
    """
    return df.apply(lambda x: 5 - (x - 1))


def fix_risk_agreement(df):
    """Normalize risk-related items so higher values reflect greater risk.

    Parameters
    ----------
    df : pandas.DataFrame
        Survey DataFrame containing risk items.

    Returns
    -------
    pandas.DataFrame
        DataFrame with selected risk items inverted.
    """
    risk_fix = [
        "DAC ist sicher.",
        "CO2-Speicherung ist sicher.",
    ]
    df.loc[df.index, risk_fix] = invert_agreement(df[risk_fix])
    return df


def fix_cost_agreement(df):
    """Invert cost-related agreement items to align interpretation.

    Parameters
    ----------
    df : pandas.DataFrame
        Survey DataFrame containing cost items.

    Returns
    -------
    pandas.DataFrame
        DataFrame with selected cost items inverted.
    """
    cost_fix = [
        "100 € für die Entnahme von 1 Tonne CO2 zu zahlen, ist ein angemessener Preis.",
    ]
    df.loc[df.index, cost_fix] = invert_agreement(df[cost_fix])
    return df


def fix_agreement(df):
    """Apply normalization across agreement items for consistent scales.

    Parameters
    ----------
    df : pandas.DataFrame
        Survey DataFrame.

    Returns
    -------
    pandas.DataFrame
        DataFrame with harmonized agreement scales.
    """
    df = fix_risk_agreement(df)
    # df = fix_cost_agreement(df)
    return df


def multicollinearity(X):
    """Compute Variance Inflation Factors (VIF) to assess multicollinearity.

    Multicollinearity occurs when independent variables in a regression model
    are correlated; high VIF values indicate potential issues.

    Parameters
    ----------
    X : pandas.DataFrame
        Predictor matrix (numeric). A constant column will be added internally.

    Returns
    -------
    pandas.DataFrame
        Table with `feature` and corresponding `VIF` values.
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
    """Calculate Cronbach's alpha for internal consistency.

    Cronbach's alpha measures how closely related a set of items are as a group.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame of related items (rows=respondents, cols=items).

    Returns
    -------
    float
        Alpha in [-inf, 1]. Values near 1 indicate high internal consistency.
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
