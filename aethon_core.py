import os
import subprocess
import platform
import shutil

class AethonEngine:
    def __init__(self, blender_path=None):
        """
        Aethon Engine: Blender yolunu otomatik tespit eden ve 3D model üreten ana motor.
        """
        if blender_path:
            self.blender_path = blender_path
        else:
            # Otomatik tespit mekanizması (Windows, Mac, Linux/Streamlit)
            self.blender_path = self._find_blender()
        
        self.output_path = "aethon_output.glb"

    def _find_blender(self):
        system = platform.system()
        
        # 1. Adım: Sistem PATH'i üzerinde 'blender' komutunu ara
        which_path = shutil.which("blender")
        if which_path:
            return which_path
            
        # 2. Adım: İşletim sistemine göre en yaygın kurulum yollarını kontrol et
        if system == "Windows":
            standard_paths = [
                r"C:\Program Files\Blender Foundation\Blender 3.6\blender.exe",
                r"C:\Program Files\Blender Foundation\Blender 4.0\blender.exe",
                r"C:\Program Files\Blender Foundation\Blender 4.1\blender.exe",
                r"C:\Program Files\Blender Foundation\Blender 3.3\blender.exe"
            ]
        elif system == "Darwin": # macOS
            standard_paths = [
                "/Applications/Blender.app/Contents/MacOS/Blender"
            ]
        else: # Linux (Streamlit Cloud, Colab vb.)
            standard_paths = [
                "/usr/bin/blender",
                "/usr/local/bin/blender",
                "/usr/bin/blender-softwaregl",
                "/snap/bin/blender"
            ]
            
        for p in standard_paths:
            if os.path.exists(p):
                return p
        
        # Hiçbir şey bulunamazsa varsayılan komutu döndür
        return "blender"

    def generate_script(self, prompt, color_code="(0, 0.95, 1, 1)", height=10):
        """
        Kullanıcı komutuna göre Blender Python scriptini oluşturur.
        """
        is_drone = "drone" in prompt.lower()
        is_high = any(word in prompt.lower() for word in ["yüksek", "kule", "tower", "high"])
        
        script = f'''
import bpy
import math

# Sahneyi sıfırla
bpy.ops.wm.read_factory_settings(use_empty=True)

def apply_pro_material(obj, name, color, metal=0.9, rough=0.2, emiss=10):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    
    # Profesyonel PBR Materyal Ayarları
    bsdf.inputs['Base Color'].default_value = color
    bsdf.inputs['Metallic'].default_value = metal
    bsdf.inputs['Roughness'].default_value = rough
    bsdf.inputs['Emission'].default_value = color
    bsdf.inputs['Emission Strength'].default_value = emiss
    obj.data.materials.append(mat)

# --- GEOMETRİ ÜRETİMİ ---
if {is_drone}:
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0,0,1))
    main_obj = bpy.context.object
    main_obj.scale = (1.5, 1, 0.2)
else:
    h = {height} if {is_high} else 4
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0,0,h/2))
    main_obj = bpy.context.object
    main_obj.scale = (2, 2, h)

# ✨ 9 PUANLIK KALİTE: Bevel (Pah Kırma)
bev = main_obj.modifiers.new(name="Bevel", type='BEVEL')
bev.width = 0.05
bev.segments = 5
bpy.ops.object.modifier_apply(modifier="Bevel")

# Materyal Uygulama
apply_pro_material(main_obj, "AethonSurface", {color_code})

# --- DIŞA AKTARIM (GLB) ---
bpy.ops.export_scene.gltf(filepath="{self.output_path}", export_format='GLB')
'''
        with open("temp_engine.py", "w", encoding="utf-8") as f:
            f.write(script)

    def run(self):
        """
        Blender'ı arka planda çalıştırır.
        """
        try:
            result = subprocess.run(
                [self.blender_path, "-b", "-P", "temp_engine.py"],
                capture_output=True,
                text=True,
                check=True
            )
            return self.output_path
        except Exception as e:
            print(f"AETHON ERROR: {e}")
            return None
