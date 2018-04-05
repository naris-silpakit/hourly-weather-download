import pandas as pd
import requests
import json
import time
import itertools
import argparse

def get_weather_data(api_key, lat, long, date):
    """Wraps a request to the Dark Sky API. Parses and formats the response.
        
        Args:
            api_key (str): A Dark Sky Secret Key.
            lat (float): Latitude of the location being requested.
            long (float): Longitude of the location being requested.
            date (timestamp): A Pandas timestamp with the year, month, and day for the date being requested.

        Returns:
            List: A list of hourly weather recordings for the given date and location. 
                    Each element contains json formatted weather data for a given hour.
    """
    # sleep for a fraction of a second to avoid sending too many requests at once
    time.sleep(0.1)
    target_date = date.strftime("%Y-%m-%dT12:00:00")
    url = 'https://api.darksky.net/forecast/{}/{},{},{}'
    api_call = url.format(api_key, lat, long, target_date)
    response = requests.get(api_call)
    weather_data = json.loads(response.text)
    # The JSON parsed from the API response gives me hourly data 
    # as the most detailed weather measurement unit, so I'll extract from the attributes there.
    return weather_data['hourly']['data']

# allow this script to be run from the terminal
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--num_days", help = "specify the number of days to capture here (limited to 1000 to avoid free tier API limit)",
                   type = int)
args = parser.parse_args()

if args.num_days > 1000:
    print("num_days given is greater than the max (1000), setting num_days to 1000.")
    days_to_capture = 1000
else:
    days_to_capture = args.num_days
    
print(days_to_capture)

# load in the api key - needed to access the Dark Sky API
api_key = open('api_key.txt', 'r').read().strip()

# Create the range of dates to capture
dates = pd.date_range(end = pd.datetime.today(), periods = days_to_capture).tolist()

# Set up the request url
# Seattle Latitude/Longitude: 47.6062° N, 122.3321° W
lat = 47.6062
long = -122.3321
url = 'https://api.darksky.net/forecast/{}/{},{},{}'

# Each element is a list containing the hourly weather records for a single day
weather_data = [get_weather_data(api_key, lat, long, date) for date in dates]

# Flatten so that we have a list where each element is an hour of weather data
weather_data_list = list(itertools.chain.from_iterable(weather_data))

# Convert to a dataframe
weather_df = pd.DataFrame(weather_data_list)

# Convert UNIX time to datetime format and convert the timezone to UTC
weather_df['time'] = pd.Series(pd.to_datetime(weather_df['time'], unit = 's')).dt.tz_localize('UTC')

# Save
weather_df.to_csv("weather_data.csv", index = False)

print("Done!")