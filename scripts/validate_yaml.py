import os
import glob
import yaml
import logging
import jsonschema
from jsonschema import validate


def get_filename_only(file_path):
    base_name = os.path.basename(file_path)
    filename_only, _ = os.path.splitext(base_name)
    return filename_only


def load_yaml(file_path):
    with open(file_path, "r") as file:
        return yaml.safe_load(file)


def validate_with_schema(file_path, schema):
    try:
        validate(load_yaml(file_path), schema)
        return True
    except jsonschema.exceptions.ValidationError as ve:
        logging.error("Validation error in " + get_filename_only(file_path))
        logging.error(ve)
        return False


def main():
    global root_path
    root_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

    brand_schema = load_yaml(os.path.join(root_path, "schemas/brand_schema.yaml"))
    brand_files = glob.glob(os.path.join(root_path, "data/brands/") + "*.yaml")
    print("Validating", len(brand_files), "brands")
    failed = False
    for file in brand_files:
        if not validate_with_schema(file, brand_schema):
            failed = True
    print("All brands are valid.")

    company_schema = load_yaml(os.path.join(root_path, "schemas/company_schema.yaml"))
    company_files = glob.glob(os.path.join(root_path, "data/companies/") + "*.yaml")
    print("Validating", len(company_files), "companies")
    for file in company_files:
        if not validate_with_schema(file, company_schema):
            failed = True

    if failed:
        exit(1)

    print("All companies are valid.")


if __name__ == "__main__":
    main()
