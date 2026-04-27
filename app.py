import streamlit as st
from aethon_core import AethonEngine
from transformers import pipeline
import os

# Sayfa Ayarı
st.set_page_config(page_title="Aethon 3D", layout="wide")

# AI Modeli Yükle (Hafif ve hızlı sürüm)
@st.cache_resource
def load_ai():
    return pipeline("text-generation", model="Qwen/Qwen2-0.5B-Instruct", device_map="auto")

pipe = load_ai()
engine = AethonEngine()

st.title("🛸 Aethon v4.0 Tasarım Paneli")

user_req = st.text_input("Ne inşa etmek istersin?", placeholder="Örn: Modern bir drone")

if st.button("İnşa Et"):
    with st.spinner("AI tasarlıyor ve Blender çiziyor..."):
        # AI sadece mesh kodunu yazar
        prompt = f"<|im_start|>user\nWrite ONLY Blender Python mesh code for: {user_req}. No imports.<|im_end|>\n<|im_start|>assistant\n"
        ai_output = pipe(prompt, max_new_tokens=500)
        mesh_code = ai_output[0]['generated_text'].split("assistant\n")[-1].split("```")[0].strip()

        # Motoru çalıştır
        engine.generate_script(mesh_code)
        output_file = engine.run()

        if output_file and os.path.exists(output_file):
            st.success("İnşaat Tamamlandı!")
            with open(output_file, "rb") as f:
                st.download_button("📥 3D Modeli İndir", f, file_name="aethon_model.glb")
        else:
            st.error("Bir hata oluştu.")
