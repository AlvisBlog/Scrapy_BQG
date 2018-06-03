# -*- coding: utf-8 -*-

import re
from time import sleep

import requests
from urllib.parse import quote
import scrapy
import pymysql

from SpiderBQG.items import Spider_bqg_novel_Item,Spider_bqg_chapter_Item


class GetSpiderUrl:

    def __init__(self):

        self.novel_search_list = {}

        self.user_url=[]

        self.spider_url=[]

        self.unspider_url = []


    def Get_User_NovelUrl(self):


        while True:

            try:

                input_data = input("请输入搜索的小说名(小说名称的关键字,避免完整名称):")

                keyword = quote(input_data, encoding='gb2312')

                url = 'http://www.biquge.com.tw/modules/article/soshu.php?searchkey={}'.format(keyword)

                response = requests.get(url)

                html = response.text.encode('ISO-8859-1').decode('GBK')

                novel_list = re.findall('<tr id="nr">(.*?)</tr>', html, re.S)

                if len(novel_list) == 0:

                    print("抱歉！无搜索结果,需要重新选择搜索关键词")

                    continue

                else:

                    print("搜索的小说如下")

                    max_page = re.findall('<em id="pagestats">1/(.*?)</em>', html, re.S)[0]

                    for page in range(1, int(max_page) + 1):

                        visited_url = url + "&page={}".format(page)

                        response = requests.get(visited_url)

                        html = response.text.encode('ISO-8859-1').decode('GBK')

                        novel_list = re.findall('<tr id="nr">(.*?)</tr>', html, re.S)

                        for novel in novel_list:
                            novel_link = re.findall('<a href="(.*?)">', novel, re.S)[0]

                            novel_name = re.findall('<td class="odd"><.*?">(.*?)<', novel, re.S)[0]

                            self.novel_search_list[novel_name] = novel_link

                            print(novel_name, novel_link)

                    while True:

                        try:

                            choose_novel = input("请从小说列表里选择需要爬取的小说:")

                            if choose_novel == 'all':

                                print("你选择爬取所有的小说")

                                sleep(5)

                                for name, link in self.novel_search_list.items():

                                    self.user_url.append(link)

                                    print("你选择的爬取链接为:%s,小说名称是:%s" % (link, name))

                                break

                            elif choose_novel == 'quit':

                                print("你选择退出爬虫")

                                break

                            else:

                                chooses = choose_novel.split(" ")

                                for choose in chooses:
                                    print("你选择的爬取链接为:%s" % self.novel_search_list[choose])

                                    self.user_url.append(self.novel_search_list[choose])

                                break

                        except Exception as s:

                            print("你的输入不合法,需要重新选择")

                            continue

                break

            except Exception as e:

                print("搜索有唯一结果,网站自动转到小说页面,需要重新选择搜索关键词")

                continue

        return self.user_url


    def Connect_DB(self):

        id_list = []

        try:

            print("---正在尝试连接数据库---")

            sleep(3)

            db = pymysql.connect(
                host='127.0.0.1',
                port=3306,
                database='biquge',
                user='root',
                passwd='',
                charset='utf8'
            )
            print("数据库连接成功")

            # 提取小说ID列表
            for url in self.user_url:

                id_list.append(re.findall('http.*?//.*?/(.*?)/', url, re.S)[0])

            cursor = db.cursor()

            try:

                print("正在查询小说是否已存在")
                sleep(3)

                # 遍历ID列表,进行查询
                for id in id_list:

                    cursor.execute('select * from novel_info WHERE novel_id=%s', [id])

                    result = cursor.fetchone()

                    if result is None:

                        self.spider_url.append("http://www.biquge.com.tw/%s" % id)

                    else:

                        self.unspider_url.append('http://www.biquge.com.tw/%s' % id)

                        print("数据库存在该小说," + "名称为: %s,ID为: %s" % (result[3], result[2]))


            except Exception as e:

                print("查询异常,错误代码:%s" % e)


        except Exception as error:

            print("连接失败,错误代码:%s" % error)


        if len(self.spider_url)==0:

            print("爬取链接为空")

        else:

            print("需要爬取的连接为:")

            print(self.spider_url)

        return self.spider_url


class SpidernovelSpider(scrapy.Spider):

    spider=GetSpiderUrl()

    spider.Get_User_NovelUrl()

    if len(spider.user_url) == 0:

        spider_url=[]

    else:
        spider_url=spider.Connect_DB()

    name = 'spidernovel'

    start_urls = spider_url


    def parse(self, response):

        print("获取小说信息")

        novel_item=Spider_bqg_novel_Item()

        html=response.text

        novel_item['novel_link']=response.url

        novel_item['novel_id'] = re.findall('http://www.biquge.com.tw/(.*?)/', novel_item['novel_link'], re.S)[0]

        novel_item['novel_name']=re.findall('<meta property="og:novel:book_name" content="(.*?)"/>',html,re.S)[0]

        novel_item['novel_author']=re.findall('<meta property="og:novel:author" content="(.*?)"/>',html,re.S)[0]

        novel_item['novel_type']=re.findall('<meta property="og:novel:category" content="(.*?)"/>',html,re.S)[0]

        novel_item['novel_last_pubdate']=re.findall('<meta property="og:novel:update_time" content="(.*?)"/>',html,re.S)[0]

        novel_item['novel_status']=re.findall('<meta property="og:novel:status" content="(.*?)"/>',html,re.S)[0]

        novel_item['novel_intro']=re.findall('<div id="intro">.*?<p>(.*?)</p>',html,re.S)[0].strip()

        chapter_link_list=re.findall('<dd>(.*?)</dd>',html,re.S)

        yield novel_item

        for part_chapter_link in chapter_link_list:

            chapter_link="http://www.biquge.com.tw"+re.findall('<a href="(.*?)"',part_chapter_link,re.S)[0]

            yield scrapy.Request(url=chapter_link,callback=self.parse_chapter)



    def parse_chapter(self,response):

        html=response.text

        chapter_item = Spider_bqg_chapter_Item()

        chapter_item['chapter_link']=response.url

        chapter_item['novel_id'] =re.findall('http://www.biquge.com.tw/(.*?)/.*?.html',response.url,re.S)[0]

        chapter_item['chapter_id'] = re.findall('http://www.biquge.com.tw/.*?/(.*?).html', response.url, re.S)[0]

        chapter_item['chapter_name']=re.findall('<h1>(.*?)</h1>',html,re.S)[0]

        data=re.findall('<div id="content">(.*?)/div>',html,re.S)[0]

        chapter_content=re.findall('&nbsp;&nbsp;&nbsp;&nbsp;(.*?)<',data,re.S)

        chapter_item['chapter_content']=''


        for sentence in chapter_content:

            chapter_item['chapter_content']=chapter_item['chapter_content']+sentence

        yield chapter_item





