import streamlit as st
import pandas as pd
from datetime import timedelta, datetime

# URL Google Sheets untuk setiap halaman
sheet_url_dump_truck = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTnflGSDkG_l9mSnawp-HEHX-R5jMfluS1rp0HlF_hMBpQvtG21d3-zPE4TxD80CvQVPjJszeOmNWJB/pub?gid=2078136743&single=true&output=csv'

# Gunakan @st.experimental_memo dengan ttl
@st.experimental_memo(ttl=timedelta(minutes=5).total_seconds())
def load_data(url):
    try:
        df = pd.read_csv(url)
        # Asumsikan kolom status dan jenis sudah ada di dataframe
        return df
    except Exception as e:
        st.error(f"Gagal memuat data: {e}")
        return None

def main():
    # Mengatur layout menjadi mode lebar dan menginisialisasi halaman dengan judul dan favicon
    st.set_page_config(page_title='Dashboard Monitoring', page_icon=':truck:', layout='wide')
    
    # Menempatkan logo di sidebar atas
    st.sidebar.image('atiga.png', width=300)  # Sesuaikan lebar sesuai kebutuhan
    
    # Menambahkan navigasi halaman menggunakan radio buttons di sidebar
    page = st.sidebar.radio('Pilih Halaman', ['Monitoring Dump Truck', 'Monitoring Heavy Equipment'])
    
    # Container untuk input dan pemilih
    with st.container():
        st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: center; margin: 20px 0; padding: 10px; border: 2px solid #ddd; border-radius: 5px;">
        """, unsafe_allow_html=True)
        # Input tanggal
        start_date = st.date_input('Tanggal Mulai', datetime.today())
        end_date = st.date_input('Tanggal Akhir', datetime.today())
        
        # Muat data dump truck
        data_dump_truck = load_data(sheet_url_dump_truck)
        if data_dump_truck is not None:
            # Pemilih untuk status DT
            status_options = st.selectbox('Pilih Status DT', options=data_dump_truck['STATUS DT'].unique())
            # Pemilih untuk jenis DT
            jenis_options = st.selectbox('Pilih Jenis DT', options=data_dump_truck['JENIS DT'].unique())
            st.markdown("</div>", unsafe_allow_html=True)  # Tutup div

            # Filter data berdasarkan tanggal dan pemilih
            filtered_data = data_dump_truck[(data_dump_truck['TANGGAL'] >= start_date) & (data_dump_truck['TANGGAL'] <= end_date) & (data_dump_truck['STATUS DT'] == status_options) & (data_dump_truck['JENIS DT'] == jenis_options)]
            st.dataframe(filtered_data)  # Tampilkan data yang difilter
        else:
            st.error("Data tidak dapat dimuat. Silakan periksa sumber data Anda.")
            st.markdown("</div>", unsafe_allow_html=True)  # Tutup div jika data tidak ada

    elif page == 'Monitoring Heavy Equipment':
        st.header('Monitoring Heavy Equipment')
        st.info("Halaman ini sedang dalam pembangunan. Silakan kembali lagi nanti.")

if __name__ == "__main__":
    main()


# import streamlit as st
# import pandas as pd
# from datetime import timedelta

# # URL Google Sheets untuk setiap halaman
# sheet_url_dump_truck = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTnflGSDkG_l9mSnawp-HEHX-R5jMfluS1rp0HlF_hMBpQvtG21d3-zPE4TxD80CvQVPjJszeOmNWJB/pub?gid=2078136743&single=true&output=csv'

# # Gunakan @st.experimental_memo dengan ttl
# @st.experimental_memo(ttl=timedelta(minutes=5).total_seconds())
# def load_data(url):
#     try:
#         df = pd.read_csv(url)
#         return df
#     except Exception as e:
#         st.error(f"Gagal memuat data: {e}")
#         return None

# def main():
#     # Mengatur layout menjadi mode lebar dan menginisialisasi halaman dengan judul dan favicon
#     st.set_page_config(page_title='Dashboard Monitoring', page_icon=':truck:', layout='wide')
    
#     # Menempatkan logo di sidebar atas
#     st.sidebar.image('atiga.png', width=300)  # Sesuaikan lebar sesuai kebutuhan
    
#     # Menambahkan navigasi halaman menggunakan radio buttons di sidebar
#     page = st.sidebar.radio('Pilih Halaman', ['Monitoring Dump Truck', 'Monitoring Heavy Equipment'])
    
#     # Container untuk judul dengan border
#     with st.container():
#         st.markdown("""
#         <div style="border: 2px solid #ddd; padding: 10px; text-align: center; background-color: #323288; border-radius: -5px;">
#             <h1 style="color: white; margin: 0;">Monitoring Ketersediaan dan Kondisi Dump Truck</h1>
#         </div>
#         """, unsafe_allow_html=True)

#     if page == 'Monitoring Dump Truck':
#         # Memuat data dump truck
#         data_dump_truck = load_data(sheet_url_dump_truck)
#         if data_dump_truck is not None:
#             st.dataframe(data_dump_truck)  # Gunakan st.dataframe untuk tampilan yang lebih baik
#         else:
#             st.error("Data tidak dapat dimuat. Silakan periksa sumber data Anda.")
            
#         # Tombol untuk memperbarui data
#         if st.button('Muat Ulang Data'):
#             st.legacy_caching.clear_cache()  # Membersihkan semua cache
#             st.rerun()  # Menjalankan ulang skrip untuk memuat data terbaru

#     elif page == 'Monitoring Alat Berat':
#         st.header('Monitoring Alat Berat')
#         st.info("Halaman ini sedang dalam pembangunan. Silakan kembali lagi nanti.")

# if __name__ == "__main__":
#     main()
