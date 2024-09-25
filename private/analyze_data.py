"""
This script is used to analyze the data and generate statistics.
"""
import matplotlib.pyplot as plt
import pandas as pd

def summarize_dataframe_quantidata(data):
    """
    Boxploting all continuous data in the dataframe and show statistics, all of this in one plot.
    """
    # Seleciona apenas as variáveis quantitativas contínuas
    data = data.select_dtypes(include=['float64', 'int64'])

    # Salva os nomes das colunas em uma lista
    data_labels = data.columns.tolist()

    plt.figure(figsize=(15, 6))
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray', alpha=0.2)
    plt.tight_layout()  
    plt.title('Quantitative Overview: Continuous data')
    plt.ylabel('Values')

    plt.boxplot(
        x = data, 
        patch_artist=True, 
        tick_labels=data_labels, 
        medianprops={'color': '#007BFF'}, 
        boxprops={'facecolor': 'white'}, 
        widths=0.2)
    
    plt.show()

if __name__ == '__main__':
    X1 = [10, 20, 30, 50, 90, 10, 20, 90, 90, 300]
    X2 = [100, 100, 30, 40, 90, 10, 30, 90, 90, 80]
    X3 = [90, 30, 40, 50, 100, 100, 40, 50, 40, 10]
    X4 = [-100, 20, 40, 60, 100, 100, 100, 50, 90, 80]
    
    df = pd.DataFrame(data = {'X1': X1, 'X2545455': X2, 'X3': X3, 'X4': X4})
    summarize_dataframe_quantidata(df)



import seaborn as sns
import matplotlib.pyplot as plt

# Exemplo com o dataset tips
tips = sns.load_dataset("tips")

# Cria um boxplot combinando a variável 'day' (dias da semana) e os valores de 'total_bill'
sns.boxplot(x="day", y="total_bill", data=tips)

# Exibe o gráfico
plt.show()

sns.boxplot(data=df)