import streamlit as st
import pandas as pd
from datetime import timedelta

# Menggunakan st.experimental_memo untuk caching dengan ttl
@st.experimental_memo(ttl=timedelta(minutes=5))
def load_data(url):
    try:
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return None

# Tempatkan URL Google Sheets Anda di sini
sheet_url_dump_truck = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTnflGSDkG_l9mSnawp-HEHX-R5jMfluS1rp0HlF_hMBpQvtG21d3-zPE4TxD80CvQVPjJszeOmNWJB/pub?gid=2078136743&single=true&output=csv'
sheet_url_alat_berat = None  # Link belum tersedia

def main():
    # sisanya tetap sama
    ...

if __name__ == "__main__":
    main()
