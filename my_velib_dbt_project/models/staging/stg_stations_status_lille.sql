
with 

final as (
    select
        *
    from {{source('lille_source', 'lille_all_tables')}}
)

select 
    * 
from 
    final