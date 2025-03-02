with 

final as (
    select * from {{ ref('stations_with_google_maps_datas') }}
)


select 
    station_fr_id,
    station_id,
    lat,
    lon,
    GMAP_address,
    GMAP_city,
    GMAP_postal_code
from final
