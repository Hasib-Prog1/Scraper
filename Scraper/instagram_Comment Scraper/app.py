from parsel import Selector
import requests
import json
import time
import json
import json
from datetime import datetime
def get_data(url):
    
    headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9,bn;q=0.8',
    'cache-control': 'max-age=0',
    'dpr': '1',
    'priority': 'u=0, i',
    'sec-ch-prefers-color-scheme': 'light',
    'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
    'sec-ch-ua-full-version-list': '"Chromium";v="142.0.7444.60", "Google Chrome";v="142.0.7444.60", "Not_A Brand";v="99.0.0.0"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-ua-platform-version': '"10.0.0"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
    'viewport-width': '1366',
   }

    max_try = 3
    err_list = None
    response = None

    for i in range(max_try):
        try:
            resp = requests.get(url, headers=headers, timeout=30)
            if resp.status_code == 200:
                response = resp
                break
            else:
                err_list = Exception(f"Non-200 status code: {resp.status_code}")
        except Exception as e:
            err_list = e
            time.sleep(1)

    if response is None:
        raise err_list if err_list else Exception("Request failed")

    selector = Selector(text=response.text)


    scripts =selector.css('script[type="application/json"][data-content-len]::text').getall()
    return scripts

scripts = data =  get_data("https://www.instagram.com/instagram/reel/DQuQGP_AO70/")



def contains_best_description(obj):
    """Recursively check if 'best_description' exists anywhere inside a JSON object"""
    if isinstance(obj, dict):
        if "child_comment_count" in obj:
            return True
        return any(contains_best_description(v) for v in obj.values())
    elif isinstance(obj, list):
        return any(contains_best_description(i) for i in obj)
    return False

data = scripts

# Step 2: Each item might be a string, so convert each to proper JSON if needed
parsed_data = []
for item in data:
    if isinstance(item, str):
        try:
            parsed_data.append(json.loads(item))
        except json.JSONDecodeError:
            continue
    elif isinstance(item, dict):
        parsed_data.append(item)
filtered = [item for item in parsed_data if contains_best_description(item)]

data = filtered


data = filtered



def find_value(obj, target_path):
    if not target_path:
        return None

    key = target_path[0]

    if isinstance(obj, dict):
        if key in obj:
            if len(target_path) == 1:
                return obj[key]
            return find_value(obj[key], target_path[1:])
        for v in obj.values():
            result = find_value(v, target_path)
            if result is not None:
                return result

    elif isinstance(obj, list):
        for item in obj:
            result = find_value(item, target_path)
            if result is not None:
                return result

    return None



path = [
    "result",
    "data",
    "xdt_api__v1__media__media_id__comments__connection",
    "edges"
]

edges = find_value(data, path)

if isinstance(edges, list) and edges:
    pk = edges[0].get("node", {}).get("pk")
    print("✅ First Comment id:", pk)
else:
    print("⚠️ No PK found.")



path = [
    "result",
    "data",
    "xdt_api__v1__media__media_id__comments__connection",
    "edges"
]

edges = find_value(data, path)

if isinstance(edges, list) and edges:
    username = edges[0].get("node", {}).get("user", {}).get("username")
    print("✅ First Comment Username:", username)
else:
    print("⚠️ No Username found.")



path = [
    "result",
    "data",
    "xdt_api__v1__media__media_id__comments__connection",
    "edges"
]

edges = find_value(data, path)

if isinstance(edges, list) and edges:
    profile_pic = edges[0].get("node", {}).get("user", {}).get("profile_pic_url")
    print("✅ First Comment User Profile Pic URL:", profile_pic)
else:
    print("⚠️ No Profile Pic URL found.")



path = [
    "result",
    "data",
    "xdt_api__v1__media__media_id__comments__connection",
    "edges"
]

edges = find_value(data, path)

if isinstance(edges, list) and edges:
    text = edges[0].get("node", {}).get("text")
    print("✅ First Comment Text:", text)
else:
    print("⚠️ No comment text found.")



import json
from datetime import datetime

# Load JSON
data = filtered


# Same flexible finder
def find_value(obj, target_path):
    if not target_path:
        return None

    key = target_path[0]

    if isinstance(obj, dict):
        if key in obj:
            if len(target_path) == 1:
                return obj[key]
            return find_value(obj[key], target_path[1:])
        for v in obj.values():
            result = find_value(v, target_path)
            if result is not None:
                return result

    elif isinstance(obj, list):
        for item in obj:
            result = find_value(item, target_path)
            if result is not None:
                return result

    return None


# Target JSON path
path = [
    "result",
    "data",
    "xdt_api__v1__media__media_id__comments__connection",
    "edges"
]

edges = find_value(data, path)

if isinstance(edges, list) and edges:


    # Convert UNIX to readable time (NO BD CONVERSION)
    created_at = edges[0].get("node", {}).get("created_at")
    if created_at:
        readable_time = datetime.fromtimestamp(created_at)
        print("⏱️ Converted Time:", readable_time)
    else:
        print("⚠️ created_at not found")





output = []

if isinstance(edges, list) and edges:
    for item in edges:
        node = item.get("node", {})

        comment_id = node.get("pk")
        username = node.get("user", {}).get("username")
        profile_pic = node.get("user", {}).get("profile_pic_url")
        text = node.get("text")
        created_at = node.get("created_at")

        # Convert UNIX time (optional)
        try:
            readable_time = datetime.fromtimestamp(created_at).strftime("%Y-%m-%d %H:%M:%S")
        except:
            readable_time = None

        output.append({
            "comment_id": comment_id,
            "username": username,
            "profile_pic": profile_pic,
            "comment_text": text,
            "created_at": readable_time
        })


with open("output.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=4)

print(f"✅ Total {len(output)} Comments Saved to output.json")

