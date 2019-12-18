# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from crawl_lianjia_single.items import CrawlLianjiaSingleItem
import pymysql

class LianjiaspiderSpider(CrawlSpider):
    name = 'lianjiaspider'
    #allowed_domains = ['sh.lianjia.com']
    start_urls = ['https://sh.lianjia.com/xiaoqu/']


    # rules = (
    #     Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    # )

    def parse(self, response):
        self.k=len(response.xpath('/html/body/div[3]/div[1]/dl[2]/dd/div/div/a//text()').getall())
        self.rawdistrict=response.xpath('/html/body/div[3]/div[1]/dl[2]/dd/div/div/a//text()').getall()
        self.rawlink=response.xpath('/html/body/div[3]/div[1]/dl[2]/dd/div/div/a/@href').getall()
        for div in range(0,self.k):  
            self.district = self.rawdistrict[div]
            self.link = self.rawlink[div]
            #print('区域区域')
            #print(self.district)
            self.region_url = 'https://sh.lianjia.com' + self.link
            #print(self.region_url)
            # yield{
            #     'district': self.district,
            #     'region_url': self.region_url,
            # }
            # for i in range(1,31):
            #     self.region_url_page = self.region_url+'pg%d' % i
                #print(self.region_url_page)
            yield scrapy.Request(url=self.region_url, callback=self.parse_district)
    def parse_district(self,response):
        #item = {}
        self.rawlinkdis = response.xpath('/html/body/div[3]/div[1]/dl[2]/dd/div/div[2]/a//@href').getall() 
        #print(self.rawlinkdis)
        #print('片区片区')

        for ii in range(0,len(self.rawlinkdis)):
            self.xiaoqu_url = 'https://sh.lianjia.com' + self.rawlinkdis[ii]
            yield scrapy.Request(url=self.xiaoqu_url, callback=self.parse_xiaoqu)
            #xiaoqu_url   例如/xiaoqu/beicai
    def parse_xiaoqu(self,response):

        #self.tradelink = response.xpath('/html/body/div[4]/div[1]/ul/li/div[1]/div[1]/a//@href').getall()
        #print(self.tradelink)
        #找出每个区的小区有多少页面
        if response.xpath('/html/body/div[4]/div[1]/div[3]/div[2]/div//@page-data').getall():
            self.page_data_xiaoqu = response.xpath('/html/body/div[4]/div[1]/div[3]/div[2]/div//@page-data').getall()
            self.totalpagestr = eval(self.page_data_xiaoqu[0])
            self.totalpage_xiaoqu = self.totalpagestr['totalPage']

            self.currentpage_url_init = response.request.url
            #循环逻辑：只有一页 else进入交易详情页parse
            #          多于一页  先进入交易详情页parse
            #                    翻页回调本函数 
            #print('当前页')
            #print(self.currentpage_url_init)
            if self.totalpage_xiaoqu>1:
                for pinjiepagenum in range(1,self.totalpage_xiaoqu+1):
                    self.tradelink = response.xpath('/html/body/div[4]/div[1]/ul/li/div[1]/div[1]/a//@href').getall()
                    for url_in_tradelink in self.tradelink:
                        #https://sh.lianjia.com/xiaoqu/5011000011178/转换为https://sh.lianjia.com/chengjiao/c5011000011178/
                        
                        yield scrapy.Request(url=url_in_tradelink,callback=self.parse_xiaoqurecord)
                    if '/pg' in self.currentpage_url_init:
                        xiabiao = self.currentpage_url_init.find('/pg')
                        self.currentpage_url_init = self.currentpage_url_init[0:xiabiao] 
                    self.pinjie = '/pg%d'% pinjiepagenum
                    self.xiaoqu_url_next = self.currentpage_url_init+self.pinjie
                    #print('小区页面返回页面')
                    #print(self.xiaoqu_url_next)

                    yield scrapy.Request(url=self.xiaoqu_url_next,callback=self.parse_xiaoqu)
    def parse_xiaoqurecord(self,response):#分析类似下面页面 https://sh.lianjia.com/xiaoqu/daning/pg2/
        self.rawlinkforurl = response.request.url
        self.traderecordurl = self.rawlinkforurl.replace('/xiaoqu/','/chengjiao/c')
        # yield{
        #     'traderecordurl':self.traderecordurl,
        # }
        yield scrapy.Request(url=self.traderecordurl,callback=self.parse_traderecord)

    def parse_traderecord(self,response):#分析类似下面页面https://sh.lianjia.com/chengjiao/c5011000011178/  首页，需要分析是否有翻页
        if response.xpath('/html/body/div[5]/div[1]/div[5]/div[2]/div/@page-data').getall():
            self.page_data = response.xpath('/html/body/div[5]/div[1]/div[5]/div[2]/div/@page-data').getall()

            self.totalpagestrstr = eval(self.page_data[0])
            self.totalpage = self.totalpagestrstr['totalPage']
            self.trade_page_link = response.xpath('/html/body/div[5]/div[1]/div[5]/div[2]/div/@page-url').getall()
            for jj in range(1,self.totalpage+1):     
                self.rawstr = self.trade_page_link[0]
                self.trade_page_url = 'https://sh.lianjia.com' + self.rawstr.replace('{page}',str(jj))
                print(self.trade_page_url)
                yield scrapy.Request(url=self.trade_page_url,callback=self.parse_traderecord_page)

    def parse_traderecord_page(self,response):
        item = {}
        if response.xpath('/html/body/div[5]/div[1]/ul/li/div/div[1]/a//text()').getall():           
            self.aaa1 = response.xpath('/html/body/div[5]/div[1]/ul/li/div/div[1]/a//text()').getall()
            self.aaa2 = response.xpath('/html/body/div[5]/div[1]/ul/li/div/div[2]/div[1]//text()').getall()
            self.aaa3 = response.xpath('/html/body/div[5]/div[1]/ul/li/div/div[2]/div[2]//text()').getall()
            self.aaa4 = response.xpath('/html/body/div[5]/div[1]/ul/li/div/div[2]/div[3]/span//text()').getall()
            self.aaa5 = response.xpath('/html/body/div[5]/div[1]/ul/li/div/div[3]/div[1]//text()').getall()
            self.aaa6 = response.xpath('/html/body/div[5]/div[1]/ul/li/div/div[3]/div[3]/span//text()').getall()
            #dealcycleprice = response.xpath('/html/body/div[5]/div[1]/ul/li/div/div[5]/span[2]/span[1]//text()').getall()
            
            #dealcycletime = response.xpath('/html/body/div[5]/div[1]/ul/li/div/div[5]/span[2]/span[2]//text()').getall()
            for dd in range(0,len(response.xpath('/html/body/div[5]/div[1]/ul/li'))):
                # item['houseinfo1'] = self.aaa1[dd]

                # item['houseinfo2'] = self.aaa2[dd]
                # item['dealdate'] = self.aaa3[dd]
                # item['totalprice'] = self.aaa4[dd]
                # item['floor'] = self.aaa5[dd]
                # item['unitprice'] = self.aaa6[dd]
                houseinfo1 = self.aaa1[dd]
                houseinfo2 = self.aaa2[dd]
                dealdate = self.aaa3[dd]
                totalprice = self.aaa4[dd]
                floor = self.aaa5[dd]
                unitprice = self.aaa6[dd]
                yield{
                    'houseinfo1':self.aaa1[dd],
                    'houseinfo2':self.aaa2[dd],
                    'dealdate':self.aaa3[dd],
                    'totalprice':self.aaa4[dd],
                    'floor':self.aaa5[dd],
                    'unitprice':self.aaa6[dd],
                }

 