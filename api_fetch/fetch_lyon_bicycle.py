import requests
import pandas as pd 

"""
To see more informations about the api :
https://data.grandlyon.com/portail/fr/jeux-de-donnees/stations-velo-v-metropole-lyon-disponibilites-temps-reel/info
"""

def fetch_lyon_station_status():
    base_url = "https://data.grandlyon.com/fr/datapusher/ws/rdata/jcd_jcdecaux.jcdvelov"
    endpoint = "/all.json"
    params = {
        "maxfeatures": -1,
        "start": 1,
        "filename": "stations-velo-v-metropole-lyon-disponibilites-temps-reel"
    }

    station_dic = {
        'address': [],
        "address2": [],
        "address_jcd": [],
        "availability": [],
        "availabilitycode": [],
        "available_bike_stands": [],
        "available_bikes": [],
        "banking": [],
        "bike_stands": [],
        "bonus": [],
        "code_insee": [],
        "commune": [],
        "description": [],
        "enddate": [],
        "etat": [],
        "gid": [],
        "langue": [],
        "last_update": [],
        "last_update_fme": [],
        "last_update_gl": [],
        "lat": [],
        "lng": [],
        "bikes": [],
        "electricalBikes": [],
        "electricalInternalBatteryBikes": [],
        "electricalRemovableBatteryBikes": [],
        "mechanicalBikes": [],
        "stands": []
    }

    dic_keys = list(station_dic.keys())
    response = requests.get(base_url+endpoint, params=params)
    status_code = response.status_code
    print(f'\n🚲 Fetching Lyon stations status 🚲 -> status code: {status_code}\n')
    stations_json = response.json()
    stations = stations_json['values']
    for station in stations:
        for key in dic_keys:
            # some key are directly accessible while others should be accessed inside another JSON
            if key in list(station.keys()):
                station_dic[key].append(station.get(key))
            else:
                sub_json = station.get('main_stands')
                if key not in list(sub_json.keys()):
                    sub_json = sub_json.get('availabilities')
                station_dic[key].append(sub_json.get(key))

    df = pd.DataFrame(station_dic)
    return df


if __name__ == "__main__":
    df = fetch_lyon_station_status()
    print(df)


