
with 

final as (
    select
        station_id,
        mechanical,
        ebike,
        numDocksAvailable,
        is_installed,
        is_renting,
        is_returning,
        GCS_loaded_at
    from {{source('paris_source', 'paris_all_tables')}}
)

select 
    * 
from 
    final