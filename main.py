import os
from dacstore.utils import get_data
from dacstore.validation import valid, highlight_invalid


report_cols = [
    "Status",
    "completion_time",
    "Bei dieser Frage ignorieren Sie bitte die folgenden Optionen und wählen Sie 'Stimme nicht zu'.",
    "valid",
]


def check_valid(filename=None, user=None, password=None):
    """Check which responses are valid and report"""
    if user is None:
        user = os.environ.get("SURVEY_HERO_USER")
    if password is None:
        password = os.environ.get("SURVEY_HERO_PASSWORD")
    df = get_data(filename, user, password, translate=False, drop=False)
    df["valid"] = valid(df)
    print(df.valid.value_counts(normalize=True))
    df.to_csv("data.csv")
    df[report_cols].style.apply(highlight_invalid, axis=1).to_excel(
        "valid.xlsx", index=True
    )


if __name__ == "__main__":
    check_valid()
