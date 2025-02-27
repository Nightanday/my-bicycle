
with 

final as (
    select
        id as station_id,
        nom as station_name,
        adresse as address,
        commune as city,
        etat as station_state,
        nb_places_dispo as available_docks_count,
        nb_velos_dispo as m_bikes_count,
        etat_connexion as connexion_state,
        x as lat,
        y as lon,
        date_modification as last_reported_at,
        GCS_loaded_at
    from {{source('lille_source', 'lille_all_tables')}}
)

select 
    * 
from 
    final