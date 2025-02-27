with 

lyon_stations as (

     select * from {{ ref('stg_stations_status_lyon') }}

),

final as (
    select
        station_id,
        null as station_name,
        lat,
        lon,
        -- reformat adress to remove useless characters
        REGEXP_REPLACE(address, r',|Face ', '') as station_address,
        -- boolean to separate working station and out of order/closed stations
        availability_code != 0 as is_active,
        total_docks_count
    from 
        lyon_stations
    -- here we filter on the last loaded row
    qualify row_number() over(partition by station_id order by GCS_loaded_at desc) =1
)

select 
    * 
from 
    final