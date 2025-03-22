import pandas as pd
from skimage import filters
import plotly.graph_objects as go 
import os

# --- Função para remoção de outliers pelo método do desvio padrão ---
def remove_outliers_std(data, column, threshold=3):
    """
    Remove outliers com base no número de desvios padrão.
    :param data: DataFrame contendo os dados.
    :param column: Nome da coluna a ser analisada.
    :param threshold: Número de desvios padrão para definir os limites.
    :return: DataFrame filtrado.
    """
    mean = data[column].mean()            # Média dos dados
    std = data[column].std()              # Desvio padrão dos dados
    lower_limit = mean - threshold * std  # Limite inferior
    upper_limit = mean + threshold * std  # Limite superior
    return data[(data[column] >= lower_limit) & (data[column] <= upper_limit)]

# --- Função par acálculo da média da aceleração máxima e da média da aceleração minima ---
def calculate_statistics(signal, reference_value):
    """
    Calcula as médias dos valores superiores e inferiores a um valor de referência.
    :param signal: Série ou array de dados.
    :param reference_value: Valor de referência para separar os dados.
    :return: Médias dos valores superiores e inferiores.
    """
    superior_values = signal[signal > reference_value]
    inferior_values = signal[signal <= reference_value]
    mean_superior = superior_values.mean()
    mean_inferior = inferior_values.mean()
    return mean_superior, mean_inferior

# --- Função para calcular o limiar de Otsu ---
def calculate_otsu_threshold(signal):
    """
    Calcula o limiar de Otsu.
    :param signal: Série ou array de dados.
    :return: Limiar de Otsu.
    """
    otsu_threshold = filters.threshold_otsu(signal.to_numpy())
    return otsu_threshold

# --- Função para salvar os gráficos gerados na pasta do dado analisado ---
def save_plot_html(fig, file_path, output_name):
    """
    Salva um gráfico em uma pasta específica como um arquivo HTML interativo.
    :param fig: Objeto Figure do Plotly.
    :param file_path: Caminho do arquivo Excel original (usado para determinar a pasta de saída).
    :param output_name: Nome do arquivo de saída.
    """
    # Obtém o diretório do arquivo Excel
    output_dir = os.path.dirname(file_path)

    # Define o caminho completo para o arquivo de saída
    output_file = os.path.join(output_dir, f"{output_name}.html")

    # Salva o gráfico como HTML
    fig.write_html(output_file)
    print(f"Gráfico salvo em: {output_file}")

# --- Função para gerar os gráficos para análise ---
def plot_signal(df, signal, median=None, mean_superior=None, mean_inferior=None, otsu=None, title='', save_path=None):
    """
    Plota o gráfico do sinal com linhas de referência e opcionalmente salva como HTML.
    :param df: DataFrame contendo os dados.
    :param signal: Série ou array com o sinal a ser plotado.
    :param median: Mediana do sinal.
    :param mean_superior: Média dos valores superiores.
    :param mean_inferior: Média dos valores inferiores.
    :param otsu: Limiar de Otsu.
    :param title: Título do gráfico.
    :param save_path: Caminho para salvar o gráfico.
    """
    fig = go.Figure()

    # Linha do sinal
    fig.add_trace(go.Scatter(x=df['datetime'], y=signal, mode='lines', name='Soma das Acelerações', line=dict(color='blue')))

    # Linhas de referência
    fig.add_trace(go.Scatter(x=df['datetime'], y=[median] * len(df), mode='lines', name='Mediana', line=dict(color='green', dash='dash')))
    fig.add_trace(go.Scatter(x=df['datetime'], y=[mean_superior] * len(df), mode='lines', name='Média dos Superiores', line=dict(color='red', dash='dash')))
    fig.add_trace(go.Scatter(x=df['datetime'], y=[mean_inferior] * len(df), mode='lines', name='Média dos Inferiores', line=dict(color='yellow', dash='dash')))
    fig.add_trace(go.Scatter(x=df['datetime'], y=[otsu] * len(df), mode='lines', name='Limiar de Otsu', line=dict(color='darkmagenta', dash='dash')))

    # Configuração do layout
    fig.update_layout(
        title=title,
        xaxis_title='Tempo',
        yaxis_title='Aceleração (g)',
        legend_title='Legenda',
        template='plotly_white',
        xaxis=dict(tickangle=45),
        margin=dict(l=50, r=50, t=50, b=50)
    )

    # Exibição do gráfico
    fig.show()

    # Salva o gráfico como HTML, se o caminho for fornecido
    if save_path:
        save_plot_html(fig, save_path, title.replace(' ', '_'))


# Caminho para o arquivo com o dado a ser analisado
file_path = 'C:/Users/laura/Dados/Amostra_1.xlsx'
# Carrega o arquivo Excel
df = pd.read_excel(file_path)
# Soma das acelerações
df['acceleration_sum'] = df['x_acceleration'] + df['y_acceleration'] + df['z_acceleration']
signal = df['acceleration_sum']


# Análise com Outlier
# Cálculo da mediana
median_value = signal.median()
# Estatísticas
mean_superior, mean_inferior = calculate_statistics(signal, median_value)
# Limiar de Otsu
otsu_trsh = calculate_otsu_threshold(signal)

# Exibição dos resultados
print(f"Mediana: {median_value}")
print(f"Média dos valores superiores: {mean_superior}")
print(f"Média dos valores inferiores: {mean_inferior}")
print(f"Limiar de Otsu: {otsu_trsh}")

# Geração do gráfico
plot_signal(
    df, signal, 
    median = median_value, 
    mean_superior = mean_superior, 
    mean_inferior = mean_inferior, 
    otsu = otsu_trsh, 
    title = 'Soma das Acelerações vs. Tempo (Sinal Bruto)', 
    save_path = file_path
)


# Análise sem Outlier
# Remove os outliers
df_filtered = remove_outliers_std(df, 'acceleration_sum')
signal_filtered = df_filtered['acceleration_sum']
# Cálculo da mediana
median_value_filtered = signal_filtered.median()
# Estatísticas
mean_superior_filtered, mean_inferior_filtered = calculate_statistics(signal_filtered, median_value_filtered)
# Limiar de Otsu
otsu_trsh_filtered = calculate_otsu_threshold(signal_filtered)

# Exibição dos resultados
print(f"Mediana do Sinal (Filtrado): {median_value_filtered}")
print(f"Média dos valores inferiores (Filtrado): {mean_inferior_filtered}")
print(f"Média dos valores superiores (Filtrado): {mean_superior_filtered}")
print(f"Limiar de Otsu (Filtrado): {otsu_trsh_filtered}")

# Geração do gráfico
plot_signal(
    df_filtered, signal_filtered, 
    median=median_value_filtered, 
    mean_superior=mean_superior_filtered, 
    mean_inferior=mean_inferior_filtered, 
    otsu=otsu_trsh_filtered, 
    title='Soma das Acelerações vs. Tempo (Após Remoção de Outliers)', 
    save_path=file_path
)



