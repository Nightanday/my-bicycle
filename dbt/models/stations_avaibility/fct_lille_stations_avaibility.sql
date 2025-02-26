with lille_stations as (

     select * from {{ ref('stg_stations_status_lille') }}

),

final as (
    select
        station_id
        m_bikes_count,
        available_docks_count,
        last_reported_at,
        GCS_loaded_at
    from 
        lille_stations
)

select * from final