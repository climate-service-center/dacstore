from dacstore.utils import ensure_floats, get_data
from dacstore.config import weighting_groups, replacer
from dacstore.dac_analysis import compute_group_averages


cols = [
    "climate_change_perception",
    "tampering",
    "maturity",
    "benefit",
    "cost",
    "risk",
    "trust",
    "emotion",
    "distance",
    "dac_knowledge",
    "storage_knowledge",
    "initial_storage_support",
    "final_storage_support",
    "initial_dac_support",
    "final_dac_support",
    "age",
    "gender",
    "education",
    "occupation",
    "state",
]


y_col = "final_dac_support"

independent = [
    "final_dac_support",
    "final_storage_support",
    "initial_storage_support",
    "initial_dac_support",
]


def create_numeric_data(df):
    """Create numeric data for regressions"""
    df = df.replace(replacer)
    df = ensure_floats(df, weighting_groups)
    df = compute_group_averages(df, weighting_groups)
    return df


if __name__ == "__main__":

    # we work here with the original column names, no translation
    df = get_data(
        source="./data/data.csv",
        drop=True,
        translate=False,
        drop_invalid=True,
        no_knowledge_to_neutral=True,
        set_dependent=True,
    )

    # an invalid entry (completed but more than 24hr completion time)
    df = df.drop(91621021)

    df = create_numeric_data(df)
    df = df[weighting_groups.keys()]
    df = df[~df.isna().any(axis=1)]
    # df = df[cols]

    print("writing numeric data")
    df.to_csv("./data/numeric_data.csv")
    df[cols].to_csv("./data/group_averages.csv")
