import requests
import pandas as pd


base_url = 'https://velib-metropole-opendata.smovengo.cloud/opendata/Velib_Metropole/'
requested_data = 'station_status.json'

response = requests.get(base_url + requested_data)
status_code = response.status_code
print(f'status code: {status_code}\n')
data = response.json()
stations_json = data['data']['stations']

print(stations_json[0],'\n')

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
print(df)




