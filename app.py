import streamlit as st
import importlib.util

def load_module(page_name):
    if page_name == 'Monitoring Dump Truck':
        page_path = 'dumptruck.py'
    elif page_name == 'Monitoring Alat Berat':
        page_path = 'alatberat.py'
    else:
        raise ValueError(f"Unknown page {page_name}")

    spec = importlib.util.spec_from_file_location(page_name, page_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def main():
    page = st.sidebar.radio('Pilih Halaman', ['Monitoring Dump Truck', 'Monitoring Alat Berat'])

    if page == 'Monitoring Dump Truck':
        import dumptruck
        dumptruck.show()
    elif page == 'Monitoring Alat Berat':
        import alatberat
        alatberat.show()

if __name__ == "__main__":
    main()

