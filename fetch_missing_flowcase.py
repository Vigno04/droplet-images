import os
import json
import urllib.request
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

missing = [
    'chrome', 'doom', 'edge', 'hunchly', 'insomnia', 'maltego', 'minetest',
    'nessus', 'parsec', 'pinta', 'postman', 'retroarch', 'spiderfoot',
    'sublime-text', 'supertuxkart', 'terminal', 'unityhub', 'vivaldi',
    'vlc', 'vscode', 'wine'
]

# Let's try to see if registry.flowcase.org has a droplets.json first
try:
    req = urllib.request.Request("https://registry.flowcase.org/droplets.json", headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        droplets_data = json.loads(response.read().decode())
except Exception as e:
    print(f"Failed to fetch droplets.json from registry.flowcase.org: {e}")
    droplets_data = []

flowcase_images = {}
for d in droplets_data:
    if 'id' in d and 'image_path' in d:
        flowcase_images[d['id']] = d['image_path']

for m in missing:
    url = flowcase_images.get(m)
    if not url:
        # Guess the URL
        url = f"https://registry.flowcase.org/images/{m}.png"
        
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = response.read()
            ext = 'svg' if '.svg' in url else 'png'
            with open(f"icons/{m}.{ext}", 'wb') as f:
                f.write(data)
            print(f"Downloaded {m}.{ext} from {url}")
            
            # Now we need to update our local droplets.json to reflect the extension
            with open('droplets.json', 'r') as json_f:
                local_droplets = json.load(json_f)
            for ld in local_droplets:
                if ld['id'] == m:
                    ld['image_path'] = f"https://raw.githubusercontent.com/vigno04/droplet-images/main/icons/{m}.{ext}"
            with open('droplets.json', 'w') as json_f:
                json.dump(local_droplets, json_f, indent=4)
                
    except Exception as e:
        print(f"Failed to fetch {m} from {url}: {e}")

print("Done trying to fetch from flowcase.org")
