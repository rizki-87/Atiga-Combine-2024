import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# URL Google Sheets untuk setiap halaman
sheet_url_dump_truck = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTnflGSDkG_l9mSnawp-HEHX-R5jMfluS1rp0HlF_hMBpQvtG21d3-zPE4TxD80CvQVPjJszeOmNWJB/pub?gid=2078136743&single=true&output=csv'

# Replace deprecated st.cache with st.cache_data or st.cache_resource
@st.experimental_memo(ttl=300)  # TTL is in seconds, so 5 minutes are 300 seconds.
def load_data(url):
    try:
        df = pd.read_csv(url)
        df['TANGGAL'] = pd.to_datetime(df['TANGGAL'], errors='coerce')  # Ensure the 'TANGGAL' column is datetime
        return df
    except Exception as e:
        st.error(f"Gagal memuat data: {e}")
        return None

def filter_data(df, start_date, end_date, status, jenis):
    # Ensure start_date and end_date are treated as pandas timestamps
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    # Filter by date range
    filtered_df = df[(df['TANGGAL'].dt.date >= start_date.date()) & (df['TANGGAL'].dt.date <= end_date.date())]
    
    # Filter by status, if not 'All'
    if status != 'All':
        filtered_df = filtered_df[filtered_df['STATUS DT'] == status]
    
    # Filter by jenis DT, if not 'All'
    if jenis != 'All':
        filtered_df = filtered_df[filtered_df['JENIS DT'] == jenis]
    
    return filtered_df

# Your main function and the rest of the code remain the same
# ...

if __name__ == "__main__":
    main()
