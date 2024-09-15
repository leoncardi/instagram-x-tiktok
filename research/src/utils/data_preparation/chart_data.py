from datetime import datetime
import pandas as pd
from .splitter import splitter

class ChartWrangler:
    @staticmethod
    def quarter_converter(data_str):
        parts = data_str.split()
        quarter = int(parts[0].replace('Q', ''))
        year = int(parts[1])

        close_quarts_dates = {
            1: datetime(year, 3, 31).date(),
            2: datetime(year, 6, 30).date(),
            3: datetime(year, 9, 30).date(),
            4: datetime(year, 12, 31).date()
        }
        return close_quarts_dates[quarter]

    @staticmethod
    def apply_wrangler(charts):
        for i, chart in enumerate(charts):
            chart.dropna(inplace=True)

            chart[['quarter', 'value(mm)']] = chart[chart.columns[0]].apply(splitter) 
            chart['value(mm)'] = chart['value(mm)'].astype(float)
            
            chart.drop(chart.columns[0], axis=1, inplace=True)
            chart.drop(chart.index[0], inplace=True)
            chart.reset_index(drop=True, inplace=True)
            
            chart['quarter_date'] = chart['quarter'].apply(ChartWrangler.quarter_converter)
            chart['quarter_date'] = pd.to_datetime(chart['quarter_date'], errors='coerce')
             
            charts[i] = chart[['quarter_date', 'quarter', 'value(mm)']]
        return charts
    

if __name__ == '__main__':
    # Implementation Test/Demo
    data_example_1 = {'data': ['instagram example raw data', 'Q1 2001|_|123', 'Q2 2001|_|456']}
    data_example_2 = {'data': ['tiktok example raw data', 'Q1 2001|_|123', 'Q2 2001|_|456']}

    df1 = pd.DataFrame(data_example_1)
    df2 = pd.DataFrame(data_example_2)
    dfs = [df1, df2]
    test_demo = ChartWrangler.apply_wrangler(dfs)
    
    for t in test_demo:
        print('\n')
        print(t.head(2))
        print('-'*35)
        print(t.dtypes)
        print('\n')

    """Output:
        quarter_date  quarter  value(mm)
    0   2001-03-31  Q1 2001      123.0
    1   2001-06-30  Q2 2001      456.0
    -----------------------------------
    quarter_date    datetime64[ns]
    quarter                 object
    value(mm)              float64
    dtype: object




    quarter_date  quarter  value(mm)
    0   2001-03-31  Q1 2001      123.0
    1   2001-06-30  Q2 2001      456.0
    -----------------------------------
    quarter_date    datetime64[ns]
    quarter                 object
    value(mm)              float64
    dtype: object    
    """
