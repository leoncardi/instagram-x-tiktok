from entrymaven import l

class ChartScrapeHandler:
        def __init__(self, page_handler: 'PageHandlerObject'):
            self.page_handler = page_handler
            self.page = page_handler.page
            self.page_id = page_handler.page_id
            self.founded_iframes_selectors = []
            self.SELECTOR_IFRAME = 'iframe[title="{iframe_title_goes_here}"]'
            self.raw_data = []

        async def multiple_target_screenshot(self, target, title):
            await target.scroll_into_view_if_needed()
            await self.page.wait_for_timeout(2000)     
            await target.screenshot(path=f'database/raw_targets_screenshots/{title}.jpg')
            l.info(f'(Page: {self.page_id}) Moved to chart and screenshot of the target {title} captured successfully')

        async def multiple_target_finder(self, target_classname: str, screenshot: bool) -> list:
            founded_targets = await self.page.query_selector_all(f'.{target_classname}') 
            for target in founded_targets:
                selector = self.SELECTOR_IFRAME 
                title = await target.get_attribute('data-title')                 
                iframe_selector = selector.format(iframe_title_goes_here=title)
                self.founded_iframes_selectors.append(iframe_selector)          
                
                if screenshot == False:
                    await target.scroll_into_view_if_needed()
                    await self.page.wait_for_timeout(2000)  
                    
                else:
                    await self.multiple_target_screenshot(target, title)
            return self.founded_iframes_selectors

        async def multiple_barchart_scraper(self, iframes: list) -> list:
            for iframe in iframes:
                iframe_title = f'iframe: {await self.page.frame_locator(iframe).locator("title").inner_text()}'
                self.raw_data.append(iframe_title) 
                
                counter = await self.page.frame_locator(iframe).locator('.igc-graph .igc-column').all()
                qtd = len(counter) + 1
                
                l.info(f'(Page: {self.page_id}) barchart ({iframe_title}) webscraping started')   
                for i in range(1, qtd):
                    await self.page.frame_locator(iframe).locator(f'path:nth-child({i})').hover()
                    await self.page.wait_for_timeout(500)

                    time_series_category = await self.page.frame_locator(iframe).locator('.tt_text').inner_text()
                    time_series_value = await self.page.frame_locator(iframe).locator('.tt_value').inner_text()
                    
                    collected_data_point = f'{time_series_category}: {time_series_value}'
                    l.info(f'(Page: {self.page_id}) time series raw data point extracted: {time_series_category} - {time_series_value}')
                
                    self.raw_data.append(collected_data_point)
                l.info(f'(Page: {self.page_id}) barchart ({iframe_title}) webscraping done successfully')
            l.info(f'(Page: {self.page_id}) All barchart webscraping ended')
            return self.raw_data