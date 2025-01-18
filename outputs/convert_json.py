import xmltodict
import json

# Read the XML file
with open('output.xml', 'r', encoding='utf-8') as xml_file:
    xml_data = xml_file.read()

# Convert XML to a Python dictionary
xml_dict = xmltodict.parse(xml_data)

# Convert dictionary to JSON
json_data = json.dumps(xml_dict, indent=4)

# Optionally, save the JSON to a file
with open('output.json', 'w', encoding='utf-8') as json_file:
    json_file.write(json_data)

# Print the JSON data
print(json_data)
