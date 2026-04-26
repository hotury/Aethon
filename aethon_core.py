
import os
import subprocess

class AethonEngine:
    def __init__(self, blender_path="./blender-3.6.0-linux-x64/blender"):
        self.blender_path = blender_path
        self.output_path = "aethon_output.glb"

    def generate_script(self, prompt, color_code="(0, 0.95, 1, 1)", height=10):
        # AI Analiz Mantığı (Burayı daha da geliştirebilirsin)
        is_drone = "drone" in prompt.lower()
        
        script = f'''
import bpy
import math

bpy.ops.wm.read_factory_settings(use_empty=True)

def apply_material(obj, name, color, emiss=10):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs['Base Color'].default_value = color
    bsdf.inputs['Emission'].default_value = color
    bsdf.inputs['Emission Strength'].default_value = emiss
    obj.data.materials.append(mat)

# ANA ÜRETİM
if {is_drone}:
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0,0,1))
    main_obj = bpy.context.object
    main_obj.scale = (1.5, 1, 0.2)
else:
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0,0,{height}/2))
    main_obj = bpy.context.object
    main_obj.scale = (2, 2, {height})

apply_material(main_obj, "AethonSurface", {color_code})

# EXPORT
bpy.ops.export_scene.gltf(filepath="{self.output_path}", export_format='GLB')
'''
        with open("temp_engine.py", "w") as f:
            f.write(script)

    def run(self):
        if os.path.exists(self.blender_path):
            subprocess.run([self.blender_path, "-b", "-P", "temp_engine.py"])
            return self.output_path
        return None

# Örnek Kullanım:
# engine = AethonEngine()
# engine.generate_script("Neon Mavi Drone", color_code="(0, 0.5, 1, 1)")
# engine.run()
