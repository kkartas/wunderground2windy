import requests
import datetime
import time

# API Endpoints and Keys
WU_STATION_ID = 'WU_STATION_ID'
WU_API_KEY = 'WU_API_KEY'
WU_ENDPOINT = 'https://api.weather.com/v2/pws/observations/current?stationId={station_id}&format=json&units=m&apiKey={key}'

WINDY_API_KEY = 'WINDY_API_KEY.eyJjaSI6NDg5Nzc2MCwiaWF0IjoxNjk0NzA4NjY5fQ.ulUoKb9fcqSOwSJcukC2PbSvGG9oOtVncYwy6F7rPTQ'
WINDY_ENDPOINT = 'https://stations.windy.com/pws/update/' + WINDY_API_KEY

# Fetch data from Weather Underground
def fetch_wu_data():
    response = requests.get(WU_ENDPOINT.format(key=WU_API_KEY, station_id=WU_STATION_ID))
    if response.status_code == 200:
       # print(response.json()) debugging satement
        return response.json()
    return None

# Prepare data for Windy and update it
def sync_with_windy(data):
    observation = data['observations'][0]
    
    windy_data = {
        'stations': [{
            'station': 0,
            'name': observation['neighborhood'],
            'lat': observation['lat'],
            'lon': observation['lon'],
            'elevation': observation.get('elev', 0),  # Assuming a default value of 0 if not available.
        }],
        'observations': [{
            'station': 0,
            'dateutc': observation['obsTimeUtc'],
            'temp': observation['metric']['temp'],
            'wind': observation['metric']['windSpeed'],
            'winddir': observation['winddir'],
            'gust': observation['metric']['windGust'],
            'humidity': observation['humidity'],
            'dewpoint': observation['metric']['dewpt'],
            'pressure': observation['metric']['pressure']
        }]
    }

    response = requests.post(WINDY_ENDPOINT, json=windy_data)
   # print(windy_data) debugging statement
    return response.status_code == 200

def main():
    while True:
        wu_data = fetch_wu_data()
        
        if wu_data:
            if sync_with_windy(wu_data):
                print("Data synced with Windy successfully.")
            else:
                print("Failed to sync data with Windy.")
        else:
            print("Failed to fetch data from Weather Underground.")
        sync_period = 600 # In seconds
        print(f"Will send data again in {sync_period/60:.2f} minutes...")
        time.sleep(sync_period)

if __name__ == "__main__":
    main()