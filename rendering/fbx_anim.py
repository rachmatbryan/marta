import bpy
from mathutils import Vector

class FbxAnimation:
    """Represents an animated armature loaded from an fbx file. 
    Provides functionality for easily looping and playing the animation.
    """
    
    def __init__(self, filepath: str):
        self._load_fbx(filepath)
        
    def loop_anim(self, start_frame: int, end_frame: int):
        """Loop the animation between two frames

        Args:
            start_frame (int): The starting frame
            end_frame (int): The ending frame
        """
        for frame in range(start_frame, end_frame, self.length):
            self.play_anim(frame, end_frame)
        self.show_start(end_frame)
            
    def show_start(self, frame: int):
        """Show the first frame of the animation at [frame]
        
        Useful for resetting the animation to a default pose

        Args:
            frame (int): The frame at which to show the start of the animation
        """
        for curve in self.action.fcurves:
            if curve.data_path not in self.anim_data: continue
            if curve.array_index not in self.anim_data[curve.data_path]: continue
            data = self.anim_data[curve.data_path][curve.array_index]
            keyframe = data[0]
            frame = keyframe[0] + frame
            curve.keyframe_points.insert(frame, keyframe[1])
    
    def play_anim(self, start_frame: int, end_frame: int | float = float('inf')):
        """Play one cycle of the animation beginning at [start_frame] and ending either after one loop or [end_frame]

        Args:
            start_frame (int): The starting frame to play at
            end_frame (int, optional): The frame to stop the animation at. Defaults to float('inf').
        """
        for curve in self.action.fcurves:
            # Skip over any curves for which there is no data
            if curve.data_path not in self.anim_data: continue
            if curve.array_index not in self.anim_data[curve.data_path]: continue
            
            # Set the keyframes
            data = self.anim_data[curve.data_path][curve.array_index]
            for keyframe in data:
                frame = keyframe[0] + start_frame
                
                # Skip any frames past [end_frame]
                if frame > end_frame: continue
                curve.keyframe_points.insert(frame, keyframe[1])
    
    def _find_child_armature(self, object: bpy.types.Object) -> bpy.types.Object | None:
        """Recursively search through the object heirarchy until an armature object is found

        Args:
            object (bpy.types.Object): The root object

        Returns:
            bpy.types.Object: The armature object
        """
        if object.type == 'ARMATURE':
            return object
        for child in object.children:
            child_arm = self._find_child_armature(child)
            if child_arm:
                return child_arm
        return None
        
    def _load_fbx(self, filepath: str):
        """Load and fbx animation from a file

        Args:
            filepath (str): The filpath of the animation to load
        """
        
        # Import the model
        bpy.ops.import_scene.fbx(filepath=filepath)
        
        # Find the root object
        root = bpy.context.active_object
        bpy.ops.object.select_all(action='DESELECT')
        while root.parent:
            root = root.parent
        self.root = root
        
        # Get information aboyt the animation
        self.armature = self._find_child_armature(root)
        self.action = self.armature.animation_data.action
        self.first_frame = int(min(min(kf.co.x for kf in fc.keyframe_points) for fc in self.action.fcurves))
        self.last_frame = int(max(max(kf.co.x for kf in fc.keyframe_points) for fc in self.action.fcurves))
        self.length = self.last_frame - self.first_frame
        self.hip_name = self._get_hip_bone_name()
        self.cycle_offset = self._get_cycle_offset()
        self.move_directon = self.cycle_offset.normalized()
        
        # Copy the animation data and clear the animation
        self.anim_data = self._copy_anim_data()
        self._clear_anim()
        
    def _clear_anim(self):
        """Clear the animation
        
        Does not clear copied animation data
        """
        for curve in self.action.fcurves:
            curve.keyframe_points.clear()
        
    def _copy_anim_data(self) -> dict[str, dict[int, list[tuple[int, float]]]]:
        """Create a copy of the animation data
        
        The copied data is indexed first by fcurve data path, then channel
        and contains a list of the keyframe positions for that datapath and channe;

        Returns:
            dict[str, dict[int, list[tuple[int, float]]]]: The copied animation data
        """
        
        copied_data = {}
        for curve in self.action.fcurves:
            data_path = curve.data_path
            array_index = curve.array_index
            
            # Make sure there is a place to store the data
            if data_path not in copied_data:
                copied_data[data_path] = {}
                
            # Copy the keyframe positions into the data path and channel
            copied_data[data_path][array_index] = [(k.co.x - self.first_frame, k.co.y) for k in curve.keyframe_points]
        return copied_data
        
    def _get_cycle_offset(self) -> Vector:
        """Get the amount that the amature moves with each animation cycle
        
        The hip bone is used to find this offset
        The z offset is always 0

        Returns:
            Vector: The movement between cycles
        """
        start_pos = [0, 0, 0]
        end_pos = [0, 0, 0]
        for curve in self.action.fcurves:
            # Find a curve that modifies the location of the hip bone
            if self.hip_name not in curve.data_path: continue
            if "location" not in curve.data_path: continue
            channel = curve.array_index
            
            # Use the keyframes to find the start and end locations
            start_pos[channel] = curve.keyframe_points[0].co.y
            end_pos[channel] = curve.keyframe_points[-1].co.y
            
        # Convert the positions to world coordinates to account for things like rotations and scaling
        start_pos_world = Vector(start_pos) @ self.armature.matrix_world
        end_pos_world = Vector(end_pos) @ self.armature.matrix_world
        offset = [-(end_pos_world[i] - start_pos_world[i]) for i in range(3)]
        
        # Cancel any z offset
        offset[2] = 0
        return Vector(offset)
        
    def _get_hip_bone_name(self) -> str:
        """Get the name of the hip bone
        
        Searches for any bone that includes 'hip'

        Raises:
            Exception: When no hip bone is found

        Returns:
            str: The name of the hip bone
        """
        for bone in self.armature.data.bones:
            if "hip" in bone.name.lower():
                return bone.name
        raise Exception("Rig has no hip bone")