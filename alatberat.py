import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime
import pytz

# Cache data loading
@st.cache_resource(ttl=300, show_spinner=True)
def load_data(url):
    try:
        df = pd.read_csv(url)
        df['TANGGAL'] = pd.to_datetime(df['TANGGAL'], dayfirst=True, errors='coerce')
        return df
    except Exception as e:
        st.error(f"Gagal memuat data: {e}")
        return pd.DataFrame()

# Data filtering function
def filter_data(df, start_date, end_date, status_dt_selected):
    if start_date:
        start_date = pd.to_datetime(start_date).normalize()
    if end_date:
        end_date = pd.to_datetime(end_date).normalize()
    df = df.dropna(subset=['TANGGAL'])
    if start_date and end_date:
        df = df[(df['TANGGAL'] >= start_date) & (df['TANGGAL'] <= end_date)]
    if status_dt_selected and 'All' not in status_dt_selected:
        df = df[df['STATUS AB'].isin(status_dt_selected)]
    return df

# Define a function to get current time and temperature (this is just a placeholder)
def get_current_time_and_temp():
    # Assuming you would have a function that gets the temperature
    current_time = datetime.now().astimezone(pytz.timezone("Asia/Jakarta")).strftime("%H:%M:%S")
    temperature = "29°C"  # Placeholder temperature
    return current_time, temperature

# Main layout and logic
# def show():
    
#     # Retrieve current time and temperature
#     current_time, temperature = get_current_time_and_temp()

#     # Top row for title and metrics
#     top_col1, top_col2, top_col3 = st.columns([2, 1, 1])
#     with top_col1:
#         st.markdown("## Monitoring Ketersediaan dan Kondisi Alat Berat", unsafe_allow_html=True)
#     with top_col2:
#         st.metric(label="Waktu Saat Ini", value=current_time)
#     with top_col3:
#         st.metric(label="Suhu Saat Ini", value=temperature)

def show():
    # Retrieve current time and temperature
    current_time, temperature = get_current_time_and_temp()

    # Define styles for the container
    container_style = """
    <style>
        .container {
            border: 2px solid #f0f0f0;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 10px;
        }
        .title {
            color: #ffffff;
            font-size: 26px;
        }
        .metric {
            padding: 0 10px;
        }
    </style>
    """

    # Apply container and title styles
    st.markdown(container_style, unsafe_allow_html=True)
    st.markdown('<div class="container">', unsafe_allow_html=True)
    st.markdown('<div class="title">Monitoring Ketersediaan dan Kondisi Alat Berat</div>', unsafe_allow_html=True)

    # Create columns for metrics
    col1, col2 = st.columns([1, 4])
    with col1:
        st.markdown('<div class="metric">', unsafe_allow_html=True)
        st.metric(label="Waktu Saat Ini", value=current_time)
        st.metric(label="Suhu Saat Ini", value=temperature)
        st.markdown('</div>', unsafe_allow_html=True)

    # Close the container div
    st.markdown('</div>', unsafe_allow_html=True)

    sheet_url_alat_berat = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQ1vygEd5Ykxt7enZtJBCWIwO91FTb3mVbsRNvq2XlItosvT8ROsXwbou354QWZqY4p0eNtRM-bAESm/pub?gid=1149198834&single=true&output=csv'  # Ganti dengan URL yang sesungguhnya
    df = load_data(sheet_url_alat_berat)

    # Side-by-side layout for the date input and status multiselect
    col1, col2 = st.columns(2)
    with col1:
        date_range = st.date_input("Pilih Tanggal", [])
    with col2:
        unique_status = df['STATUS AB'].unique().tolist() if not df.empty else []
        status_selected = st.multiselect('Pilih Status Alat Berat', ['All'] + unique_status, default=['All'])

    start_date = date_range[0] if len(date_range) > 0 else None
    end_date = date_range[-1] if len(date_range) > 1 else start_date

    filtered_df = filter_data(df, start_date, end_date, status_selected)
    
    if not filtered_df.empty:
        # Bar chart for 'STATUS AB'
        status_counts = filtered_df['STATUS AB'].value_counts().reset_index()
        status_counts.columns = ['STATUS AB', 'count']
        status_bar_chart = alt.Chart(status_counts).mark_bar().encode(
            x=alt.X('count:Q', title='Jumlah'),
            y=alt.Y('STATUS AB:N', sort='-x', title='Status Alat Berat')
        ).properties(
            width=600,
            height=400,
            title="Distribusi Status Alat Berat"
        )
        st.altair_chart(status_bar_chart, use_container_width=True)

        # Vertical bar chart for 'MERK'
        merk_counts = filtered_df['MERK'].value_counts().reset_index()
        merk_counts.columns = ['MERK', 'count']
        merk_bar_chart = alt.Chart(merk_counts).mark_bar().encode(
            x=alt.X('MERK:N', title='Merk Alat Berat', sort='-y'),
            y=alt.Y('count:Q', title='Jumlah'),
            tooltip=['MERK:N', 'count:Q']
        ).properties(
            width=600,
            height=400,
            title="Distribusi Merk Alat Berat"
        )
        st.altair_chart(merk_bar_chart, use_container_width=True)

    else:
        st.warning("Tidak ada data yang sesuai dengan kriteria filter.")

if __name__ == "__main__":
    show()

#############################################################################################################################################
# import streamlit as st

# def show():
#     st.title("Halaman Monitoring Alat Berat")
#     st.header("Under Construction")
