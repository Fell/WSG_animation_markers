[![Blender](img/Blender_logo.png)](http://www.blender.org/) [![glTF](img/glTF_logo.png)](https://www.khronos.org/gltf/) [![three.js](img/threejs_logo.png)](https://threejs.org/)

Pose markers to extras extension
===============================

Custom extension to export action pose markers as extras in glTF. Adjusted for internal use at Winning Streak Games GmbH.

Installation
------------

### [Download WSG_animation_markers.py](./WSG_animation_markers.py)

Install the addon in Blender by choosing: *Preferences → Add-ons → Install...*

How it works
------------

**Warning: This extension will delete any existing custom properties on all actions!**

This is neccesary to work with Blender 3.6.0, because the hooks provided the glTF exporter do not allow to add extension data for each animation any longer, even though it is supported by the glTF specification. Instead, during the export process, all pose markers on all actions are converted to custom properties using the marker name as the key and the offset in seconds as the value. After the export, all custom properties on all actions are removed again.

In the resulting glTF file, the pose markers can be found under `extras` like so:
```json
...
"animations":[
    {
        "name":"CubeAction",
        "extras":{
            "marker1":1.0333333333333334,
            "marker2":1.2833333333333334
        },
        ...
    }
],
...
```