import bpy
from .utils import get_uv_maps, get_materials

# Panel for UV Map management
class UVPanel(bpy.types.Panel):
    bl_label = "UV Map Manager"
    bl_idname = "PT_UVPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'UV & Material'
    
    def draw(self, context):
        layout = self.layout
        layout.label(text="UV Map Management", icon='UV')
        
        # Dynamic UV Map list
        layout.prop(context.scene, "uv_map_selector", text="UV Maps")
        
        # Buttons for UV Map operations
        layout.operator("object.uv_map_set_active", text="Set Active UV Map")
        layout.operator("object.uv_map_delete", text="Delete Selected UV Map")
        
        # New UV Map creation and renaming
        layout.prop(context.scene, "new_uv_map_name", text="UV Map Name")
        layout.operator("object.uv_map_create", text="Create New UV Map")
        layout.operator("object.uv_map_rename", text="Rename Active UV Map")

# Panel for Material management
class MaterialPanel(bpy.types.Panel):
    bl_label = "TSMaterial"
    bl_idname = "PT_MaterialPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'UV & Material'
    
    def draw(self, context):
        layout = self.layout
        layout.label(text="Material Management", icon='MATERIAL')
        
        # Toggle for material list scope
        layout.prop(context.scene, "show_all_materials", text="Show All Scene Materials")
        
        # Dynamic Material list
        layout.prop(context.scene, "material_selector", text="Materials")
        
        # Buttons for Material operations
        layout.operator("object.material_delete", text="Delete Selected Material")
        layout.operator("object.material_select_objects", text="Select Objects with Material")
        layout.operator("object.material_apply", text="Apply Material to Selected")