from entrymaven import l

class BrowserHandler:
    @staticmethod
    async def launch_chromium(p):
        try:
            chromium_browser = await p.chromium.launch()
            l.info('(Scraper) Browser launched')
            standard_context = await chromium_browser.new_context()
            l.info('(Scraper) Context created')
            return standard_context
        except Exception as e:
            l.error(f'(BrowserHandler.launch) {e}')
            raise e 