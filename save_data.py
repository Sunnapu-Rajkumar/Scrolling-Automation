import os

def save_data(array,base_folder):
    # Example list of college names
    # colleges = [
    #     "School of Arts & Sciences",
    #     "The Wharton School",
    #     "Annenberg School for Communication",
    #     "School of Engineering and Applied Science",
    # ]

    # # Define the base directory where folders should be created
    # base_folder = r"C:\Users\rajku\Desktop\Penn_University"

    # Ensure the base directory exists
    os.makedirs(base_folder, exist_ok=True)

    # Create folders for each college
    for item in array:
        folder_name = item.replace(" ", "_").replace("&", "and")  # Clean folder name
        folder_path = os.path.join(base_folder, folder_name)  # Generate folder path
        
        os.makedirs(folder_path, exist_ok=True)  # Create folder if it doesn't exist

    print(f"Folders successfully created in '{base_folder}' directory!")
def save_excel(data,output_folder):
    os.makedirs(output_folder, exist_ok=True)  # Create "Colleges" folder if not exists
    output_file = os.path.join(output_folder, "Colleges.xlsx")
    # Save to Excel
    data.to_excel(output_file, index=False)

    print(f"✅ Data saved successfully in {output_file}")