
# 爬取wallhaven上的的图片，支持自定义搜索关键词，自动爬取并该关键词下所有图片并存入本地电脑。
# file wallhaven
# python3.6

import os
import requests
import time 
import random
from lxml import etree

keyword = input('Please input the keywords that you want to download :')

class Spider():
    
    def __init__(self):
        self.headers = {#headers是请求头，"User-Agent"、"Accept"等字段可通过谷歌Chrome浏览器查找！
                "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0",
        }
        self.filepath = ('/home/yaoxinzhi/桌面/杂/python_小程序/爬取wallhaven图片/' + keyword + "/")
    
    def creat_Folder(self):
        filePath = self.filepath
        if not os.path.exists(filePath):
            os.mkdir(filePath)
            
    def get_pageNum(self):
        total = ''
        url = ("https://alpha.wallhaven.cc/search?q={}&categories=111&purity=100&sorting=relevance&order=desc").format(keyword)
        html = requests.get(url)
        selector = etree.HTML(html.text)
        pageInfo = selector.xpath('//header[@class="listing-header"]/h1[1]/text()')
        string = str(pageInfo[0])
        numlist = list (filter(str.isdigit,string))
        for item in numlist:
            total += item 
        totalpagenum = int(total)
        return totalpagenum
    
    def get_links(self,number):
        url = ("https://alpha.wallhaven.cc/search?q={}&categories=111&purity=100&sorting=relevance&order=desc&page={}").format(keyword,number)
        try:
            html = requests.get(url)
            selector = etree.HTML(html.text)
            pic_Linklist = selector.xpath('//a[@class="jsAnchor thumb-tags-toggle tagged"]/@href')
        except Exception as e:
            print (repr(e))
        return pic_Linklist
    
    def download(self,url,count):
        string = url.strip('/thumbTags').strip('https://alpha.wallhaven.cc/wallpaper/')
        html = 'http://wallpapers.wallhaven.cc/wallpapers/full/wallhaven-' + string + '.jpg'
        pic_path = (self.filepath + keyword + str(count) + '.jpg' )
        try:
            start = time.time()
            pic = requests.get(html,headers = self.headers)
            with open(pic_path,'wb') as f:
                f.write(pic.content)
            end = time.time()
            print ("Image :{count} has been downla=oaded,cost:",end - start ,'s')
        except Exception as e:
            print (repr(r))
    
    def main_function(self):
        self.creat_Folder()
        count = self.get_pageNum()
        print ('we have found:{} images!'.format(count))
        times = int(count/24 +1)
        j=1
        start = time.time()
        
        for i in range(times):
            pic_Urls = self.get_links(i+1)
            start2 = time.time()
            for item in pic_Urls:
                self.download(item,j)
                j += 1
            end2 = time.time()
            print ('This page cost:',end2 - start2,'s')
        end = time.time()
        print ('Total cost :',end-start ,'s')
        
spider = Spider()
spider.main_function()
