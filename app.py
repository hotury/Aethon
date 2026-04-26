import streamlit as st
import os
import shutil
from aethon_core import AethonEngine

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Aethon 3D AI", page_icon="🛸")
st.title("🛸 Aethon 3D Tasarım Motoru")
st.write("Doğal dil ile 3D modeller oluşturun.")

# --- SİSTEM KONTROLÜ (KRİTİK) ---
# Streamlit Cloud'un Blender'ı kurup kurmadığını kontrol eder
blender_exists = shutil.which("blender")

if not blender_exists:
    st.error("⚠️ HATA: Blender sunucuda bulunamadı!")
    st.info("""
    **Çözüm Adımları:**
    1. GitHub reponda **packages.txt** adında bir dosya olduğundan emin ol.
    2. İçinde sadece **blender** yazdığından emin ol.
    3. Streamlit Cloud panelinden 'Reboot App' yap veya uygulamayı silip baştan kur.
    """)
else:
    st.success("✅ Blender Motoru Hazır!")

# --- KULLANICI ARAYÜZÜ ---
with st.sidebar:
    st.header("Tasarım Ayarları")
    color = st.color_picker("Model Rengi", "#00F2FF")
    height = st.slider("Yükseklik (Mimari için)", 1, 20, 10)
    
    # RGB formatına çevirme (Blender için 0-1 arası)
    hex_color = color.lstrip('#')
    rgb = tuple(int(hex_color[i:i+2], 16)/255 for i in (0, 2, 4))
    blender_color = f"({rgb[0]}, {rgb[1]}, {rgb[2]}, 1)"

prompt = st.text_input("Ne inşa etmek istersin?", placeholder="Örn: Modern bir kule veya fütüristik bir drone")

if st.button("🚀 TASARLA VE İNŞA ET"):
    if not prompt:
        st.warning("Lütfen bir komut girin.")
    elif not blender_exists:
        st.error("Blender yüklü olmadığı için işlem başlatılamıyor.")
    else:
        with st.spinner("Aethon Motoru çalışıyor, 3D model üretiliyor..."):
            # Motoru başlat
            engine = AethonEngine()
            
            # Script oluştur ve çalıştır
            engine.generate_script(prompt, color_code=blender_color, height=height)
            output_file = engine.run()
            
            if output_file and os.path.exists(output_file):
                st.balloons()
                st.success("Tasarım başarıyla tamamlandı!")
                
                # Modeli indir
                with open(output_file, "rb") as f:
                    st.download_button(
                        label="📦 3D Modeli İndir (.GLB)",
                        data=f,
                        file_name="aethon_model.glb",
                        mime="model/gltf-binary"
                    )
                
                st.info("İpucu: İndirdiğin dosyayı Blender'da veya online 'GLB Viewer' sitelerinde görüntüleyebilirsin.")
            else:
                st.error("Model üretiminde bir sorun oluştu. Lütfen logları kontrol et.")
                st.info("Hata detayı için sağ alttaki 'Manage app > Logs' kısmına bakabilirsin.")

# Alt Bilgi
st.divider()
st.caption("Aethon v1.0 | 9 Puanlık Kalite Standartları Aktif (Bevel & PBR)")
