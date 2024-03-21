import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# URL Google Sheets untuk setiap halaman
sheet_url_dump_truck = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTnflGSDkG_l9mSnawp-HEHX-R5jMfluS1rp0HlF_hMBpQvtG21d3-zPE4TxD80CvQVPjJszeOmNWJB/pub?gid=2078136743&single=true&output=csv'

# Use @st.experimental_memo with ttl
@st.cache(ttl=300)  # TTL is in seconds, so 5 minutes are 300 seconds.
def load_data(url):
    try:
        df = pd.read_csv(url)
        df['TANGGAL'] = pd.to_datetime(df['TANGGAL'], errors='coerce')  # Ensure the 'TANGGAL' column is datetime
        return df
    except Exception as e:
        st.error(f"Gagal memuat data: {e}")
        return None

def filter_data(df, start_date, end_date, status, jenis):
    # Filter by date range
    filtered_df = df[(df['TANGGAL'] >= start_date) & (df['TANGGAL'] <= end_date)]
    
    # Filter by status, if not 'All'
    if status != 'All':
        filtered_df = filtered_df[filtered_df['STATUS DT'] == status]
    
    # Filter by jenis DT, if not 'All'
    if jenis != 'All':
        filtered_df = filtered_df[filtered_df['JENIS DT'] == jenis]
    
    return filtered_df

def main():
    st.set_page_config(page_title='Dashboard Monitoring', page_icon=':truck:', layout='wide')
    st.sidebar.image('atiga.png', width=300)
    page = st.sidebar.radio('Pilih Halaman', ['Monitoring Dump Truck', 'Monitoring Heavy Equipment'])

    if page == 'Monitoring Dump Truck':
        st.markdown("""
            <div style="border: 2px solid #ddd; padding: 10px; text-align: center; background-color: #323288; border-radius: 0px;">
                <h1 style="color: white; margin: 0;">Monitoring Ketersediaan dan Kondisi Dump Truck</h1>
            </div>
            """, unsafe_allow_html=True)
        start_date = st.sidebar.date_input('Tanggal Mulai', datetime.today())
        end_date = st.sidebar.date_input('Tanggal Akhir', datetime.today())
        status_option = st.sidebar.selectbox('Pilih Status DT', ['All', 'Ready', 'Rusak', 'Rusak Berat'])
        jenis_option = st.sidebar.selectbox('Pilih Jenis DT', ['All', 'DT Loading', 'DT Produksi','DT Support Operasional'])

        df = load_data(sheet_url_dump_truck)
        if df is not None:
            filtered_df = filter_data(df, start_date, end_date, status_option, jenis_option)
            status_dt_counts = filtered_df['STATUS DT'].value_counts()
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Distribusi Status DT")
                fig1, ax1 = plt.subplots(figsize=(8, 6))
                ax1.pie(status_dt_counts, labels=status_dt_counts.index, autopct='%1.1f%%', startangle=140)
                ax1.set_title('Distribusi Status DT')
                st.pyplot(fig1)
            
            with col2:
                st.subheader("Distribusi Status DT Berdasarkan Jenis DT")
                jenis_dt_counts = filtered_df.groupby(['JENIS DT', 'STATUS DT']).size().unstack(fill_value=0)
                fig2, ax2 = plt.subplots(figsize=(8, 6))
                jenis_dt_counts.plot(kind='barh', stacked=True, ax=ax2)
                ax2.set_title('Distribusi Status DT Berdasarkan Jenis DT')
                ax2.set_xlabel('Jumlah')
                ax2.set_ylabel('Jenis DT')
                st.pyplot(fig2)

    elif page == 'Monitoring Heavy Equipment':
        st.header('Monitoring Alat Berat')
        st.info("Halaman ini sedang dalam pembangunan. Silakan kembali lagi nanti.")

if __name__ == "__main__":
    main()
