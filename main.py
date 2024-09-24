import os
from dacstore.utils import get_data, report_to_excel, survey_id_bilendi
from dacstore.validation import gender_age


def check_valid(filename=None, user=None, password=None):
    """Check which responses are valid and report for Bilendi"""
    if user is None:
        user = os.environ.get("SURVEY_HERO_USER")
    if password is None:
        password = os.environ.get("SURVEY_HERO_PASSWORD")

    df = get_data(
        filename,
        user,
        password,
        translate=False,
        drop=False,
        survey_ids=survey_id_bilendi,
        validate=True,
    )
    # df["valid"] = valid(df)

    valid_fraction = df.valid.value_counts().valid / len(df)
    print(f"responses: {len(df)}")
    print(f"valid: {valid_fraction}")
    print(df.valid.value_counts(normalize=True))
    print(100 * "-")
    print("Check: Valid answers grouped by gender and age")
    print(gender_age(df))
    # df[report_cols].style.apply(highlight_invalid, axis=1)
    report_to_excel(df, "valid.xlsx")


if __name__ == "__main__":
    check_valid()
