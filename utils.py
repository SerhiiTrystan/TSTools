import bpy

# Utility function to get UV Maps for selected objects
def get_uv_maps(context):
    uv_maps = set()
    for obj in context.selected_objects:
        if obj.type == 'MESH':
            for uv in obj.data.uv_layers:
                uv_maps.add(uv.name)
    return [(name, name, "") for name in sorted(uv_maps)]

# Utility function to get materials (visible objects or all in scene)
def get_materials(context):
    show_all = context.scene.show_all_materials
    materials = set()
    
    if show_all:
        # Get all materials in the scene
        for mat in bpy.data.materials:
            materials.add(mat.name)
    else:
        # Get materials from visible objects
        for obj in context.scene.objects:
            if obj.type == 'MESH' and not obj.hide_viewport:
                for slot in obj.material_slots:
                    if slot.material:
                        materials.add(slot.material.name)
    
    return [(name, name, "") for name in sorted(materials)]

def create_bake_node_group(): #descriprion main node group for baking
    #checking if this node group exist 
    if "bake" in bpy.data.node_groups:
        return bpy.data.node_groups["bake"]
    node_group = bpy.data.node_groups.new("bake", 'GeometryNodeThree') 
    #input node cretion
    inp_nd = node_group.nodes.new('NodeGroupsInput') #rename function
    inp_nd.location = (620,300)
    #output node creation
    out_nd = node_group.nodes.new('NodeGroupOutput')
    out_nd.location = (660,350)
    
    nm_attrb = nodes.new(type='GeometryNodeStoreNamedAttribute')
    nm_attrb.location = (530,100)

    rgb_curve = nodes.new(type='ShaderNodeRGBCurve')
    rgb_curve.location = (700,300)

    cl_rmp = nodes.new(type='ShaderNodeValToRGB')
    cl_rmp.location = (950,320)

    blur_attrb = nodes.new(type='GeometryNodeBlurAttribute')
    blur_attrb.location = (730,250)
    #links

def apply_bake_modifier(context):
    # asighn modifiere for selected objects
    node_group = create_bake_node_group()
    apllied_objects = []

    for obj in context.selected_objects:
        if obj.type == 'MESH':
            mod = obj.modifiers.new(name="Bake Geometry Nodes", type= 'NODES')
            mod.node_group = node_group
            apply_objects.append(obj)
    return applied_objects