import pandas as pd
from   skimage import filters
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

# --- Função para calcular o limiar de Otsu ---
def calculate_otsu_threshold(signal):
    """
    Calcula o limiar de Otsu.
    :param signal: Série ou array de dados.
    :return: Limiar de Otsu.
    """
    otsu_threshold = filters.threshold_otsu(signal.to_numpy())
    return otsu_threshold

def save_plot_html(fig, file_path, output_name):
    """
    Salva um gráfico em uma pasta específica como um arquivo HTML interativo.
    :param fig: Objeto Figure do Plotly.
    :param file_path: Caminho do arquivo Excel original (usado para determinar a pasta de saída).
    :param output_name: Nome do arquivo de saída (sem extensão).
    """
    output_dir = os.path.dirname(file_path)
    output_file = os.path.join(output_dir, f"{output_name}.html")
    fig.write_html(output_file)
    print(f"Gráfico salvo em: {output_file}")

def plot_signal(df, signal, threshold, threshold_30, otsu, title='', save_path=None):
    """
    Plota um gráfico discreto do sinal com linhas de referência, permitindo alternar entre pontos ou linha
    através da legenda de visibilidade.
    :param df: DataFrame contendo os dados.
    :param signal: Série ou array com o sinal a ser plotado.
    :param threshold: Valor do limiar principal.
    :param threshold_30: Valor do limiar reduzido em 30% do principal.
    :param otsu: Limiar de Otsu.
    :param title: Título do gráfico.
    :param save_path: Caminho para salvar o gráfico.
    """
    fig = go.Figure()

    # Pontos discretos do sinal (modo 'markers' - apenas pontos)
    fig.add_trace(go.Scatter(
        x=df['datetime'], 
        y=signal, 
        mode='markers', 
        name='Soma das Acelerações (Pontos)', 
        marker=dict(color='blue'),
        visible=True  # Inicia visível
    ))

    # Linha conectando os pontos (modo 'lines' - linha contínua)
    fig.add_trace(go.Scatter(
        x=df['datetime'], 
        y=signal, 
        mode='lines', 
        name='Soma das Acelerações (Linha)', 
        line=dict(color='blue', width=1),
        visible=True  # Inicia visível
    ))

    # Linhas de referência (Thresholds e Otsu)
    fig.add_trace(go.Scatter(
        x=df['datetime'], 
        y=[threshold] * len(df), 
        mode='lines', 
        name='Limiar Global', 
        line=dict(color='red', width=3)
    ))
    fig.add_trace(go.Scatter(
        x=df['datetime'], 
        y=[threshold_30] * len(df), 
        mode='lines', 
        name='Limiar Global Reduzido', 
        line=dict(color='green', width=3)
    ))
    fig.add_trace(go.Scatter(
        x=df['datetime'], 
        y=[otsu] * len(df), 
        mode='lines', 
        name='Limiar de Otsu', 
        line=dict(color='yellow', width=3)
    ))

    # Configuração do layout
    fig.update_layout(
        title=title,
        xaxis_title='Tempo',
        yaxis_title='Aceleração(g)',
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
file_path = 'C:/Users/laura/Dados/Amostra.xlsx'
# Carrega o arquivo Excel
df = pd.read_excel(file_path)
# Soma das acelerações
df['acceleration_sum'] = df['x_acceleration'] + df['y_acceleration'] + df['z_acceleration']
signal = df['acceleration_sum']
len_signal = len(df['acceleration_sum'])

# Definição dos valores de threshold
threshold = 0.18015
threshold_30 = 0.126105

# Remove os outliers
df_filtered = remove_outliers_std(df, 'acceleration_sum')
signal_filtered = df_filtered['acceleration_sum']
# Limiar de Otsu
otsu_trsh_filtered = calculate_otsu_threshold(signal_filtered)

print(f"Número total de pontos: {len_signal}")

print(f"Limiar de Otsu (Filtrado): {otsu_trsh_filtered}")

# Plota o gráfico original com as linhas de referência
plot_signal(df, signal, threshold, threshold_30, otsu_trsh_filtered, title="Análise Thresholds e Otsu", save_path=file_path)
