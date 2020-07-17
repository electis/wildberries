import scrapy


class WildberriesSpider(scrapy.Spider):
    name = 'products'

    def __init__(self, *args, **kwargs):
        super(WildberriesSpider, self).__init__(*args, **kwargs)
        start_url = 'https://www.wildberries.ru/catalog/'
        # if kwargs.get('section'):
        #     section = models.Section.objects.get(pk=kwargs['section'])
        #     start_url += section.make_path()
        start_url += 'elektronika/tehnika-dlya-doma/uvlazhniteli'
        self.start_urls = [start_url]


    def parse(self, response):
        for product in response.css("div.catalog_main_table div.dtList"):
            try:
                _ = product.css('div.dtList-inner div.dtlist-inner-brand .lower-price::text').get()
                price = int(_.strip().replace(u'\xa0', '').replace(u'₽', '')) if _ else None
                _ = product.css('div.dtList-inner div.dtlist-inner-brand-name strong.brand-name::text').get()
                brand = _.strip() if _ else None
                _ = product.css('div.dtList-inner div.dtlist-inner-brand-name span.goods-name::text').get()
                name = _.strip() if _ else None
                _ = product.css('div.dtList-inner div.l_class::attr(id)').get()
                product_id = _.replace('c', '') if _ else None
                print(product_id, price, brand, name)
            except Exception as Ex:
                print(Ex)
            yield {}
        next_page = response.css('div.pager-bottom a.pagination-next::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
