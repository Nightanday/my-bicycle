
with 

final as (
    select
        station_id,
        mechanical as m_bikes_count,
        ebike as e_bikes_count,
        numDocksAvailable as available_docks_count,
        cast(is_installed as bool) as is_installed,
        cast(is_renting as bool) as is_renting,
        cast(is_returning as bool) as is_returning,
        TIMESTAMP_SECONDS(last_reported) as last_reported_at,
        GCS_loaded_at
    from {{source('paris_source', 'paris_all_tables')}}
)

select 
    * 
from 
    final