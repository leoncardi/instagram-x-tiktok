import asyncio

import entrymaven as emav
from playwright.async_api import async_playwright

from pom_scraper_utils.browser import BrowserHandler
from pom_scraper_utils.page import PageHandler
from pom_scraper_utils.resources import ChartScrapeHandler
from pom_scraper_utils.resources import TableScrapeHandler
from db_handler import SQLiteHandler

log_config = emav.Essentials()
generic_logger = log_config.gen(filename='scraper.log')
l = emav.l 

async def base(
    p: 'Playwright',
    page_id: str,
    target_url: str,
    raw_dataset_name: str
    ):

    browser, context = await BrowserHandler.launch(p)
    target_ph = PageHandler(page_id, context)
    await target_ph.new_page()
    await target_ph.goto(target_url)
    
    table_scraper = TableScrapeHandler(target_ph)
    chart_scraper = ChartScrapeHandler(target_ph)

    founded_tables = await table_scraper.multiple_target_finder(
        table_selector='footable_parent_',
        screenshot=False
    )
    
    founded_charts = await chart_scraper.multiple_target_finder(
        chart_selector='infogram-embed',
        screenshot=True
    )

    table_data = await table_scraper.multiple_table_scraper(tables=founded_tables)
    chart_data = await chart_scraper.multiple_barchart_scraper(iframes=founded_charts)  

    sql_handler = SQLiteHandler('database', 'raw.db')
    sql_handler.create_dataset_for_chart_data(
        extracted_data=chart_data,
        table_name=raw_dataset_name
    )

async def main():
    async with async_playwright() as p:
        try:
            l.info('[NEW SCRAPING SESSION STARTED]')
            #code
        finally:
            l.info('[CURRENT SCRAPING SESSION ENDED]')
if __name__ == '__main__':
    asyncio.run(main())