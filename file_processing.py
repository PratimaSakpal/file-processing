import glob
import pandas as pd

print('Start')

CSV_PATHS = glob.glob("./Input/*.DAT")

def read_input_files():
    dataframes = []
    for i, csv_file_path in enumerate(CSV_PATHS):
        try:
            print(f'Processing file {csv_file_path}...')
            df = pd.read_csv(csv_file_path,sep='\t')
            if i == 0:
                csv_schema = df.columns
            #    print(csv_schema)
            #elif csv_schema == df.columns:
            #    print(f"Error: File schema does not match. Skipping...")    
            #    break
            dataframes.append(df)
        except pd.errors.ParserError as e:
            print(f"Error parsing '{csv_file_path}': {e}") 
    return dataframes

def get_salary_details():
    merged_df = pd.concat(dataframes)
    print(merged_df.columns.tolist())
    merged_df = merged_df.drop_duplicates()
    unique_salary = list(set(merged_df['basic_salary'].tolist()))
    unique_salary.sort()
    print(unique_salary[-5:])
    avg_basic_salary = merged_df['basic_salary'].aggregate('mean')
    # second_highest = merged_df['basic_salary'].nlargest(2).iloc[1]
    second_highest = unique_salary[-2]
    merged_df.to_csv("merged_data.csv") 
    result_data = {'Second Highest Salary': [f'Second Highest Salary={second_highest}'], 'average salary = ': [f'average salary = {avg_basic_salary}'] }
    summary_df = pd.DataFrame(result_data)
    print(f'Second Highest Salary={second_highest}: average salary = {avg_basic_salary} ')
    summary_df.to_csv("Result.csv", index=False, header=False) 

if __name__ == "__main__":
    dataframes = read_input_files()
    get_salary_details(dataframes)
