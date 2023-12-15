import asyncio
from playwright.async_api import async_playwright

import entrymaven as emav
from pom_scraper_utils.browser import BrowserHandler as bh
from pom_scraper_utils.page import PageHandler

log_config = emav.Essentials()
generic_logger = log_config.gen(filename='ELT.log')
l = emav.l

async def main():
    async with async_playwright() as p:
        try:
            browser, context = await bh.launch(p)    
            gram_ph = PageHandler('Instagram', context)
            await gram_ph.new_page()     
            await gram_ph.goto('https://www.businessofapps.com/data/instagram-statistics/')
        except Exception as e:
            l.error(f'(main) {e}')
            raise e
        
asyncio.run(main())