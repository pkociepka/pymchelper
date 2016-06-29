%%
sph_type : SPH_T VALUE VALUE VALUE VALUE VALUE ;
rpp_type : RPP_T VALUE VALUE VALUE VALUE VALUE VALUE VALUE ;
box_type : BOX_T VALUE VALUE VALUE VALUE VALUE VALUE VALUE VALUE VALUE VALUE VALUE VALUE VALUE ;
rcc_type : RCC_T VALUE VALUE VALUE VALUE VALUE VALUE VALUE VALUE ;
type: sph_type | rpp_type | box_type | rcc_type ;
bodies : type bodies | type ;
operator : PLUS | MINUS ;
expr : operator VALUE expr | operator VALUE ;
zone_operation: ZONE_NAME expr | ZONE_NAME VALUE expr;
zones : zone_operation zones | zone_operation ;
material: VALUE VALUE ;
media: material media | material ;
file : DESCRIPTION SEPARATOR bodies SEPARATOR zones SEPARATOR media ;
%%
