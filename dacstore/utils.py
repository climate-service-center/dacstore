import pandas as pd
import requests
from io import BytesIO


survey_id = 1837044
api_url = f"https://api.surveyhero.com/v1/surveys/{survey_id}/responses"


def get_data(source=None, user=None, password=None):
    """read csv from file or surveyhero api"""
    if source is None:
        params = {"format": "csv", "status": "completed"}
        r = requests.get(api_url, params=params, auth=(user, password))
        print(r.status_code)
        print(f"API request status code: {r.status_code}")
        source = BytesIO(r.content)
    df = pd.read_csv(source)
    return df
