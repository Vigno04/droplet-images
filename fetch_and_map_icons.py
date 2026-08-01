import os
import json
import urllib.request
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

if not os.path.exists('icons'):
    os.makedirs('icons')

with open('droplets.json', 'r') as f:
    droplets = json.load(f)

for droplet in droplets:
    image_name = droplet['id']
    
    icon_name = image_name
    if 'ubuntu' in image_name: icon_name = 'ubuntu'
    elif 'libre-office' in image_name: icon_name = 'libreoffice'
    elif 'tor-browser' in image_name: icon_name = 'tor'
    elif 'super-tux-kart' in image_name: icon_name = 'supertuxkart'
    elif 'vs-code' in image_name: icon_name = 'vscode'
    elif 'only-office' in image_name: icon_name = 'onlyoffice'
    elif 'tor' in image_name: icon_name = 'tor'

    # Try downloading from selfhst
    url = f"https://cdn.jsdelivr.net/gh/selfhst/icons/svg/{icon_name}.svg"
    icon_filename = f"{image_name}.svg"
    local_path = f"icons/{icon_filename}"
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            with open(local_path, 'wb') as out_file:
                out_file.write(response.read())
        print(f"Downloaded {icon_name}.svg from selfhst")
    except Exception as e:
        print(f"Failed to download {icon_name}.svg: {e}")
        # Even if it fails, we point it to the local github raw URL so the user can add it later
        
    droplet['image_path'] = f"https://raw.githubusercontent.com/vigno04/droplet-images/main/icons/{icon_filename}"

with open('droplets.json', 'w') as f:
    json.dump(droplets, f, indent=4)
print("Done!")
