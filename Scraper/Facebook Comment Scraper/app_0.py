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
        'priority': 'u=0, i',
        'sec-ch-ua': '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
        'sec-ch-ua-full-version-list': '"Google Chrome";v="141.0.7390.108", "Not?A_Brand";v="8.0.0.0", "Chromium";v="141.0.7390.108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"10.0.0"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
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


scripts =  data = get_data("https://www.facebook.com/humansofnewyork/posts/pfbid0BbKbkisExKGSKuhee9a7i86RwRuMKFC8NSkKStB7CsM3uXJuAAfZLrkcJMXxhH4Yl")



def contains_best_description(obj):
    """Recursively check if 'best_description' exists anywhere inside a JSON object"""
    if isinstance(obj, dict):
        if "comment_composer_placeholder" in obj:
            return True
        return any(contains_best_description(v) for v in obj.values())
    elif isinstance(obj, list):
        return any(contains_best_description(i) for i in obj)
    return False

data = scripts

def get_urls(urls):
    all_data = []
    

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
    "comment_list_renderer",
    "feedback",
    "comment_rendering_instance_for_feed_location",
    "comments",
    "edges"
]

edges = find_value(data, path)

if isinstance(edges, list) and len(edges) > 0:
    author_name = edges[0].get("node", {}).get("author", {}).get("name")
    print("✅ First Comment Author Name:", author_name)
else:
    print("⚠️ No comment author found.")




path = [
    "comment_list_renderer",
    "feedback",
    "comment_rendering_instance_for_feed_location",
    "comments",
    "edges"
]

edges = find_value(data, path)

if isinstance(edges, list) and len(edges) > 0:
    reactors_count = edges[0].get("node", {}).get("feedback", {}).get("reactors", {}).get("count_reduced")
    print("✅ First Comment Reactors (Likes) Count:", reactors_count)
else:
    print("⚠️ No comment reactors count found.")


path = [
    "comment_list_renderer",
    "feedback",
    "comment_rendering_instance_for_feed_location",
    "comments",
    "edges"
]

edges = find_value(data, path)

if isinstance(edges, list) and len(edges) > 0:
    first_comment_text = edges[0].get("node", {}).get("body", {}).get("text")
    print("✅ First Comment Text:", first_comment_text)
else:
    print("⚠️ No comment text found.")

path = [
    "comment_list_renderer",
    "feedback",
    "comment_rendering_instance_for_feed_location",
    "comments",
    "edges"
]

edges = find_value(data, path)

if isinstance(edges, list) and len(edges) > 0:
    replies_count = edges[0].get("node", {}).get("feedback", {}).get("replies_fields", {}).get("total_count")
    print(" First Comment Replies Count:", replies_count)
else:
    print(" No replies count found.")

path = [
    "comment_list_renderer",
    "feedback",
    "comment_rendering_instance_for_feed_location",
    "comments",
    "edges"
]

edges = find_value(data, path)

if isinstance(edges, list) and len(edges) > 1:
    
    plugins = edges[1].get("node", {}).get("feedback", {}).get("plugins", [])
    if isinstance(plugins, list) and len(plugins) > 0:
        post_id = plugins[0].get("post_id")
        print("✅ Second Comment Post ID:", post_id)
    else:
        print("⚠️ No plugins found on second comment.")
else:
    print("⚠️ Not enough comments found.")


path = [
    "comment_list_renderer",
    "feedback",
    "comment_rendering_instance_for_feed_location",
    "comments",
    "edges"
]

edges = find_value(data, path)


edges_path = [
    "comment_list_renderer",
    "feedback",
    "comment_rendering_instance_for_feed_location",
    "comments",
    "edges"
]

edges = find_value(data, edges_path)


if isinstance(edges, list) and len(edges) > 0:
    author_id = edges[0].get("node", {}).get("author", {}).get("id")
    print("✅ First Comment Author ID:", author_id)
else:
    print("⚠️ No author id found.")



if isinstance(edges, list) and len(edges) > 0:
    feedback_url = edges[0].get("node", {}).get("feedback", {}).get("url")
    print("✅ First Comment Feedback URL:", feedback_url)
else:
    print("⚠️ Comment feedback URL not found.")


metadata_path = [
    "context_layout",
    "story",
    "comet_sections",
    "metadata"
]

metadata_list = find_value(data, metadata_path)


if isinstance(metadata_list, list) and len(metadata_list) > 0:
    creation_time = metadata_list[0].get("story", {}).get("creation_time")

    if creation_time:
        

        converted_time = datetime.fromtimestamp(creation_time).strftime("%Y-%m-%d %H:%M:%S")
        print("✅ Converted Date & Time:", converted_time)
    else:
        print("⚠️ creation_time not found inside first metadata element.")
else:
    print("⚠️ metadata list not found.")


path = [
    "comment_list_renderer",
    "feedback",
    "comment_rendering_instance_for_feed_location",
    "comments",
    "edges"
]

edges = find_value(data, path)

if isinstance(edges, list) and len(edges) > 0:
    feedback_url = (
        edges[0]
        .get("node", {})
        .get("feedback", {})
        .get("url")
    )
    print("✅ First Comment Feedback URL:", feedback_url)
else:
    print("⚠️ Feedback URL not found.")  


output_data = []

edges = find_value(data, [
    "comment_list_renderer",
    "feedback",
    "comment_rendering_instance_for_feed_location",
    "comments",
    "edges"
])

output_data = []

if isinstance(edges, list):
    for edge in edges:
        node = edge.get("node", {})

        author_name = node.get("author", {}).get("name")
        author_id = node.get("author", {}).get("id")
        comment_text = node.get("body", {}).get("text")
        likes_count = node.get("feedback", {}).get("reactors", {}).get("count_reduced")
        replies_count = node.get("feedback", {}).get("replies_fields", {}).get("total_count")
        comment_url = node.get("feedback", {}).get("url")

        comment_time = node.get("created_time")
        if comment_time:
            date = datetime.fromtimestamp(comment_time).strftime("%Y-%m-%d %H:%M:%S")
        else:
            date = None

        output_data.append({
            "facebookUrl": comment_url,
            "commentUrl": comment_url,
            "id": author_id,
            "feedbackId": author_id,
            "date": date,
            "text": comment_text,
            "profileId": author_id,
            "profileName": author_name,
            "likesCount": likes_count,
            "commentsCount": replies_count,
            "comments": [],
            "threadingDepth": 0,
            "facebookId": author_id
        })


with open("output.json", "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=4, ensure_ascii=False)

print(" Saved ALL comments with correct date!")
