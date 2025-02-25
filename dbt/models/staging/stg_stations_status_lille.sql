
with 

final as (
    select
        nom,
        adresse,
        commune,
        etat,
        nb_places_dispo,
        nb_velos_dispo,
        etat_connexion,
        x,
        y,
        GCS_loaded_at
    from {{source('lille_source', 'lille_all_tables')}}
)

select 
    * 
from 
    final