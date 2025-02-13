import json

with open("private.json","r") as jfile:
    data = json.loads(jfile.read())

print(data['nmaprun'])
    
