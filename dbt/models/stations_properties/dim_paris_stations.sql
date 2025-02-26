with 

paris_stations_status as (
    select * from {{ ref('stg_stations_status_paris') }}
),

paris_stations_location as (
    select * from {{ ref('paris_stations_location') }}
),

final as (
    select
        location.station_id,
        location.name as station_name,
        location.lat,
        location.lon,
        null as station_address,
        null as city,
        null as station_district,
        -- boolean indicating if the station is currently on service
        (
            status.is_installed = true 
            and status.is_renting = true
            and status.is_returning = true
        ) as is_active,
        -- to get the total of docks we sum the number of mech
        m_bikes_count + e_bikes_count + available_docks_count as total_docks_count
    from 
        paris_stations_location as location
    left join 
        paris_stations_status as status
        on status.station_id = location.station_id
    -- here we filter on the last loaded row
    qualify row_number() over(partition by station_id order by GCS_loaded_at desc) =1
)

select 
    * 
from 
    final