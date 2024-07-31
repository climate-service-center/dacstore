import pandas as pd
import copy


completion_time_limit = pd.Timedelta(3, "min")

NOT_COMPLETED = 1
COMPLETION_TIME_TOO_LONG = 2
STRAIGHTLINING = 3

status_dict = {
    NOT_COMPLETED: {"description": "survey was not completed", "status": False},
    COMPLETION_TIME_TOO_LONG: {
        "description": f"completion time was longer than {completion_time_limit}",
        "status": False,
    },
    STRAIGHTLINING: {"description": "answers seem to be random", "status": False},
}


def create_row_status(status):
    report = ""
    for k, v in status.items():
        if v["status"] is True:
            report += " | " if report else ""
            report += v["description"]
    if not report:
        report = "valid"
    return report


def check_row(row):
    """Check valid status of a row"""
    status = copy.deepcopy(status_dict)
    if row.completion_time < completion_time_limit:
        status[COMPLETION_TIME_TOO_LONG]["status"] = True
        status[COMPLETION_TIME_TOO_LONG][
            "description"
        ] = f"completion time too short: {row.completion_time.seconds} seconds"
    if row.Status != "Completed":
        status[NOT_COMPLETED]["status"] = True
    return create_row_status(status)


def valid(df):
    "add a colum with validation check"
    return df.apply(check_row, axis=1)


def highlight_invalid(s):
    """Highlight cells"""
    is_above_threshold = s != "valid"
    return ["background-color: yellow" if v else "" for v in is_above_threshold]
