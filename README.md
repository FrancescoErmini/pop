1. install python requirements.txt on virtual env ( python > 3.8 )
2. install nginx and set proper permissions

====================
CREATE DB
====================
in define.py set the indexes_names: ndvi, ri, ...etc.
Run python storage/create_db.py to create one table per index, with cols poly_id, value, datetime

use qgis to export shape file to a new table, with:
db type: sqlite
db file: pop.sqlite
table(layer for qgis) name: pioppeti
crs: WGS84 - EPSG: 4326 ( projected )
poly_id: required name in attribute table, with id of polygon.

Note: see screenshot in docs.
Note 2: Projected coordinated are nneded by leaflet in order to correcly show polygons.

========================
SETUP SERVER
==========================

Copy server/index.html on /var/www/pop/html/ ( or whatever nginx uses )
Set in define.py GEOJSON_NAME to /var/www/pop/html/pop.geojson
( so that the goejson file will be create in that direcotry )


