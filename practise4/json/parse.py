import json

# Load the JSON data from the file
with open('sample-data.json', 'r') as file:
    data = json.load(file)

# Print the header
print("Interface Status")
print("=" * 80)
print(f"{'DN':<50} {'Description':<20} {'Speed':<10} {'MTU'}")
print("-" * 50, "-" * 20, "-" * 10, "-" * 6)

# Iterate through the interfaces and print each row
for item in data['imdata']:
    attributes = item['l1PhysIf']['attributes']
    dn = attributes['dn']
    descr = attributes['descr']
    speed = attributes['speed']
    mtu = attributes['mtu']
    print(f"{dn:<50} {descr:<20} {speed:<10} {mtu}")