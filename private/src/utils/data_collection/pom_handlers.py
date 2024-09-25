from entrymaven import l

class BrowserObject:
    @staticmethod
    async def launch_chromium(p):
        try:
            chromium_browser = await p.chromium.launch()
            l.info('(Scraper) Browser launched')
            standard_context = await chromium_browser.new_context()
            l.info('(Scraper) Context created')
            return standard_context
        except Exception as e:
            l.error(f'(BrowserObject.launch) {e}')
            raise e 
        
class PageObject:
    def __init__(
            self, 
            page_id: str, 
            context: 'ContextObject'):
        self.page_id = page_id
        self.context = context
        self.page = None

    async def new_page(self):
        try:
            self.page = await self.context.new_page()
            l.info(f'(Scraper: {self.page_id}) Page {self.page_id} created in the context')
        except Exception as e:
            l.error(f'(PageObject.new_page) {e}')
    
    async def goto(self, url):
        try:
            await self.page.goto(url)
            l.info(f'(Scraper: {self.page_id}) Reached {self.page.url}')
            
            if self.page.url != url:
                l.warning(f'(Scraper: {self.page_id}) Reached {self.page.url}')                      
        except Exception as e:
            l.error(f'(PageObject.goto) {e}')
        
    async def popup_checkout(self):
        identificable_popups = ['#brave_popup_70278__step__0']
        try:
            try:
                l.info(f'(Scraper: {self.page_id}) Waiting for any popup to appear in order to close it')
                await self.page.wait_for_timeout(2000)
                for popup in identificable_popups:
                    if await self.page.locator(popup).count() > 0:
                        l.info(f'(Scraper: {self.page_id}) A popup was raised and subsequently closed by automation')
                        await self.page.locator(popup).get_by_role('img').first.click()

                l.info(f'(Scraper: {self.page_id}) A popup was raised and subsequently closed by automation')
            except:
                l.info(f'(Scraper: {self.page_id}) No identifiable popup type was raised')
        except Exception as e:
            l.error(f'(PageObject.popup_checkout) {e}')
        
    async def close(self):
        try:
            self.page = await self.page.close()
            l.info(f'(Scraper: {self.page_id}) Page disposed')
        except Exception as e:
            l.error(f'(PageObject.close) {e}')
