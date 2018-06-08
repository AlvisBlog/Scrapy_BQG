# -*- coding: utf-8 -*-

import re
from time import sleep

from urllib.parse import quote
import requests
import pymysql


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


spider=GetSpiderUrl()

spider.Get_User_NovelUrl()

if len(spider.user_url)==0:
    pass
else:
    spider.Connect_DB()



