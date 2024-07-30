import pandas as pd
import requests
from io import BytesIO


survey_id = 1837044
api_url = f"https://api.surveyhero.com/v1/surveys/{survey_id}/responses"


def get_data(source=None, user=None, password=None, postprocess=True):
    """read csv from file or surveyhero api"""
    if source is None:
        # params = {"format": "csv", "status": "completed"}
        params = {"format": "csv"}
        r = requests.get(api_url, params=params, auth=(user, password))
        print(r.status_code)
        print(f"API request status code: {r.status_code}")
        source = BytesIO(r.content)
    df = pd.read_csv(
        source, index_col="ID", date_format="%d.%m.%Y %H:%M:%S", parse_dates=[1, 2]
    )
    if postprocess is True:
        df["completion_time"] = df["Last updated on"] - df["Started on"]
    return df


def valid_row(row):
    pass


def valids(df):
    "add a colum with validation check"
    pass
