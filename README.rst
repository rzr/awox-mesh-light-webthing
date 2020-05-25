========================
AWOX-MESH-LIGHT-WEBTHING
========================

Webthings RESTful API for Awox's "SmartLight" (SKRLm-c9-E27).

This lightbulb is supporting Bluetooth mesh.


USAGE
=====

::

   MAC=A4:C1:38:78:11:33 ./awox_mesh_light_single_webthing.py 

   curl http://localhost:8888/properties
   #| {"on": true, "brightness": 50, "color": "#ffffff"}

   curl -X PUT --data '{"color": "#00A000"}' \
     -H 'Content-Type: "application/json" ' \
     "http://localhost:8888/properties/color"

    
RESOURCES
=========

* https://github.com/Leiaz/python-awox-mesh-light
* https://iot.mozilla.org
* https://www.amazon.fr/dp/B01L3C1V5G/rzr-21
* https://www.awox.com/en/awox_product/smartlight-mesh-c9/
* https://www.upcitemdb.com/upc/3760118941004
* https://en.wikipedia.org/wiki/Bluetooth_mesh_networking
* https://purl.org/rzr/presentations
