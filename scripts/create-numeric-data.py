from dacstore.utils import ensure_floats, get_data
from dacstore.config import weighting_groups, replacer
from dacstore.dac_analysis import compute_group_averages


def create_numeric_data(df):
    """Create numeric data for regressions"""
    print(replacer)
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
    df_numeric = create_numeric_data(df)
    print("writing numeric data")
    df_numeric.to_csv("./data/numeric_data.csv")
    df_numeric[weighting_groups.keys()].to_csv("./data/group_averages.csv")
