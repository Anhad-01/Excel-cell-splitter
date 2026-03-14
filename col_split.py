import pandas as pd

def split_and_clean(text):
    if pd.isna(text):
        return []
    # Split by newline and remove empty entries or whitespace
    return [line.strip() for line in str(text).split('\n') if line.strip()]

def process_dataframe(df: pd.DataFrame, column_index: int = 3) -> pd.DataFrame:
    col_to_split = df.columns[column_index]
    df_processed = df.copy()
    df_processed[col_to_split] = df_processed[col_to_split].apply(split_and_clean)
    return df_processed.explode(col_to_split).reset_index(drop=True)


def process_file(input_path: str, output_path: str, column_index: int = 3) -> pd.DataFrame:
    if input_path.lower().endswith('.xlsx'):
        df = pd.read_excel(input_path)
    else:
        df = pd.read_csv(input_path)

    df_final = process_dataframe(df, column_index=column_index)
    df_final.to_csv(output_path, index=False)
    return df_final


if __name__ == '__main__':
    input_file = 'Copy of ECA Middle Mathematics.xlsx'
    output_file = 'Processed_Middle_Mathematics_ECA.csv'
    process_file(input_file, output_file)