import bpy
from math import radians, atan2, floor
from mathutils import Vector

from fbx_anim import FbxAnimation

class AnimatedObject:
    """Represents and object that could have multiple animations and provides functionality for animating the object
    """
    
    def __init__(self, name: str="Object", scale: float=1):
        self.scale = scale
        self.animations = {}
        self.fbx_anims = {}
        bpy.ops.object.empty_add() 
        self.root = bpy.context.active_object
        self.root.name = name
        self.root.scale = (scale, scale, scale)
        self.root.keyframe_insert(data_path="scale", frame=0)
        
        # Resetting the scale because it messes with adding other objects
        self.root.scale = (1, 1, 1)
        
    def add_animation(self, name: str, anim_object: bpy.types.Object):
        """Add an animation to this object

        Args:
            name (str): The name of the animation
            anim_object (bpy.types.Object): The object to use for the animation
        """
        self.animations[name] = anim_object
        
        # Parent anim_object to the root
        bpy.ops.object.select_all(action='DESELECT')
        anim_object.select_set(True)
        self.root.select_set(True)
        bpy.context.view_layer.objects.active = self.root
        bpy.ops.object.parent_set(type='OBJECT', keep_transform=False)
        
    def add_fbx_anim(self, anim_name: str, filepath: str):
        """Add an fbx animation to this object

        Args:
            anim_name (str): The name of the animation
            filepath (str): The file containing the animation
        """
        anim = FbxAnimation(filepath)
        self.add_animation(anim_name, anim.root)
        self.fbx_anims[anim_name] = anim
        
    def animate_path(
        self, anim_name: str, start_pos: tuple[float, float, float] | Vector, end_pos: tuple[float, float, float] | Vector, start_frame: int
    ) -> int:
        """Move the object along a line between two points while looping an animation
        
        Accounts for animations that move the entire object and then reset to the center by only moving the position at the end of each
        animation cycle

        Args:
            anim_name (str): The name of the animation to loop
            start_pos (tupe[float, float, float] | Vector): The starting position of the animation
            end_pos (tuple[float, float, float] | Vector): The ending position of the animation
            start_frame (int): The frame at which to start moving along the path

        Returns:
            int: The frame at which the object reaches the end
        """
        # Get the animation
        if anim_name not in self.fbx_anims: raise Exception(f"Unkown animation: {anim_name}")
        anim = self.fbx_anims[anim_name]
        
        start_pos = Vector(start_pos)
        end_pos = Vector(end_pos)
        
        
        # Find the number of animation cycles and the end frame
        cycle_offset_length = anim.cycle_offset.length * self.scale
        cycles = (end_pos - start_pos).length / cycle_offset_length
        end_frame = floor(cycles * anim.length)
        
        # Loop the animation while traveling the path
        anim.loop_anim(start_frame, end_frame) 
        
        # Point in the direction of the path
        direction = (end_pos - start_pos).normalized()
        self.root.rotation_euler[2] = atan2(direction.y, direction.x) + radians(90)
        
        # Set the animation and starting and ending positions
        self.set_animation(anim_name, start_frame)
        self.set_position(start_pos, start_frame)
        self.set_position(end_pos, end_frame)
        
        # Determine how far to move the character every frame
        cycle_offset = direction * cycle_offset_length
        position = start_pos
        
        # Move the character after each cycle
        for i in range(floor(cycles)):
            frame = start_frame + anim.length * (i + 1)
            self.set_position(position, frame-1)
            position = tuple(position[i] + cycle_offset[i] for i in range(3))
            self.set_position(position, frame)
        self.set_position(position, end_frame - 1)
        
        return end_frame
    
    def loop_animation(self, anim_name: str, start_frame: int, end_frame: int):
        """Loop animation [anim_name] from [start_frame] to [end_frame]

        Args:
            anim_name (str): The name of the animation
            start_frame (int): The starting frame of the loop
            end_frame (int): The ending frame of the loop
        """
        if anim_name not in self.fbx_anims: raise Exception(f"Unkown animation: {anim_name}")
        anim = self.fbx_anims[anim_name]
        anim.loop_anim(start_frame, end_frame) 
        
    def set_animation(self, name: str, frame: int):
        """Switch to a new animation

        Args:
            name (str): The name of the animation
            frame (int): The frame on which to switch
        """
        for anim_name in self.animations:
            anim = self.animations[anim_name]
            hide = anim_name != name
            anim.hide_viewport = hide
            anim.hide_render = hide
            anim.keyframe_insert(data_path="hide_viewport", frame=frame) 
            anim.keyframe_insert(data_path="hide_render", frame=frame)
            
    def set_visible(self, visible: bool, frame: int):
        """Set the visibility of the object on a frame
        
        Also affects the visibility on all following frames until the next frame where visibility is set

        Args:
            visible (bool): The visibility of the object
            frame (int): The frame to set the visibility for
        """
        self.root.hide_viewport = visible
        self.root.hide_render = visible
        self.root.keyframe_insert(data_path="hide_viewport", frame=frame)
        self.root.keyframe_insert(data_path="hide_render", frame=frame)
        
    def set_position(self, position: tuple[int, int, int] | Vector, frame: int):
        """Create a position keyframe for this object

        Args:
            position (tuple[float, float, float] | Vector): The position for the object
            frame (int): The frame to place the keyframe at
        """
        self.root.location = position
        self.root.keyframe_insert(data_path="location", frame=frame)
    
    def set_rotation(self, rotation: tuple[float, float, float], frame: int):
        """Create a rotation keyframe for this object

        Args:
            rotation (tuple[float, float, float]): The euler rotation for the object in degrees
            frame (int): The frame to place the keyframe at
        """
        self.root.rotation_euler = tuple(map(radians, rotation))
        self.root.keyframe_insert(data_path="rotation_euler", frame=frame)