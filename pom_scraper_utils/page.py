from entrymaven import l

class PageHandler:
    def __init__(
            self, 
            page_id: str, 
            context: 'ContextObject'
        ):
        self.page_id = page_id
        self.context = context
        self.page: 'PageObject'

    async def new_page(self):
        try:
            self.page = await self.context.new_page()
            l.info(f'({self.page_id}) Page created')
        except Exception as e:
            l.error(f'(PageHandler.new_page) {e}')
            raise e
    
    async def goto(self, url):
        try:
            await self.page.goto(url)
            if self.page.url == url:
                l.info(f'({self.page_id}) Reached {self.page.url}')
            else:
                l.warning(f'({self.page_id}) Reached {self.page.url}')
        except Exception as e:
            l.error(f'(PageHandler.goto) {e}')
            raise e
        
    async def close(self):
        try:
            if self.page:
                self.page = await self.page.close()
                l.info(f'({self.page_id}) Page disposed')
            else:
                l.warning(f"({self.page_id}) Attempted (PageHandler.close), but there is no PageObject available for disposal")
        except Exception as e:
            l.error(f'(PageHandler.close) {e}')
            raise e