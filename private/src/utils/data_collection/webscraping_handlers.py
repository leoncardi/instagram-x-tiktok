from entrymaven import l


class ScrapeHandlerUtils:
    @staticmethod
    async def target_screenshot(page: 'PageObject', page_id: 'PageObject.page_id',
                                      target: str, raw_dv: str, title: str, load: bool = True):
        try:
            await target.scroll_into_view_if_needed()

            if load:
                for i in range(1, 3):
                    await page.wait_for_timeout(1000)
                    l.info(f'(Scraper: {page_id}) Waiting for {title} ({i}/2 seconds)')

            await target.screenshot(path=f'research/data/raw/screenshots_raw_init_data_{raw_dv}/{title}.jpg')
            l.info(f'(Scraper: {page_id}) Attempt to take a screenshot of the {title} element')
        except Exception as e:
            l.error(f'(Scraper: {page_id}) {e}')


class ChartScrapeHandler:
    @staticmethod
    async def chart_finder(
        page: 'PageObject',
        page_id: 'PageObject.page_id',
        chart_selector: str,
        raw_dv: str,
        iframe_selector: str,
        screenshot: bool = True
    ) -> list:
        """
        Chart finder.
        """
        founded_iframes_selectors = []
        founded_charts = await page.query_selector_all(f'.{chart_selector}')
        for target in founded_charts:
            title = await target.get_attribute('data-title')
            iframe_selector = iframe_selector.format(barchart_iframe_title_goes_here=title)
            founded_iframes_selectors.append(iframe_selector)

            if screenshot:
                await ScrapeHandlerUtils.target_screenshot(page=page, page_id=page_id,
                                                                 target=target, raw_dv=raw_dv, title=title)
            else:
                await target.scroll_into_view_if_needed()
                await page.wait_for_timeout(2000)
        return founded_iframes_selectors

    @staticmethod
    async def barchart_scraper(page: 'PageObject', page_id: 'PageObject.page_id', barcharts: list) -> dict:
        """
        barcharts: list within iframes target selectors
        """
        scraped_barchart_data = {}
        for barchart in barcharts:
            try:
                barchart_iframe_title = f'{await page.frame_locator(barchart).locator("title").inner_text()}'

                columns_qtd = await page.frame_locator(barchart).locator('.igc-graph .igc-column').all()
                columns_qtd = len(columns_qtd) + 1

                l.info(f'(Scraper: {page_id}) Barchart ({barchart_iframe_title}) webscraping started')
                for i in range(1, columns_qtd):
                    await page.frame_locator(barchart).locator(f'path:nth-child({i})').hover()

                    target_time_series_category = await page.frame_locator(barchart).locator('.tt_text').inner_text()
                    target_time_series_value = await page.frame_locator(barchart).locator('.tt_value').inner_text()
          
                    # Add the extracted data to the dictionary
                    scraped_barchart_data[barchart_iframe_title] = {
                        'category': target_time_series_category,
                        'value': target_time_series_value
                    }

                    # To preview extracted data in the console and log file
                    datapoint_content = f'{target_time_series_category} ; {target_time_series_value}'

                    if not target_time_series_category or not target_time_series_value:
                        l.warning(f'(Scraper: {page_id}) Chart raw data point not extracted correctly: {datapoint_content}')
                    else:
                        l.info(f'(Scraper: {page_id}) Chart raw data point extracted: {datapoint_content}')
                l.info(f'(Scraper: {page_id}) Barchart ({barchart_iframe_title}) webscraping ended')
            except Exception as e:
                l.error(f'(Scraper: {page_id}) {e}')
                l.warning(f'(Scraper: {page_id}) Barchart webscraping may not have been completed successfully')
        l.info(f'(Scraper: {page_id}) All barchart webscraping ended')
        return scraped_barchart_data
