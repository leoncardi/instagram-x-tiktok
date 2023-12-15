from entrymaven import l

class BrowserHandler:
    @staticmethod
    async def launch(p):
        try:
            browser = await p.chromium.launch()
            l.info('Browser launched')
            context = await browser.new_context()
            l.info('Context created')
            return browser, context
        except Exception as e:
            l.error(f'(BrowserHandler.launch) {e}')
            raise e