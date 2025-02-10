import requests
import pandas as pd

def fetch_station_location():
    base_url = 'https://velib-metropole-opendata.smovengo.cloud/opendata/Velib_Metropole/'
    requested_data = 'station_information.json'

    response = requests.get(base_url + requested_data)
    status_code = response.status_code
    print(f'🚲 Fetching stations location 🚲 -> status code: {status_code}\n')
    data = response.json()
    stations_json = data['data']['stations']

    name, id, lat, lon = [],[],[],[]
    #building station status dataframe

    for station in stations_json:
        id.append(station['station_id'])
        name.append(station['name'])
        lat.append(station['lat'])
        lon.append(station['lon'])

    stations_dic = {
        'id': id,
        'name': name,
        'lat': lat,
        'lon': lon
    }

    df = pd.DataFrame(stations_dic)
    return df

if __name__ == "__main__":
   data = fetch_station_location() 
   print(data)
