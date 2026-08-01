import os
import json
import urllib.request
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

# 1. Fetch official Kasm workspaces.json
req = urllib.request.Request("https://registry.kasmweb.com/1.0/workspaces.json", headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as response:
        kasm_data = json.loads(response.read().decode())
        kasm_workspaces = kasm_data.get('workspaces', [])
except Exception as e:
    print("Error fetching kasm registry:", e)
    kasm_workspaces = []

# create mapping from image_name to kasm's image_url
kasm_image_map = {}
for w in kasm_workspaces:
    # w['image_name'] is like 'kasmweb/chrome'
    if 'image_name' in w and 'image_url' in w:
        name_part = w['image_name'].split('/')[-1]
        kasm_image_map[name_part] = w['image_url']

# Create icons directory
if not os.path.exists('icons'):
    os.makedirs('icons')

# 2. Update our droplets.json
with open('droplets.json', 'r') as f:
    droplets = json.load(f)

for droplet in droplets:
    image_name = droplet['id']
    
    icon_filename = f"{image_name}.png"
    # Try to find a match in Kasm's registry
    kasm_url = None
    
    # Check exact match
    if image_name in kasm_image_map:
        kasm_url = kasm_image_map[image_name]
    # Check fuzzy match
    else:
        for k_name, url in kasm_image_map.items():
            if k_name in image_name or image_name in k_name:
                kasm_url = url
                break
                
    if kasm_url:
        print(f"Downloading icon for {image_name} from {kasm_url}")
        if kasm_url.endswith('.svg'):
            icon_filename = f"{image_name}.svg"
            
        try:
            icon_req = urllib.request.Request(kasm_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(icon_req) as response, open(f"icons/{icon_filename}", 'wb') as out_file:
                out_file.write(response.read())
        except Exception as e:
            print(f"Failed to download {kasm_url}: {e}")
            
    # Set the image path to github raw url
    droplet['image_path'] = f"https://raw.githubusercontent.com/vigno04/droplet-images/main/icons/{icon_filename}"

with open('droplets.json', 'w') as f:
    json.dump(droplets, f, indent=4)
print("Done!")
