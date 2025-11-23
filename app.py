import streamlit as st
import google.generativeai as genai

# --- 1. SETUP HALAMAN ---
st.set_page_config(page_title="Magic Copywriting AI", page_icon="🤖")

st.title("📱 UMKM Copywriting AI (Auto-Detect)")
st.markdown("---")

# --- 2. PASSWORD AKSES ---
pwd = st.sidebar.text_input("Kode Akses:", type="password")
if pwd != "SUKSES2025":
    st.warning("🔒 Masukkan Kode Akses di menu kiri.")
    st.stop()

# --- 3. INPUT API KEY (DENGAN SCANNER OTOMATIS) ---
st.info("ℹ️ Masukkan API Key, sistem akan otomatis mencari model yang tersedia.")
api_key = st.text_input("Tempel API Key Gemini:", type="password")

# WADAH UNTUK MENYIMPAN MODEL HASIL SCAN
model_pilihan = None 

# --- BAGIAN "CERDAS"-NYA ADA DISINI ---
if api_key:
    try:
        # 1. Hubungkan ke Google
        genai.configure(api_key=api_key)
        
        # 2. SCANNING... (Minta daftar model ke Google)
        daftar_model_hidup = []
        for m in genai.list_models():
            # Filter: Hanya ambil model yang bisa menulis teks (generateContent)
            if 'generateContent' in m.supported_generation_methods:
                # Bersihkan nama model (misal: models/gemini-pro -> gemini-pro)
                nama_bersih = m.name.replace("models/", "")
                daftar_model_hidup.append(nama_bersih)
        
        # 3. Tampilkan Hasil Scan di Dropdown
        if daftar_model_hidup:
            st.success(f"✅ Koneksi Sukses! Ditemukan {len(daftar_model_hidup)} model aktif.")
            model_pilihan = st.selectbox("Pilih Model:", daftar_model_hidup)
        else:
            st.error("API Key valid, tapi akun ini tidak memiliki akses ke model teks apapun.")
            
    except Exception as e:
        st.error(f"❌ API Key Salah / Gangguan Koneksi.\nError: {e}")

# --- 4. INPUT PRODUK ---
st.markdown("---")
st.subheader("📝 Data Produk")
nama = st.text_input("Nama Barang")
fitur = st.text_area("Fitur/Keunggulan")
gaya = st.selectbox("Gaya Bahasa", ["Gaul/Viral", "Ramah", "Formal"])

# --- 5. EKSEKUSI ---
if st.button("BUAT DESKRIPSI"):
    if not api_key:
        st.error("API Key wajib diisi dulu di atas!")
    elif not model_pilihan:
        st.error("Tunggu sampai nama model muncul di kotak pilihan.")
    else:
        try:
            # Pakai model hasil scan
            model = genai.GenerativeModel(model_pilihan)
            
            prompt = f"""
            Buatkan deskripsi produk Shopee.
            Produk: {nama}
            Fitur: {fitur}
            Gaya: {gaya}
            Format: Judul, Hook, Poin-poin, Hashtag.
            """
            
            with st.spinner(f'Sedang menulis menggunakan {model_pilihan}...'):
                response = model.generate_content(prompt)
                st.success("Selesai!")
                st.text_area("Hasil:", value=response.text, height=400)
                
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")
