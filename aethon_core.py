import os
import subprocess
import platform

class AethonEngine:
    def __init__(self, blender_path=None):
        if blender_path:
            self.blender_path = blender_path
        else:
            system = platform.system()
            if system == "Windows":
                self.blender_path = r"C:\Program Files\Blender Foundation\Blender 3.6\blender.exe"
            elif system == "Darwin":
                self.blender_path = "/Applications/Blender.app/Contents/MacOS/Blender"
            else:
                self.blender_path = "blender"
        
        self.output_path = "aethon_output.glb"

    def generate_script(self, ai_mesh_code):
        script = f'''
import bpy
import math

bpy.ops.wm.read_factory_settings(use_empty=True)

def apply_pro_material(obj, name, color, metal=0.9, rough=0.2, emiss=0.5):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = color
        bsdf.inputs['Metallic'].default_value = metal
        bsdf.inputs['Roughness'].default_value = rough
    obj.data.materials.append(mat)

# AI tarafından üretilen kod buraya yerleşir
{ai_mesh_code}

if bpy.context.active_object:
    apply_pro_material(bpy.context.active_object, "AethonSurface", (0, 0.95, 1, 1))

bpy.ops.export_scene.gltf(filepath="{self.output_path}", export_format='GLB')
'''
        with open("temp_engine.py", "w", encoding="utf-8") as f:
            f.write(script)

    def run(self):
        try:
            subprocess.run([self.blender_path, "-b", "-P", "temp_engine.py"], capture_output=True, text=True, check=True)
            return self.output_path
        except Exception as e:
            print(f"Aethon Motor Hatası: {{e}}")
            return None
