import bpy
import sys

def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
def load_model(filepath, modelname="Mesh"):
    # Load the model
    bpy.ops.wm.obj_import(
        filepath=filepath,
        up_axis='Z',
        forward_axis='Y'
    )
    model = bpy.context.active_object
    model.name = modelname
    
    # Place the character's feet at z=0
    min_z = min(v[2] for v in model.bound_box)
    model.location.z -= min_z
    bpy.ops.object.transform_apply()
    
    return model

def load_rig(filepath):
    bpy.ops.import_scene.fbx(filepath = filepath)
    rig = bpy.context.active_object
    rig.show_in_front=True
    return rig

def get_highest_frame(rig):
    action = rig.animation_data.action
    return int(max(max(kf.co.x for kf in fc.keyframe_points) for fc in action.fcurves))

def get_head_bone(rig):
    for bone in rig.data.bones:
        if "head" in bone.name.lower():
            return bone
    raise Exception("Rig has no head bone")
    
def scale_model_to_rig(model, rig):
    # Scale the character to match the rig
    head = get_head_bone(rig)
    head_min = (head.head_local @ rig.matrix_world)[2]
    head_max = (head.tail_local @ rig.matrix_world)[2]
    
    # Note: Not sure why it is negative for some rigs
    head_z = abs(head_min + (head_max - head_min) * 0.75)
    max_z = max(v[2] for v in model.bound_box)
    scale = head_z / max_z
    model.scale *= scale
    
    # Apply the scale transform
    rig.select_set(False)
    model.select_set(True)
    bpy.context.view_layer.objects.active = model
    bpy.ops.object.transform_apply()
    
def connect_model_rig(model, rig):
    bpy.ops.object.select_all(action='DESELECT')
    model.select_set(True)
    rig.select_set(True)
    bpy.context.view_layer.objects.active = rig
    bpy.ops.object.parent_set(type='ARMATURE_AUTO')
    
def finalize(model, rig, target_height):
    bpy.ops.object.select_all(action='DESELECT')
    
    # Determine the scaling factor
    highest_point = max(model.bound_box, key=lambda v: v[2])[2]
    scale = target_height / highest_point 
    
    # Create the root object
    bpy.ops.object.empty_add()
    root = bpy.context.active_object
    root.name = "Root"
    
    # Parent the rig to the root
    rig.select_set(True)
    bpy.ops.object.parent_set(type='OBJECT', keep_transform=False)
    
    # Scale the root
    root.scale *= scale
    
    return root

def export_fbx(object, filepath):
    bpy.ops.object.select_all(action='SELECT')
    object.select_set(True)
    bpy.context.view_layer.objects.active = object
    bpy.ops.export_scene.fbx(
        filepath=filepath, 
        check_existing=False, 
        use_selection=True, 
        
        # Speeds up the export
        # May cause issues with mutliple animations in one file
        bake_anim_use_all_actions=False,
        bake_anim_use_nla_strips=False
    )

def main():
    arg_index = sys.argv.index('--') + 1
    model_file = sys.argv[arg_index]
    rig_file = sys.argv[arg_index + 1]
    out_file = sys.argv[arg_index + 2]
    target_height = float(sys.argv[arg_index + 3])
    
    clear_scene()
    model = load_model(model_file)
    rig = load_rig(rig_file)
    bpy.context.scene.frame_end = get_highest_frame(rig)
    scale_model_to_rig(model, rig)
    connect_model_rig(model, rig)
    root = finalize(model, rig, target_height)
    export_fbx(root, out_file)
    
main()
bpy.ops.wm.quit_blender()