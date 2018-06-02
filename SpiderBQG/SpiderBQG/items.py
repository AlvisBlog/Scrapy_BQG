# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Spider_bqg_novel_Item(scrapy.Item):

    novel_id=scrapy.Field()

    novel_link = scrapy.Field()

    novel_name = scrapy.Field()

    novel_author = scrapy.Field()

    novel_type = scrapy.Field()

    novel_status = scrapy.Field()

    novel_last_pubdate=scrapy.Field()

    novel_intro=scrapy.Field()

class Spider_bqg_chapter_Item(scrapy.Item):

    chapter_id=scrapy.Field()

    novel_id = scrapy.Field()

    chapter_name=scrapy.Field()

    chapter_link=scrapy.Field()

    chapter_content=scrapy.Field()


