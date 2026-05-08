import pandas as pd
import os

# Base folder containing yearly cleaned data
base_path = r"C:\Users\94sun\OneDrive - Coventry University\Desktop\projects\NHS_RTT_Project\RTT_CLEAN_DATA"

all_data = []

for folder in os.listdir(base_path):
    folder_path = os.path.join(base_path, folder)

    if os.path.isdir(folder_path):

        file_path = os.path.join(folder_path, "RTT_FULL_DATA.csv")

        if os.path.exists(file_path):
            print(f"Adding: {folder}")

            df = pd.read_csv(file_path)
            df["year_folder"] = folder

            all_data.append(df)

# Combine all datasets
final_df = pd.concat(all_data, ignore_index=True)

# Clean column names
final_df.columns = final_df.columns.str.strip().str.replace(" ", "_")

# Save output
output_path = os.path.join(base_path, "rtt_master_data.csv")
final_df.to_csv(output_path, index=False)

print(" MASTER DATA CREATED")