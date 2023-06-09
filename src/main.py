#!/usr/bin/env python
from authorize import user_token
from get import get_recently_played
import pandas as pd
from dotenv import load_dotenv
import format
import os
from datetime import datetime,timedelta

load_dotenv()

def run_spotify_etl(): 
    default_dir_location = os.getenv('DEFAULT_DIR_LOCATION') or os.getcwd()
    previous_date = datetime.today() - timedelta(days=1)
    millisec_timestamp = int(previous_date.timestamp() *1000)
    history_playlist = get_recently_played(user_token,after=millisec_timestamp,limit=50)
    df = pd.DataFrame(
        {
        "song_name": pd.Series([data["track"]["name"] for data in history_playlist]),
        "album_type": pd.Series([data["track"]["album"]["album_type"] for data in history_playlist]),
        "artist":pd.Series([format.extract_artists_name(data["track"]["artists"]) for data in history_playlist]),
        "release_date": pd.to_datetime([data["track"]["album"]["release_date"] for data in history_playlist]),
        "duration_minute": pd.Series([format.to_duration_minute(data["track"]["duration_ms"]) for data in history_playlist]),
        "played_at": pd.to_datetime([format.to_th_time(data["played_at"]) for data in history_playlist]),
        }
    )
    df.to_csv("s3://intouch-spotify-data-pipeline-bucket/"+format.set_file_name(previous_date))
    print(df)


if __name__ =="__main__":
    run_spotify_etl()
