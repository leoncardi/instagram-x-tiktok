import os
import asyncio

from entrymaven import l, Essentials
from playwright.async_api import async_playwright

from utils import(
    AsyncSQLiteCommiter,
    BrowserObject,
    PageObject,
    ChartScrapeHandler,
    RawDVC
)




if __name__ == '__main__':
    project_root = os.getcwd()
    if os.path.exists(f'{project_root}/logs') == False:
        os.mkdir(f'{project_root}/logs')
    Essentials.gen(filename=f'{project_root}/logs/webscraping.log')

    
    async def main(): 
        async with async_playwright() as p:
            browser = await BrowserObject.launch_chromium(p)
            page = PageObject(page_id='Instagram', context=browser)

            await page.new_page()
            await page.goto('https://www.businessofapps.com/data/instagram-statistics/')


    asyncio.run(main())




    
if __name__ != '__main__':


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
