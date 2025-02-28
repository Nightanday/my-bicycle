with 

fr_stations as (
    --select 'paris' as service, * from {{ ref('fct_paris_stations_availability') }}
    --union all
    select 'lille' as service, * from {{ ref('fct_lille_stations_availability') }}
    union all
    select 'marseille' as service, * from {{ ref('fct_marseille_stations_availability') }}
    union all
    select 'bordeaux' as service, * from {{ ref('fct_bordeaux_stations_availability') }}
    union all
    select 'lyon' as service, * from {{ ref('fct_lyon_stations_availability') }}
),

final as (
    select
        station_fr_id,
        station_id,
        m_bikes_count,
        e_bikes_count,
        m_bikes_count+e_bikes_count as bikes_count,
        available_docks_count,
        last_reported_at,
        GCS_loaded_at
    from 
        fr_stations
)

select * from final