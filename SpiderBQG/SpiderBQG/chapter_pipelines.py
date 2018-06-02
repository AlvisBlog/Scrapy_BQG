# -*- coding: utf-8 -*-

import time

import pymysql

from SpiderBQG import settings


class Spider_bqg_Pipeline(object):
    def __init__(self):

        '''初始化连接数据库'''

        print("正在为写入小说章节信息连接数据库")

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
                "insert into chapter_info (chapter_id,novel_id,chapter_link,chapter_name,chapter_content) "
                "values(%s,%s,%s,%s,%s)",
                [item['chapter_id'], item['novel_id'], item['chapter_link'], item['chapter_name'],item['chapter_content']
        ])

            # 提交sql语句
            self.connect.commit()

            with open("chapter.log","a+") as f:

                f.write(time.strftime("%Y-%m-%d %H:%M:%S  ")+"章节信息:%s,写入数据库成功"%item['chapter_name']+"\n")

            print("章节信息:%s,写入数据库成功"%item['chapter_name'])

        except Exception as error:

            with open("chapter.log", "a+") as f:

                f.write(time.strftime("%Y-%m-%d %H:%M:%S  ")+"Exception: 章节信息:%s,数据库已存在同样的数据" % item['chapter_name']+"   原因:%s"%error+"\n")

            print("章节信息:%s,数据库已存在同样的数据"%item['chapter_name'])

            pass


        return item
