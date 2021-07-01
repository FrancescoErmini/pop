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

Go to /var/www/pop/html/ ( or whatever nginx uses )
and use symlinks to point those file:
geojson/pop.geojson
server/index.html
```
frer@dev:/var/www/pop/html$ ll
total 8
drwxrwxr-x 2 frer frer 4096 lug  1 15:21 ./
drwxr-xr-x 3 frer frer 4096 giu 10 14:48 ../
lrwxrwxrwx 1 frer frer   43 lug  1 12:01 index.html -> /home/frer/workspace/pop2/server/index.html
lrwxrwxrwx 1 frer frer   45 lug  1 12:11 pop.geojson -> /home/frer/workspace/pop2/geojson/pop.geojson
frer@dev:/var/www/pop/html$ 
```




