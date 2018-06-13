# -*- coding: utf-8 -*-

import pymysql
import os
db=pymysql.connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    passwd='',
    charset='utf8',
    database='biquge'
)

novel_id=input("请输入小说ID:")
novel_name=input("请输入小说名称:")

sql="SELECT chapter_name,chapter_content FROM biquge.chapter_info WHERE novel_id='{}' ORDER BY chapter_id".format(novel_id)


cursor=db.cursor()

cursor.execute(sql)

result=cursor.fetchall()

filename=novel_name

for data in result:
    with open('./novel/{}.txt'.format(filename), 'a+', encoding='utf8') as f:
        f.write(data[0]+"\n")
    try:
        chapter_content=data[1].split('br')
        for content in chapter_content:
            with open('./novel/{}.txt'.format(filename), 'a+', encoding='utf8') as f:
                f.write(content+'\n')
        with open('./novel/{}.txt'.format(filename), 'a+', encoding='utf8') as f:
            f.write('\n'+'\n'+'\n')
    except Exception as e:
        pass
    print(data[0])
