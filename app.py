# import streamlit as st
# import pandas as pd
# from datetime import timedelta, datetime

# # URL Google Sheets untuk setiap halaman
# sheet_url_dump_truck = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTnflGSDkG_l9mSnawp-HEHX-R5jMfluS1rp0HlF_hMBpQvtG21d3-zPE4TxD80CvQVPjJszeOmNWJB/pub?gid=2078136743&single=true&output=csv'

# @st.experimental_memo(ttl=timedelta(minutes=5).total_seconds())
# def load_data(url):
#     try:
#         df = pd.read_csv(url)
#         df['TANGGAL'] = pd.to_datetime(df['TANGGAL'], errors='coerce')
#         return df
#     except Exception as e:
#         st.error(f"Gagal memuat data: {e}")
#         return None

# def main():
#     st.set_page_config(page_title='Dashboard Monitoring', page_icon=':truck:', layout='wide')
#     st.sidebar.image('atiga.png', width=300)
    
#     with st.container():
#         st.markdown("""
#         <div style="border: 2px solid #ddd; padding: 10px; text-align: center; background-color: #323288; border-radius: 0px;">
#             <h1 style="color: white; margin: 0;">Monitoring Ketersediaan dan Kondisi Dump Truck</h1>
#         </div>
#         """, unsafe_allow_html=True)

#     page = st.sidebar.radio('Pilih Halaman', ['Monitoring Dump Truck', 'Monitoring Heavy Equipment'])
    
#     if page == 'Monitoring Dump Truck':
#         # Code for 'Monitoring Dump Truck' page...
#         pass  # Replace this with actual code to handle this page
#     elif page == 'Monitoring Heavy Equipment':
#         st.header('Monitoring Heavy Equipment')
#         st.info("Halaman ini sedang dalam pembangunan. Silakan kembali lagi nanti.")


# if __name__ == "__main__":
#     main()





import streamlit as st
import pandas as pd
from datetime import timedelta

# URL Google Sheets untuk setiap halaman
sheet_url_dump_truck = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTnflGSDkG_l9mSnawp-HEHX-R5jMfluS1rp0HlF_hMBpQvtG21d3-zPE4TxD80CvQVPjJszeOmNWJB/pub?gid=2078136743&single=true&output=csv'

# Gunakan @st.experimental_memo dengan ttl
@st.experimental_memo(ttl=timedelta(minutes=5).total_seconds())
def load_data(url):
    try:
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"Gagal memuat data: {e}")
        return None

def main():
    st.set_page_config(page_title='Dashboard Monitoring', page_icon=':truck:', layout='wide')
    st.sidebar.image('atiga.png', width=300)

    page = st.sidebar.radio('Pilih Halaman', ['Monitoring Dump Truck', 'Monitoring Heavy Equipment'])

    if page == 'Monitoring Dump Truck':
        # Only create the title container for the "Monitoring Dump Truck" page
        with st.container():
            st.markdown("""
            <div style="border: 2px solid #ddd; padding: 10px; text-align: center; background-color: #323288; border-radius: 0px;">
                <h1 style="color: white; margin: 0;">Monitoring Ketersediaan dan Kondisi Dump Truck</h1>
            </div>
            """, unsafe_allow_html=True)
            
    elif page == 'Monitoring Alat Berat':
        st.header('Monitoring Alat Berat')
        st.info("Halaman ini sedang dalam pembangunan. Silakan kembali lagi nanti.")

if __name__ == "__main__":
    main()
