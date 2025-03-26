import pandas as pd 
def normalize_data(data):
    flat_data = []

    if isinstance(data, dict):
        for college_or_dept, prof_list in data.items():
            if isinstance(prof_list, str):
                flat_data.append({
                    "Department": college_or_dept,
                    "Name": prof_list
                })
            elif isinstance(prof_list, list):
                for prof in prof_list:
                    row = {"Department": college_or_dept}

                    if prof is None:
                        continue  # Skip None items

                    if isinstance(prof, (list, tuple)):
                        if len(prof) > 0 and prof[0]:
                            row["Name"] = prof[0]
                        if len(prof) > 1 and prof[1]:
                            row["Title"] = prof[1]
                        if len(prof) > 2 and prof[2]:
                            row["Email"] = prof[2].replace('(link sends email)', '').strip()
                        flat_data.append(row)
                    elif isinstance(prof, str):
                        row["Name"] = prof
                        flat_data.append(row)
                    else:
                        # Catch unexpected type like dict, int, etc.
                        row["Name"] = str(prof)
                        flat_data.append(row)
            else:
                flat_data.append({
                    "Department": college_or_dept,
                    "Name": str(prof_list)
                })

    return flat_data


def download_excel(data, file_name="output_name", columns=None, drop_na=True, index=False):
    if not file_name.endswith(".xlsx"):
        file_name += ".xlsx"

    flat_data = normalize_data(data)
    df = pd.DataFrame(flat_data)

    if drop_na:
        df.dropna(inplace=True)
    if columns:
        df = df[columns]

    df.to_excel(file_name, index=index)
    print(f"✅ Excel file saved as {file_name}")

