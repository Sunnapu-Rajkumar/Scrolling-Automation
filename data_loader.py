import pandas as pd
import json
import xml.etree.ElementTree as ET

def normalize_data(data, parent_key=''):
    flat_data = []

    if isinstance(data, dict):
        for key, value in data.items():
            full_key = f"{parent_key}.{key}" if parent_key else key
            if isinstance(value, (dict, list, set, tuple)):
                flat_data.extend(normalize_data(value, full_key))
            else:
                flat_data.append({"Key": full_key, "Value": value})

    elif isinstance(data, (list, tuple, set)):
        for idx, item in enumerate(data):
            full_key = f"{parent_key}[{idx}]" if parent_key else f"[{idx}]"
            if isinstance(item, (dict, list, set, tuple)):
                flat_data.extend(normalize_data(item, full_key))
            else:
                flat_data.append({"Key": full_key, "Value": item})

    else:
        flat_data.append({"Key": parent_key, "Value": data})

    return flat_data


def dynamic_loader(file_path, return_type="array_of_dicts"):
    if file_path.endswith(".xlsx"):
        df = pd.read_excel(file_path)
    elif file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    elif file_path.endswith(".json"):
        with open(file_path, 'r') as f:
            data = json.load(f)
            return data  # for JSON just return directly
    elif file_path.endswith(".xml"):
        tree = ET.parse(file_path)
        root = tree.getroot()
        data = []
        for child in root:
            record = {elem.tag: elem.text for elem in child}
            data.append(record)
        return data
    else:
        raise ValueError("Unsupported file format")

    # Return as per user request
    if return_type == "array_of_dicts":
        return df.to_dict(orient='records')
    elif return_type == "dict_of_arrays":
        return {col: df[col].tolist() for col in df.columns}
    elif return_type == "array_of_arrays":
        return df.values.tolist()
    elif return_type == "pandas":
        return df
    else:
        raise ValueError("Unsupported return_type option")

# Example
# result = dynamic_loader("file.xlsx", return_type="dict_of_arrays")
# print(result)
