import requests

def get(url, params):
    # 添加必要的请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0',
        'Cookie': "SESSDATA=5fafb6ea%2C1766838842%2Cb3bba%2A61CjBqZ3NFgTWToB-ezuVyNbftWvo7TQB4mWsN9z7g0iR7TRKtjaJfo8Y7eXInwuxlg_wSVm5xSGRWTEtqM2FLbDR1T1BPTDFkOXZoaU5CdVFRMEhiMEFQbUJIaXNRckZsMUtad2p1YjJHV1Nrc0RURDB4VzJRZFRYMWZQb25HdDdtdExEOFhwQlhRIIEC"
        # 'Accept': 'application/json, text/plain, */*',
        # 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        # 'Accept-Encoding': 'gzip, deflate, br',
        # 'Referer': 'https://live.bilibili.com/',
        # 'Origin': 'https://live.bilibili.com',
        # 'Connection': 'keep-alive',
        # 'Sec-Fetch-Dest': 'empty',
        # 'Sec-Fetch-Mode': 'cors',
        # 'Sec-Fetch-Site': 'same-site'
    }
    
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()  # 检查HTTP错误
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        print(f"状态码: {getattr(e.response, 'status_code', 'N/A')}")
        print(f"响应内容: {getattr(e.response, 'text', 'N/A')}")
        return None

def get_dynamic(host_mid):
    url = "https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/all"
    params = {
        "host_mid": host_mid,
        "features": "itemOpusStyle"
    }
    return get(url, params)