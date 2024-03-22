import streamlit as st

# Menginisialisasi multi-page app
def main():
    st.set_page_config(page_title='Dashboard Monitoring', page_icon=':truck:', layout='wide')
    st.sidebar.image('atiga.png', width=300)
    page = st.sidebar.radio('Pilih Halaman', ['Monitoring Dump Truck', 'Monitoring Heavy Equipment'])

    if page == 'Monitoring Dump Truck':
        from pages import monitoring_dump_truck
        monitoring_dump_truck.show()
    elif page == 'Monitoring Heavy Equipment':
        from pages import monitoring_heavy_equipment
        monitoring_heavy_equipment.show()

if __name__ == "__main__":
    main()
