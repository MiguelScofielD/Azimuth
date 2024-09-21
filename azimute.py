from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterField,
    QgsProcessingParameterFeatureSink,
    QgsField,
    QgsFeature,
    QgsFeatureSink,
    QgsProcessingException
)
from qgis.PyQt.QtCore import QVariant
from math import atan2, degrees, floor

def dms(angulo):
    """Converte um ângulo em graus decimais para o formato DMS (graus, minutos, segundos)."""
    graus = floor(angulo)
    minutos = floor(abs(angulo - graus) * 60)
    segundos = round(abs(angulo - graus) * 3600) % 60
    return f"{graus}° {minutos}' {segundos}\""

class CalcularAzimuteAlg(QgsProcessingAlgorithm):
    INPUT = 'INPUT'
    FIELD = 'FIELD'
    OUTPUT = 'OUTPUT'

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT,
                'Camada de pontos',
                [QgsProcessing.TypeVectorPoint]
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                self.FIELD,
                'Campo id',
                type=QgsProcessingParameterField.Numeric,
                parentLayerParameterName=self.INPUT
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT,
                'Camada com Azimute'
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        layer = self.parameterAsSource(parameters, self.INPUT, context)
        id_field = self.parameterAsFields(parameters, self.FIELD, context)[0]

        # Configuração da camada de saída
        fields = layer.fields()
        fields.append(QgsField('Azimute', QVariant.String))  # Mudando para String

        (sink, dest_id) = self.parameterAsSink(parameters, self.OUTPUT, context,
                                               fields, layer.wkbType(), layer.sourceCrs())

        # Lista de coordenadas dos pontos
        features = list(layer.getFeatures())
        if len(features) < 2:
            raise QgsProcessingException('Camada precisa de pelo menos 2 pontos.')

        # Adiciona o azimute entre pontos consecutivos
        for i in range(len(features) - 1):
            feature_A = features[i]
            feature_B = features[i + 1]

            # Obtém coordenadas
            x_A, y_A = feature_A.geometry().asPoint()
            x_B, y_B = feature_B.geometry().asPoint()

            # Cálculo do azimute
            delta_x = x_B - x_A
            delta_y = y_B - y_A
            azimute = degrees(atan2(delta_x, delta_y))

            # Ajusta o azimute para ficar entre 0 e 360
            if azimute < 0:
                azimute += 360

            # Converte para DMS
            azimute_dms = dms(azimute)

            # Cria nova feição com azimute em DMS
            new_feature = QgsFeature(fields)
            new_feature.setGeometry(feature_A.geometry())
            new_feature.setAttributes(feature_A.attributes() + [azimute_dms])
            sink.addFeature(new_feature, QgsFeatureSink.FastInsert)

        # Para o último ponto, atribuímos '0° 0' 0"' como azimute
        last_feature = features[-1]
        new_feature = QgsFeature(fields)
        new_feature.setGeometry(last_feature.geometry())
        new_feature.setAttributes(last_feature.attributes() + ['0° 0\' 0"'])  # Último ponto com azimute 0.0
        sink.addFeature(new_feature, QgsFeatureSink.FastInsert)

        return {self.OUTPUT: dest_id}

    def name(self):
        return 'calcular_azimute'

    def displayName(self):
        return 'Calcular Azimute entre Pontos'

    def createInstance(self):
        return CalcularAzimuteAlg()
