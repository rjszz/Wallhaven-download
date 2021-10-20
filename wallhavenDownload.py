"""
wallhavenDownload.py
爬取wallhaven的toplist,latest,hot图片
author: rjszz
"""

import subprocess, json
import argparse
import os, time

#参数解析
parser = argparse.ArgumentParser()
parser.add_argument('--mode', '-m', required=True, choices=['toplist', 'latest', 'hot'],help='爬取图片模式')
parser.add_argument('--savePath', required=True, help='图片保存路径')
parser.add_argument('--maxPage', default=5, help='最大页数')
args = parser.parse_args()

# 填写自己的APIkey
# Fill in your APIkey
APIKey = "your APIkey"

wallHavenUrlBase = ""

picTypeMap = {
    'image/png': 'png',
    'image/jpeg': 'jpg',
}
    


"""
初始化
init function
"""
def init():
    
    args = parser.parse_args()
    
    #设置需要爬取的url
    #set target url
    global wallHavenUrlBase
    wallHavenUrlBase = "https://wallhaven.cc/api/v1/search?apikey={}&topRange=1M&sorting={}&page=".format(APIKey, args.mode)
    
    
    # 创建文件保存目录
    # create dir which save the picture
    os.makedirs(args.savePath, exist_ok=True)

"""
通过wget获取下载图片
download pictrue by wget
"""
def wget(url, savePath):
    subprocess.run(["wget", "-O", savePath, url])


"""
curl 实现get请求
get by curl
"""
def curlGet(url):
    res = subprocess.run(["curl", "-XGET", "-L", url, "--max-time", "60", "--retry", "3"], stdout=subprocess.PIPE).stdout
    return res

"""
将get请求结果转化为dict
Convert the response into a dict
结果结构:
result struct:
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
def handleResponseRes(responseResBytes) -> dict:
    try:  
        responseResStr = str(responseResBytes, encoding = "utf-8")  
        responseResDict = json.loads(responseResStr)
        return responseResDict
    except Exception as e:
        print("[error]结果转化错误:{}".format(e))
        return None


"""
下载单张图片
downlaod single picture
"""
def downloadOnePic(targetPic: map):
    id = targetPic['id']
    resolution = targetPic['resolution']
    url = targetPic['url']
    picType = targetPic['fileType']
    
    picPath = "{}/{}_{}.{}".format(args.savePath, resolution, id, picTypeMap[picType])

    print("[info]正在下载图片\tID:{}\t规格为:{}\t下载url:{}\t文件保存路径:{}".format(id, resolution, url, picPath))
    if os.path.isfile(picPath):
        print("[warning]图片已存在\n")
        return
    
    wget(url, picPath)
    print("[info]图片下载成功\n")

"""
获取可下载图片
列表形式保存，每项保存了单张图片的 id,尺寸,url
get downloadable pictures
return: the list that saves every picture's info, include id,resolution and url
"""
def getPendingPicUrl(wallHavenUrl) -> list:
    responseRes = curlGet(wallHavenUrl)
    responseResDict = handleResponseRes(responseRes)

    pendingPicUrlList = []
    if not responseResDict.get("data"):
        print("[error]获取图片列表失败")
        exit(1)
    
    for PicMsg in responseResDict["data"]:
        PicMsgMain = {
            'id': PicMsg['id'],
            'resolution': PicMsg['resolution'],
            'url': PicMsg['path'],
            'fileType': PicMsg['file_type'],    # image/png image/jpeg
        }
        pendingPicUrlList.append(PicMsgMain)
    
    return pendingPicUrlList


"""
下载某一页中所有图片
download all picture in one single page
"""
def downloadAllPicInOnePage(pageNum):
    print("[info]正在下载第{}页图片".format(str(pageNum)))

    wallHavenUrl = wallHavenUrlBase + str(pageNum)

    pendingPicUrlList = getPendingPicUrl(wallHavenUrl)

    for targetPic in pendingPicUrlList:
        downloadOnePic(targetPic)
    
    print("[info]第{}页图片下载完成".format(str(pageNum)))
    



"""
主流程
main process
"""
def WallhavenDownload():
    # 初始化
    # init
    init()

    for pageNum in range(1, int(args.maxPage)+1):
        downloadAllPicInOnePage(pageNum)


if __name__ == "__main__":
    print("--------------" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "-----------------")
    WallhavenDownload()
    print("--------------END---------------")