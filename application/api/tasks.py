from project.celery import app
from crawling.crawlers import crawl
from crawling.spiders import products, sections, test


def initial_settings():
    pass

@app.task(ignore_result=True)
def products_crawl():
    crawl(products.WildberriesSpider)


@app.task(ignore_result=True)
def sections_crawl():
    crawl(sections.WildberriesSpider)


@app.task(ignore_result=True)
def test_crawl():
    crawl(test.QuotesSpider)
