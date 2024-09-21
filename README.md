# Cálculo de Azimutes entre Pontos

Este projeto utiliza o QGIS Processing para calcular os azimutes entre pontos de uma camada shapefile do tipo ponto, ordenada com um campo ID.

## Funcionamento

O script realiza o cálculo dos azimutes entre pontos consecutivos em uma camada de entrada. Por exemplo, se a camada de entrada possui 5 pontos numerados de 1 a 5, os azimutes serão calculados da seguinte forma:

- Ponto inicial / Ponto final
  - 1 -> 2
  - 2 -> 3
  - 3 -> 4
  - 4 -> 5

## Pré-requisitos

- QGIS instalado
- Camada shapefile do tipo ponto com um campo ID

## Como Usar

1. Carregue sua camada shapefile no QGIS.
2. Execute o script de cálculo de azimutes.
3. Os resultados serão exibidos na tabela de atributos da camada de saída.

