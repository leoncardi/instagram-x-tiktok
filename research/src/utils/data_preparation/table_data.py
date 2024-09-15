import pandas as pd

from .splitter import splitter

class TableWrangler:
    """AD-HOC Approach to Wrangle Tables"""
    @staticmethod
    def apply_wrangler_ig(ig_tables):
        for index, table in enumerate(ig_tables):
            table.dropna(inplace=True)
            table[['category', 'value']] = table[table.columns[0]].apply(splitter)
            table.drop(table.columns[0], axis=1, inplace=True)
            table.drop(table.index[0], inplace=True)
            if index > 0:
                table['value'] = table['value'].astype(float)
            table.reset_index(drop=True, inplace=True)
        ig_tables[1].rename(columns={'category': 'region'}, inplace=True) # raw_ig_table_4
        ig_tables[2].rename(columns={'category': 'age_bk'}, inplace=True) # raw_ig_table_5
        ig_tables[3].rename(columns={'category': 'gender'}, inplace=True) # raw_ig_table_6
        ig_tables[2]['age_bk'] = ['18-24', '25-34', '35-44', '45-54', '55-64', '65+']
        return ig_tables

    @staticmethod
    def apply_wrangler_tk(tk_tables):
        for table in tk_tables:
            table.dropna(inplace=True)
            table[['category', 'value']] = table[table.columns[0]].apply(splitter)
            
            if table['value'].str.contains('%').any():
                table['value'] = table['value'].str.split('%').str[0]
            table.drop(table.columns[0], axis=1, inplace=True)
            table.drop(table.index[0], inplace=True)
            table.reset_index(drop=True, inplace=True)    
        
        tk_tables[1].reset_index(drop=True, inplace=True)
        tk_tables[1].drop(tk_tables[1].index[0], inplace=True)
        tk_tables[1].rename(columns={'category': 'year'}, inplace=True)
        tk_tables[2].rename(columns={'category': 'age_bk'}, inplace=True)
        tk_tables[3].rename(columns={'category': 'gender'}, inplace=True)
        years = tk_tables[1]['year'].copy()
        regions_tk = tk_tables[1]['value'].str.split(r'\|_\|', expand=True).copy()
        regions_tk.columns = ['APAC', 'NAMER', 'europe', 'LATAM', 'MENA']
        tk_tables[1] = pd.concat([years, regions_tk], axis=1)
        
        for index, col in enumerate(tk_tables[1].columns):
            if index > 0:
                tk_tables[1][col] = tk_tables[1][col].astype(float)
            else:
                tk_tables[1][col] = pd.to_datetime(tk_tables[1][col], format='%Y').dt.to_period('Y').dt.end_time
                tk_tables[1][col] = pd.to_datetime(tk_tables[1][col]).dt.date

        for table in (tk_tables[2], tk_tables[3]):
            table['value'] = table['value'].astype(float)
        return tk_tables
