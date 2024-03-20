import streamlit as st
import pandas as pd
from datetime import timedelta

# URL Google Sheets for each page
sheet_url_dump_truck = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTnflGSDkG_l9mSnawp-HEHX-R5jMfluS1rp0HlF_hMBpQvtG21d3-zPE4TxD80CvQVPjJszeOmNWJB/pub?gid=2078136743&single=true&output=csv'

# Using st.cache to cache the data with ttl
@st.cache(ttl=timedelta(minutes=5), allow_output_mutation=True)
def load_data(url):
    try:
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return None

def main():
    st.title('Dashboard Monitoring')

    # Button for refreshing data
    if st.button('Refresh Data'):
        st.legacy_caching.clear_cache()  # Clear all the cache
        st.rerun()  # Rerun the script to load the latest data

    # Add page navigation using radio buttons
    page = st.sidebar.radio('Choose Page', ['Monitoring Dump Truck', 'Monitoring Heavy Equipment'])

    if page == 'Monitoring Dump Truck':
        st.header('Monitoring Dump Truck')
        # Load the dump truck data
        data_dump_truck = load_data(sheet_url_dump_truck)
        if data_dump_truck is not None:
            st.dataframe(data_dump_truck)  # Use st.dataframe for a better display
        else:
            st.error("Data could not be loaded. Please check your data source.")

    elif page == 'Monitoring Heavy Equipment':
        st.header('
