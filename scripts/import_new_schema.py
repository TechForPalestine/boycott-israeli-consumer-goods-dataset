import sys
import json
import re
import os
from glob import glob
from unidecode import unidecode
import yaml
import pdb

# brand/company fields
NAME = "name"
DESCRIPTION = "description"
REASONS = "reasons"
COUNTRIES = "countries"
LOGO_URL = "logo_url"
ALTERNATIVES = "alternatives"
ALTERNATIVES_TEXT = "alternatives_text"
STAKEHOLDERS = "stakeholders"
STATUS = "status"
CATEGORIES = "categories"
WEBSITE = "website"

# stakeholder fields
ID = "id"
TYPE = "type"
OWNERSHIP_PERCENT = "ownership_percent"

# path to the repo
root_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
brands_path = os.path.join(root_path, "data/brands/")
companies_path = os.path.join(root_path, "data/companies/")

# Get pre-existing files so we don"t overwrite them.
# To overwrite them just delete the existing one and re-run the script.
existing_files = glob(brands_path + "*.yaml") + glob(companies_path + "*.yaml")

owner_regex = re.compile(r"[O|o]wned [B|b]y \*\*(.+?)(?:\.+)?\*\*")

witness_owner_regex = re.compile(r"[B|b]y ([\S]+)")


def parent_from_details(details):
    if details:
        match = owner_regex.search(details)
        if match:
            return match.group(1)
    return ""


def witness_parent_from_details(details):
    if details:
        match = witness_owner_regex.search(details)
        if match:
            return match.group(1)
    return ""


spaces_before_newline_regex = re.compile(r" +\n")


# Custom representer for multiline strings
def literal_presenter(dumper, data):
    # Try and convert unicode characters that forces YAML to use the "" style instead of |.
    # Also remove trailing whitespace for the same reason.
    # Also remove whitespace before new lines for the same reason.
    data = unidecode(spaces_before_newline_regex.sub("\n", data.strip()))
    if "\n" in data or len(data) > 30:
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    if " " in data:
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="")
    if not data or data == "":
        return dumper.represent_scalar("tag:yaml.org,2002:null", "")
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


def none_representer(dumper, _):
    return dumper.represent_scalar("tag:yaml.org,2002:null", "")


# Apply the custom representer
yaml.add_representer(str, literal_presenter)
yaml.add_representer(type(None), none_representer)


def create_alternatives_data_models(data):
    brands_yaml_data = {}
    for row in data:
        alternative = row.get("attributes").get("alternative").get("data")
        if alternative:
            brand_name = alternative.get("attributes").get("name").lower()
            image_url = alternative.get("attributes").get("imageUrl")

            if not brand_name:
                continue

            # assume that if it has a parent it"s a brand, otherwise it"s a company
            brands_yaml_data[brand_name] = {
                NAME: brand_name,
                STATUS: "support",
                COUNTRIES: [],
                CATEGORIES: [],
                DESCRIPTION: brand_name,
            }
            if image_url:
                brands_yaml_data[brand_name][LOGO_URL] = image_url

    return brands_yaml_data


def name_to_id(name):
    return "".join(
        x for x in unidecode(name.lower().replace(" ", "-")) if x.isalnum() or x == "-"
    )


def create_data_models(data):
    brands_yaml_data, companies_yaml_data = {}, {}
    for row in data:
        brand_name = row.get("attributes").get("name")
        proof_raw = row.get("attributes").get("proof")
        proof_url = row.get("attributes").get("proofUrl")
        proof = f"{proof_raw}[^1]\n\n[^1]: {proof_url}"

        parent_name = parent_from_details(proof).lower()
        image_url = row.get("attributes").get("imageUrl")
        reason = (
            "operations_in_settlements"
            if "settlements" in proof.lower()
            else "operations_in_israel"
        )

        alternatives = []
        alt_data = row.get("attributes").get("alternative").get("data")
        if alt_data:
            alternatives.append(
                name_to_id(alt_data.get("attributes").get("name").lower())
            )

        if not brand_name:
            continue

        # assume that if it has a parent it"s a brand, otherwise it"s a company
        if parent_name:
            brands_yaml_data[brand_name] = {
                NAME: brand_name,
                STATUS: "avoid",
                DESCRIPTION: proof,
                REASONS: [reason],
                COUNTRIES: ["global"],
                CATEGORIES: [],
            }
            if image_url:
                brands_yaml_data[brand_name][LOGO_URL] = image_url
            brands_yaml_data[brand_name][ALTERNATIVES] = alternatives
            brands_yaml_data[brand_name][STAKEHOLDERS] = [
                {ID: name_to_id(parent_name), TYPE: "owner"}
            ]
        else:
            companies_yaml_data[brand_name] = {
                NAME: brand_name,
                STATUS: "avoid",
                DESCRIPTION: proof,
            }

    return brands_yaml_data, companies_yaml_data


def create_data_models_from_witness_json(data):
    brands_yaml_data, companies_yaml_data = {}, {}

    for row in data:
        brand_name = row.get("name")
        desc = row.get("reason")
        how_to_boycott = "\n".join(row.get("howToBoycott"))
        proof_url = row.get("source")
        proof = f"{desc}[^1]\n\n{how_to_boycott}\n[^1]: {proof_url}"
        categories = row.get("category")
        parent_name = witness_parent_from_details(row.get("description")).lower()
        image_url = row.get("logo")
        reason = (
            "operations_in_settlements"
            if "settlement" in proof.lower()
            else "operations_in_israel"
        )

        alternatives_txt = "\n".join(row.get("alternatives"))

        if not brand_name:
            continue

        brands_yaml_data[brand_name] = {
            NAME: brand_name,
            STATUS: "avoid",
            DESCRIPTION: proof,
            REASONS: [reason],
            COUNTRIES: ["global"],
            CATEGORIES: categories,
        }
        if image_url:
            brands_yaml_data[brand_name][LOGO_URL] = image_url
        if alternatives_txt:
            brands_yaml_data[brand_name][ALTERNATIVES_TEXT] = alternatives_txt
        if parent_name:
            brands_yaml_data[brand_name][STAKEHOLDERS] = [
                {ID: name_to_id(parent_name), TYPE: "owner"}
            ]

    return brands_yaml_data, companies_yaml_data


# Write yaml data to the given path, if there is no file already there.
# Returns True if a file was written, false otherwise.
def write_yaml_if_not_exists(file_path, data, overwrite):
    if file_path not in existing_files or overwrite:
        with open(file_path, "w", encoding="utf-8") as yaml_file:
            print(f"writing: {file_path}")
            yaml.dump(data, yaml_file, default_flow_style=False, sort_keys=False)
            return True
    else:
        return False


def get_filename(name):
    return "".join(x for x in unidecode(name.lower()) if x.isalnum()) + ".yaml"


def import_data(file_name, input_type, overwrite):
    with open(file_name, encoding="utf-8") as fh:
        raw_data = json.load(fh)
        brands = {}
        companies = {}

        if input_type == "bds":
            boycott_brands, companies = create_data_models(raw_data)
            alt_brands = create_alternatives_data_models(raw_data)
            brands = boycott_brands | alt_brands

        if input_type == "witness":
            brands, companies = create_data_models_from_witness_json(raw_data)

        files_written = 0

        for brand, details in brands.items():
            file_path = os.path.join(brands_path, get_filename(brand))
            if write_yaml_if_not_exists(file_path, details, overwrite):
                files_written += 1

        for company, details in companies.items():
            file_path = os.path.join(companies_path, get_filename(company))
            if write_yaml_if_not_exists(file_path, details, overwrite):
                files_written += 1

        file_or_files = "files" if files_written > 1 else "file"
        print(f"Wrote {files_written} {file_or_files}.")


if __name__ == "__main__":
    args = sys.argv[1:]

    if len(args) < 2 or args[1] not in ("witness", "bds", "disoccupied"):
        print(
            "Usage: python3 import_new_schema.py <path to JSON file to import> <type witness|disoccupied|bds> <overwrite true, defaults to false>"
        )
        sys.exit(1)

    input_file = args[0]
    input_type = args[1]
    overwrite = len(args) > 2

    import_data(input_file, input_type, overwrite)
