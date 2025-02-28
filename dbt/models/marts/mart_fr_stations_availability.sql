{{
 config(
   materialized = 'table',
   partition_by = {
     'field': 'date', 
     'data_type': 'date',
     'granularity': 'day'
   }
 )
}}


with 

fr_stations_availability as (
    select 
        station_fr_id,
        m_bikes_count,
        e_bikes_count,
        bikes_count,
        available_docks_count,
        extract(date from GCS_loaded_at) as date, 
        extract(hour from GCS_loaded_at) as hour,
    from {{ ref('fct_fr_stations_availability') }}
),

fr_stations_properties as (
    select
        station_fr_id,
        service,
        lat,
        lon,
        total_docks_count,
        station_name,
        station_city,
        station_address,
        station_district
    from
        {{ ref('dim_fr_stations') }}
    where 
        is_active = true
),

final as (
    select 
        p.station_fr_id,
        coalesce(m_bikes_count, 0) as m_bikes_count,
        coalesce(e_bikes_count, 0) as e_bikes_count,
        coalesce(bikes_count, 0) bikes_count,
        coalesce(available_docks_count, 0) available_docks_count,
        date,
        hour,
        service,
        lat,
        lon,
        total_docks_count,
        station_name,
        station_city,
        station_address,
        station_district,
        case 
            when coalesce(bikes_count,0) = 0 then 'No availability'
            when coalesce(bikes_count,0) <= 3 then 'Low availability'
            when coalesce(bikes_count,0) <= 5 then 'Average availabililty'
            when coalesce(bikes_count,0) >5 then 'High availability'
            end as bikes_availability,
        case 
            when coalesce(m_bikes_count, 0) = 0 then 'No availability'
            when coalesce(m_bikes_count, 0) <= 3 then 'Low availability'
            when coalesce(m_bikes_count, 0) <= 5 then 'Average availabililty'
            when coalesce(m_bikes_count, 0) >5 then 'High availability'
            end as m_bikes_availability,
        case 
            when coalesce(e_bikes_count, 0) = 0 then 'No availability'
            when coalesce(e_bikes_count, 0) <= 3 then 'Low availability'
            when coalesce(e_bikes_count, 0) <= 5 then 'Average availabililty'
            when coalesce(e_bikes_count, 0) >5 then 'High availability'
            end as e_bikes_availability,
        case 
            when coalesce(available_docks_count, 0) = 0 then 'No availability'
            when coalesce(available_docks_count, 0) <= 3 then 'Low availability'
            when coalesce(available_docks_count, 0) <= 5 then 'Average availabililty'
            when coalesce(available_docks_count, 0) >5 then 'High availability'
            end as places_availability
    from 
        fr_stations_properties as p
    left join
        fr_stations_availability as a
        on p.station_fr_id = a.station_fr_id
)

select * from final