
with 

final as (
    select
        station_id,
        nom_division,
        name,
        capacity,
        num_bikes_available,
        num_docks_available,
        is_installed,
        is_renting,
        is_returning,
        lon,
        lat,
        GCS_loaded_at
    from {{source('marseille_source', 'marseille_all_tables')}}
)

select 
    * 
from 
    final