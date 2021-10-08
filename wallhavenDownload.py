"""
爬取wallhaven的toplist图片
author: rjszz
"""

import subprocess, json
import argparse
import os

#参数解析
parser = argparse.ArgumentParser()

APIKey = "y6L3vWvPfZSDbxilkIiyZrM4nGZSAhST"

wallHavenUrlBase = ""

"""
参数配置
"""
def parserInit():
    parser.add_argument('--mode', '-m', required=True, choices=['toplist', 'latest', 'hot'],help='爬取图片模式')
    parser.add_argument('--savePath', required=True, help='图片保存路径')
    parser.add_argument('--maxPage', default=5, help='最大页数')


"""
初始化
"""
def init():
    parserInit()

    args = parser.parse_args()
    
    #设置需要爬取的url
    global wallHavenUrlBase
    wallHavenUrlBase = "https://wallhaven.cc/api/v1/search?apikey={}&topRange=1M&sorting={}&page=".format(APIKey, args.mode)
    
    print(wallHavenUrlBase)
    
    # 创建文件保存目录
    # os.makedirs(args.savePath, exist_ok=True)

"""
通过wget获取下载图片
"""
def wget(url, savePath):
    subprocess.run(["wget", "-O", savePath, url])


"""
curl 实现get请求
"""
def curlGet(url):
    res = subprocess.run(["curl", "-XGET", "-L", url, "--max-time", "60", "--retry", "3"], stdout=subprocess.PIPE).stdout
    return res

"""
将get请求结果转化为dict
结果结构:
{
"data":[
    "id":   "72rxqo"
    ...
    "resolution": "1920x1080"
    ...
    "path": imgUrl(https://w.wallhaven.cc/full/72/wallhaven-72rxqo.jpg)
    ...
]
}
"""
def handleResponseRes(responseResBytes):
    try:  
        responseResStr = str(responseResBytes, encoding = "utf-8")  
        responseResDict = json.loads(responseResStr)
        print(responseResDict["data"][0]['path'])
        return responseResDict
    except Exception as e:
        print("结果转化错误:{}".format(e))
        return None

"""
主流程
"""

if __name__ == "__main__":
    # wget("https://w.wallhaven.cc/full/72/wallhaven-72rxqo.jpg", "72rxqo.jpg")
    # res = curlGet('https://wallhaven.cc/api/v1/search?apikey=y6L3vWvPfZSDbxilkIiyZrM4nGZSAhST&topRange=1M&sorting=toplist&page=1')
    # handleResponseRes(res)
    # parserInit()
    # args = parser.parse_args() 
    # print(args.mode)
    init()