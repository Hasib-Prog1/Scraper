from parsel import Selector
import requests
import time
import re

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
    
    scripts = selector.css('script[src*="static.xx.fbcdn.net"][src*="rsrc.php"][async="1"]::attr(src)').getall()
    


    for s in scripts:

        
        
        script_url = s

        

        try:
            js = requests.get(script_url, headers=headers, timeout=20).text
        except:
            continue

        match = re.search(r'\b(24939608725693942)\b', js)
        


        if match:
            
            return match.group(0)

    print("No data found!")
    return None


get_data("https://www.facebook.com/Cristiano/followers")
