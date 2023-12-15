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
            l.error(f'(new_page method) {e}')
            raise e
    
    async def goto(self, url):
        try:
            await self.page.goto(url)
            l.info(f'({self.page_id}) Reached {url}')
        except Exception as e:
            l.error(f'(goto method) {e}')
            raise e
        
    async def close(self):
        try:
            await self.page.close()
            l.info(f'({self.page_id}) Page disposed')
        except Exception as e:
            l.error(f'(close method) {e}')
            raise e