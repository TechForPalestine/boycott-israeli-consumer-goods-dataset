
import yaml
import csv
import json

def read_yaml(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    return data

def export_to_csv(data, csv_file, delimiter=','):
    if isinstance(data, list):
        header = data[0].keys() if data else []
        rows = []
        for item in data:
            item["parent name"]=item["parents"][0]["name"]
            item["parent location"]=item["parents"][0]["location"]
            item["parent level"]=item["parents"][0]["level"]
            item["reason"]=item["parents"][0]["details"]["reason"]
            item["source_url"]=item["parents"][0]["details"]["source_url"]
            del item['parents']
            row = list(item.values())
            rows.append(row)



    with open(csv_file, 'w', newline='', encoding='utf-8') as csv_output:
        csv_writer = csv.writer(csv_output, delimiter=delimiter)
        csv_writer.writerow(header)
        csv_writer.writerows(rows)

def export_to_json(data, json_file):
    with open(json_file, 'w') as file:
        json.dump(data, file, indent=2)

if __name__ == "__main__":
    yaml_all_boycott = 'output/yaml/all_boycott.yaml'
    yaml_all = 'output/yaml/all.yaml'
    yaml_alternatives = 'output/yaml/alternatives.yaml'

    csv_all_boycott = 'output/csv/all_boycott.csv'
    csv_all = 'output/csv/all.csv'
    csv_alternatives = 'output/csv/alternatives.csv'

    json_all_boycott = 'output/json/all_boycott.json'
    json_all = 'output/json/all.json'
    json_alternatives = 'output/json/alternatives.json'

    # Read YAML data
    all_boycott_data = read_yaml(yaml_all_boycott)
    all_data = read_yaml(yaml_all)
    altenatives_data = read_yaml(yaml_alternatives)

    # Export to JSON
    export_to_json(all_boycott_data, json_all_boycott)
    print(f'Data exported to {json_all_boycott}')

    export_to_json(all_data, json_all)
    print(f'Data exported to {json_all}')

    export_to_json(altenatives_data, json_alternatives)
    print(f'Data exported to {json_alternatives}')
    # Export to CSV
    export_to_csv(all_boycott_data["brands"], csv_all_boycott, delimiter=';')
    print(f'Data exported to {csv_all_boycott}')

    export_to_csv(all_data["brands"], csv_all, delimiter=';')
    print(f'Data exported to {csv_all}')

    export_to_csv(altenatives_data["brands"], csv_alternatives, delimiter=';')
    print(f'Data exported to {csv_alternatives}')





