
with 

final as (
    select
        address,
        address2,
        address_jcd,
        availability,
        availabilitycode,
        available_bike_stands,
        available_bikes,
        bike_stands,
        code_insee,
        commune,
        gid,
        lat,
        lng,
        bikes,
        electricalBikes,
        mechanicalBikes,
        GCS_loaded_at
    from {{source('lyon_source', 'lyon_all_tables')}}
)

select 
    * 
from 
    final