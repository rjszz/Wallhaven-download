"""
爬取wallhaven的toplist图片
author: rjszz
"""

import subprocess, json

APIKey = "y6L3vWvPfZSDbxilkIiyZrM4nGZSAhST"

wallHavenUrlBase = "https://wallhaven.cc/api/v1/search? \
                    apikey={}&topRange=1M&sorting=toplist&page=".format(APIKey)

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

if __name__ == "__main__":
    # wget("https://w.wallhaven.cc/full/72/wallhaven-72rxqo.jpg", "72rxqo.jpg")
    res = curlGet('https://wallhaven.cc/api/v1/search?apikey=y6L3vWvPfZSDbxilkIiyZrM4nGZSAhST&topRange=1M&sorting=toplist&page=1')
    handleResponseRes(res)