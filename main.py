import os
import tempfile
from pathlib import Path

import pandas as pd
import streamlit as st

from col_split import process_file


st.set_page_config(page_title="ECA File Processor", layout="wide")
st.title("ECA File Processor")

uploaded_file = st.file_uploader("Upload input file", type=["xlsx", "csv"])

if uploaded_file is not None:
    input_stem = Path(uploaded_file.name).stem
    output_file_name = f"Processed_{input_stem}.csv"

    with tempfile.TemporaryDirectory() as temp_dir:
        input_path = os.path.join(temp_dir, uploaded_file.name)
        output_path = os.path.join(temp_dir, output_file_name)

        with open(input_path, "wb") as file_handle:
            file_handle.write(uploaded_file.getbuffer())

        try:
            process_file(input_path, output_path)
            output_df = pd.read_csv(output_path)

            st.subheader("Output Preview")
            st.dataframe(output_df, use_container_width=True)

            with open(output_path, "rb") as output_handle:
                st.download_button(
                    label="Download Processed File",
                    data=output_handle.read(),
                    file_name=output_file_name,
                    mime="text/csv",
                )
        except Exception as error:
            st.error(f"Failed to process file: {error}")
