import streamlit as st
import google.generativeai as genai

# --- 1. SETUP HALAMAN ---
st.set_page_config(
    page_title="Magic Copywriting AI",
    page_icon="💎",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. CSS "SULTAN THEME" (INILAH RAHASIA TAMPILANNYA) ---
st.markdown("""
    <style>
    /* Mengubah Latar Belakang Jadi Gradasi Gelap Premium */
    .stApp {
        background: rgb(15,23,42);
        background: linear-gradient(180deg, rgba(15,23,42,1) 0%, rgba(30,41,59,1) 100%);
        color: white;
    }
    
    /* Mengubah Warna Tombol Jadi Merah Menyala (Gradient) */
    .stButton>button {
        width: 100%;
        background: linear-gradient(45deg, #FF3131, #FF914D);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 15px;
        font-weight: bold;
        font-size: 18px;
        box-shadow: 0 4px 15px rgba(255, 75, 75, 0.4);
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 20px rgba(255, 75, 75, 0.6);
    }

    /* Mengubah Kotak Input Jadi Lebih Modern */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #1E293B;
        color: white;
        border-radius: 10px;
        border: 1px solid #475569;
    }
    .stSelectbox>div>div>div {
        background-color: #1E293B;
        color: white;
        border-radius: 10px;
    }
    
    /* Mempercantik Judul */
    h1 {
        text-align: center;
        background: -webkit-linear-gradient(45deg, #00C9FF, #92FE9D);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        padding-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. KONTEN APLIKASI ---
st.title("💎 UMKM Copywriting PRO")
st.markdown("<p style='text-align: center; color: #94A3B8;'>Buat deskripsi produk memukau dalam hitungan detik.</p>", unsafe_allow_html=True)
st.markdown("---")

# --- 4. KEAMANAN ---
pwd = st.sidebar.text_input("🔑 Kode Akses:", type="password")
if pwd != "SUKSES2025":
    st.warning("🔒 Aplikasi terkunci. Masukkan Kode Akses di menu kiri.")
    st.stop()

# --- 5. INPUT API KEY & AUTO SCAN ---
with st.expander("⚙️ Pengaturan Sistem (API Key)", expanded=False):
    st.info("ℹ️ Masukkan API Key Gemini Anda (Gratis & Aman).")
    api_key = st.text_input("Tempel API Key:", type="password")

model_pilihan = None 

# Logika Auto-Scan Model
if api_key:
    try:
        genai.configure(api_key=api_key)
        semua_model = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                nama = m.name.replace("models/", "")
                semua_model.append(nama)
        
        # Filter Model Aman
        model_aman = [m for m in semua_model if ("flash" in m or "pro" in m) and "exp" not in m]
        model_aman.sort(key=lambda x: "flash" not in x) 

        if model_aman:
            st.success(f"✅ Sistem Terhubung!")
            model_pilihan = st.selectbox("Pilih Otak AI:", model_aman, index=0)
        else:
            model_pilihan = st.selectbox("Pilih Otak AI:", semua_model)
            
    except Exception as e:
        st.error(f"❌ Kunci Salah / Gangguan. Error: {e}")

# --- 6. FORMULIR PRODUK ---
col1, col2 = st.columns(2)
with col1:
    nama = st.text_input("📦 Nama Produk")
with col2:
    gaya = st.selectbox("🎭 Gaya Bahasa", ["Gaul / Viral 🔥", "Elegan / Mewah 💎", "Ramah / Akrab 😊", "Tegas / Formal 💼"])

fitur = st.text_area("✨ Keunggulan / Fitur Produk")

# --- 7. EKSEKUSI ---
if st.button("🚀 BUAT DESKRIPSI AJAIB"):
    if not api_key:
        st.error("⚠️ Masukkan API Key dulu di menu Pengaturan (atas).")
    elif not model_pilihan:
        st.error("⚠️ Tunggu sebentar, sedang memuat sistem AI...")
    elif not nama:
        st.error("⚠️ Nama produk belum diisi!")
    else:
        try:
            model = genai.GenerativeModel(model_pilihan)
            
            prompt = f"""
            Bertindaklah sebagai Copywriter Penjualan Senior.
            Produk: {nama}
            Keunggulan: {fitur}
            Target/Gaya: {gaya}
            
            Tugas: Buat deskripsi produk yang SANGAT PERSUASIF (Hypnotic Writing).
            Format Output:
            1. HEADLINE (Bombastis & Clickbait positif)
            2. PARAGRAF PEMBUKA (Sentuh emosi pembeli)
            3. POIN KEUNGGULAN (Gunakan Emoji yang estetik)
            4. SPESIFIKASI SINGKAT
            5. CLOSING (Ajakan beli yang mendesak)
            6. HASHTAG RELEVAN
            """
            
            with st.spinner(f'🤖 Sedang meracik kata-kata terbaik...'):
                response = model.generate_content(prompt)
                
                # Tampilkan Hasil dengan Kotak yang Bagus
                st.markdown("### 🎉 Hasil Copywriting Anda:")
                st.text_area("Salin teks di bawah ini:", value=response.text, height=450)
                st.success("Tips: Tekan pojok kanan atas kotak teks untuk menyalin semua.")
                
        except Exception as e:
            st.error(f"Gagal. Coba ganti model lain.\nError: {e}")

# Footer
st.markdown("<br><hr><center><small style='color: #64748B;'>Powering UMKM Indonesia 🇮🇩 | AI Tools Series</small></center>", unsafe_allow_html=True)
