# ECA File Processing

A minimal Streamlit app to process uploaded Excel/CSV files using the transformation logic from `col_split.py`.

## What it does

- Upload an input file (`.xlsx` or `.csv`)
- Splits line-separated values in the 4th column (index `3`) into multiple rows
- Shows the processed output as a preview
- Lets you download the output as:
  - `Processed_<input_file_name>.csv`

## Project files

- `main.py` - Streamlit interface
- `col_split.py` - Core processing logic
- `requirements.txt` - Python dependencies

## Setup

1. (Optional) Create and activate a virtual environment
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the app

```bash
streamlit run main.py
```

Then open the local URL shown in your terminal (usually `http://localhost:8501`).

## Notes

- For `.xlsx` files, `openpyxl` is used as the Excel engine.
- If your target split column is not the 4th column, update the `column_index` argument in `process_file(...)` inside `main.py`.
