import requests

def process_video_with_gemini(video_path):
    url = 'https://gemini.api/endpoint'  # 替換為你的 Gemini API 端點
    files = {'file': open(video_path, 'rb')}
    response = requests.post(url, files=files)
    
    if response.status_code == 200:
        result = response.json()
        return result.get('score', 0)
    else:
        return 0
