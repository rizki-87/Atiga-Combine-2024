import streamlit as st
import importlib.util
# import dumptruck
# import alatberat

def load_module(page_name):
    if page_name == 'Monitoring Dump Truck':
        page_path = 'dumptruck.py'
    elif page_name == 'Monitoring Alat Berat':
        page_path = 'alatberat.py'
    else:
        raise ValueError(f"Unknown page {page_name}")

    try:
        spec = importlib.util.spec_from_file_location(page_name, page_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    except Exception as e:
        st.error(f"Failed to load module {page_name}: {e}")
        return None


def main():
    st.set_page_config(page_title='Dashboard Monitoring', page_icon="atiga.png", layout='wide')
    st.sidebar.image('atiga.png', width=300)
    page = st.sidebar.radio('Pilih Halaman', ['Monitoring Dump Truck', 'Monitoring Alat Berat'])

    page_module = load_module(page)
    if page_module is not None:
        page_module.show()

if __name__ == "__main__":
    main()
