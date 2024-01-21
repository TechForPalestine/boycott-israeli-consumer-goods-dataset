import sys
import json
import csv
import yaml
import re
from collections import defaultdict

import pdb

"""
  {
    "id": 330,
    "attributes": {
      "name": "Aspirin",
      "imageUrl": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ad/Logo_Aspirin.svg/640px-Logo_Aspirin.svg.png",
      "proof": "Owned by **Bayer**.\n\nThere is a partnership between **Bayer** and the Israeli Innovation Authority. The Israel Innovation Authority (IIA) is the support arm of the Israeli government, charged with fostering the development of industrial research and development in the State of Israel.",
      "priority": false,
      "createdAt": "2023-11-10T23:36:27.370Z",
      "updatedAt": "2023-11-14T17:11:46.770Z",
      "publishedAt": "2023-11-10T23:45:51.158Z",
      "proofUrl": "https://www.bayer.com/en/il/climate-tech-program",
      "tags": null,
      "filename": "aspirin.webp",
      "alternative": {
        "data": null
      }
    }
  },
"""

UID = "uid"
NAME = "name"
IMAGE_URL = "image_url"
CATEGORIES = "categories"
PARENTS = "parents"
WEBSITE = "website"
LOCATION = "location"
GLOBAL = "global"
DETAILS = "details"
REASON = "reason"
SOURCE = "source_url"
LEVEL = "level"
DIRECT = "direct"
ALTERNATIVE = "alternative"
SHAREHOLDER = "shareholder"
NEUTRAL_MULTI = "neutral_multi_national"
NEUTRAL_SME = "neutral_small_medium_enterprise"
MINORITY_OWNER = "minority_owner"
PALESTINE_OWNER_SUPPORTER = "palestine_owner_supporter"


def parent_from_details(details):
    if details:
        if "owned by **" in details.lower():
            parse_for_parent = details.split("**")
            if len(parse_for_parent) > 0:
                return parse_for_parent[1]
    return ""


# Custom representer for multiline strings
def literal_presenter(dumper, data):
    if "\n" in data or len(data) > 30:
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    if " " in data:
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style='"')
    if not data or data == "":
        return dumper.represent_scalar("tag:yaml.org,2002:null", "")
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


def none_representer(dumper, data):
    return dumper.represent_scalar("tag:yaml.org,2002:null", "")


# Apply the custom representer
yaml.add_representer(str, literal_presenter)
yaml.add_representer(type(None), none_representer)


def create_data_model(data, default_level=ALTERNATIVE):
    yaml_data = {}
    for row in data:
        # alternative = row.get('attributes')['alternative']['data']
        # if alternative:
        #     brand_name = alternative.get('attributes').get('name')
        #     reason = alternative.get('attributes').get('proof')
        #     parent_name = parent_from_details(reason)
        #     source_url = alternative.get('attributes').get('proofUrl')
        #     image_url = alternative.get('attributes').get('imageUrl')
        #     website = alternative.get('attributes').get('Website', '')
        #     level = alternative.get('attributes').get('Level', default_level)
        #     country = alternative.get('attributes').get('Market', None)
        #     categories_raw = alternative.get('attributes').get('tags')
        #     categories = categories.split(",") if categories_raw else [] #split_categories(categories_raw)

        brand_name = row.get("attributes").get("name")
        reason = row.get("attributes").get("proof")
        parent_name = parent_from_details(reason)
        source_url = row.get("attributes").get("proofUrl")
        image_url = row.get("attributes").get("imageUrl")
        website = row.get("attributes").get("Website", "")
        level = row.get("attributes").get("Level", default_level)
        country = row.get("attributes").get("Market", None)
        categories_raw = row.get("attributes").get("tags")
        categories = (
            categories.split(",") if categories_raw else []
        )  # split_categories(categories_raw)
        location = GLOBAL if not country or country == "" else country

        if not brand_name:
            continue

        if brand_name in data:
            new_parent = {
                NAME: parent_name,
                LOCATION: location,
                LEVEL: level,
                DETAILS: {REASON: reason, SOURCE: source_url},
            }
            yaml_data[brand_name][PARENTS].append(new_parent)
        else:
            yaml_data[brand_name] = {
                NAME: brand_name,
                WEBSITE: website,
                IMAGE_URL: image_url,
                CATEGORIES: categories,
                PARENTS: [
                    {
                        NAME: parent_name,
                        LOCATION: location,
                        LEVEL: level,
                        DETAILS: {REASON: reason, SOURCE: source_url},
                    }
                ],
            }
    return yaml_data


def write_yaml(data, file_name):
    data_list = {"brands": list(data.values())}
    with open(file_name, "w", encoding="utf-8") as yaml_file:
        yaml.dump(data_list, yaml_file, default_flow_style=False, sort_keys=False)


def json_to_csv(json_file, output):
    with open(json_file, encoding="utf-8") as fh:
        data = json.load(fh)
        yaml_data = create_data_model(data)
        write_yaml(yaml_data, output)

    pdb.set_trace()


if __name__ == "__main__":
    args = sys.argv[1:]

    file_to_parse = args[0]
    output_yaml = args[1]

    json_to_csv(file_to_parse, output_yaml)
