import os
from dacstore.utils import get_data


def main(filename=None, user=None, password=None):
    if user is None:
        user = os.environ.get("SURVEY_HERO_USER")
    if password is None:
        password = os.environ.get("SURVEY_HERO_PASSWORD")
    df = get_data(filename, user, password)
    print(df.info())


if __name__ == "__main__":
    main()
