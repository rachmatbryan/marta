import bpy
import os, sys
import addon_utils
import importlib

# Add the scripts folder to the path
WORKING_DIR = os.getcwd()
sys.path.append(f'{WORKING_DIR}/rendering')

import static_objects
import fbx_anim
import animated_object
import renderer
import scene_setup

# This makes sure to use the most recent versions of the files
importlib.reload(static_objects) 
importlib.reload(fbx_anim)
importlib.reload(animated_object)
importlib.reload(renderer)
importlib.reload(scene_setup)

from renderer import Renderer

def main():
    arg_index = sys.argv.index('--') + 1
    args = sys.argv[arg_index:]
    scene_file = args[0]
    output_file = args[1]
    addon_utils.enable("io_import_images_as_planes")
    scene_setup.setup_scene(scene_file)
    Renderer.render(os.path.join(os.getcwd(), output_file))

main()
bpy.ops.wm.quit_blender()