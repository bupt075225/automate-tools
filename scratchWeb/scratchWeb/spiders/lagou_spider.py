# -*- coding: utf-8 -*-
import json

import scrapy
from scratchWeb.items import LagouJob


class LagouSpiderSpider(scrapy.Spider):
    name = "lagou_spider"
    allowed_domains = ["lagou.com"]
    #start_urls = ['https://www.lagou.com/']

    # lagou网搜索表单提交地址
    jobs_url = "http://www.lagou.com/jobs/positionAjax.json?"
    # 职位信息搜索关键字
    search_key_word = ["python",]
    crawl_count = 0

    def start_requests(self):
        '''
        按关键字搜索职位信息
        '''
        return [scrapy.http.FormRequest(self.jobs_url,
            formdata={"first":"true", "pn":"1", "kd":self.search_key_word[0]},
            callback=self.parse)]

    def parse(self, response):
        '''
        filename = 'lagou_jobs_list.html'
        with open(filename, 'wb') as fd:
            fd.write(response.body)
        '''

        # 请求响应的是JSON格式数据
        search_result = json.loads(response.body)
        if search_result["success"] != True:
            self.log("Result response failed")
            raise ValueError("Response failed")

        # 关键字搜索结果分页显示,当前的页数
        cur_page = search_result["content"]["pageNo"]
        # 当前页面显示的记录数
        page_size = search_result["content"]["pageSize"]
        # 职位信息列表
        job_list = search_result["content"]["positionResult"]["result"]
        # 搜索结果总的记录条数
        total_count = search_result["content"]["positionResult"]["totalCount"]

        self.crawl_count += page_size

        job_item = LagouJob()
        for job in job_list:
            job_item["company_name"] = job["companyShortName"]
            job_item["position_name"] = job["positionName"]
            job_item["release_time"] = job["formatCreateTime"]
            job_item["salary"] = job["salary"]
            job_item["city"] = job["city"]
            job_item["work_address"] = job["district"]
            job_item["finance_stage"] = job["financeStage"]
            job_item["industry_field"] = job["industryField"]
            job_item["company_size"] = job["companySize"]
            job_item["education"] = job["education"]
            yield job_item

        if cur_page > 0 and self.crawl_count < total_count:
            next_page = cur_page + 1
            self.log("Now request page %d" % next_page)
            yield scrapy.http.FormRequest(self.jobs_url,
                formdata={"first":"false", 
                          "pn":str(next_page), 
                          "kd":self.search_key_word[0]},
                callback=self.parse)
