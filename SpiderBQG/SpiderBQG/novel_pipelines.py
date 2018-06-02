# -*- coding: utf-8 -*-

import time

import pymysql

from SpiderBQG import settings

class Spider_bqg_Pipeline(object):

    def __init__(self):

        '''初始化连接数据库'''

        print("正在为写入小说信息连接数据库")

        time.sleep(5)

        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            port=3306,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True)

        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()

        print("数据库连接成功")


    def process_item(self, item, spider):

        try:


            self.cursor.execute(
                "insert into novel_info (novel_id,novel_name,novel_author,novel_link,novel_type,novel_status,novel_last_pubdate,novel_intro) "
                "values(%s,%s,%s,%s,%s,%s,%s,%s)",
                [item['novel_id'], item['novel_name'], item['novel_author'], item['novel_link'],
                 item['novel_type'], item['novel_status'],item['novel_last_pubdate'],item['novel_intro']])

            # 提交sql语句
            self.connect.commit()

            with open("novel.log","a+") as f:

                f.write(time.strftime("%Y-%m-%d %H:%M:%S  ")+"小说信息:%s,写入数据库成功"%item['novel_name']+"\n"+"\n")

            print("小说信息:%s,写入数据库成功"%item['novel_name'])

        except Exception as e:

            pass



        return item
