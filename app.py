import streamlit as st
from aethon_core import AethonEngine
from transformers import pipeline
import os

# Sayfa yapılandırması
st.set_page_config(page_title="Aethon 3D Designer", layout="wide")

# AI modelini yükle (İşlemci dostu sürüm)
@st.cache_resource
def load_ai():
    return pipeline("text-generation", model="Qwen/Qwen2-0.5B-Instruct", device_map="auto")

pipe = load_ai()
engine = AethonEngine()

st.title("🛸 Aethon v4.0: Profesyonel 3D Tasarım")
st.write("Detaylı komutlar verin (Örn: 'İçinde bir masa ve iki sandalye olan bir oda çiz')")

user_req = st.text_input("Tasarım Fikriniz:", placeholder="Modern bir ofis odası...")

if st.button("İnşa Et"):
    if user_req:
        with st.spinner("AI mimariyi planlıyor ve Blender inşa ediyor..."):
            # AKILLI PROMPT: AI'yı kutu çizmekten vazgeçiren talimat
            prompt = f"""
            <|im_start|>system
            Sen profesyonel bir Blender Python uzmanısın. 
            Basit bir kutu çizmek yerine, sahnede birden fazla obje (duvarlar, zemin, mobilya parçaları) oluşturmalısın.
            Her obje için bpy.ops.mesh komutlarını kullan ve objelerin konumlarını (location) ve boyutlarını (scale) mantıklı ayarla.
            <|im_end|>
            <|im_start|>user
            Görev: {user_req} için detaylı bir Blender Python kodu yaz. Sadece kodu ver, açıklama yapma.
            <|im_end|>
            <|im_start|>assistant
            """
            
            ai_output = pipe(prompt, max_new_tokens=1000, do_sample=True, temperature=0.4)
            mesh_code = ai_output[0]['generated_text'].split("assistant\n")[-1].split("```")[0].strip()

            # Motoru çalıştır
            engine.generate_script(mesh_code)
            output_file = engine.run()

            if output_file and os.path.exists(output_file):
                st.success("Tasarım Başarıyla Tamamlandı!")
                with open(output_file, "rb") as f:
                    st.download_button("📥 3D Modeli İndir (.glb)", f, file_name="aethon_design.glb")
            else:
                st.error("Blender inşa sırasında bir sorunla karşılaştı.")
                st.code(mesh_code, language="python") # Hatayı görmek için kodu göster
    else:
        st.warning("Lütfen bir şeyler yazın.")
