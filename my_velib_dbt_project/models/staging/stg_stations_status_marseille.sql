
with 

final as (
    select
        *
    from {{source('marseille_source', 'marseille_all_tables')}}
)

select 
    * 
from 
    final