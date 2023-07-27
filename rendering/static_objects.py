import bpy
import os
from math import radians

class StaticObjects:
    
    CUBE = bpy.ops.mesh.primitive_cube_add
    PLANE = bpy.ops.mesh.primitive_plane_add
    SPHERE = bpy.ops.mesh.primitive_uv_sphere_add
    
    @staticmethod
    def create(
        create_func, position: tuple[float, float, float]=(0,0,0), rotation: tuple[float, float, float]=(0,0,0), 
        scale: tuple[float, float, float]=(0,0,0), name="Object"
    ):
        """Create a primitive object

        Args:
            create_func (Callable): The function used to create the object [CUBE / PLANE / SPHERE]
            position (tuple[float, float, float], optional): _description_. Defaults to (0,0,0).
            rotation (tuple[float, float, float], optional): _description_. Defaults to (0,0,0).
            scale (tuple[float, float, float], optional): _description_. Defaults to (0,0,0).
            name (str, optional): _description_. Defaults to "Object".

        Returns:
            bpy.types.Object: The new object
        """
        create_func(
            location=position, 
            rotation=tuple(map(radians, rotation)), 
            scale=scale
        )
        bpy.context.active_object.name = name
        return bpy.context.active_object
    
    @staticmethod
    def load_water(scale: float=6, position: tuple[float, float, float]=(0, -6, 0)):
        """Load a water object

        Args:
            scale (float, optional): The scale of the water. Defaults to 6.
            position (tuple[float, float, float], optional): The position of the water. Defaults to (0, -6, 0).
        """
        working_dir = os.path.dirname(bpy.data.filepath)
        file = os.path.join(working_dir, "water.blend")
        inner_path = 'Object'
        object_name = 'Water'
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.wm.append(
            filename=f"{file}/{inner_path}/{object_name}"
        )
        water = bpy.context.selected_objects[0]
        water.scale = (scale, scale, scale)
        water.location = position
    
    @staticmethod
    def load_image(filepath: str, scale: float=12, rotation: tuple[float, float, float]=(90, 0, 0), name: str="Background"):
        """Load an image

        Args:
            filepath (str): The path to the image
            scale (float, optional): The scale of the image. Defaults to 12.
            rotation (tuple[float, float, float], optional): The rotation of the image. Defaults to (90, 0, 0).
            name (str, optional): The name for the image object. Defaults to "Background".

        Returns:
            bpy.types.Object: The image object
        """
        print(f"IMAGE FILE: {filepath}")
        bpy.ops.import_image.to_plane(files=[{"name":filepath}], relative=False)

        # Setup the image
        image = bpy.context.active_object
        image.name = name
        image.rotation_euler = tuple(map(radians, rotation))
        bpy.ops.object.transform_apply()

        # Placing it around 0
        # Not sure why it needs to be negative
        image.location.z -= min(v[2] for v in image.bound_box)
        image.location.y += min(v[1] for v in image.bound_box)
        bpy.ops.object.transform_apply()
        
        
        # Turn off shadows
        bpy.context.object.active_material.shadow_method = 'NONE'
        image.scale *= scale
        return image