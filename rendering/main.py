import bpy
import os, sys
import glob
import addon_utils
from math import radians
import imp

# Add the scripts folder to the path
WORKING_DIR = os.path.dirname(bpy.data.filepath)
sys.path.append(f'{WORKING_DIR}/rendering')

import static_objects
import fbx_anim
import animated_object
import renderer


imp.reload(static_objects) 
imp.reload(fbx_anim)
imp.reload(animated_object)
imp.reload(renderer)

from static_objects import StaticObjects
from animated_object import AnimatedObject
from fbx_anim import FbxAnimation
from renderer import Renderer

BACKGROUND_IMAGE = f"{WORKING_DIR}/images/background.jpeg" 
GROUND_IMAGE = f"{WORKING_DIR}/images/ground.png"
SKYBOX_FILE = f"{WORKING_DIR}/images/skybox.hdr"

OUTPUT_PATH = f"{WORKING_DIR}/output/result.mp4"

FBX_PATH = f"{WORKING_DIR}/rigged/t_pose_Walking.fbx"
        
def main():
    addon_utils.enable("io_import_images_as_planes")
    
    Renderer.setup(Renderer.CYCLES)
    Renderer.load_basic_scene(BACKGROUND_IMAGE, GROUND_IMAGE, use_water=True)
   
    # Testing
    character = AnimatedObject("Test", 2)
    character.add_fbx_anim("cartwheel", FBX_PATH)
    end_frame = character.animate_path("cartwheel", (-6, -2, 0), (6, -2, 0), 0)
    
    Renderer.set_animation_length(end_frame)
    bpy.ops.view_3d.view_camera()
#    Renderer.render(OUTPUT_PATH)
    
if __name__ == "__main__":
    main()
