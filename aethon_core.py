import os
import subprocess
import platform
import shutil

class AethonEngine:
    def __init__(self, blender_path=None):
        self.output_path = "aethon_output.glb"
        self.blender_path = blender_path or self._find_blender()

    def _find_blender(self):
        # 1. PATH kontrolü
        path = shutil.which("blender")
        if path: return path
        
        # 2. Linux / Streamlit Cloud için derin arama
        linux_paths = ["/usr/bin/blender", "/usr/local/bin/blender", "/usr/bin/blender-softwaregl"]
        for p in linux_paths:
            if os.path.exists(p): return p
            
        return "blender"

    def generate_script(self, prompt, color_code="(0, 0.95, 1, 1)", height=10):
        # Model üretim senaryosu
        is_drone = "drone" in prompt.lower()
        script = f'''
import bpy
bpy.ops.wm.read_factory_settings(use_empty=True)
def apply_mat(obj, color):
    mat = bpy.data.materials.new(name="Mat")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs['Base Color'].default_value = color
    bsdf.inputs['Metallic'].default_value = 0.9
    bsdf.inputs['Roughness'].default_value = 0.2
    obj.data.materials.append(mat)

bpy.ops.mesh.primitive_cube_add(size=1, location=(0,0,{height}/2))
obj = bpy.context.object
obj.scale = (2, 2, {height})

# Bevel (Kalite artırıcı)
bev = obj.modifiers.new(name="B", type='BEVEL')
bev.width = 0.05
bpy.ops.object.modifier_apply(modifier="B")

apply_mat(obj, {color_code})
bpy.ops.export_scene.gltf(filepath="{self.output_path}", export_format='GLB')
'''
        with open("temp_engine.py", "w", encoding="utf-8") as f:
            f.write(script)

    def run(self):
        try:
            # Blender'ı arka planda (headless) çalıştır
            # capture_output=True sayesinde tüm detayları loglara yazdırıyoruz
            result = subprocess.run(
                [self.blender_path, "-b", "-P", "temp_engine.py"],
                capture_output=True,
                text=True,
                check=True
            )
            print("--- BLENDER ÇIKTISI ---")
            print(result.stdout)
            return self.output_path
        except Exception as e:
            # Hata anında log ekranına (siyah ekran) bu bilgiler düşecek
            print("!!! AETHON MOTORU KRİTİK HATA !!!")
            print(f"Denenen Blender Yolu: {self.blender_path}")
            if hasattr(e, 'stderr') and e.stderr:
                print(f"Blender Hatası: {e.stderr}")
            else:
                print(f"Sistem Hatası: {e}")
            return None
