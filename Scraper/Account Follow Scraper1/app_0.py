import requests
import json
import time
from dok_id import get_data
from cursor import cursor
from id import get_collection_token

try:
    ha = get_data("https://www.facebook.com/Cristiano/followers")
    id_token = get_collection_token()
    cursor_val = cursor()
except Exception as e:
    print(f"Error fetching initial data (dok_id, cursor, id): {e}")
    exit()


req = 15
num = 1
count = 100 # Increased batch size for faster scraping

headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://www.facebook.com',
    'priority': 'u=1, i',
    'referer': 'https://www.facebook.com/Cristiano/followers',
    'sec-ch-prefers-color-scheme': 'light',
    'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
    'sec-ch-ua-full-version-list': '"Chromium";v="142.0.7444.60", "Google Chrome";v="142.0.7444.60", "Not_A Brand";v="99.0.0.0"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-ua-platform-version': '"10.0.0"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
    'x-asbd-id': '359341',
    'x-fb-friendly-name': 'ProfileCometAppCollectionListRendererPaginationQuery',
    'x-fb-lsd': 'AdEe1a8v4Lo',
    'cookie': 'PASTE_YOUR_COOKIE_HERE', # TODO: Replace with your actual Facebook cookies
}

request_payload = {
    '__a': num,
    '__req': 'c',
    '__comet_req': req,
    # Using the fetched values in the 'variables' JSON string
    'variables': f'{{"count":{count},"cursor":"{cursor_val}","scale":1,"search":null,"id":"{id_token}","__relay_internal__pv__FBProfile_enable_perf_improv_gkrelayprovider":false}}',
    'doc_id': ha
}

print(f"Doc ID (ha): {ha}")
print(f"Collection ID (id): {id_token}")
print(f"Cursor: {cursor_val}")

all_followers = []

proxies = {
    "http": "http://tanvirdipt0:Hyc7XRGgZNh2nZznOt16@core-residential.evomi.com:1000",
    "https": "http://tanvirdipt0:Hyc7XRGgZNh2nZznOt16@core-residential.evomi.com:1000"
}

# Create a session for connection pooling
session = requests.Session()
session.headers.update(headers)
session.proxies.update(proxies)

try:
    response = session.post('https://www.facebook.com/api/graphql/', data=request_payload)
    response.raise_for_status() # Check for HTTP errors
except requests.exceptions.RequestException as e:
    print(f"Error during API request: {e}")
    exit()



try:
    response_json = json.loads(response.text)
except json.JSONDecodeError:
    print("❌ Error: API response is not valid JSON. Check your cookies/authentication.")
    response_json = {}



def find_value(obj, target_path):
    """Recursive ফাংশন: nested JSON থেকে নির্দিষ্ট path খুঁজে বের করে"""
    if not target_path:
        return None

    key = target_path[0]

    # dict হলে
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

def extract_followers(node_data):
    extracted = []
    if not node_data or "pageItems" not in node_data:
        return extracted
        
    edges = node_data["pageItems"]["edges"]
    for edge in edges:
        try:
            node = edge["node"]

            title_text = node["title"]["text"] if "title" in node else None
            image_data = node.get("image")
            url_value = node.get("url")
            facebook_id = node.get("id")
            node_id = node.get("id")

            output_data = {
                "username": title_text,
                "image": image_data,
                "url": url_value,
                "facebookId": facebook_id,
                "id": node_id
            }
            extracted.append(output_data)
            print(f"✅ Found follower: {title_text}")

        except Exception as e:
            print("⚠️ Error reading follower:", e)
    return extracted


path = [
    "data", 
    "node"
]

node_data = find_value(response_json, path) 

# Extract initial followers
if node_data:
    initial_followers = extract_followers(node_data)
    all_followers.extend(initial_followers)
else:
    print("⚠️ Path element 'data.node' not found in the response JSON.")


import json


path = [
    "data",
    "node",
    "pageItems",
    "page_info",
    "end_cursor"
]

end_cursor = find_value(response_json, path)

if end_cursor:
    print("✅ End Cursor:", end_cursor)
else:
    print("⚠️ end_cursor not found.")


def send_request(next_cursor):

    request_payload['variables'] = (
    f'{{"count":{count},"cursor":"{next_cursor}","scale":1,"search":null,"id":"{id_token}",'
    f'"__relay_internal__pv__FBProfile_enable_perf_improv_gkrelayprovider":false}}'
)

    max_retries = 3
    for attempt in range(max_retries):
        try:
            # Use the session to send the request
            resp = session.post('https://www.facebook.com/api/graphql/', data=request_payload)
            resp.raise_for_status()
            return json.loads(resp.text)
        except requests.exceptions.HTTPError as e:
            if resp.status_code == 500:
                print(f"⚠️ 500 Server Error on attempt {attempt + 1}/{max_retries}. Retrying...")
                time.sleep(2 ** attempt) # Exponential backoff: 1s, 2s, 4s
            else:
                print(f"❌ HTTP Error: {e}")
                return None
        except Exception as e:
            print(f"❌ Request failed: {e}")
            return None
    
    print("❌ Max retries exceeded for 500 error.")
    return None

current_cursor = end_cursor

while current_cursor and len(all_followers) < 1000:
    print(f"🔄 Fetching next page with cursor: {current_cursor} (Total collected: {len(all_followers)})")

    # Add delay to avoid rate limiting
    time.sleep(2) 

    response_json = send_request(current_cursor)
    if not response_json:
        break

    # আবার followers extract (same logic)
    node_data = find_value(response_json, ["data", "node"])
    if not node_data or "pageItems" not in node_data:
        print("❌ No more followers or node_data missing.")
        break

    # Extract followers from pagination response
    new_followers = extract_followers(node_data)
    all_followers.extend(new_followers)


    # নতুন cursor বের করা
    current_cursor = find_value(
        response_json,
        ["data", "node", "pageItems", "page_info", "end_cursor"]
    )

    if current_cursor:
        print("➡️ Next Cursor:", current_cursor)
    else:
        print("🚫 No more cursor. Pagination finished.")
        break

# Limit to exactly 100 followers
all_followers = all_followers[:1000]

# Save all data to output.json
try:
    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(all_followers, f, indent=4, ensure_ascii=False)
    print(f"\n✅ Successfully saved {len(all_followers)} followers to output.json")
except Exception as e:
    print(f"❌ Error saving to output.json: {e}")





