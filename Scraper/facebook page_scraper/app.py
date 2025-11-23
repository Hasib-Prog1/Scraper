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
    'accept-language': 'en-US,en;q=0.9',
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
    'viewport-width': '1009',
    # 'cookie': 'datr=bb8VaVGvEUsnJ5guvkzmuXZ_; sb=bb8VaXaOazXamx-NrxRlj_ev; ps_l=1; ps_n=1; wd=1009x641',
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
    
    scripts = selector.css('script[type="application/json"][data-content-len]::text').getall()
    return scripts  


all_profiles = []


followers_list = []
followings_list = []

base_urls = [
        "https://www.facebook.com/Cristiano",
]


all_data = []

 
for base in base_urls:
    print(f"\n🔍 Processing main profile: {base}")

    # followers আর following এর URL বানাও
    urls_to_check = [
        f"{base}/followers",
        f"{base}/following"
    ]

    for url in urls_to_check:
        print(f"\n➡️ Fetching data from: {url}")
        script = get_data(url)

        # এখানে নিচের অংশে তোমার parsing (filtered, find_value ইত্যাদি) code থাকবে
        # ঠিক যেভাবে তুমি আগে করেছো
        print(f"\n🔍 Processing: {url}")
        



        def contains_best_description(obj):
            """Recursively check if 'best_description' exists anywhere inside a JSON object"""
            if isinstance(obj, dict):
                if "profile_actions" in obj:
                    return True
                return any(contains_best_description(v) for v in obj.values())
            elif isinstance(obj, list):
                return any(contains_best_description(i) for i in obj)
            return False

        # Step 2: Each item might be a string, so convert each to proper JSON if needed
        parsed_data = []
        for item in script:
            if isinstance(item, str):
                try:
                    parsed_data.append(json.loads(item))
                except json.JSONDecodeError:
                    continue
            elif isinstance(item, dict):
                parsed_data.append(item)



        import json
        filtered = [item for item in parsed_data if contains_best_description(item)]
        data = filtered 


        
        # JSON ফাইল লোড
        data = filtered


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
                # অন্য value গুলোর মধ্যে খুঁজে দেখো
                for v in obj.values():
                    result = find_value(v, target_path)
                    if result is not None:
                        return result

            # list হলে
            elif isinstance(obj, list):
                for item in obj:
                    result = find_value(item, target_path)
                    if result is not None:
                        return result

            return None


        # ===========================
        # 🔹 Extract all_collections.nodes[0].style_renderer.collection.pageItems.edges[0].node.title.text
        # ===========================
        path = [
            "result",
            "data",
            "node",
            "all_collections",
            "nodes"
        ]

        nodes = find_value(data, path)

        if isinstance(nodes, list) and len(nodes) > 0:
            try:
                title_text = (
                    nodes[0]["style_renderer"]["collection"]["pageItems"]
                    ["edges"][0]["node"]["title"]["text"]
                )
                print("✅ username:", title_text)
            except (KeyError, IndexError, TypeError):
                print("⚠️ title.text key not found.")


        if isinstance(nodes, list) and len(nodes) > 0:
            try:
                image_data = (
                    nodes[0]["style_renderer"]["collection"]["pageItems"]
                    ["edges"][0]["node"]["image"]
                )
                print(" Image :", image_data)
            except (KeyError, IndexError, TypeError):
                print("⚠️ image key not found inside node.")
        else:
            print("⚠️ nodes[0] not found.")


        if isinstance(nodes, list) and len(nodes) > 0:
            try:
                url_value = (
                    nodes[0]["style_renderer"]["collection"]["pageItems"]
                    ["edges"][0]["node"]["url"]
                )
                print("✅ Node URL:", url_value)
            except (KeyError, IndexError, TypeError):
                print("⚠️ url key not found inside node.")
        else:
            print("⚠️ nodes[0] not found.")

        path = [
            "result",
            "data",
            "node",
            "all_collections",
            "nodes"
        ]

        nodes = find_value(data, path)

        if isinstance(nodes, list) and len(nodes) > 0:
            try:
                node_id = (
                    nodes[0]["style_renderer"]["collection"]["pageItems"]
                    ["edges"][0]["node"]["node"]["id"]
                )
                print("ID:", node_id)
            except (KeyError, IndexError, TypeError):
                print("⚠️ 'node.node.id' key not found inside JSON.")
        else:
            print("⚠️ nodes[0] not found.")

        if isinstance(nodes, list) and len(nodes) > 0:
            try:
                node_id = (
                    nodes[0]["style_renderer"]["collection"]["pageItems"]
                    ["edges"][0]["node"]["id"]
                )
                print("facebookId:", node_id)
            except (KeyError, IndexError, TypeError):
                print(" key not found inside JSON.")
        else:
            print(" not found.")   

        if isinstance(nodes, list) and len(nodes) > 0:
          edges = nodes[0]["style_renderer"]["collection"]["pageItems"]["edges"]

        for edge in edges:
            try:
                node = edge["node"]
                title_text = node["title"]["text"] if "title" in node else None
                image_data = node["image"] if "image" in node else None
                url_value = node["url"] if "url" in node else None
                facebook_id = node.get("id") or node.get("node", {}).get("id")
                

                output_data = {
                    "input_url": url,
                    "username": title_text,
                    "image": image_data,
                    "url": url_value,
                    "facebookId": facebook_id,
                    "id" : node_id
                }
                print(f"✅ Found follower: {title_text}")

            except Exception as e:
                print("⚠️ Error reading follower:", e)
        
            all_data.append(output_data)
            if url.endswith("/followers"):
                followers_list.append(output_data)
            elif url.endswith("/following"):
                followings_list.append(output_data)


final_output = [
    {"followers": followers_list},
    {"followings": followings_list}
]

with open("output.json", "w", encoding="utf-8") as f:
    json.dump(final_output, f, ensure_ascii=False, indent=4)

print("\n💾 Saved successfully as output.json ✅")

