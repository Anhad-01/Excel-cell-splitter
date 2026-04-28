# ECA File Processing

A Streamlit app with two processing flows:

- Split uploaded Excel/CSV files using the transformation logic from `col_split.py`
- Convert uploaded HTML carousel/mockup files into a downloadable PDF using `html_to_pdf.py`

## What it does

### Excel/CSV processing

- Upload an input file (`.xlsx` or `.csv`)
- Splits line-separated values in the 4th column (index `3`) into multiple rows
- Shows the processed output as a preview
- Lets you download `Processed_<input_file_name>.csv`

### HTML to PDF conversion

- Upload an input file (`.html` or `.htm`)
- Looks for `.slide` elements in the HTML
- Captures the `.frame` element for each slide
- Combines the captured slides into a single PDF for download

## Project files

- `main.py` - Streamlit interface
- `col_split.py` - Core processing logic
- `html_to_pdf.py` - HTML-to-PDF conversion logic
- `requirements.txt` - Python dependencies

## Setup

1. (Optional) Create and activate a virtual environment
2. Install dependencies:

```bash
pip install -r requirements.txt
playwright install chromium
```

## Run the app

```bash
streamlit run main.py
```

Then open the local URL shown in your terminal (usually `http://localhost:8501`).

## Notes

- For `.xlsx` files, `openpyxl` is used as the Excel engine.
- If your target split column is not the 4th column, update the `column_index` argument in `process_file(...)` inside `main.py`.
- The HTML-to-PDF flow expects the uploaded HTML to contain `.slide` elements and a `.frame` element matching the notebook's existing structure.
- `playwright install chromium` must be run once after installing dependencies so the PDF conversion flow can launch Chromium.
