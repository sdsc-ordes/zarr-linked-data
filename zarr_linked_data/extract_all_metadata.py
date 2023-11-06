import zarr
import json
import os
from rdflib import Graph

# Define the input JSON file path and the output file path
input_json_file = "data/test_store.zarr/.all_metadata"
output_zattrs_file = 'output_zattrs.json'

# Function to recursively extract .zattrs objects
def extract_zattrs(json_data, zattrs_list):
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            if key.endswith(".zattrs"):
                zattrs_list.append(value)
            if isinstance(value, (dict, list)):
                extract_zattrs(value, zattrs_list)

# Load the input JSON file
try:
    with open(input_json_file, 'r') as f:
        json_data = json.load(f)
except FileNotFoundError:
    print(f"Input JSON file '{input_json_file}' not found.")
    exit(1)
except json.JSONDecodeError:
    print(f"Error parsing JSON from '{input_json_file}'. Make sure it's a valid JSON file.")
    exit(1)

# Initialize a list to store .zattrs values
zattrs_list = []

# Start the extraction process
extract_zattrs(json_data, zattrs_list)

# Write the extracted .zattrs values to the output file
with open(output_zattrs_file, 'w') as output_f:
    json.dump(zattrs_list, output_f, indent=2)

g = Graph()
g.parse('output_zattrs.json', format='json-ld')

# Serialize the RDF graph to Turtle (TTL) format
output_ttl_file = 'output_zattrs.ttl'
with open(output_ttl_file, 'w') as ttl_file:
    ttl_file.write(g.serialize(format='turtle'))