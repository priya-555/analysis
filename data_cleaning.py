import pandas as pd
import glob

# Path to the directory where all CSV files are stored
path = r"file_path"
all_files = glob.glob(path + "*.csv")

# List to hold dataframes
dfs = []

# Loop through each file, load it into a dataframe, and append to the list
for filename in all_files:
    try:
        df = pd.read_csv(filename, encoding='ISO-8859-1', on_bad_lines='skip')
        dfs.append(df)
    except Exception as e:
        print(f"Error reading {filename}: {e}")

# Concatenate all dataframes into one
if dfs:
    combined_df = pd.concat(dfs, ignore_index=True)
else:
    print("No dataframes to concatenate.")
    exit()

# Handling missing values
# Fill numeric columns with the median
for col in combined_df.select_dtypes(include=['float64', 'int64']).columns:
    median_value = combined_df[col].median()
    combined_df[col] = combined_df[col].fillna(median_value)

# Fill categorical columns with the mode
for col in combined_df.select_dtypes(include=['object']).columns:
    mode_value = combined_df[col].mode()[0] if not combined_df[col].mode().empty else 'Unknown'
    combined_df[col] = combined_df[col].fillna(mode_value)

# Save the cleaned DataFrame to a new CSV file
combined_df.to_csv('Cleaned_Data.csv', index=False)
print("Data cleaning complete. Cleaned data saved to 'Cleaned_Data.csv'.")
