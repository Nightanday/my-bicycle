with lyon_stations as (

     select * from {{ ref('stg_stations_status_lyon') }}

),

final as (
    select
        station_id,
        available_docks_count,
        bikes_count,
        e_bikes_count,
        m_bikes_count,
        total_docks_count,
        last_reported_at,
        GCS_loaded_at
    from 
        lyon_stations
)

select * from final