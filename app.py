import streamlit as st
import google.generativeai as genai

# --- KONFIGURASI TAMPILAN ---
st.set_page_config(
    page_title="Magic Desc Generator",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CSS AGAR TOMBOL BAGUS ---
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
        border-radius: 10px;
        padding: 10px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- JUDUL APLIKASI ---
st.title("📱 UMKM Copywriting AI")
st.caption("Jasa bikin deskripsi produk Shopee/Tokopedia kilat!")
st.markdown("---")

# --- KEAMANAN PASSWORD ---
password_akses = st.sidebar.text_input("Masukkan Kode Akses:", type="password")

if password_akses != "SUKSES2025":
    st.warning("🔒 Masukkan Kode Akses di menu kiri (tanda panah >) dulu ya.")
    st.stop()

# --- INPUT API KEY (PEMBELI INPUT SENDIRI) ---
with st.expander("⚙️ Pengaturan API Key (Wajib Diisi)", expanded=True):
    api_key = st.text_input("Tempel API Key Gemini disini:", type="password")
    st.caption("Belum punya? Cari di Google: 'Cara dapat API Key Gemini AI Studio'")

# --- INPUT PRODUK ---
st.subheader("📝 Data Produk")
nama_produk = st.text_input("Nama Barang", placeholder="Contoh: Keripik Pisang")
fitur_produk = st.text_area("Keunggulan", placeholder="Contoh: Renyah, manis, murah")
gaya_bahasa = st.selectbox("Target Pembeli", ("Umum", "Anak Muda", "Ibu-ibu", "Formal"))

# --- PROSES GENERATE ---
if st.button("✨ BUAT DESKRIPSI SEKARANG"):
    if not api_key:
        st.error("⚠️ API Key masih kosong! Isi dulu di atas.")
    elif not nama_produk:
        st.error("⚠️ Nama produk wajib diisi.")
    else:
        try:
            # KONFIGURASI AI
            genai.configure(api_key=api_key)
            
            # --- BAGIAN YANG DIPERBAIKI (ANTI ERROR) ---
            # Kita ganti ke 'gemini-pro' karena ini paling stabil
            model = genai.GenerativeModel('gemini-pro')
            
            # PROMPT RAINTAS
            prompt = f"""
            Buatkan deskripsi produk marketplace Indonesia (Shopee/Tokopedia).
            Produk: {nama_produk}
            Fitur: {fitur_produk}
            Gaya: {gaya_bahasa}
            
            Format Output:
            1. JUDUL SEO (Menarik & Ada Kata Kunci)
            2. PARAGRAF PEMBUKA (Hook Masalah & Solusi)
            3. POIN KEUNGGULAN (Pakai Emoji)
            4. SPESIFIKASI SINGKAT
            5. KALIMAT PENUTUP (Ajakan Beli)
            6. HASHTAG
            """
            
            with st.spinner('Sedang mengetik...'):
                response = model.generate_content(prompt)
                st.success("Berhasil! Silakan copy di bawah:")
                st.text_area("Hasil Copywriting:", value=response.text, height=400)
                
        except Exception as e:
            st.error(f"Gagal: API Key salah atau koneksi bermasalah.\nDetail: {e}")

st.markdown("---")
st.caption("Developed for UMKM Indonesia")
