import os
from renderer import Renderer
from animated_object import AnimatedObject

def setup_scene(filepath):
    """Read a scene file and setup the scene

    Args:
        filepath (str): The path to the scene value
    """
    
    print("Setting up scene")
    working_directory = os.getcwd()
    with open(filepath, 'r') as scene_file:
        
        background_image = ''
        ground_image = ''
        use_water = False
        render_mode = Renderer.EEVEE
        character_scale = 1
        characters = {}
        anim_length = 0
        
        line = scene_file.readline()
        
        # Basic Scene Setup
        while line:
            if not line.strip():
                line = scene_file.readline()
                continue
            if line.startswith('CHARACTER '): break
            parts = line.split()
            match(parts[0]):
                case "BACKGROUND_IMAGE":
                    background_image = os.path.join(working_directory, parts[1])
                case "GROUND_IMAGE":
                    ground_image = os.path.join(working_directory, parts[1])
                case "USE_WATER":
                    use_water = parts[1] == 'True'
                case "USE_CYCLES":
                    render_mode = Renderer.CYCLES if parts[1] == 'True' else Renderer.EEVEE
                case "CHARACTER_SCALE":
                    character_scale = float(parts[1])
                case "ANIM_LENGTH":
                    anim_length = int(parts[1])
                case _:
                    raise Exception(f"Unkown Scene Setup Command: {line}")
            line = scene_file.readline()
        Renderer.setup(render_mode)
        Renderer.load_basic_scene(background_image, ground_image, use_water, working_dir=working_directory)
        
        print("Loading Characters")
        current_character = None
        while line:
            # Skip empty lines
            if not line.strip():
                line = scene_file.readline()
                continue
                
            # Stop when we reach the animation section
            if line.startswith('ANIMATION'): break
            
            # Read the character information
            parts = line.split()
            match(parts[0]):
                # Load a new character
                case "CHARACTER":
                    current_character = AnimatedObject(parts[1], character_scale)
                    characters[parts[1]] = current_character
                # Load a new animation
                case "anim":
                    if current_character == None: raise Exception("Anim defined before character!")
                    current_character.add_fbx_anim(parts[1], os.path.join(working_directory, parts[2]))
                case _:
                    raise Exception(f"Unkown Character Setup Command: {line}")
            line = scene_file.readline()
        
        print("Loading Animations")
        line = scene_file.readline()
        while line:
            # Skup empty lines
            if not line.strip():
                line = scene_file.readline()
                continue
            
            parts = line.split()
            if parts[0] not in characters: raise Exception(f"Unkown Character: {parts[0]}")
            character = characters[parts[0]]
            frame = 0
            
            # Parse each of the possible animation commands
            match(parts[1]):
                case "visible":
                    frame = int(parts[3])
                    character.set_visible(parts[2] == 'True', frame)
                case "position": 
                    frame = int(parts[5])
                    character.set_position(tuple(map(int, parts[2:5])), frame)
                case "rotation":
                    frame = int(parts[5])
                    character.set_rotation(tuple(map(int, parts[2:5])), frame)
                case "animation":
                    frame = int(parts[5])
                    character.set_animation(parts[2], frame)
                case "loop_anim":
                    frame = int(parts[4])
            
                    character.loop_animation(parts[2], int(parts[3]), int(parts[4]))
                case "path":
                    frame = character.animate_path(parts[2], tuple(map(int, parts[3:6])), tuple(map(int, parts[6:9])), int(parts[9]))
                case _:
                    raise Exception(f"Unkown Animation Command: {line}")
            anim_length = max(anim_length, frame)
            line = scene_file.readline()
        Renderer.set_animation_length(anim_length)