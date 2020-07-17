import scrapy


class WildberriesSpider(scrapy.Spider):
    name = 'sections'
    menu = None

    def __init__(self, *args, **kwargs):
        super(WildberriesSpider, self).__init__(*args, **kwargs)
        start_url = 'https://www.wildberries.ru'
        # if kwargs.get('section'):
        #     section = models.Section.objects.get(pk=kwargs['section'])
        #     start_url += section.make_path()
        # start_url += 'elektronika/tehnika-dlya-doma/uvlazhniteli'
        self.start_urls = [start_url]

    def close(spider, reason):
        print(spider.menu)


    def parse(self, response):
        if self.menu:
            for section in response.css("div.main-content div.left ul.maincatalog-list-2 li"):
                _ = section.css('a::attr(href)').get()
                url = _.strip() if _ else None
                path = url.split('/catalog/')[-1] if url else None
                _ = section.css('a::text').get()
                name = _.strip() if _ else None
                self.menu[path] = {'name': name, 'path': path}
            yield {}
        else:
            menu = {}
            for section in response.css("div.wrapper-for-dropdown ul.topmenus li.topmenus-item"):
                try:
                    _ = section.css('a::attr(href)').get()
                    url = _.strip() if _ else None
                    path = url.split('/')[-1] if url else None
                    _ = section.css('a::text').get()
                    name = _.strip() if _ else None
                except Exception as Ex:
                    print(Ex)
                else:
                    menu[path] = {'name': name, 'path': path, 'parent': None}
            self.menu = menu
            urls = response.css("div.wrapper-for-dropdown ul.topmenus li.topmenus-item a::attr(href)").getall()
            for url in urls:
                next_page = response.urljoin(url)
                yield scrapy.Request(next_page, callback=self.parse)
