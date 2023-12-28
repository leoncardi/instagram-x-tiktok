from entrymaven import l

class ScrapeHandlerUtils:
    @staticmethod
    async def multi_target_screenshot(page: 'PageObject', page_id: 'PageObject.page_id',
            target: str, title: str, load: bool = True):
        try:
            await target.scroll_into_view_if_needed()
            
            if load:
                for i in range(1, 3):
                    await page.wait_for_timeout(1000)
                    l.info(f'(Scraper: {page_id}) Waiting for {title} ({i}/2 seconds)')
            
            await target.screenshot(path=f'database/raw_data_screenshots/{title}.jpg')
            l.info(f'(Scraper: {page_id}) Attempt to take a screenshot of the {title} element')
        except Exception as e:
            l.error(f'(Scraper: {page_id}) {e}')

class TableScrapeHandler:
    def __init__(self, page_handler: 'PageHandlerObject'):
        self.page_handler = page_handler
        self.page = page_handler.page
        self.page_id = page_handler.page_id
        self.table_selector: str = None
        self.founded_tables = []
        self.raw_tables_data = []

    async def multi_table_finder(self, table_selector: str, screenshot: bool = True) -> list:
        founded_tables = await self.page.query_selector_all(f"div [id^='{table_selector}'] table")   
        for target in founded_tables:
            try:
                aria_label = await target.get_attribute('aria-label')
                l.info(f'(Scraper: {self.page_id}) Table founded by aria-label: {aria_label}') 

                if screenshot:
                    screenshot_file_name = f"{aria_label.replace(' ', '_')}"
                    await ScrapeHandlerUtils.multi_target_screenshot(page=self.page, page_id=self.page_id,
                        target=target, title=screenshot_file_name)
                    
            except Exception as e:
                l.error(f'(Scraper: {self.page_id} | TableScrapeHandler.multi_table_finder) {e}')
                l.warning(f'(Scraper: {self.page_id} | TableScrapeHandler.multi_table_finder) Table finder may not have been completed successfully. Returning founded tables so far')
                return founded_tables
        return founded_tables

    async def multi_table_scraper(self, tables: list) -> list:
        for table in tables:
            try:
                single_table_raw_data = []
                datapoints = await table.query_selector_all('tr')
                num_columns = 0
                
                for datapoint in datapoints:
                    columns = await datapoint.query_selector_all('td')
                    if len(columns) > num_columns:
                        num_columns = len(columns)
                
                for datapoint in datapoints:
                    row_content = ""
                    columns = await datapoint.query_selector_all('td')
                    
                    for col in range(num_columns):
                        if col < len(columns):
                            col_content = await columns[col].inner_text()
                            row_content += col_content + "|_|"
                        else:
                            row_content += "|_|"             
                    row_content = row_content[:-3]
                    single_table_raw_data.append(row_content)
                    
                    if "|_|" in row_content:
                        l.info(f"(Scraper: {self.page_id}) Table raw data point extracted: {row_content}")
                    else:
                        l.warning(f"(Scraper: {self.page_id}) Chart raw data point may not extracted correctly: {row_content}")
                
                self.raw_tables_data.append(single_table_raw_data)
            except Exception as e:
                l.error(f'(Scraper: {self.page_id}) {e}')
                l.warning(f'(Scraper: {self.page_id}) Table webscraping may not have been completed successfully')
        return self.raw_tables_data
class ChartScrapeHandler:
        def __init__(self, page_handler: 'PageHandlerObject'):
            self.page_handler = page_handler
            self.page = page_handler.page
            self.page_id = page_handler.page_id
            self.founded_iframes_selectors = []
            self.SELECTOR_IFRAME = 'iframe[title="{iframe_title_goes_here}"]'
            self.raw_data = []

        async def multiple_target_finder(self, chart_selector: str, screenshot: bool) -> list:
            founded_targets = await self.page.query_selector_all(f'.{chart_selector}') 
            for target in founded_targets:
                selector = self.SELECTOR_IFRAME 
                title = await target.get_attribute('data-title')                 
                iframe_selector = selector.format(iframe_title_goes_here=title)
                self.founded_iframes_selectors.append(iframe_selector)          
                
                if screenshot == False:
                    await target.scroll_into_view_if_needed()
                    await self.page.wait_for_timeout(2000)  
                else:
                    await ScrapeHandlerUtils.multiple_target_screenshot(
                        page = self.page,
                        target = target, 
                        title = title
                    )         
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