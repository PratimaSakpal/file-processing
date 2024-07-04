"""
Author: Pratima Sakpal
Date: 03 July 2014
"""
import pandas as pd
import os

def read_input_files(path):
    """
    Description: Method to read files and create data frame.
    Input: None
    Output: data_frames (list)
    """
    try:
        csv_paths = os.listdir(path)
    except Exception as FileNotFoundError:
        print("Error: Input Folder not found.")
        return None
    
    data_frames = []
    for index, csv_file_path in enumerate(csv_paths):
        try:
            # print(f'Processing file {csv_file_path}...')
            csv_df = pd.read_csv(path + '/'+ csv_file_path, sep='\t')
        except pd.errors.ParserError as e:
            print(f"Error parsing '{csv_file_path}': {e}") 
            break
        if index == 0:
            csv_schema = list(csv_df.columns).sort()
        elif csv_schema != list(csv_df.columns).sort():
            print("Error: File schema does not match. Skipping...")    
            break
        data_frames.append(csv_df)
        
    if data_frames:
        merged_df = pd.concat(data_frames)
        merged_df = merged_df.drop_duplicates()
        return merged_df
    return pd.DataFrame([])

def get_salary_details(dataframe):
    """
    Description: Method to do second highest and average salary.
    Input: data_frame (list)
    Output: Creates CSV file 
    """
    unique_salary = list(set(dataframe['basic_salary'].tolist()))
    unique_salary.sort()
    avg_basic_salary = dataframe['basic_salary'].aggregate('mean')
    second_highest = unique_salary[-2]
     
    result_data = {
        'Second Highest Salary': [f'Second Highest Salary={second_highest}'],
        'average salary = ': [f'average salary = {avg_basic_salary}'] }
    return result_data
    
def generate_result(dataframe, result_data, path):
    """
    Desription: Method to write generated output into CSV file.
    Input: dataframe (object), result_data (dictionary), path (string)
    Output: Generate CSV file.
    """
    directory = '\\'.join(path.split('\\')[:-1]) +"/Output"
    if not os.path.exists(directory):
        os.makedirs(directory)
    dataframe.to_csv("Output/Result.csv")
    summary_df = pd.DataFrame(result_data)
    summary_df.to_csv("Output/Result.csv", mode='a', index=False, header=False) 
    print(f"Find an output file on below path:\n{directory}/Result.csv")

def driver():
    """
    Description: For calling methods
    Input: None
    Output: None
    """
    path = 'E:\Projects\InterviewQ\FileProcessing\Input'
    dataframe = read_input_files(path)
    if not dataframe.empty:
        result_data = get_salary_details(dataframe)
        generate_result(dataframe, result_data, path)
    else:
        print('File not found.')

if __name__ == "__main__":
    driver()
