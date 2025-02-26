
with 

final as (
    select
        gid as station_id,
        address,
        address2,
        address_jcd,
        availability as avaibility,
        availabilitycode as availability_code,
        available_bike_stands as available_docks_count,
        bike_stands as total_docks_count,
        code_insee as insee_code,
        commune as city,
        lat,
        lng as lon,
        bikes as bikes_count,
        electricalBikes as e_bikes_count,
        mechanicalBikes as m_bikes_count,
        last_update as last_reported_at,
        GCS_loaded_at
    from {{source('lyon_source', 'lyon_all_tables')}}
)

select 
    * 
from 
    final