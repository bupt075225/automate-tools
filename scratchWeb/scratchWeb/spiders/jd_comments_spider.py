# -*- coding: utf-8 -*-
import json

import scrapy
from scratchWeb.items import JDComment

from scrapy.conf import settings
import pymongo

class JdCommentsSpiderSpider(scrapy.Spider):
    name = "jd_comments_spider"

    def __init__(self):
        self.comment_url = "https://club.jd.com/comment/productPageComments.action?productId={}&score=0&sortType=5&page={}&pageSize=10"
        self.db = pymongo.MongoClient(settings["MONGODB_HOST"])[settings["MONGODB_DATABASE"]] 

    def start_requests(self):
        goods = self.get_item_sku_id()
        pymongo.MongoClient(settings["MONGODB_HOST"]).close()
        for sku_id,good_name in goods:
            yield scrapy.Request(url=self.comment_url.format(sku_id, 1),
                        callback=self.parse_comment,
                        meta={'page':1,
                              'sku_id':sku_id,
                              'good_name':good_name})

    def parse_comment(self, response):
        comment_item = JDComment()
        page = response.meta["page"]
        sku_id = response.meta["sku_id"]
        good_name = response.meta["good_name"]
        rsp_body = response.text

        # 评论可能为空
        if rsp_body != '':
            data = json.loads(rsp_body)
            max_page = data.get("maxPage")
            comments = data.get("comments")
            comment_item["good_name"] = good_name

            for comment in comments:
                comment_item["comment_id"] = comment.get("id")
                comment_item["content"] = comment.get("content")
                comment_item["create_time"] = comment.get("creationTime")
                comment_item["score"] = comment.get("score", "")
                comment_item["useful_vote_count"] = comment.get("usefulVoteCount", "")
                comment_item["useless_vote_count"] = comment.get("uselessVoteCount", "")
                comment_item["reference_time"] = comment.get("referenceTime", "")

                yield comment_item

            if page < max_page:
                yield scrapy.Request(url=self.comment_url.format(sku_id, page + 1),
                                     callback=self.parse_comment,
                                     meta={'page':page + 1,
                                           'sku_id':sku_id,
                                           'good_name':good_name})
        else:
            print "There is no comment"


    def get_item_sku_id(self):
        goods = self.db["jd_goods"].find({})
        goods_list = [good for good in goods]
        sku_ids = []
        good_names = []

        for item in goods_list:
            sku_id = dict(item).get("sku_id", None)
            good_name = dict(item).get("good_name", None)
            if good_name:
                good_name = good_name
            else:
                good_name = ""

            sku_ids.append(sku_id)
            good_names.append(good_name)

        good = set(list(zip(sku_ids, good_names)))
        return list(good)
