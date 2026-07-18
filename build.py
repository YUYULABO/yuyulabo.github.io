import urllib.request
import json
import os
import re

# 1. 環境変数からAPI設定を取得
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
    
    # ★追加: URLフィールドを取得（未入力の場合は空文字）
    url = work.get('url', '')
    
    # ★追加: URLがある場合だけ、リンクのHTMLタグを生成
    link_html = f'<a href="{url}" target="_blank" style="display: inline-block; margin-top: 15px; font-size: 0.9rem; font-weight: bold;">詳細を見る ＞</a>' if url else ''
    
    # HTML組み立て（{link_html} を追加）
    works_html += f"""
    <div class="work-card">
        <img src="{image_url}" alt="{title}" class="work-img">
        <div class="work-info">
            <h3>{title}</h3>
            <p>{description}</p>
            {link_html}
        </div>
    </div>
    """

# 4. index.html を読み込み、正規表現で部分置換して保存
try:
    with open('index.html', 'r', encoding='utf-8') as f:
        html_content = f.read()

    pattern = r'<!-- WORKS_START -->.*?<!-- WORKS_END -->'
    replacement = f'<!-- WORKS_START -->\n{works_html}\n<!-- WORKS_END -->'
    
    new_html = re.sub(pattern, replacement, html_content, flags=re.DOTALL)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_html)
        
    print("Build successful!")
except Exception as e:
    print(f"Failed to build HTML: {e}")
    exit(1)
