import pandas as pd

def auto_clean_excel(input_file, output_file='cleaned_output.xlsx'):
    # Read Excel
    df = pd.read_excel(input_file)
    
    # Automatically melt all columns into Department + Value
    df_long = df.melt(var_name='Department', value_name='Data')

    # Drop rows where 'Data' is empty
    df_long.dropna(subset=['Data'], inplace=True)

    # Optional: Trim whitespace from both columns
    df_long['Department'] = df_long['Department'].str.strip()
    df_long['Data'] = df_long['Data'].str.strip()

    # Save cleaned file
    df_long.to_excel(output_file, index=False)
    print(f"✅ Done! Cleaned file saved as: {output_file}")

# Example usage:
auto_clean_excel('your_file.xlsx')
