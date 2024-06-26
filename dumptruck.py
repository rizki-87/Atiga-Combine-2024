import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

@st.cache_resource(ttl=300, show_spinner=True)
def load_data(url):
    try:
        df = pd.read_csv(url)
        df['TANGGAL'] = pd.to_datetime(df['TANGGAL'], dayfirst=True, errors='coerce')
        return df
    except Exception as e:
        st.error(f"Gagal memuat data: {e}")
        return pd.DataFrame()

def filter_data(df, start_date, end_date, status_dt_selected):
    start_date = pd.to_datetime(start_date).normalize()
    end_date = pd.to_datetime(end_date).normalize()
    df = df.dropna(subset=['TANGGAL'])
    if start_date is not None and end_date is not None:
        df = df[(df['TANGGAL'] >= start_date) & (df['TANGGAL'] <= end_date)]
    if status_dt_selected and 'All' not in status_dt_selected:
        df = df[df['STATUS DT'].isin(status_dt_selected)]
    return df

def show_filtered_table(df_filtered):
    df_filtered = df_filtered.reset_index(drop=True)
    df_to_show = df_filtered[['NO DT', 'LEVEL KERUSAKAN', 'JENIS KERUSAKAN', 'PART YANG DIBUTUHKAN', 'QTY', 'STATUS SPAREPART', 'LAMA BREAKDOWN (Days)']]
    st.dataframe(df_to_show)

def create_line_clustered_chart(df_filtered, date_col='TANGGAL', status_col='STATUS DT', ready_status='Ready', rusak_status='Rusak', rusak_berat_status='Rusak Berat'):
    df_grouped = df_filtered.groupby([pd.Grouper(key=date_col, freq='D'), status_col]).size().unstack(fill_value=0)
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    for status, color in zip([rusak_status, rusak_berat_status], ['orange', 'red']):
        if status in df_grouped.columns:
            fig.add_trace(go.Bar(x=df_grouped.index, y=df_grouped[status], name=status, marker_color=color), secondary_y=False)
    
    if ready_status in df_grouped.columns:
        fig.add_trace(go.Scatter(x=df_grouped.index, y=df_grouped[ready_status], name=ready_status, mode='lines', line=dict(color='blue')), secondary_y=True)

    fig.update_xaxes(title_text='Tanggal')
    fig.update_yaxes(title_text='Jumlah Rusak & Rusak Berat', secondary_y=False)
    fig.update_yaxes(title_text='Jumlah Ready', secondary_y=True)
    
    fig.update_layout(title='Status Harian Truk', legend_title='Legenda', legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    
    return fig

def create_stacked_bar_chart(df_filtered, brand_col='MEREK', status_col='STATUS DT'):
    # Define the colors for each status
    status_colors = {'Ready': 'blue', 'Rusak': 'orange', 'Rusak Berat': 'red'}

    # Group data by brand and status
    df_grouped = df_filtered.groupby([brand_col, status_col]).size().reset_index(name='counts')
    
    # Pivot the dataframe to have brands on rows and statuses on columns
    df_pivot = df_grouped.pivot(index=brand_col, columns=status_col, values='counts').fillna(0)
    
    # Create a horizontal bar chart
    fig = px.bar(
        df_pivot,
        x=df_pivot.columns,
        y=df_pivot.index,
        orientation='h',
        title='Distribusi Truk per Merek',
        labels={'value':'Jumlah Truk', 'variable':'Status', brand_col:'Merek'},
        color_discrete_map=status_colors
    )
    
    # Update layout for stacked bar chart
    fig.update_layout(barmode='stack')
    
    return fig

def show():
    st.markdown("""
    <div style="border: 2px solid #ddd; padding: 10px; text-align: center; background-color: #323288; border-radius: 0px;">
        <h1 style="color: white; margin: 0;">Monitoring Ketersediaan dan Kondisi Dump Truck</h1>
    </div>
    """, unsafe_allow_html=True)

    sheet_url_dump_truck = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTnflGSDkG_l9mSnawp-HEHX-R5jMfluS1rp0HlF_hMBpQvtG21d3-zPE4TxD80CvQVPjJszeOmNWJB/pub?gid=2078136743&single=true&output=csv'

    df = load_data(sheet_url_dump_truck)

    with st.container():
        date_range = st.date_input("Pilih Tanggal", [])
        start_date = None
        end_date = None
        if len(date_range) == 1:
            start_date = end_date = date_range[0]
        elif len(date_range) == 2:
            start_date, end_date = date_range

        unique_status = df['STATUS DT'].unique().tolist() if not df.empty else []
        status_selected = st.multiselect('Pilih Status DT', ['All'] + unique_status, default=['All'])

    if start_date and end_date:
        df_filtered = filter_data(df, start_date, end_date, status_selected)

        col1, col_mid, col3 = st.columns([1, 2, 1])
        with col1:
            if not df_filtered.empty:
                df_grouped = df_filtered.groupby('STATUS DT').size().reset_index(name='counts')
                colors = ['blue' if status == 'Ready' else 'orange' if status == 'Rusak' else 'red' for status in df_grouped['STATUS DT']]
                fig_pie = px.pie(df_grouped, names='STATUS DT', values='counts', title='Distribusi STATUS DT', color_discrete_sequence=colors)
                fig_pie.update_traces(textinfo='percent+label+value')
                st.plotly_chart(fig_pie)

        with col_mid:
            if not df_filtered.empty:
                fig_stacked_bar = create_stacked_bar_chart(df_filtered, 'MEREK', 'STATUS DT')
                st.plotly_chart(fig_stacked_bar, use_container_width=True)
            else:
                st.warning("Tidak ada data yang sesuai dengan filter yang diberikan untuk grafik batang tumpuk.")

        with col3:
            if not df_filtered.empty:
                fig_line_clustered = create_line_clustered_chart(df_filtered)
                st.plotly_chart(fig_line_clustered, use_container_width=True)

        show_filtered_table(df_filtered)
    else:
        st.warning("Silakan pilih tanggal awal dan akhir untuk melihat data.")

if __name__ == "__main__":
    show()

###############################################################################################################################################

# import streamlit as st
# import pandas as pd
# import plotly.express as px
# from plotly.subplots import make_subplots
# import plotly.graph_objects as go

# @st.cache_resource(ttl=300, show_spinner=True)
# def load_data(url):
#     try:
#         df = pd.read_csv(url)
#         df['TANGGAL'] = pd.to_datetime(df['TANGGAL'], dayfirst=True, errors='coerce')
#         return df
#     except Exception as e:
#         st.error(f"Gagal memuat data: {e}")
#         return pd.DataFrame()

# def filter_data(df, start_date, end_date, status_dt_selected):
#     start_date = pd.to_datetime(start_date).normalize()
#     end_date = pd.to_datetime(end_date).normalize()
#     df = df.dropna(subset=['TANGGAL'])
#     if start_date is not None and end_date is not None:
#         df = df[(df['TANGGAL'] >= start_date) & (df['TANGGAL'] <= end_date)]
#     if status_dt_selected and 'All' not in status_dt_selected:
#         df = df[df['STATUS DT'].isin(status_dt_selected)]
#     return df

# def show_filtered_table(df_filtered):
#     df_filtered = df_filtered.reset_index(drop=True)
#     df_to_show = df_filtered[['NO DT', 'LEVEL KERUSAKAN', 'JENIS KERUSAKAN', 'PART YANG DIBUTUHKAN','QTY','STATUS SPAREPART', 'LAMA BREAKDOWN (Days)']]
#     st.dataframe(df_to_show)

# # def create_line_clustered_chart(df_filtered, date_col='TANGGAL', status_col='STATUS DT', status_value='Ready'):
# #     # Group and resample the data
# #     df_grouped = df_filtered.groupby([pd.Grouper(key=date_col, freq='D'), status_col]).size().unstack(fill_value=0)
# #     df_grouped['Total'] = df_grouped.sum(axis=1)
    
# #     # Create subplots
# #     fig = make_subplots(specs=[[{"secondary_y": True}]])
    
# #     # Add the bar chart for total count
# #     fig.add_trace(
# #         go.Bar(x=df_grouped.index, y=df_grouped['Total'], name='Total Trucks'),
# #         secondary_y=False,
# #     )
    
# #     # Add the line chart for "Ready" status count
# #     if status_value in df_grouped.columns:
# #         fig.add_trace(
# #             go.Scatter(x=df_grouped.index, y=df_grouped[status_value], name='Ready Trucks', mode='lines'),
# #             secondary_y=True,
# #         )
    
# #     # Set x-axis title
# #     fig.update_xaxes(title_text='Date')
    
# #     # Set y-axes titles
# #     fig.update_yaxes(title_text='Total Trucks', secondary_y=False)
# #     fig.update_yaxes(title_text='Ready Trucks', secondary_y=True)
    
# #     # Set layout for the title and legend
# #     fig.update_layout(
# #         title='Daily Status of Trucks',
# #         legend_title='Legend',
# #         legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
# #     )
    
# #     return fig
# def create_line_clustered_chart(df_filtered, date_col='TANGGAL', status_col='STATUS DT', ready_status='Ready', rusak_status='Rusak', rusak_berat_status='Rusak Berat'):
#     # Mengelompokkan dan menyampel ulang data berdasarkan hari
#     df_grouped = df_filtered.groupby([pd.Grouper(key=date_col, freq='D'), status_col]).size().unstack(fill_value=0)
    
#     # Membuat subplot
#     fig = make_subplots(specs=[[{"secondary_y": True}]])

#     # Menambahkan grafik batang untuk status 'Rusak'
#     if rusak_status in df_grouped:
#         fig.add_trace(
#             go.Bar(x=df_grouped.index, y=df_grouped[rusak_status], name=rusak_status, marker_color='orange'),
#             secondary_y=False,
#         )

#     # Menambahkan grafik batang untuk status 'Rusak Berat'
#     if rusak_berat_status in df_grouped:
#         fig.add_trace(
#             go.Bar(x=df_grouped.index, y=df_grouped[rusak_berat_status], name=rusak_berat_status, marker_color='red'),
#             secondary_y=False,
#         )
    
#     # Menambahkan grafik garis untuk jumlah status 'Ready'
#     if ready_status in df_grouped.columns:
#         fig.add_trace(
#             go.Scatter(x=df_grouped.index, y=df_grouped[ready_status], name=ready_status, mode='lines', line=dict(color='green')),
#             secondary_y=True,
#         )
    
#     # Mengatur tumpukan grafik batang
#     fig.update_layout(barmode='stack')

#     # Mengatur judul sumbu x
#     fig.update_xaxes(title_text='Tanggal')

#     # Mengatur judul sumbu y
#     fig.update_yaxes(title_text='Jumlah Rusak & Rusak Berat', secondary_y=False)
#     fig.update_yaxes(title_text='Jumlah Ready', secondary_y=True)

#     # Mengatur layout untuk judul dan legenda
#     fig.update_layout(
#         title='Status Harian Truk',
#         legend_title='Legenda',
#         legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
#     )
    
#     return fig

# def show():
#     st.markdown("""
#         <div style="border: 2px solid #ddd; padding: 10px; text-align: center; background-color: #323288; border-radius: 0px;">
#             <h1 style="color: white; margin: 0;">Monitoring Ketersediaan dan Kondisi Dump Truck</h1>
#         </div>
#         """, unsafe_allow_html=True)

#     sheet_url_dump_truck = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTnflGSDkG_l9mSnawp-HEHX-R5jMfluS1rp0HlF_hMBpQvtG21d3-zPE4TxD80CvQVPjJszeOmNWJB/pub?gid=2078136743&single=true&output=csv'

#     df = load_data(sheet_url_dump_truck)

#     with st.container():
#         date_range = st.date_input("Pilih Tanggal", [])
#         start_date = None
#         end_date = None
#         if len(date_range) == 1:
#             start_date = end_date = date_range[0]
#         elif len(date_range) == 2:
#             start_date, end_date = date_range

#         unique_status = df['STATUS DT'].unique().tolist() if not df.empty else []
#         status_selected = st.multiselect('Pilih Status DT', ['All'] + unique_status, default=['All'])

#     if start_date and end_date:
#         df_filtered = filter_data(df, start_date, end_date, status_selected)
#         col1, col2 = st.columns(2)  # Splitting the layout into two columns

#         with col1:
#             if not df_filtered.empty:
#                 # Define the colors for each status, ensuring 'Rusak Berat' is red
#                 status_colors = {'Ready': 'blue', 'Rusak': 'orange', 'Rusak Berat': 'red'}
#                 df_grouped = df_filtered.groupby('STATUS DT').size().reset_index(name='counts')
#                 colors = [status_colors[status] if status in status_colors else 'grey' for status in df_grouped['STATUS DT']]
                
#                 fig_pie = px.pie(df_grouped, names='STATUS DT', values='counts', title='Distribusi STATUS DT', color_discrete_sequence=colors)
#                 fig_pie.update_traces(textinfo='percent+label+value')
#                 st.plotly_chart(fig_pie)

#         with col2:
#             if not df_filtered.empty:
#                 fig_line_clustered = create_line_clustered_chart(df_filtered)
#                 st.plotly_chart(fig_line_clustered, use_container_width=True)
#             else:
#                 st.warning("Tidak ada data yang sesuai dengan filter yang diberikan untuk grafik garis dan kolom.")  
#          else:
#             st.warning("Silakan pilih tanggal awal dan akhir untuk melihat data.")

# if __name__ == "__main__":
#     show()

#####################################################################################################################################kode dibawah sudah berhasil

# import streamlit as st
# import pandas as pd
# import plotly.express as px

# @st.cache_resource(ttl=300, show_spinner=True)
# def load_data(url):
#     try:
#         df = pd.read_csv(url)
#         # Konversi 'TANGGAL' ke datetime, membiarkan nilai tidak valid menjadi NaT
#         df['TANGGAL'] = pd.to_datetime(df['TANGGAL'], dayfirst=True, errors='coerce')
#         return df
#     except Exception as e:
#         st.error(f"Gagal memuat data: {e}")
#         return pd.DataFrame()

# def filter_data(df, start_date, end_date, status_dt_selected):
#     # Ensure start_date and end_date are Timestamps
#     start_date = pd.to_datetime(start_date).normalize()
#     end_date = pd.to_datetime(end_date).normalize()

# # def filter_data(df, start_date, end_date, status_dt_selected):
# #     # Konversi start_date dan end_date ke datetime jika mereka adalah tipe date
# #     if type(start_date) is not pd.Timestamp:
# #         start_date = pd.to_datetime(start_date)
# #     if type(end_date) is not pd.Timestamp:
# #         end_date = pd.to_datetime(end_date)
    
#     # Menghilangkan baris dengan 'TANGGAL' NaT
#     df = df.dropna(subset=['TANGGAL'])

#     # Filter berdasarkan tanggal
#     if start_date is not None and end_date is not None:
#         df = df[(df['TANGGAL'] >= start_date) & (df['TANGGAL'] <= end_date)]
    
#     # Filter berdasarkan status DT jika tidak 'All'
#     if status_dt_selected and 'All' not in status_dt_selected:
#         df = df[df['STATUS DT'].isin(status_dt_selected)]
    
#     return df
    
# # def show_filtered_table(df_filtered):
# #     # Pilih hanya kolom yang diinginkan dengan nama yang tepat
# #     try:
# #         df_to_show = df_filtered[['NO DT', 'LEVEL KERUSAKAN','JENIS KERUSAKAN', 'LAMA BREAKDOWN (Days)']]
# #         st.dataframe(df_to_show)
# #     except KeyError as e:
# #         st.error(f'Kolom tidak ditemukan dalam DataFrame: {e}')
# #         st.write('Kolom yang tersedia di DataFrame:', df_filtered.columns.tolist())

# def show_filtered_table(df_filtered):
#     # Setel indeks DataFrame ke None
#     df_filtered = df_filtered.reset_index(drop=True)
#     df_to_show = df_filtered[['NO DT', 'LEVEL KERUSAKAN', 'JENIS KERUSAKAN', 'PART YANG DIBUTUHKAN', 'LAMA BREAKDOWN (Days)']]
#     st.dataframe(df_to_show)
    
# def show():
#     st.markdown("""
#         <div style="border: 2px solid #ddd; padding: 10px; text-align: center; background-color: #323288; border-radius: 0px;">
#             <h1 style="color: white; margin: 0;">Monitoring Ketersediaan dan Kondisi Dump Truck</h1>
#         </div>
#         """, unsafe_allow_html=True)

#     sheet_url_dump_truck = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTnflGSDkG_l9mSnawp-HEHX-R5jMfluS1rp0HlF_hMBpQvtG21d3-zPE4TxD80CvQVPjJszeOmNWJB/pub?gid=2078136743&single=true&output=csv'

#     df = load_data(sheet_url_dump_truck)

#     with st.container():
#         date_range = st.date_input("Pilih Tanggal", [])
#         start_date = None
#         end_date = None
#         if len(date_range) == 1:
#             start_date = end_date = date_range[0]
#         elif len(date_range) == 2:
#             start_date, end_date = date_range

#         unique_status = df['STATUS DT'].unique().tolist() if not df.empty else []
#         status_selected = st.multiselect('Pilih Status DT', ['All'] + unique_status, default=['All'])

#     if start_date and end_date:
#         df_filtered = filter_data(df, start_date, end_date, status_selected)

#         if not df_filtered.empty:
#             df_grouped = df_filtered.groupby('STATUS DT').size().reset_index(name='counts')
#             fig = px.pie(df_grouped, names='STATUS DT', values='counts', title='Distribusi STATUS DT')
#             fig.update_traces(textinfo='percent+label+value')
#             st.plotly_chart(fig)
#             show_filtered_table(df_filtered)  # Pemanggilan fungsi untuk menampilkan tabel
#         else:
#             st.warning("Tidak ada data yang sesuai dengan filter yang diberikan.")
#     else:
#         st.warning("Silakan pilih tanggal awal dan akhir untuk melihat data.")

# if __name__ == "__main__":
#     show()









