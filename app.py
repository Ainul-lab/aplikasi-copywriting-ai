import streamlit as st
import google.generativeai as genai
import time

# --- KONFIGURASI HALAMAN (Agar pas di HP) ---
st.set_page_config(
    page_title="Magic Desc Generator",
    page_icon="✨",
    layout="centered", # Fokus di tengah untuk tampilan mobile
    initial_sidebar_state="collapsed" # Sidebar sembunyi agar layar lega
)

# --- CSS CUSTOM (Agar Tampilan Modern seperti App) ---
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
    .reportview-container .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    div[data-testid="stExpander"] div[role="button"] p {
        font-size: 1.1rem;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.title("📱 UMKM Copywriting AI")
st.caption("Buat deskripsi produk Shopee/Tokopedia dalam 5 detik.")
st.markdown("---")

# --- SISTEM LOGIN SEDERHANA (Untuk Proteksi Jualan Anda) ---
# Password ini bisa Anda jual di Lynk.id
password_akses = st.sidebar.text_input("Masukkan Kode Akses Premium:", type="password")

if password_akses != "SUKSES2025": # Ganti password ini sesuai keinginan
    st.warning("🔒 Silakan masukkan Kode Akses Premium di menu sebelah kiri (tanda panah >) untuk menggunakan aplikasi.")
    st.stop() # Hentikan program jika password salah

# --- INPUT API KEY (User membawa key sendiri) ---
with st.expander("⚙️ Pengaturan API Key (Wajib)", expanded=True):
    api_key = st.text_input("Tempel Gemini API Key disini:", type="password", help="Dapatkan gratis di aistudio.google.com")

# --- INPUT DATA PRODUK ---
st.subheader("📝 Detail Produk")

nama_produk = st.text_input("Nama Barang", placeholder="Cth: Keripik Pisang Lumer")
fitur_produk = st.text_area("Keunggulan / Fitur", placeholder="Cth: Coklat tebal, renyah, kemasan ziplock, tahan 1 bulan")

# Pilihan gaya bahasa dengan Dropdown (Lebih mudah di HP)
gaya_bahasa = st.selectbox(
    "Target Pembeli",
    ("Umum (Ramah)", "Anak Muda (Gaul/Viral)", "Ibu-ibu (Sopan & Akrab)", "Elegan/Mewah (Formal)")
)

# --- LOGIKA GENERATE ---
if st.button("✨ BUAT DESKRIPSI SEKARANG"):
    if not api_key:
        st.error("⚠️ API Key belum diisi! Cek pengaturan di atas.")
    elif not nama_produk:
        st.error("⚠️ Nama produk wajib diisi.")
    else:
        try:
            # Animasi Loading
            with st.spinner('Sedang meracik kata-kata ajaib...'):
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # --- PROMPT ENGINEERING (RISET/OTAK APLIKASI) ---
                prompt = f"""
                Role: Copywriter E-commerce Marketplace Indonesia (Shopee/Tokopedia).
                Task: Buat deskripsi produk yang optimal untuk UX Mobile (nyaman dibaca di HP).
                
                DATA INPUT:
                - Produk: {nama_produk}
                - Keunggulan: {fitur_produk}
                - Target Audiens: {gaya_bahasa}
                
                INSTRUKSI FORMAT OUTPUT (Markdown):
                1. **JUDUL (SEO Friendly):** Maksimal 100 karakter. Taruh kata kunci paling penting di depan. Tambahkan emoji pemanis.
                2. **HOOK PARAGRAF:** 2 kalimat pembuka yang menyentuh emosi/masalah pembeli.
                3. **POIN KEUNGGULAN:** Gunakan Bullet Points. Setiap poin WAJIB diawali emoji yang relevan.
                4. **SPESIFIKASI:** List teknis singkat.
                5. **CALL TO ACTION:** Ajakan checkout yang mendesak tapi sopan.
                6. **HASHTAG:** 5-8 hashtag relevan.

                PENTING: Jangan gunakan kalimat bertele-tele. Fokus pada "Benefit" bukan sekedar "Fitur".
                """
                
                response = model.generate_content(prompt)
                hasil = response.text

            # --- TAMPILAN HASIL ---
            st.success("Selesai! Silakan salin di bawah ini:")
            st.text_area("Hasil Copywriting", value=hasil, height=400)
            st.caption("Tips: Tekan lama pada kotak teks untuk Select All & Copy di HP.")
            
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")

# --- FOOTER ---
st.markdown("---")
st.markdown("<center><small>Developed for UMKM Indonesia</small></center>", unsafe_allow_html=True)