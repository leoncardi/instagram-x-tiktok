# setup
import sqlite3
import pandas as pd

conn = sqlite3.connect('data.db')
c = conn.cursor()

# puxar dados do banco de dados
ig_MAUs = pd.read_sql_query("SELECT * FROM ig_MAUs", conn)
ig_revs = pd.read_sql_query("SELECT * FROM ig_revs", conn)

# combine ig_MAUs e revs
ig = pd.merge(ig_MAUs, ig_revs, on='quarter_date', how='outer')

# renomear colunas
ig = ig.rename(columns={'value(mm)_x': 'maus(mm)', 'value(mm)_y': 'revenue($mm)'})

# deletar coluna quarter_y
ig = ig.drop(columns=['quarter_y'])

ig = ig.tail(21)

# resetar o index
ig = ig.reset_index(drop=True)

ig = ig.rename(columns={'quarter_date': 'quarter_datetime', 'quarter_x': 'quarter_label'})

# exportar para csv
ig.to_csv('ig_data.csv', index=False)



# puxar dados do banco de dados
tk_MAUs = pd.read_sql_query("SELECT * FROM tk_MAUs", conn)
tk_revs = pd.read_sql_query("SELECT * FROM tk_revs", conn)

# combine tk_MAUs e revs
tk = pd.merge(tk_MAUs, tk_revs, on='quarter_date', how='outer')

# renomear colunas
tk = tk.rename(columns={'value(mm)_x': 'maus(mm)', 'value(mm)_y': 'revenue($mm)'})

# deletar coluna quarter_y
tk = tk.drop(columns=['quarter_y'])

tk = tk.tail(21)

# resetar o index
tk = tk.reset_index(drop=True)

tk = tk.rename(columns={'quarter_date': 'quarter_datetime', 'quarter_x': 'quarter_label'})

# exportar para csv
tk.to_csv('tk_data.csv', index=False)