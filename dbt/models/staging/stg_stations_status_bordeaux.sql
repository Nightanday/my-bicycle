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
        to_hex(md5('bordeaux' || cast(gid as string))) as station_fr_id,
        lon,
        lat,
        insee as insee_code,
        commune as city,
        cast(gid as string) as station_id,
        nom as station_name,
        etat as state,
        coalesce(nbplaces, 0) as available_docks_count,
        coalesce(nbvelos, 0) as bikes_count,
        coalesce(nbclassiq, 0) as m_bikes_count,
        coalesce(nbelec, 0) as e_bikes_count,
        code_commune as city_code,
        mdate as last_reported_at,
        GCS_loaded_at
    from {{source('bordeaux_source', 'raw_view_bordeaux')}}
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