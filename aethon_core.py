import os
import subprocess
import platform
import shutil

class AethonEngine:
    def __init__(self, blender_path=None):
        self.output_path = "aethon_output.glb"
        self.blender_path = blender_path or self._find_blender()

    def _find_blender(self):
        # PATH ve standart klasörleri tara
        path = shutil.which("blender")
        if path: return path
        linux_paths = ["/usr/bin/blender", "/usr/local/bin/blender"]
        for p in linux_paths:
            if os.path.exists(p): return p
        return "blender"

    def generate_script(self, prompt, color_code="(0, 0.95, 1, 1)", height=10):
        # AI Analiz: Drone mu Kule mi?
        is_drone = "drone" in prompt.lower()
        
        script = f'''
import bpy
# Fabrika ayarlarıyla başlat (Hata riskini azaltır)
bpy.ops.wm.read_factory_settings(use_empty=True)

def apply_mat(obj, color):
    mat = bpy.data.materials.new(name="AethonMat")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = color
        bsdf.inputs['Metallic'].default_value = 0.9
        bsdf.inputs['Roughness'].default_value = 0.2
    obj.data.materials.append(mat)

if {is_drone}:
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0,0,1))
    obj = bpy.context.object
    obj.scale = (1.5, 1, 0.2)
else:
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0,0,{height}/2))
    obj = bpy.context.object
    obj.scale = (2, 2, {height})

# Profesyonel Dokunuş: Bevel
bev = obj.modifiers.new(name="B", type='BEVEL')
bev.width = 0.05
bpy.ops.object.modifier_apply(modifier="B")

apply_mat(obj, {color_code})

# GLB Olarak Kaydet
bpy.ops.export_scene.gltf(filepath="{self.output_path}", export_format='GLB')
'''
        with open("temp_engine.py", "w", encoding="utf-8") as f:
            f.write(script)

    def run(self):
        try:
            # KRİTİK: --factory-startup ekleyerek tüm eklentileri devre dışı bırakıyoruz
            # Bu, sunucudaki Blender çakışmalarını önler.
            result = subprocess.run(
                [self.blender_path, "--background", "--factory-startup", "-P", "temp_engine.py"],
                capture_output=True,
                text=True,
                check=True
            )
            print("BLENDER BAŞARILI: Model üretildi.")
            return self.output_path
        except subprocess.CalledProcessError as e:
            print(f"!!! BLENDER HATASI !!!: {e.stderr}")
            return None
        except Exception as e:
            print(f"!!! SİSTEM HATASI !!!: {e}")
            return None
