# -*- coding: utf-8 -*-
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.utils.url import urljoin_rfc
from scrapy_webgraph.items import webgraphItem

site_considere = 'perso.ens-lyon.fr'
class GraphspiderSpider(CrawlSpider):
    name = 'webgraph_perso'
    #allowed_domains = ['unodieuxconnard.com']
    #start_urls = ['http://unodieuxconnard.com/']
    allowed_domains = [site_considere]
    start_urls = ['http://perso.ens-lyon.fr/baptiste.roziere/']

    rules = (
        Rule(SgmlLinkExtractor(allow=(), unique= True), callback='parse_item', follow=True),
    )

    def parse_start_url(self, response):
        self.log('>>>>>>>> PARSE START URL: %s' % response)
        return self.parse_item(response)

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        i = webgraphItem()
        i['node'] = response.url
        print "#######################"
        print response.url
        print "#######################"
       # i['http_status'] = response.status
        llinks=[]
        for anchor in hxs.select('//a[@href]'):
            href=anchor.select('@href').extract()[0]
            if not href.lower().startswith("javascript") and  href.startswith("http://perso.ens-lyon.fr/baptiste.roziere/"):
                llinks.append(urljoin_rfc(response.url,href))
        i['edge'] = llinks
        return i
   
