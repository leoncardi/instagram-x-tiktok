import os
import asyncio

from entrymaven import l, Essentials
from playwright.async_api import async_playwright

from utils import(
    AsyncSQLiteCommiter,
    BrowserObject,
    PageObject,
    TableScrapeHandler,
    ChartScrapeHandler,
    RawDVC
)

async def scraper_base(context: 'PlaywrightContextOjbect',
        page_id: str, target_url: str, raw_dv: str) -> (list, list):
    
    target_ph = PageObject(page_id, context)
    await target_ph.new_page()
    await target_ph.goto(target_url)
    await target_ph.popup_checkout()
    
    table_scraper = TableScrapeHandler(target_ph)
    chart_scraper = ChartScrapeHandler(target_ph)

    founded_tables = await table_scraper.multi_table_finder(table_selector='footable_parent_', raw_dv=raw_dv, screenshot=True) 
    founded_charts = await chart_scraper.multi_chart_finder(chart_selector='infogram-embed', raw_dv=raw_dv, screenshot=True)

    raw_table_data = await table_scraper.multi_table_scraper(tables=founded_tables)
    raw_chart_data = await chart_scraper.multi_chart_scraper(charts=founded_charts)

    await target_ph.close()
    return raw_table_data, raw_chart_data

async def single_loader_base(raw_dataset_name: str, data: list, 
        data_type: str, asql_c: AsyncSQLiteCommiter):
    for i, item in enumerate(data):
        item_name = f'{raw_dataset_name}_{data_type}_{i}'
        
        await asql_c.create_table(item_name)
        await asql_c.insert_extracted_raw_data([item], item_name)
    l.info(f'(Database: {asql_c.db_file_name}.db) All expected attempted {data_type}s from {raw_dataset_name} datapoints commit ended')

async def multi_loader_base(asql_c: AsyncSQLiteCommiter, raw_dataset_name: str, 
        tables_data: list, charts_data: list):
    l.info(f'(Database: {db_file_name}.db) Attempting to commit all target data')

    await single_loader_base(raw_dataset_name, tables_data, 'table', asql_c)
    await single_loader_base(raw_dataset_name, charts_data, 'chart', asql_c)

    l.info(f'(Database: {db_file_name}.db) All attempted expected target data commit ended') 

async def scraper_main(raw_dv) -> list:
    async with async_playwright() as p:
        browser_context = await BrowserObject.launch_chromium(p)      
        #tasks = [scraper_base(browser_context, page_id, target_url) for page_id, target_url in zip(pages_id, targets_url)]
        tasks = [scraper_base(browser_context, page_id, target_url, raw_dv) for page_id, target_url in zip(pages_id, targets_url)]
        extracted_raw_data = await asyncio.gather(*tasks)
        return extracted_raw_data

async def loader_main(db_file_name: str, extracted_raw_data: list):
    async with AsyncSQLiteCommiter('research/data/raw', db_file_name) as asql_c:
        tasks = [multi_loader_base(asql_c, raw_dataset_name, table_data, chart_data) for raw_dataset_name, (table_data, chart_data) 
            in zip(raw_dataset_names, extracted_raw_data)]
        await asyncio.gather(*tasks)
    
if __name__ == '__main__':
    project_root = os.getcwd()
    if os.path.exists(f'{project_root}/logs') == False:
        os.mkdir(f'{project_root}/logs')
    Essentials.gen(filename=f'{project_root}/logs/webscraping.log')

    pages_id = ['Instagram', 'TikTok']
    targets_url = ['https://www.businessofapps.com/data/instagram-statistics/', 'https://www.businessofapps.com/data/tik-tok-statistics/']

    raw_dataset_names = ['raw_ig', 'raw_tk']
    
    db_file_prefix = 'raw_init_data'
    raw_dv = RawDVC.generate_raw_data_version_name()
    db_file_name = f'{db_file_prefix}_{raw_dv}'

    l.info('[NEW WEBSCRAPING SESSION STARTED]')
    extracted_raw_data = asyncio.run(scraper_main(raw_dv))
    asyncio.run(loader_main(db_file_name=db_file_name, extracted_raw_data=extracted_raw_data))
    l.info('[ACTUAL WEBSCRAPING SESSION ENDED]')
