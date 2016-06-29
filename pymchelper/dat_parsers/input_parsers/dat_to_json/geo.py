
from plyplus import Grammar, STransformer

from modules.parsers.dat_to_json.geo.geo_preparser import convert_geo

json_grammar = Grammar(r"""

start: sph_type  ;

sph_type : SPH_T VALUE VALUE VALUE VALUE VALUE ;

rpp_type : RPP_T VALUE VALUE VALUE VALUE VALUE VALUE VALUE ;

box_type : BOX_T VALUE VALUE VALUE VALUE VALUE VALUE VALUE VALUE VALUE VALUE VALUE VALUE VALUE ;

rcc_type : RCC_T VALUE VALUE VALUE VALUE VALUE VALUE VALUE VALUE ;

type: sph_type | rpp_type | box_type | rcc_type ;

bodies : type bodies | type ;

operator : PLUS | MINUS ;

expr : operator VALUE expr | operator VALUE ;

zone_operation: ZONE_NAME expr | ZONE_NAME VALUE expr ;

zones : zone_operation zones | zone_operation ;

material: VALUE VALUE ;

media: material media | material ;

file : DESCRIPTION SEPARATOR bodies SEPARATOR zones SEPARATOR media ;

VALUE : '-?([0-9]+)(\.[0-9]+)?' ;
SPH_T : 'SPH' ;
RPP_T : 'RPP' ;
BOX_T : 'BOX' ;
RCC_T : 'RCC' ;
SEPARATOR : 'END' ;
MINUS : '\-' ;
PLUS : '\+' ;
DESCRIPTION : '".*"' ;
ZONE_NAME : '[a-zA-Z0-9]{3,3}' ;
WS: '[ \t\n]+' (%ignore);

""")

class Geo_parserTransformer(STransformer):
    sph_type  = lambda self, node: node
    rpp_type  = lambda self, node: node
    box_type  = lambda self, node: node
    rcc_type  = lambda self, node: node
    type = lambda self, node: node
    bodies  = lambda self, node: node
    operator  = lambda self, node: node
    expr  = lambda self, node: node
    zone_operation = lambda self, node: node
    zones  = lambda self, node: node
    material = lambda self, node: node
    media = lambda self, node: node
    file  = lambda self, node: node
    VALUE = lambda self, node: node
    SPH_T = lambda self, node: node
    RPP_T = lambda self, node: node
    BOX_T = lambda self, node: node
    RCC_T = lambda self, node: node
    SEPARATOR = lambda self, node: node
    MINUS = lambda self, node: node
    PLUS = lambda self, node: node
    DESCRIPTION = lambda self, node: node
    ZONE_NAME = lambda self, node: node

file = open("geo.dat")
content = file.read()
preprocessed_dat = convert_geo(content)
tree = json_grammar.parse(preprocessed_dat)

tree.to_png_with_pydot(r'tree.png')
print(Geo_parserTransformer().transform(tree))
