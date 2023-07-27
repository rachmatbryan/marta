import bpy
import os
from math import radians
from static_objects import StaticObjects

class Renderer:
    
    EEVEE = 1
    CYCLES = 2
    
    @staticmethod
    def setup(render_mode=EEVEE):
        Renderer.clear_scene()
        
        if render_mode == Renderer.EEVEE:
            eevee = bpy.context.scene.eevee
            eevee.use_ssr = True
            eevee.use_ssr_refraction = True
            eevee.ssr_quality = 1
            eevee.use_bloom = True
            eevee.bloom_threshold = 0.8
            eevee.bloom_knee = 0.5
            eevee.bloom_radius = 6.5
            eevee.bloom_intensity = 0.05
            eevee.bloom_clamp = 0
            bpy.context.scene.render.engine = 'BLENDER_EEVEE'
        elif render_mode == Renderer.CYCLES:
            cycles = bpy.context.scene.cycles
            cycles.device = 'GPU'
            cycles.samples = 1024
            cycles.adaptive_threshold = 0.1
            bpy.context.scene.render.engine = 'CYCLES'
        
    
    @staticmethod
    def clear_scene():
        if bpy.context.active_object and bpy.context.active_object.mode == 'EDIT':
            bpy.objps.object.editmode_toggle()
            
        for obj in bpy.data.objects:
            obj.hide_set(False)
            obj.hide_select = False
            obj.hide_viewport = False
            
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()
        
        bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)
        
    @staticmethod
    def load_basic_scene(background_image, ground_image="", use_water=False, working_dir=""):
        if working_dir == "":
            working_dir = os.path.dirname(bpy.data.filepath)
        skybox_file = os.path.join(working_dir, "images/skybox.hdr")
        
        print("Loading Skybox")
        Renderer.load_skybox(skybox_file)
        
        print("Loading background")
        StaticObjects.load_image(background_image)
        
        print("Loading Ground")
        if not use_water:
            StaticObjects.load_image(ground_image, rotation=(0, 0, 0), scale=12, name="Ground")
        else:
            StaticObjects.load_water()
        
        print("Setting up lighting and camera")
        Renderer.setup_camera()
        Renderer.load_light()
        
    @staticmethod
    def load_skybox(skybox_file):
        '''
        From @brokmann's answer to the question posted at
        https://blender.stackexchange.com/questions/209584/using-python-to-add-an-hdri-to-world-node
        '''
        world_node_tree = bpy.context.scene.world.node_tree
        world_nodes = world_node_tree.nodes
        world_nodes.clear()
        
        background_node = world_nodes.new(type='ShaderNodeBackground')
        environment_node = world_nodes.new('ShaderNodeTexEnvironment')
        environment_node.image = bpy.data.images.load(skybox_file)
        environment_node.location = (-300, 0)
        
        output_node = world_nodes.new(type='ShaderNodeOutputWorld')
        output_node.location = (200, 0)
        
        links = world_node_tree.links
        links.new(environment_node.outputs["Color"], background_node.inputs["Color"])
        links.new(background_node.outputs["Background"], output_node.inputs["Surface"])
        
    @staticmethod
    def setup_camera():
        bpy.ops.object.camera_add(rotation=(radians(80), 0, 0), location=(0, -15, 4))
        bpy.context.scene.camera = bpy.context.active_object
        return bpy.context.active_object
        
    @staticmethod
    def load_light(direction=(45, -40, 203), strength=5):
        bpy.ops.object.light_add(type='SUN', rotation=tuple(map(radians, direction)))
        sun = bpy.context.active_object
        sun.data.energy = strength
        return sun
    
    @staticmethod
    def set_animation_length(frames):
        bpy.context.scene.frame_end = frames
         
    @staticmethod
    def render(output_path):
        print("Beggining Render")
        bpy.context.scene.render.image_settings.file_format = 'FFMPEG'
        bpy.context.scene.render.filepath = output_path
        bpy.context.scene.render.ffmpeg.format = 'MPEG4'
        bpy.ops.render.render(animation=True)
        print(f"Saved animation to {output_path}")