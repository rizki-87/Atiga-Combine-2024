# import time
# import streamlit as st
# import pandas as pd
# import plotly.express as px
# from datetime import datetime
# import plotly.graph_objs as go
# from plotly.subplots import make_subplots

# # Fungsi untuk memuat data dari Google Sheets
# @st.cache_resource(ttl=300, show_spinner=True)
# def load_data(url):
#     try:
#         df = pd.read_csv(url, parse_dates=['TANGGAL'], dayfirst=True)
#         return df
#     except Exception as e:
#         st.error(f"Gagal memuat data: {e}")
#         return pd.DataFrame()

# # Fungsi untuk membuat line dan clustered column chart
# def create_status_trend_chart(df):
#     status_counts = df.groupby(['TANGGAL', 'STATUS DT']).size().unstack(fill_value=0)
#     fig = make_subplots(rows=1, cols=2, specs=[[{"type": "xy"}, {"type": "domain"}]],
#                         subplot_titles=('Trend STATUS DT', 'Distribusi STATUS DT'))
#     # Add line chart for 'Ready' trend
#     fig.add_trace(go.Scatter(x=status_counts.index, y=status_counts['Ready'], mode='lines+markers',
#                              name='Ready Trend', line=dict(color='royalblue')), row=1, col=1)
#     # Add clustered column chart for other statuses
#     for status in status_counts.columns:
#         if status != 'Ready':
#             fig.add_trace(go.Bar(x=status_counts.index, y=status_counts[status], name=status), row=1, col=1)
#     # Update layout
#     fig.update_layout(barmode='stack', showlegend=False)
#     fig.update_traces(marker=dict(line=dict(width=0.5, color='black')), selector=dict(type='bar'))
#     fig.update_xaxes(tickangle=-45, row=1, col=1)
#     return fig

# # Fungsi utama untuk menampilkan halaman Monitoring Dump Truck
# def show():
#     st.markdown("""
#         <div style="border: 2px solid #ddd; padding: 10px; text-align: center; background-color: #323288; border-radius: 0px;">
#             <h1 style="color: white; margin: 0;">Monitoring Ketersediaan dan Kondisi Dump Truck</h1>
#         </div>
#         """, unsafe_allow_html=True)

#     sheet_url_dump_truck = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTnflGSDkG_l9mSnawp-HEHX-R5jMfluS1rp0HlF_hMBpQvtG21d3-zPE4TxD80CvQVPjJszeOmNWJB/pub?gid=2078136743&single=true&output=csv'
#     df = load_data(sheet_url_dump_truck)

#     with st.container():
#         col1, col2, col3 = st.columns(3)
#         with col1:
#             min_date = st.date_input("Tanggal Mulai", datetime(2024, 1, 1))
#             max_date = st.date_input("Tanggal Akhir", datetime(2024, 12, 31))
#         with col2:
#             unique_status = df['STATUS DT'].unique().tolist() if not df.empty else []
#             status_selected = st.selectbox('Pilih Status DT', ['All'] + unique_status)
#         with col3:
#             unique_jenis = df['JENIS DT'].unique().tolist() if not df.empty else []
#             jenis_selected = st.selectbox('Pilih Jenis DT', ['All'] + unique_jenis)

#         df_filtered = filter_data(df, min_date, max_date, jenis_selected, status_selected)

#         if not df_filtered.empty:
#             status_trend_chart = create_status_trend_chart(df_filtered)
#             st.plotly_chart(status_trend_chart, use_container_width=True)
#         else:
#             st.write("Tidak ada data yang sesuai dengan filter yang diberikan.")

# def filter_data(df, min_date, max_date, jenis_dt_selected, status_dt_selected):
#     min_date = pd.Timestamp(min_date)
#     max_date = pd.Timestamp(max_date)
#     df_filtered = df[(df['TANGGAL'] >= min_date) & (df['TANGGAL'] <= max_date)]
#     if jenis_dt_selected != 'All':
#         df_filtered = df_filtered[df_filtered['JENIS DT'] == jenis_dt_selected]
#     if status_dt_selected != 'All':
#         df_filtered = df_filtered[df_filtered['STATUS DT'] == status_dt_selected]
#     return df_filtered

# if __name__ == "__main__":
#     show()

#################################################################################################################################

# import time
# import streamlit as st
# import pandas as pd
# import plotly.express as px
# from datetime import datetime
# import plotly.graph_objs as go
# from plotly.subplots import make_subplots

# # Fungsi untuk memuat data dari Google Sheets
# @st.cache(ttl=300, show_spinner=True)
# def load_data(url):
#     try:
#         df = pd.read_csv(url, parse_dates=['TANGGAL'], dayfirst=True)
#         return df
#     except Exception as e:
#         st.error(f"Gagal memuat data: {e}")
#         return pd.DataFrame()

# # Fungsi untuk membuat line dan clustered column chart
# def create_status_trend_chart(df_filtered):
#     status_counts = df_filtered['STATUS DT'].value_counts().reset_index()
#     status_counts.columns = ['STATUS DT', 'count']
#     pie_chart = px.pie(status_counts, values='count', names='STATUS DT', title='Distribusi STATUS DT')
#     return pie_chart

# # Fungsi utama untuk menampilkan halaman Monitoring Dump Truck
# def show():
#     st.markdown("""
#         <div style="border: 2px solid #ddd; padding: 10px; text-align: center; background-color: #323288; border-radius: 0px;">
#             <h1 style="color: white; margin: 0;">Monitoring Ketersediaan dan Kondisi Dump Truck</h1>
#         </div>
#         """, unsafe_allow_html=True)

#     sheet_url_dump_truck = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTnflGSDkG_l9mSnawp-HEHX-R5jMfluS1rp0HlF_hMBpQvtG21d3-zPE4TxD80CvQVPjJszeOmNWJB/pub?gid=2078136743&single=true&output=csv'
#     df = load_data(sheet_url_dump_truck)

#     with st.container():
#         col1, col2, col3 = st.columns(3)
#         with col1:
#             min_date = st.date_input("Tanggal Mulai", datetime.now())
#             max_date = st.date_input("Tanggal Akhir", datetime.now())
#         with col2:
#             unique_status = df['STATUS DT'].unique().tolist() if not df.empty else ['All']
#             status_selected = st.selectbox('Pilih Status DT', ['All'] + unique_status)
#         with col3:
#             unique_jenis = df['JENIS DT'].unique().tolist() if not df.empty else ['All']
#             jenis_selected = st.selectbox('Pilih Jenis DT', ['All'] + unique_jenis)

#         df_filtered = filter_data(df, min_date, max_date, jenis_selected, status_selected)

#         if not df_filtered.empty:
#             pie_chart = create_status_trend_chart(df_filtered)
#             st.plotly_chart(pie_chart, use_container_width=True)
#         else:
#             st.write("Tidak ada data yang sesuai dengan filter yang diberikan.")

# def filter_data(df, min_date, max_date, jenis_dt_selected, status_dt_selected):
#     min_date = pd.Timestamp(min_date)
#     max_date = pd.Timestamp(max_date)
#     df_filtered = df[(df['TANGGAL'] >= min_date) & (df['TANGGAL'] <= max_date)]
#     if jenis_dt_selected != 'All':
#         df_filtered = df_filtered[df_filtered['JENIS DT'] == jenis_dt_selected]
#     if status_dt_selected != 'All':
#         df_filtered = df_filtered[df_filtered['STATUS DT'] == status_dt_selected]
#     return df_filtered

# if __name__ == "__main__":
#     show()

###############################################################################################################################################

import streamlit as st
import pandas as pd
from plotly import graph_objs as go
from plotly.subplots import make_subplots
from datetime import datetime

# Fungsi untuk memuat data dari Google Sheets
@st.cache(ttl=300, show_spinner=True)
def load_data(url):
    try:
        df = pd.read_csv(url, parse_dates=['TANGGAL'], dayfirst=True)
        return df
    except Exception as e:
        st.error(f"Gagal memuat data: {e}")
        return pd.DataFrame()

# Fungsi utama untuk menampilkan halaman Monitoring Dump Truck
def show():
    st.markdown("""
        <div style="border: 2px solid #ddd; padding: 10px; text-align: center; background-color: #323288; border-radius: 0px;">
            <h1 style="color: white; margin: 0;">Monitoring Ketersediaan dan Kondisi Dump Truck</h1>
        </div>
        """, unsafe_allow_html=True)

    sheet_url_dump_truck = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTnflGSDkG_l9mSnawp-HEHX-R5jMfluS1rp0HlF_hMBpQvtG21d3-zPE4TxD80CvQVPjJszeOmNWJB/pub?gid=2078136743&single=true&output=csv'
    df = load_data(sheet_url_dump_truck)

    with st.container():
        col1, col2, col3 = st.columns(3)
        with col1:
            min_date = st.date_input("Tanggal Mulai", datetime(2024, 1, 1))
            max_date = st.date_input("Tanggal Akhir", datetime(2024, 12, 31))
        with col2:
            unique_status = df['STATUS DT'].unique().tolist() if not df.empty else ['All']
            status_selected = st.selectbox('Pilih Status DT', unique_status)
        with col3:
            unique_jenis = df['JENIS DT'].unique().tolist() if not df.empty else ['All']
            jenis_selected = st.selectbox('Pilih Jenis DT', unique_jenis)

        df_filtered = filter_data(df, min_date, max_date, jenis_selected, status_selected)

        if not df_filtered.empty:
            fig = make_subplots(rows=1, cols=2, specs=[[{"type": "xy"}, {"type": "domain"}]],
                                subplot_titles=('Trend STATUS DT', 'Distribusi STATUS DT'))
            status_counts = df_filtered['STATUS DT'].value_counts().reset_index()
            status_counts.columns = ['STATUS DT', 'count']
            
            # Line chart for Ready status
            ready_df = df_filtered[df_filtered['STATUS DT'] == 'Ready']
            ready_trend = ready_df.groupby('TANGGAL').size().reset_index(name='count')
            fig.add_trace(go.Scatter(x=ready_trend['TANGGAL'], y=ready_trend['count'],
                                     mode='lines', name='Ready Trend'), row=1, col=1)
            
            # Bar chart for other statuses
            for status, count in status_counts.itertuples(index=False):
                if status != 'Ready':
                    fig.add_trace(go.Bar(x=[status], y=[count], name=status), row=1, col=1)
            
            # Pie chart for status distribution
            fig.add_trace(go.Pie(labels=status_counts['STATUS DT'], values=status_counts['count'],
                                 name='STATUS DT Distribution'), row=1, col=2)
            
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write("Tidak ada data yang sesuai dengan filter yang diberikan.")

def filter_data(df, min_date, max_date, jenis_dt_selected, status_dt_selected):
    # Pastikan min_date dan max_date adalah objek datetime yang tepat
    min_date = pd.to_datetime(min_date)
    max_date = pd.to_datetime(max_date)

    # Filter berdasarkan rentang tanggal
    df_filtered = df[(df['TANGGAL'] >= min_date) & (df['TANGGAL'] <= max_date)]

    # Filter berdasarkan jenis DT jika tidak 'All'
    if jenis_dt_selected != 'All':
        df_filtered = df_filtered[df_filtered['JENIS DT'] == jenis_dt_selected]

    # Filter berdasarkan status DT jika tidak 'All'
    if status_dt_selected != 'All':
        df_filtered = df_filtered[df_filtered['STATUS DT'] == status_dt_selected]

    return df_filtered

if __name__ == "__main__":
    show()
