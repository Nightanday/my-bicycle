{{
 config(
   materialized = 'incremental',
   incremental_strategy = 'insert_overwrite',
   partition_by = {
     'field': 'GCS_loaded_at', 
     'data_type': 'timestamp',
     'granularity': 'day'
   }
 )
}}

with 

final as (
    select
        to_hex(md5('lille' || cast(id as string))) as station_fr_id,
        cast(id as string) as station_id,
        nom as station_name,
        adresse as address,
        commune as city,
        etat as station_state,
        coalesce(nb_places_dispo, 0) as available_docks_count,
        coalesce(nb_velos_dispo, 0) as bikes_count,
        coalesce(nb_velos_dispo, 0) as m_bikes_count,
        0 as e_bikes_count,
        etat_connexion as connexion_state,
        y as lat,
        x as lon,
        date_modification as last_reported_at,
        GCS_loaded_at
    from {{source('lille_source', 'raw_view_lille')}}
    {% if is_incremental() %}
    -- this filter will only be applied on an incremental run
    -- (uses >= to include records arriving later on the same day as the last run of this model)
    where date(GCS_loaded_at) >= (select coalesce(max(date(GCS_loaded_at)), '1900-01-01') from {{ this }})
    {% endif %}
)

select 
    * 
from 
    final