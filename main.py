import os
from dacstore.utils import get_data
from dacstore.validation import valid


def check_valid(filename=None, user=None, password=None):
    if user is None:
        user = os.environ.get("SURVEY_HERO_USER")
    if password is None:
        password = os.environ.get("SURVEY_HERO_PASSWORD")
    df = get_data(filename, user, password, translate=False, drop=False)
    df["valid"] = valid(df)
    print(df.valid.value_counts(normalize=True))
    df.to_csv("output.csv")


if __name__ == "__main__":
    check_valid()
