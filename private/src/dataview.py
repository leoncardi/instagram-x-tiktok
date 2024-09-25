def compute_statistics(df, column_name):
    """
    Calculate statistics and count outliers
    """
    Q1 = df[column_name].quantile(0.25)
    Q3 = df[column_name].quantile(0.75)
    IQR = Q3 - Q1
    outliers = df[(df[column_name] < (Q1 - 1.5 * IQR)) | (df[column_name] > (Q3 + 1.5 * IQR))]

    stats = {
        'mean': df[column_name].mean(),
        'std': df[column_name].std(),
        'max': df[column_name].max(),
        'Q3': Q3,
        'median': df[column_name].median(),
        'Q1': Q1,
        'min': df[column_name].min(),
        'n_count': len(df),
        'outliers_count': len(outliers)
    }
    return stats

def format_value(value):
    """
    Format value to integer or float with 2 decimal places
    """
    return f'{value:.0f}' if value.is_integer() else f'{value:.2f}'

def plot_boxplot(self):
    """
    Generate boxplot and add text
    """
    plt.figure(figsize=(15, 6))
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray', alpha=0.2)
    plt.boxplot(self.data, patch_artist=True, tick_labels=self.labels, medianprops={'color': '#007BFF'}, boxprops={'facecolor': 'white'}, widths=0.2)
    plt.ylabel('values (mm)')
    plt.title('Quantitative Overview: Continuous data')

    for i, label in enumerate(self.labels):
        y_pos = max(self.data[i]) * 1.05 if max(self.data[i]) * 1.05 < plt.ylim()[1] else max(self.data[i]) * 0.60
        plt.text(
            i + 1.12, y_pos,
            f'n: {self.stats[i]["n_count"]}\n'
            f'outliers: {self.stats[i]["outliers_count"]}\n\n' 
            f'max: {self.format_value(self.stats[i]["max"])}\n'
            f'3rd-Q: {self.format_value(self.stats[i]["Q3"])}\n'
            f'median: {self.format_value(self.stats[i]["median"])}\n'
            f'1st-Q: {self.format_value(self.stats[i]["Q1"])}\n'
            f'min: {self.format_value(self.stats[i]["min"])}\n\n'
            f'mean: {self.stats[i]["mean"]:.2f}\n'
            f'std: {self.stats[i]["std"]:.2f}\n'
            f'cv: {round(self.stats[i]["std"] / self.stats[i]["mean"] * 100)}%', 
            ha='left', va='bottom', fontsize=10,
            bbox=dict(facecolor='white', alpha=0.7, edgecolor='black', boxstyle='round,pad=0.3')
        )

    plt.tight_layout()
    plt.show()

def print_statistics(self):
    """
    Print statistics
    """
    for i, label in enumerate(self.labels):
        print(
            f'\n{label}\n'
            f'n: {self.stats[i]["n_count"]}\n'
            f'outliers: {self.stats[i]["outliers_count"]}\n\n'
            f'max: {self.format_value(self.stats[i]["max"])}\n'
            f'3rd-Q: {self.format_value(self.stats[i]["Q3"])}\n'
            f'median: {self.format_value(self.stats[i]["median"])}\n'
            f'1st-Q: {self.format_value(self.stats[i]["Q1"])}\n'
            f'min: {self.format_value(self.stats[i]["min"])}\n\n'
            f'mean: {self.stats[i]["mean"]:.2f}\n'
            f'std: {self.stats[i]["std"]:.2f}\n'
            f'cv: {round(self.stats[i]["std"] / self.stats[i]["mean"] * 100)}%\n'
            '\n-       -       -'
        )

    def process_datasets(self, column_name='value(mm)'):
        """
        Process all datasets and compute statistics
        """
        for dt in self.datasets:
            df = pd.read_sql_query(f"SELECT * from {dt[0]}", self.conn)
            self.labels.append(dt[0])
            self.data.append(df[column_name])
            self.stats.append(self.compute_statistics(df, column_name))
        
        self.plot_boxplot()
        #self.print_statistics()

# Instanciação e processamento
# Exemplo: datasets = [('dataset1',), ('dataset2',)]
# conn é a conexão com o banco de dados, por exemplo, uma conexão SQLite.






statistics = DataStatistics(datasets, conn)
statistics.process_datasets()






import numpy as np

# Definir o número de amostras
num_amostras = 1000

# Gerar uma variável quantitativa contínua com distribuição normal
# Parâmetros: média=0, desvio padrão=1, número de amostras=num_amostras
variavel_continua = np.random.normal(loc=0, scale=1, size=num_amostras)

# Exibir os primeiros 10 valores gerados
print(variavel_continua[:10])


