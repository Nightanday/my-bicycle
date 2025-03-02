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
        to_hex(md5('lyon' || cast(gid as string))) as station_fr_id,
        cast(gid as string) as station_id,
        address,
        address_jcd,
        availability as avaibility,
        availabilitycode as availability_code,
        coalesce(available_bike_stands, 0) as available_docks_count,
        coalesce(bike_stands, 0) as total_docks_count,
        code_insee as insee_code,
        commune as city,
        lat,
        lng as lon,
        coalesce(bikes, 0) as bikes_count,
        coalesce(electricalBikes, 0) as e_bikes_count,
        coalesce(mechanicalBikes, 0) as m_bikes_count,
        last_update as last_reported_at,
        GCS_loaded_at
    from {{source('lyon_source', 'raw_view_lyon')}}
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