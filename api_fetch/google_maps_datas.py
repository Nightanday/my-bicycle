import googlemaps
from google.cloud import bigquery
import os
import pandas as pd


def load_stations_lat_lon_from_bq(csv_file_path='stations_lat_lon.csv'):
    """
    This function take all latitudes and longitudes from biq query dim_fr_stations table
    and save it in a csv file
    """
    client = bigquery.Client()
    query = """
        SELECT station_fr_id, station_id, lat, lon 
        FROM `my-bicycle-project-452309.dev_my_velib.dim_fr_stations`
    """
    query_job = client.query(query)
    results_df = query_job.to_dataframe()
    return results_df
    #results_df.to_csv(csv_file_path, index=False, encoding='utf-8')
    



def get_geo_datas(latitudes, longitudes):
    """
    function to get all localization informations (ie: address, city and postal code)
    from list of latitudes and longitudes
    """
    gmaps = googlemaps.Client(key= os.getenv('GOOGLE_MAPS_API_KEY'))
    datas = []
    for lat, lon in zip(latitudes, longitudes):
        # Utilisez la méthode reverse_geocode pour obtenir les données détaillées
        resultat = gmaps.reverse_geocode((lat, lon))
        if resultat:
            address = resultat[0].get('formatted_address', 'Unknown')
            composants = resultat[0].get('address_components', [])
            city = ''
            postal_code = ''
            for composant in composants:
                if 'locality' in composant['types']:
                    city = composant['long_name']
                elif 'postal_code' in composant['types']:
                    postal_code = composant['long_name']
            datas.append({
                'GMAP_lat': lat,
                'GMAP_lon': lon,
                'GMAP_address': address,
                'GMAP_city': city,
                'GMAP_postal_code': postal_code
            })
    result_df = pd.DataFrame(datas)
    return result_df

if __name__ == "__main__":
    df = load_stations_lat_lon_from_bq()
    latitudes = df['lat']
    longitudes = df['lon']
    # get geo datas from google maps
    geo_df = get_geo_datas(latitudes, longitudes)
    # merging dataframes
    merged_df = df.merge(geo_df, left_on=['lat', 'lon'], right_on=['GMAP_lat', 'GMAP_lon'], how='left')
    # save merged dataframe in dbt seeds
    merged_df.to_csv('dbt/seeds/stations_with_google_maps_datas.csv', index=False, encoding='utf-8')



