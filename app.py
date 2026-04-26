import streamlit as st
from aethon_core import AethonEngine
import os

# Sayfa Ayarları
st.set_page_config(page_title="AETHON AI", page_icon="🛸", layout="wide")

# Aethon Engine'i Başlat
# Not: Localde çalıştırırken blender_path'i kendi bilgisayarına göre güncellemelisin.
engine = AethonEngine(blender_path="blender") 

st.title("🛸 AETHON 3D Generator")
st.write("Hayalindeki tasarımı yaz, AI saniyeler içinde 3D modelini oluştursun.")

# Kullanıcı Girişi
with st.sidebar:
    st.header("Tasarım Parametreleri")
    color = st.color_picker("Neon Rengi Seç", "#00F2FF")
    # Streamlit renk kodunu Blender formatına çevir (0-1 aralığı)
    r = int(color[1:3], 16) / 255
    g = int(color[3:5], 16) / 255
    b = int(color[5:7], 16) / 255
    blender_color = f"({r}, {g}, {b}, 1)"

prompt = st.text_input("Ne üretmek istersin?", placeholder="Örn: Agresif bir drone...")

if st.button("İNŞA ET"):
    if prompt:
        with st.spinner("Aethon Motoru çalışıyor..."):
            # 1. Scripti Oluştur
            engine.generate_script(prompt, color_code=blender_color)
            
            # 2. Blender'ı Çalıştır
            output_file = engine.run()
            
            if output_file and os.path.exists(output_file):
                st.success("Tasarım Başarıyla Oluşturuldu!")
                
                # 3. Modeli İndirme Butonu
                with open(output_file, "rb") as f:
                    st.download_button(
                        label="📦 .GLB Dosyasını İndir",
                        data=f,
                        file_name="aethon_output.glb",
                        mime="model/gltf-binary"
                    )
            else:
                st.error("Hata: Blender çalıştırılamadı. Yolun doğru olduğundan emin olun.")
    else:
        st.warning("Lütfen bir prompt girin.")
