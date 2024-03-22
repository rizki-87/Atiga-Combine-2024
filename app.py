import streamlit as st
import importlib.util

def load_module(page_name):
    if page_name == 'Monitoring Dump Truck':
        page_path = 'dumptruck.py'
    elif page_name == 'Monitoring Heavy Equipment':
        page_path = 'alatberat.py'
    else:
        raise ValueError(f"Unknown page {page_name}")

    spec = importlib.util.spec_from_file_location(page_name, page_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def main():
    st.set_page_config(page_title='Dashboard Monitoring', page_icon=':truck:', layout='wide')
    st.sidebar.image('atiga.png', width=300)
    page = st.sidebar.radio('Pilih Halaman', ['Monitoring Dump Truck', 'Monitoring Heavy Equipment'])

    page_module = load_module(page)
    page_module.show()

if __name__ == "__main__":
    main()
