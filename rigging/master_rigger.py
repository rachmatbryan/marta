import subprocess

BLENDER_SCRIPT = 'rigging/blender_rigger.py'

def rig(model_file, rig_file, out_file, target_height=1.8):
    subprocess.call(["blender", "-b", "--python", BLENDER_SCRIPT, "--", model_file, rig_file, out_file, str(target_height)])
    
if __name__ == "__main__":
    MODEL_FOLDER = '../3D_assets/characters'
    ANIM_FOLDER = '../animations'
    OUTPUT_FOLDER = '../rigged'

    MODEL_FILE = 't_pose'
    ANIM_FILE = 'Cartwheel'

    rig(f"{MODEL_FOLDER}/{MODEL_FILE}.obj", f'{ANIM_FOLDER}/{ANIM_FILE}.fbx', f'{OUTPUT_FOLDER}/{MODEL_FILE}_{ANIM_FILE}.fbx', target_height=1)
    print("Done")