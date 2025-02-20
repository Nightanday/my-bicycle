import requests
import pandas as pd
from geopy.geocoders import Nominatim

def fetch_station_location():
    base_url = 'https://velib-metropole-opendata.smovengo.cloud/opendata/Velib_Metropole/'
    requested_data = 'station_information.json'

    response = requests.get(base_url + requested_data)
    status_code = response.status_code
    print(f'\n🚲 Fetching stations location 🚲 -> status code: {status_code}\n')
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

def fetch_station_status():
    base_url = 'https://velib-metropole-opendata.smovengo.cloud/opendata/Velib_Metropole/'
    requested_data = 'station_status.json'

    response = requests.get(base_url + requested_data)
    status_code = response.status_code
    print(f'\n🚲 Fetching station status 🚲 -> status code: {status_code}\n')
    data = response.json()
    stations_json = data['data']['stations']

    #building station status dataframe
    id, mechanical_available, ebike_available, available_docks, is_deployed, is_renting, is_returning, last_reported = [],[],[],[],[],[],[],[]
    for station in stations_json:
        id.append(station['station_id'])
        mechanical_available.append(station['num_bikes_available_types'][0].get('mechanical'))
        ebike_available.append(station['num_bikes_available_types'][1].get('ebike'))
        available_docks.append(station['numDocksAvailable'])
        is_deployed.append(station['is_installed'])
        is_renting.append(station['is_renting'])
        is_returning.append(station['is_returning'])
        last_reported.append(station['last_reported'])

    stations_dic = {
        'id': id,
        'nb_mechanical_available': mechanical_available,
        'nb_ebike_available': ebike_available,
        'nb_available_docks': available_docks,
        'is_deployed': is_deployed,
        'is_renting': is_renting,
        'is_returning': is_returning,
        'last_reported': last_reported
    }

    df = pd.DataFrame(stations_dic)
    return df


def get_address_coordinates(name: str):
    # calling the Nominatim tool
    loc = Nominatim(user_agent="GetLoc")
    
    # entering the location name
    getLoc = loc.geocode(name)
    if getLoc is not None:
        print('Location found ✅')
        return getLoc.latitude, getLoc.longitude
    else: 
        print('Location not found ❌')
        return None



if __name__ == "__main__":

    data_station_location = fetch_station_location() 
    print(data_station_location.head(5))
    data_stations_status = fetch_station_status()
    print(data_stations_status.head(5))

    #search for an adress location
    searched_adress = '19 rue Richer, Paris'
    coordinates = get_address_coordinates(searched_adress)
    print(f"les coordonées de l'adresse {searched_adress} sont: {coordinates}")