import os
from dacstore.dac_analysis import get_df


def main(filename=None, user=None, password=None):
    if user is None:
        user = os.environ.get("SURVEY_HERO_USER")
    if password is None:
        user = os.environ.get("SURVEY_HERO_PASSWORD")
    df = get_df(filename, user, password)
    print(df.info())


if __name__ == "__main__":
    main()
