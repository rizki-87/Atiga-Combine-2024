import streamlit as st
import pandas as pd
import altair as alt

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

ef create_radial_chart(df, status_dt_selected):
    # Ensure we're only dealing with the selected statuses
    if status_dt_selected and 'All' not in status_dt_selected:
        df = df[df['STATUS AB'].isin(status_dt_selected)]

    # Calculate counts and percentage
    radial_df = df['STATUS AB'].value_counts().reset_index()
    radial_df.columns = ['STATUS AB', 'count']
    total = radial_df['count'].sum()
    radial_df['percentage'] = (radial_df['count'] / total).map(lambda n: '{:.1%}'.format(n))
    
    # Determine the midpoint of the arcs to place the text labels
    radial_df['midpoint'] = (radial_df['count'] / total * 2 * 3.14159265).cumsum() - (radial_df['count'] / total * 3.14159265)

    # Create the Radial Chart
    chart = alt.Chart(radial_df).mark_arc(innerRadius=50).encode(
        theta=alt.Theta(field="count", type="quantitative", stack=True),
        color=alt.Color(field="STATUS AB", type="nominal"),
        tooltip=['STATUS AB', 'count', 'percentage']
    ).properties(width=300, height=300)

    # Add text labels
    text = chart.mark_text(
        radiusOffset=120,  # You can adjust this value if needed
        align='center',
        baseline='middle',
        angle=alt.Angle('midpoint', scale=None)  # Use the calculated midpoint angle for text labels
    ).encode(
        text='count:N',
        theta=alt.Theta(field="count", type="quantitative", stack=True),
        color=alt.value('black'),  # Set text color to black (or any other color)
        angle='midpoint:Q'  # Assign the calculated midpoint angle to the angle encoding
    )

    # Combine the layers
    layered_chart = chart + text
    
    return layered_chart

# Main layout and logic
def show():
    st.markdown("""
    <div style="border: 2px solid #ddd; padding: 10px; text-align: center; background-color: #323288; border-radius: 0px;">
        <h1 style="color: white; margin: 0;">Monitoring Ketersediaan dan Kondisi Alat Berat</h1>
    </div>
    """, unsafe_allow_html=True)

    sheet_url_alat_berat = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQ1vygEd5Ykxt7enZtJBCWIwO91FTb3mVbsRNvq2XlItosvT8ROsXwbou354QWZqY4p0eNtRM-bAESm/pub?gid=1149198834&single=true&output=csv'
    df = load_data(sheet_url_alat_berat)

    with st.container():
        date_range = st.date_input("Pilih Tanggal", [])
        start_date = date_range[0] if len(date_range) > 0 else None
        end_date = date_range[-1] if len(date_range) > 1 else start_date
        unique_status = df['STATUS AB'].unique().tolist() if not df.empty else []
        status_selected = st.multiselect('Pilih Status Alat Berat', ['All'] + unique_status, default=['All'])

        if df.empty:
            st.warning("Data tidak ditemukan.")
        else:
            # Call the create_radial_chart within the container after filters
            filtered_data = filter_data(df, start_date, end_date, status_selected)
            if not filtered_data.empty:
                radial_chart = create_radial_chart(filtered_data, status_selected)
                st.altair_chart(radial_chart, use_container_width=True)
            else:
                st.warning("Tidak ada data yang sesuai dengan kriteria filter.")

if __name__ == "__main__":
    show()


#############################################################################################################################################################################

# import streamlit as st
# import pandas as pd
# import plotly.express as px
# from plotly.subplots import make_subplots
# import plotly.graph_objects as go
# import altair as alt

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
#         df = df[df['STATUS AB'].isin(status_dt_selected)]
#     return df

# def create_radial_chart(df, status_dt_selected):
#     # Filter data based on the selected status
#     if status_dt_selected and 'All' not in status_dt_selected:
#         df = df[df['STATUS AB'].isin(status_dt_selected)]

#     # Create a DataFrame suitable for a radial chart
#     radial_df = df['STATUS AB'].value_counts().reset_index()
#     radial_df.columns = ['STATUS AB', 'count']

#     # Create the Radial Chart
#     chart = alt.Chart(radial_df).mark_arc(innerRadius=50).encode(
#         theta=alt.Theta(field="count", type="quantitative"),
#         color=alt.Color(field="STATUS AB", type="nominal"),
#         tooltip=['STATUS AB', 'count']
#     ).properties(
#         width=300,
#         height=300
#     )
#     return chart

# def show_radial_chart(df, date_range, unique_status):
#     # Extracting the selected statuses if provided, otherwise using all available statuses
#     status_selected = st.multiselect(
#         'Pilih Status Alat Berat', 
#         ['All'] + unique_status, 
#         default=['All']
#     )
    
#     # Filter data
#     filtered_data = filter_data(df, date_range[0], date_range[1], status_selected)
    
#     # Creating and displaying Radial Chart
#     radial_chart = create_radial_chart(filtered_data, status_selected)
#     st.altair_chart(radial_chart, use_container_width=True)


# def show():
#     st.markdown("""
#     <div style="border: 2px solid #ddd; padding: 10px; text-align: center; background-color: #323288; border-radius: 0px;">
#         <h1 style="color: white; margin: 0;">Monitoring Ketersediaan dan Kondisi Alat Berat</h1>
#     </div>
#     """, unsafe_allow_html=True)

#     sheet_url_alat_berat = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQ1vygEd5Ykxt7enZtJBCWIwO91FTb3mVbsRNvq2XlItosvT8ROsXwbou354QWZqY4p0eNtRM-bAESm/pub?gid=1149198834&single=true&output=csv'

#     df = load_data(sheet_url_alat_berat)

#     with st.container():
#         date_range = st.date_input("Pilih Tanggal", [])
#         start_date = None
#         end_date = None
#         if len(date_range) == 1:
#             start_date = end_date = date_range[0]
#         elif len(date_range) == 2:
#             start_date, end_date = date_range

#         unique_status = df['STATUS AB'].unique().tolist() if not df.empty else []
#         status_selected = st.multiselect('Pilih Status Alat Berat', ['All'] + unique_status, default=['All'])
#############################################################################################################################################
# import streamlit as st

# def show():
#     st.title("Halaman Monitoring Alat Berat")
#     st.header("Under Construction")
