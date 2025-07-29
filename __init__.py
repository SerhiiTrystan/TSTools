# Import necessary Blender modules
import bpy
from . import operators, ui_panels

# Add-on metadata
bl_info = {
    "name": "TST",
    "author": "Grok and TS",
    "version": (0, 9),
    "blender": (4, 5, 0),
    "location": "View3D > N-Panel > UV & Material Manager",
    "description": "Manages UV Maps and Materials for selected objects",
    "category": "Object",
}

# List of classes to register
classes = (
    operators.UVMapSetActiveOperator,
    operators.UVMapDeleteOperator,
    operators.UVMapCreateOperator,
    operators.UVMapRenameOperator,
    operators.MaterialDeleteOperator,
    operators.MaterialSelectOperator,
    operators.MaterialApplyOperator,
    ui_panels.UVPanel,
    ui_panels.MaterialPanel,
)

# Register function
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    # Add custom property for UV Map selection, ensuring unique UV Map names
    bpy.types.Scene.uv_map_selector = bpy.props.EnumProperty(
        items=lambda self, context: [(name, name, "") for name in sorted(set(
            uv.name for obj in context.selected_objects if obj.type == 'MESH' for uv in obj.data.uv_layers
        ))],
        name="UV Maps",
        description="Select a UV Map from the list",
        update=lambda self, context: None  # Placeholder for dynamic updates
    )
    # Add custom property for material selection
    bpy.types.Scene.material_selector = bpy.props.EnumProperty(
        items=lambda self, context: [(mat.name, mat.name, "") for mat in bpy.data.materials],
        name="Materials",
        description="Select a Material from the list",
        update=lambda self, context: None
    )
    # Add toggle for material list scope
    bpy.types.Scene.show_all_materials = bpy.props.BoolProperty(
        name="Show All Materials",
        description="Toggle between showing materials on visible objects or all materials in the scene",
        default=False
    )
    # Add property for new UV Map name
    bpy.types.Scene.new_uv_map_name = bpy.props.StringProperty(
        name="UV Map Name",
        description="Name for creating or renaming a UV Map",
        default="UVMap_New"
    )

# Unregister function
def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    # Clean up custom properties
    del bpy.types.Scene.uv_map_selector
    del bpy.types.Scene.material_selector
    del bpy.types.Scene.show_all_materials
    del bpy.types.Scene.new_uv_map_name

# Entry point
if __name__ == "__main__":
    register()