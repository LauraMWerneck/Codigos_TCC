# Análise Comparativa de Métodos para Definição de Limiar na Detecção de Máquinas Paradas

Este repositório contém os códigos desenvolvidos para o meu Trabalho de Conclusão de Curso (TCC), apresentado ao Instituto Federal de Educação, Ciência e Tecnologia de Santa Catarina - Câmpus Florianópolis, como parte dos requisitos para obtenção do título de Engenheira em Eletrônica.

## Sobre o Trabalho
O trabalho busca aprimorar o monitoramento preditivo de máquinas industriais por meio da **definição de limiares para detecção de máquinas paradas**. Foram analisados dois métodos principais:

1. **Método Empírico**: Define um limiar global com base na análise das acelerações médias máximas e mínimas das máquinas monitoradas.
2. **Algoritmo de Otsu**: Segmenta os dados automaticamente para definir um limiar de detecção de operação ou inatividade das máquinas.

Os resultados mostraram que:
- O **limiar global** é mais eficiente para máquinas com aceleração moderada a alta.
- O **algoritmo de Otsu** apresenta maior precisão para máquinas com aceleração muito baixa, embora demande mais tempo de processamento.

Com essa abordagem, a empresa Dynamox pode otimizar seus recursos computacionais, reduzindo o processamento de dados irrelevantes e aumentando a precisão das análises.

## Códigos Disponíveis
Este repositório contém os seguintes scripts em Python:

### 1. `Analise_empirica_e_Otsu.py`
Este código implementa os dois métodos analisados no trabalho:
- **Remoção de Outliers**: Utiliza o método do desvio padrão para eliminar valores extremos dos dados de aceleração.
- **Cálculo do Limiar Global**: Baseia-se na média das acelerações máximas e mínimas após a remoção de outliers, determinando um valor fixo para separar máquinas ligadas de máquinas paradas.
- **Aplicação do Algoritmo de Otsu**: O algoritmo determina automaticamente um limiar ideal para segmentação dos dados.
- **Geração de Gráficos Interativos**: Usa a biblioteca Plotly para exibir visualmente os resultados, permitindo analisar o desempenho dos limiares calculados.

### 2. `Analise_Final.py`
Este script realiza a validação final dos limiares calculados e compara os resultados com um conjunto independente de amostras. Ele também:
- **Reprocessa os dados filtrando outliers**: Garante que os cálculos dos limiares sejam baseados em dados limpos.
- **Compara os limiares definidos**: Inclui a comparação entre o limiar global original, o limiar global reduzido em 30% e o limiar de Otsu.
- **Gera gráficos dinâmicos**: Apresenta os dados analisados e os limiares em gráficos interativos, facilitando a interpretação visual dos resultados.

## Resultados e Conclusões
Os experimentos mostraram que a definição de limiares é fundamental para evitar a análise de dados desnecessários e garantir maior confiabilidade na detecção de falhas. O uso combinado do **limiar global reduzido** e do **algoritmo de Otsu** pode proporcionar um monitoramento mais eficiente e econômico para empresas que utilizam sensores para controle preditivo.

## Autor
**Laura Martin da Silva Werneck**  
Instituto Federal de Educação, Ciência e Tecnologia de Santa Catarina - Câmpus Florianópolis  
Orientador: Prof. Robinson Pizzio, Dr.  
Coorientador: Lucas Sousa Feitosa, Esp.  
