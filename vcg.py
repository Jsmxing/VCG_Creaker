import json
import requests
import re
import os
from urllib.parse import urlsplit


def download_image(id, url):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        file_name = os.path.basename(urlsplit(url).path)
        file_path = os.path.join(os.path.dirname(__file__), file_name)
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(id + "下载完成")
    else:
        print(id + "下载失败")


if __name__ == '__main__':
    url = input("请输入要下载的视觉中国图片地址(例如: https://www.vcg.com/creative/1252497020): ")
    response = requests.get(url)

    if response.status_code == 200:
        content = response.text
        match = re.search(r'<script>(.*?)<\/script>', content, re.DOTALL)
        if match:
            script_content = match.group(1)
            # 去除开头的特定文本
            start_index = script_content.find('window.__PRELOADED_STATE__=')
            if start_index != -1:
                script_content = script_content[start_index + len('window.__PRELOADED_STATE__='):]
            script_content = script_content[:-1]

            script_content_json = json.dumps(script_content, indent=4)
            parsed_data = json.loads(script_content_json, strict=False)
            test = json.loads(parsed_data, strict=False)

            VCG_ID = test["imageDetail"]["data"]["picInfo"]["res_id"]
            VCG_OSS = "https:" + test["imageDetail"]["data"]["picInfo"]["oss800"]
            download_image(VCG_ID, VCG_OSS)
        else:
            print("查找失败")
    else:
        print("请求失败，状态码:", response.status_code)