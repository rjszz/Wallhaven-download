# Wallhaven-download
下载wallhaven的toplist,latest,hot图片

## 使用

使用前先替换`wallhavenDownload.py`中的`APIKey`为自己的APIkey

```bash
python3 wallhavenDownload.py -m toplist --savePath ~/Pic --maxPage 1
```



## 参数说明

```bash
--mode {toplist,latest,hot}, -m {toplist,latest,hot}    爬取图片模式,toplist,latest,hot三种模式
--savePath SAVEPATH   图片保存路径
--maxPage MAXPAGE     最大页数
```

