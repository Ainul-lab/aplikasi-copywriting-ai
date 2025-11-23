import streamlit as st
import google.generativeai as genai

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Magic Desc Generator", page_icon="✨", layout="centered", initial_sidebar_state="collapsed")

# --- CSS ---
st.markdown("""
    <style>
    .stButton>button { width: 100%; background-color: #FF4B4B; color: white; padding: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("📱 UMKM Copywriting AI")
st.markdown("---")

# --- PASSWORD ---
if st.sidebar.text_input("Kode Akses:", type="password") != "SUKSES2025":
    st.warning("🔒 Masukkan Kode Akses di menu kiri.")
    st.stop()

# --- INPUT API KEY ---
with st.expander("⚙️ Pengaturan API Key (Wajib)", expanded=True):
    api_key = st.text_input("Tempel API Key Gemini:", type="password")

# --- PILIH MODEL (SOLUSI BIAR GAK EROR) ---
# Ini fitur agar user bisa ganti model kalau ada yang eror
pilihan_model = st.selectbox(
    "Pilih Model AI (Ganti jika error):",
    ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-1.0-pro"],
    index=0
)
st.caption("ℹ️ Saran: Gunakan '1.5-flash' untuk gratisan/cepat. Gunakan '1.0-pro' jika versi baru bermasalah.")

# --- INPUT PRODUK ---
st.subheader("📝 Data Produk")
nama = st.text_input("Nama Barang")
fitur = st.text_area("Keunggulan")
gaya = st.selectbox("Gaya Bahasa", ["Gaul/Viral", "Ramah/Sopan", "Formal/Mewah"])

# --- TOMBOL ---
if st.button("✨ BUAT DESKRIPSI"):
    if not api_key:
        st.error("⚠️ API Key kosong!")
    elif not nama:
        st.error("⚠️ Nama produk kosong!")
    else:
        try:
            # KONFIGURASI
            genai.configure(api_key=api_key)
            
            # PAKAI MODEL SESUAI PILIHAN DI ATAS
            model = genai.GenerativeModel(pilihan_model)
            
            prompt = f"""
            Buatkan deskripsi produk Shopee/Tokopedia.
            Produk: {nama}
            Fitur: {fitur}
            Gaya: {gaya}
            Format: Judul SEO, Hook, Poin Keunggulan (Emoji), Spesifikasi, CTA, Hashtag.
            """
            
            with st.spinner(f'Sedang berpikir pakai otak {pilihan_model}...'):
                response = model.generate_content(prompt)
                st.success("Berhasil!")
                st.text_area("Hasil:", value=response.text, height=400)
                
        except Exception as e:
            st.error(f"Gagal dengan model {pilihan_model}. Coba ganti model lain di kotak pilihan atas.\n\nError teknis: {str(e)}")

st.markdown("---")
st.caption("Developed for UMKM Indonesia")
