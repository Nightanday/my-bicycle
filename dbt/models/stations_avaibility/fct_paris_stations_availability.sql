with paris_stations as (

     select * from {{ ref('stg_stations_status_paris') }}

),

final as (
    select
        station_id,
        m_bikes_count,
        e_bikes_count,
        m_bikes_count+e_bikes_count as bikes_count,
        available_docks_count,
        last_reported_at,
        GCS_loaded_at
    from 
        paris_stations
)

select * from final