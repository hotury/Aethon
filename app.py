from transformers import pipeline
import torch
from google.colab import files
import os

# 1. AI Motorunu Hazırla (Beyin)
print("🧠 Aethon Beyni Hazırlanıyor...")
pipe = pipeline("text-generation", model="Qwen/Qwen2-0.5B-Instruct", device_map="auto")

# 2. Senin Güncellediğin Core'u Başlat
# aethon_core.py dosyasının yüklü olduğundan emin ol
from aethon_core import AethonEngine
engine = AethonEngine()

def build_smart_3d():
    user_req = input("\n🛸 Ne inşa edelim? (Örn: 'Modern bir drone'): ")
    
    # AI'ya sadece mesh (geometri) kısmını yazdırıyoruz
    prompt = f"<|im_start|>user\nWrite ONLY the Blender Python code to create the mesh for: {user_req}. Use 'bpy.ops.mesh' commands. Do not include imports or exports.<|im_end|>\n<|im_start|>assistant\n"
    
    print("🧠 AI Tasarlıyor...")
    output = pipe(prompt, max_new_tokens=500, do_sample=True, temperature=0.4)
    ai_mesh_code = output[0]['generated_text'].split("<|im_start|>assistant\n")[-1].split("```")[0].strip()

    # Core motoru AI koduyla besle
    print("🛠️ Blender İnşa Ediyor...")
    engine.generate_script(ai_mesh_code)
    output_file = engine.run()

    if output_file and os.path.exists(output_file):
        print(f"🚀 BAŞARILI! {output_file} indiriliyor...")
        files.download(output_file)
    else:
        print("⚠️ Hata oluştu. AI kodunu kontrol et:\n", ai_mesh_code)

# Çalıştır
build_smart_3d()
