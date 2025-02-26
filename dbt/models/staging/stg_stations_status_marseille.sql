
with 

final as (
    select
        station_id,
        nom_division as district,
        name as station_name,
        capacity as total_docks_count,
        num_bikes_available as bikes_count,
        num_bikes_available as m_bikes_count,
        num_docks_available as available_docks_count,
        cast(is_installed as bool) as is_installed,
        cast(is_renting as bool) as is_renting,
        cast(is_returning as bool) as is_returning,
        lon,
        lat,
        GCS_loaded_at
    from {{source('marseille_source', 'marseille_all_tables')}}
)

select 
    * 
from 
    final