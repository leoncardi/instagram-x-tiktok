import sqlite3
import pandas as pd

from utils import(
    ChartWrangler, 
    TableWrangler
)
dvc = 'v20240910-231504-GMT3'

raw_db = f'research/data/raw/raw_init_data_{dvc}.db'
transformed_db = f'research/data/interim/prep_init_data_{dvc}.db'

conn = sqlite3.connect(raw_db)

tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
tables = [table[0] for table in tables]

dfs = {'ig_table': [], 'ig_chart': [], 'tk_table': [], 'tk_chart': []}

for table in tables:
    for key in dfs.keys():
        if f'raw_{key}' in table:
            dfs[key].append(pd.read_sql_query(f'SELECT * FROM {table}', conn))

ig_table_df = pd.concat(dfs['ig_table'], ignore_index=True)
ig_chart_df = pd.concat(dfs['ig_chart'], ignore_index=True)
tk_table_df = pd.concat(dfs['tk_table'], ignore_index=True)
tk_chart_df = pd.concat(dfs['tk_chart'], ignore_index=True)

raw_ig_table_0 = ig_table_df.iloc[:, [1]].copy()
raw_ig_table_4 = ig_table_df.iloc[:, [5]].copy()
raw_ig_table_5 = ig_table_df.iloc[:, [6]].copy()
raw_ig_table_6 = ig_table_df.iloc[:, [7]].copy()
raw_ig_chart_0 = ig_chart_df.iloc[:, [1]].copy()
raw_ig_chart_1 = ig_chart_df.iloc[:, [2]].copy()

raw_tk_table_0 = tk_table_df.iloc[:, [1]].copy()
raw_tk_table_3 = tk_table_df.iloc[:, [4]].copy()
raw_tk_table_6 = tk_table_df.iloc[:, [7]].copy()
raw_tk_table_7 = tk_table_df.iloc[:, [8]].copy()
raw_tk_chart_0 = tk_chart_df.iloc[:, [1]].copy()
raw_tk_chart_1 = tk_chart_df.iloc[:, [2]].copy()
raw_tk_chart_2 = tk_chart_df.iloc[:, [3]].copy()

ig_tables = [raw_ig_table_0, raw_ig_table_4, raw_ig_table_5, raw_ig_table_6]
ig_charts = [raw_ig_chart_0, raw_ig_chart_1]

tk_tables = [raw_tk_table_0, raw_tk_table_3, raw_tk_table_6, raw_tk_table_7]
tk_charts = [raw_tk_chart_0, raw_tk_chart_1, raw_tk_chart_2]

ig_tables = TableWrangler.apply_wrangler_ig(ig_tables)
ig_charts = ChartWrangler.apply_wrangler(ig_charts)

tk_tables = TableWrangler.apply_wrangler_tk(tk_tables)
tk_charts = ChartWrangler.apply_wrangler(tk_charts)

transf_conn = sqlite3.connect(transformed_db)
#ig_tables[0].to_sql('ig_overview', transf_conn, if_exists='replace', index=False)
#ig_tables[1].to_sql('ig_regions', transf_conn, if_exists='replace', index=False)
#ig_tables[2].to_sql('ig_ages_bk', transf_conn, if_exists='replace', index=False)
#ig_tables[3].to_sql('ig_genders', transf_conn, if_exists='replace', index=False)

ig_charts[0].to_sql('ig_revs', transf_conn, if_exists='replace', index=False)
ig_charts[1].to_sql('ig_MAUs', transf_conn, if_exists='replace', index=False)

#tk_tables[0].to_sql('tk_overview', transf_conn, if_exists='replace', index=False)
#tk_tables[1].to_sql('tk_regions', transf_conn, if_exists='replace', index=False)
#tk_tables[2].to_sql('tk_ages_bk', transf_conn, if_exists='replace', index=False)
#tk_tables[3].to_sql('tk_genders', transf_conn, if_exists='replace', index=False)

tk_charts[0].to_sql('tk_revs', transf_conn, if_exists='replace', index=False)
tk_charts[1].to_sql('tk_MAUs', transf_conn, if_exists='replace', index=False)
#tk_charts[2].to_sql('tk_downlds', transf_conn, if_exists='replace', index=False)

transf_conn.close()
conn.close()
