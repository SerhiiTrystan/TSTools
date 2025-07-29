import bpy

# Operator to set selected UV Map as active
class UVMapSetActiveOperator(bpy.types.Operator):
    bl_idname = "object.uv_map_set_active"
    bl_label = "Set Active UV Map"
    
    def execute(self, context):
        uv_map_name = context.scene.uv_map_selector
        selected_objects = context.selected_objects
        objects_with_uv = []
        objects_without_uv = []
        
        # Iterate through selected objects
        for obj in selected_objects:
            if obj.type == 'MESH' and uv_map_name in [uv.name for uv in obj.data.uv_layers]:
                obj.data.uv_layers[uv_map_name].active = True
                objects_with_uv.append(obj)
            else:
                objects_without_uv.append(obj)
        
        # Deselect all objects
        bpy.ops.object.select_all(action='DESELECT')
        # Select objects without the UV Map
        for obj in objects_without_uv:
            obj.select_set(True)
        
        self.report({'INFO'}, f"Set '{uv_map_name}' as active for applicable objects")
        return {'FINISHED'}

# Operator to delete selected UV Map
class UVMapDeleteOperator(bpy.types.Operator):
    bl_idname = "object.uv_map_delete"
    bl_label = "Delete Selected UV Map"
    
    def execute(self, context):
        uv_map_name = context.scene.uv_map_selector
        for obj in context.selected_objects:
            if obj.type == 'MESH' and uv_map_name in [uv.name for uv in obj.data.uv_layers]:
                obj.data.uv_layers.remove(obj.data.uv_layers[uv_map_name])
        self.report({'INFO'}, f"Deleted UV Map '{uv_map_name}'")
        return {'FINISHED'}

# Operator to create a new UV Map
class UVMapCreateOperator(bpy.types.Operator):
    bl_idname = "object.uv_map_create"
    bl_label = "Create New UV Map"
    
    def execute(self, context):
        uv_map_name = context.scene.new_uv_map_name
        if not uv_map_name:
            self.report({'ERROR'}, "UV Map name cannot be empty")
            return {'CANCELLED'}
        
        for obj in context.selected_objects:
            if obj.type == 'MESH':
                # Create new UV Map
                new_uv = obj.data.uv_layers.new(name=uv_map_name)
                if new_uv:
                    new_uv.active = True
        self.report({'INFO'}, f"Created UV Map '{uv_map_name}'")
        return {'FINISHED'}

# Operator to delete selected material
class MaterialDeleteOperator(bpy.types.Operator):
    bl_idname = "object.material_delete"
    bl_label = "Delete Selected Material"
    
    def execute(self, context):
        mat_name = context.scene.material_selector
        material = bpy.data.materials.get(mat_name)
        if material:
            bpy.data.materials.remove(material)
            self.report({'INFO'}, f"Deleted material '{mat_name}'")
        else:
            self.report({'ERROR'}, f"Material '{mat_name}' not found")
        return {'FINISHED'}

# Operator to select objects with selected material
class MaterialSelectOperator(bpy.types.Operator):
    bl_idname = "object.material_select_objects"
    bl_label = "Select Objects with Material"
    
    def execute(self, context):
        mat_name = context.scene.material_selector
        bpy.ops.object.select_all(action='DESELECT')
        for obj in context.scene.objects:
            if obj.type == 'MESH' and any(slot.material and slot.material.name == mat_name for slot in obj.material_slots):
                obj.select_set(True)
        self.report({'INFO'}, f"Selected objects with material '{mat_name}'")
        return {'FINISHED'}

# Operator to apply selected material to selected objects
class MaterialApplyOperator(bpy.types.Operator):
    bl_idname = "object.material_apply"
    bl_label = "Apply Material to Selected"
    
    def execute(self, context):
        mat_name = context.scene.material_selector
        material = bpy.data.materials.get(mat_name)
        if not material:
            self.report({'ERROR'}, f"Material '{mat_name}' not found")
            return {'CANCELLED'}
        
        for obj in context.selected_objects:
            if obj.type == 'MESH':
                # Assign material to the first material slot
                if not obj.material_slots:
                    obj.data.materials.append(material)
                else:
                    obj.material_slots[0].material = material
        self.report({'INFO'}, f"Applied material '{mat_name}' to selected objects")
        return {'FINISHED'}