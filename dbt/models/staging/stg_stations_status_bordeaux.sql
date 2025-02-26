
with 

final as (
    select
        lon,
        lat,
        insee as insee_code,
        commune as city,
        gid as station_id,
        nom as station_name,
        etat as state,
        nbplaces as available_docks_count,
        nbvelos as bikes_count,
        nbelec e_bikes_count,
        nbclassiq as m_bikes_count,
        code_commune as city_code,
        GCS_loaded_at
    from {{source('bordeaux_source', 'bordeaux_all_tables')}}
)

select 
    * 
from 
    final