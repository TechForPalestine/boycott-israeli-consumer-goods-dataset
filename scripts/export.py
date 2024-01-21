import yaml
import csv
import json
import csv
import os


def read_yaml(file_path):
    with open(file_path, "r") as file:
        data = yaml.safe_load(file)
    return data


def clean_value(value):
    if isinstance(value, list):
        return ", ".join(map(str, value))
    else:
        return value


def export_to_csv(input_dir, output_csv, schema_file):
    schema = read_yaml(schema_file)

    with open(output_csv, "w", newline="") as csvfile:
        schema_fields = list(schema["properties"].keys())
        if "stakeholders" in schema_fields:
            # Haven't decided how to represent stakeholders in the CSV format, so just remove it for now.
            schema_fields.remove("stakeholders")
        fieldnames = ["id"] + schema_fields
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write header based on the schema
        writer.writeheader()

        for yaml_file in sorted(os.listdir(input_dir)):
            if yaml_file.endswith(".yaml"):
                yaml_file_path = os.path.join(input_dir, yaml_file)
                with open(yaml_file_path, "r") as file:
                    data = yaml.safe_load(file)

                    cleaned_data = {
                        key: clean_value(data.get(key, None)) for key in fieldnames
                    }
                    cleaned_data["id"] = os.path.splitext(yaml_file)[0]

                    writer.writerow(cleaned_data)

                    print(f"Converted {yaml_file} to CSV")


def convert_yaml_to_json(directory_path, key):
    data = {}

    for file_name in sorted(os.listdir(directory_path)):
        if file_name.endswith(".yaml"):
            file_path = os.path.join(directory_path, file_name)
            with open(file_path, "r") as yaml_file:
                yaml_data = {}

                yaml_data = yaml.safe_load(yaml_file)

                data[os.path.splitext(file_name)[0]] = {
                    "id": os.path.splitext(file_name)[0],
                    **yaml_data,
                }

    return {key: data}


def export_to_json(directory1, directory2, output_json):
    brands_data = convert_yaml_to_json(directory1, "brands")
    companies_data = convert_yaml_to_json(directory2, "companies")

    combined_data = {**brands_data, **companies_data}

    with open(output_json, "w") as json_file:
        json.dump(combined_data, json_file, indent=2)

        print(f"Converted data to JSON")


if __name__ == "__main__":
    brands_yaml = "data/brands"
    companies_yaml = "data/companies"

    brands_csv_file = "output/csv/brands.csv"
    companies_csv_file = "output/csv/companies.csv"

    data_json_file = "output/json/data.json"

    brand_schema = "schemas/brand_schema.yaml"
    company_schema = "schemas/company_schema.yaml"

    export_to_csv(brands_yaml, brands_csv_file, brand_schema)
    export_to_csv(companies_yaml, companies_csv_file, company_schema)
    export_to_json(brands_yaml, companies_yaml, data_json_file)
