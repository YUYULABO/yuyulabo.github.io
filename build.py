import urllib.request
import json
import os

# 1. 環境変数からAPI設定を取得
# GitHub Actions側で安全に設定したシークレット値を読み込みます
SERVICE_ID = os.environ.get('MICROCMS_SERVICE_ID')
API_KEY = os.environ.get('MICROCMS_API_KEY')
ENDPOINT = f"https://{SERVICE_ID}.microcms.io/api/v1/works"

# 2. microCMSからデータを取得
req = urllib.request.Request(ENDPOINT, headers={'X-MICROCMS-API-KEY': API_KEY})
try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
except Exception as e:
    print(f"Failed to fetch data: {e}")
    exit(1)

# 3. HTMLパーツを生成
works_html = ""
for work in data.get('contents', []):
    image_url = work.get('image', {}).get('url', 'https://unsplash.com/...')
    title = work.get('title', 'No Title')
    description = work.get('description', '')
    
    # カードのHTMLを組み立て
    works_html += f"""
    
        
        
            {title}
            {description}
        
    
    """

# 4. index.html を読み込み、目印の部分を置換して保存
try:
    with open('index.html', 'r', encoding='utf-8') as f:
        html_content = f.read()

    new_html = html_content.replace('', works_html)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_html)
        
    print("Build successful!")
except Exception as e:
    print(f"Failed to build HTML: {e}")
    exit(1)
