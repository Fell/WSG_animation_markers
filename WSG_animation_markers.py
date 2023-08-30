import bpy

bl_info = {
    "name": "Markers to extras",
    "extension_name": "WSG_animation_markers",
    "category": "GLTF Exporter",
    "version": (1, 2, 0),
    "blender": (3, 6, 0),
    'location': 'File > Export > glTF 2.0',
    'description': 'Copies pose markers to custom properties when exporting as glTF.',
    'tracker_url': 'https://github.com/Fell/WSG_animation_markers/issues',  # Replace with your issue tracker
    'isDraft': False,
    'developer': "Winning Streak Games GmbH",
    'url': 'https://winningstreakgames.de',
}

class TimelineMarkersExtensionProperties(bpy.types.PropertyGroup):
    enabled: bpy.props.BoolProperty(
        name=bl_info["name"],
        description='Copy pose markers to custom properties when exporting',
        default=True
    )

def register():
    bpy.utils.register_class(TimelineMarkersExtensionProperties)
    bpy.types.Scene.TimelineMarkersExtensionProperties = bpy.props.PointerProperty(type=TimelineMarkersExtensionProperties)

def register_panel():
    # Register the panel on demand, we need to be sure to only register it once
    # This is necessary because the panel is a child of the extensions panel,
    # which may not be registered when we try to register this extension
    try:
        bpy.utils.register_class(GLTF_PT_TimelineMarkersExtensionPanel)
    except Exception:
        pass
    
    # If the glTF exporter is disabled, we need to unregister the extension panel
    # Just return a function to the exporter so it can unregister the panel
    return unregister_panel

def unregister_panel():
    # Since panel is registered on demand, it is possible it is not registered
    try:
        bpy.utils.unregister_class(GLTF_PT_TimelineMarkersExtensionPanel)
    except Exception:
        pass

def unregister():
    unregister_panel()
    bpy.utils.unregister_class(TimelineMarkersExtensionProperties)
    del bpy.types.Scene.TimelineMarkersExtensionProperties

class GLTF_PT_TimelineMarkersExtensionPanel(bpy.types.Panel):

    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOL_PROPS'
    bl_label = "Enabled"
    bl_parent_id = "GLTF_PT_export_user_extensions"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        sfile = context.space_data
        operator = sfile.active_operator
        return operator.bl_idname == "EXPORT_SCENE_OT_gltf"

    def draw_header(self, context):
        props = bpy.context.scene.TimelineMarkersExtensionProperties
        self.layout.prop(props, 'enabled')

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        props = bpy.context.scene.TimelineMarkersExtensionProperties
        layout.active = props.enabled

        #box = layout.box()
        layout.label(text="Exporting custom properties will be forced")
        layout.label(text="when this extension is enabled.")

class glTF2ExportUserExtension:

    def __init__(self):
        # We need to wait until we create the gltf2TimelineMarkersExtension to import the gltf2 modules
        # Otherwise, it may fail because the gltf2 may not be loaded yet
        from io_scene_gltf2.io.com.gltf2_io_extensions import Extension
        self.Extension = Extension
        self.properties = bpy.context.scene.TimelineMarkersExtensionProperties
  
    def gather_scene_hook(self, gltf2_scene, blender_scene, export_settings):
        if self.properties.enabled:
            export_settings['gltf_extras'] = True

            VALID_NAMES = ['move_start','move_stop','ball_contact','ball_release','left_foot','right_foot']
            invalid_names = []

            for action in bpy.data.actions:

                for key in list(action.keys()):
                    del action[key]

                for marker in action.pose_markers:
                    marker.name = marker.name.lower()

                    action[marker.name] = marker.frame / blender_scene.render.fps

                    if(marker.name not in VALID_NAMES and marker.name not in invalid_names):
                        invalid_names.append(marker.name)
            
            if(len(invalid_names)):
                message = "Unknown marker names: "
                for name in invalid_names:
                    message += name + ' '
                
                show_warning(message)
    
    def gather_gltf_hook(self, active_scene_idx, scenes, animations, export_settings):
        if self.properties.enabled:
            for action in bpy.data.actions:
                for key in list(action.keys()):
                    del action[key]


def debug_dump(obj):
    for attr in dir(obj):
        if hasattr( obj, attr ):
            print( "obj.%s = %s" % (attr, getattr(obj, attr)))

def show_warning(message = "", title = "Warning", icon = 'ERROR'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)