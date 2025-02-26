
with 

final as (
    select
        lon,
        lat,
        insee,
        commune,
        gid,
        nom,
        etat,
        nbplaces,
        nbvelos,
        nbelec,
        nbclassiq,
        code_commune,
        GCS_loaded_at
    from {{source('bordeaux_source', 'bordeaux_all_tables')}}
)

select 
    * 
from 
    final