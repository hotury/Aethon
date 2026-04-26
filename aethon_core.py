import os
import subprocess
import platform
import shutil

class AethonEngine:
    def __init__(self, blender_path=None):
        """
        Aethon Engine: Blender'ı bulmak için sunucuda derin arama yapar.
        """
        self.output_path = "aethon_output.glb"
        
        if blender_path:
            self.blender_path = blender_path
        else:
            self.blender_path = self._find_blender_pro()

    def _find_blender_pro(self):
        system = platform.system()
        
        # 1. YOL: Sistem PATH kontrolü (shutil)
        path_check = shutil.which("blender")
        if path_check:
            return path_check

        # 2. YOL: İşletim sistemine özel bilinen tüm yollar
        search_paths = []
        if system == "Windows":
            search_paths = [
                r"C:\Program Files\Blender Foundation\Blender 3.6\blender.exe",
                r"C:\Program Files\Blender Foundation\Blender 4.0\blender.exe",
                r"C:\Program Files\Blender Foundation\Blender 4.1\blender.exe"
            ]
        elif system == "Darwin": # macOS
            search_paths = ["/Applications/Blender.app/Contents/MacOS/Blender"]
        else: # Linux / Streamlit Cloud
            search_paths = [
                "/usr/bin/blender",
                "/usr/local/bin/blender",
                "/usr/bin/blender-softwaregl",
                "/usr/lib/blender",
                "blender"
            ]

        for path in search_paths:
            if os.path.exists(path):
                return path

        # Hiçbiri olmazsa son çare
        return "blender"

    def generate_script(self, prompt, color_code="(0, 0.95, 1, 1)", height=10):
        is_drone = "drone" in prompt.lower()
        is_high = any(word in prompt.lower() for word in ["yüksek", "kule", "tower", "high"])
        
        script = f'''
import bpy
import math

bpy.ops.wm.read_factory_settings(use_empty=True)

def apply_pro_material(obj, name, color, metal=0.9, rough=0.2, emiss=10):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    bsdf.inputs['Base Color'].default_value = color
    bsdf.inputs['Metallic'].default_value = metal
    bsdf.inputs['Roughness'].default_value = rough
    bsdf.inputs['Emission'].default_value = color
    bsdf.inputs['Emission Strength'].default_value = emiss
    obj.data.materials.append(mat)

if {is_drone}:
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0,0,1))
    main_obj = bpy.context.object
    main_obj.scale = (1.5, 1, 0.2)
else:
    h = {height} if {is_high} else 4
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0,0,h/2))
    main_obj = bpy.context.object
    main_obj.scale = (2, 2, h)

# 9 PUANLIK KALİTE: Bevel
bev = main_obj.modifiers.new(name="Bevel", type='BEVEL')
bev.width = 0.05
bev.segments = 5
bpy.ops.object.modifier_apply(modifier="Bevel")

apply_pro_material(main_obj, "AethonSurface", {color_code})
bpy.ops.export_scene.gltf(filepath="{self.output_path}", export_format='GLB')
'''
        with open("temp_engine.py", "w", encoding="utf-8") as f:
            f.write(script)

    def run(self):
        try:
            # Komutu tam yol ile çalıştırıyoruz
            result = subprocess.run(
                [self.blender_path, "-b", "-P", "temp_engine.py"],
                capture_output=True,
                text=True,
                check=True
            )
            return self.output_path
        except Exception as e:
            # Hata olduğunda terminale tam olarak neyin yanlış olduğunu yazar
            print(f"--- AETHON HATA RAPORU ---")
            print(f"Denenen Blender Yolu: {self.blender_path}")
            print(f"Hata Mesajı: {e}")
            return None
