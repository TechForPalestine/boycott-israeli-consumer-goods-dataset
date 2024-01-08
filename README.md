[![Ceasefire Now](https://badge.techforpalestine.org/default)](https://techforpalestine.org/learn-more)

# boycott-israeli-consumer-goods-dataset

Collating all consumer boycott and alternatives data into a single, golden-source, version-controlled repository. This can be consumed by software products and services.

If you're a company looking for SaaS products to avoid, see [TechForPalestine/boycott-israeli-tech-companies-dataset](https://github.com/TechForPalestine/boycott-israeli-tech-companies-dataset).


Sources:

- https://pastebin.com/raw/ks9GRE4L

## Data
All data is inputted & stored as YAML files in the `data/` directory.
Output formats, such as CSV and JSON are in the `generated/` directory.

Schemas for the YAML data can be found in the `schemas` directory, along with descriptions for each field.
These schemas are in [JSON Schema](https://json-schema.org/) format, but represented in YAML for simplicity.
The `validate_yaml.py` script validates all brands and companies using the schemas.

## Useful Resources & Links

* [Who Profits Research Center](https://www.whoprofits.org/)
* [BDS Movement guide to targeted consumer boycotts](https://bdsmovement.net/Act-Now-Against-These-Companies-Profiting-From-Genocide)
* [AFSC's list of companies profiting from Israel's 2023 attack on Gaza](https://afsc.org/companies-behind-2023-attack-gaza)


## TODO

- high level location to country codes? https://www.iban.com/country-codes
- update empty parents (manual?)
- review the data + sanitize
- validation script - read everything in data/companies, check for dupes, check required + optional fields etc.
- script to read in data/companies in and generate full data in csv, json, yaml format + add timestamps. 




