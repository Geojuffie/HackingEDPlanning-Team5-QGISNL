import os

from qgis.PyQt.QtWidgets import QAction, QMessageBox
from qgis.PyQt.uic import loadUi

from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtCore import QVariant

from qgis.gui import (
    QgsMapLayerComboBox,
    QgsFieldComboBox
)
from qgis.core import (
    QgsVectorLayer,
    QgsField,
    QgsProject,
    QgsFeature
)

from .sprague import Sprague




class SpraguePlugin:

    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        print(self.plugin_dir)


    def initGui(self):
        icon_fn = os.path.join(self.plugin_dir, 'iiep_logo.png')
        icon = QIcon(icon_fn)
        self.action = QAction(icon, 'Open Sprague dialog', self.iface.mainWindow())
        self.action.triggered.connect(self.show_calculate_ages_dialog)
        self.iface.addToolBarIcon(self.action)

        calculate_ages_ui_fn = os.path.join(self.plugin_dir, 'calculate_ages.ui')
        self.calculate_ages_dialog = loadUi(calculate_ages_ui_fn)
        self.calculate_ages_dialog.buttonBox.accepted.connect(self.calculate_ages)
        self.calculate_ages_dialog.combo_pop_layer.layerChanged.connect(self.update_field_combo)

        self.update_field_combo()


    def unload(self):
        self.calculate_ages_dialog.combo_pop_layer.layerChanged.disconnect(self.update_field_combo)
        self.iface.removeToolBarIcon(self.action)
        del self.action


    def show_calculate_ages_dialog(self):
        self.calculate_ages_dialog.show()


    def calculate_ages(self):
        print('calculate_ages()')

        src_layer = self.calculate_ages_dialog.combo_pop_layer.currentLayer()
        print(src_layer)

        self.src_name_field = self.calculate_ages_dialog.combo_name.currentText()
        print(self.src_name_field)

        genders = self.calculate_ages_dialog.combo_gender.currentText()
        entry_age = self.calculate_ages_dialog.spinBox_entry_age.value()
        duration = self.calculate_ages_dialog.spinBox_duration.value()

        self.output_categories = {}
        self.output_categories['age_cat_1'] = [entry_age, duration, genders]
        self.output_categories['age_cat_2'] = [10, 4, 'M']

        self.create_result_layer("age_calculation_result")

        self.age_group_fields = self.find_age_group_fields(src_layer, genders)
        print(self.age_group_fields)

        ages = [k for k in self.age_group_fields]
        ages.sort()
        for age in ages:
            print(age, self.age_group_fields[age])

        self.sprague_calculator = Sprague()

        if src_layer.selectedFeatureCount():
            for src_feat in src_layer.getSelectedFeatures():
                #print(src_feat)
                self.process_feature(src_feat)
        else:
            for src_feat in src_layer.getFeatures():
                #print(src_feat)
                self.process_feature(src_feat)

        for age_key, age_value in self.sprague_calculator.ages.items():
            print(age_key, round(age_value))


    def update_field_combo(self):
        layer = self.calculate_ages_dialog.combo_pop_layer.currentLayer()
        if isinstance(layer, QgsVectorLayer):
            self.calculate_ages_dialog.combo_name.setLayer(layer)
        else:
            print('here :)')
            self.calculate_ages_dialog.combo_name.clear()

        self.iface.mapCanvas().refreshAllLayers()


    def create_result_layer(self, name, addToMap=True, qml=None):
        featureType = 'Polygon?crs=' + self.iface.mapCanvas().mapSettings().destinationCrs().authid()
        layer = QgsVectorLayer(featureType, name, 'memory')

        provider = layer.dataProvider()

        fields = []
        fields.append(QgsField('id', QVariant.LongLong, 'int8'))
        fields.append(QgsField('name', QVariant.String))
        for cat_key in self.output_categories:
            fields.append(QgsField(cat_key, QVariant.LongLong, 'int8'))
        provider.addAttributes(fields)
        layer.updateFields()

        if addToMap:
            QgsProject.instance().addMapLayer(layer)

        if qml is not None:
            layer.loadNamedStyle(qml)

        self.dst_layer = layer
        self.dst_provider = provider


    def process_feature(self, src_feat):
        dst_feat = QgsFeature()
        dst_feat.setGeometry(src_feat.geometry())
        attributes = [0]
        attributes.append(src_feat[self.src_name_field])

        age_group_values = self.get_values_for_age_groups(src_feat)
        print(age_group_values)

        self.sprague_calculator.set_by_age_groups(age_group_values, max_age=15)

        for cat_key in self.output_categories:
            entry_age = self.output_categories[cat_key][0]
            duration = self.output_categories[cat_key][1]
            pop_value = self.sprague_calculator.get_population_for_ages(entry_age, duration)
            attributes.append(pop_value)
        dst_feat.setAttributes(attributes)

        self.dst_provider.addFeatures([dst_feat])


    def find_age_group_fields(self, src_layer, genders):
        result = {}
        for field in src_layer.fields():
            print(field.name())
            parts = field.name().split('_')
            if len(parts) < 2:
                continue
            if parts[0].upper() in genders:
                age = int(parts[1])
                if age == 1:
                    age = 0
                if age in result:
                    result[age].append(field.name())
                else:
                    result[age] = [field.name()]
        return result


    def get_values_for_age_groups(self, feat):
        result = {}
        for i in range(0, 80, 5):
            #print(i)
            if i in self.age_group_fields:
                total_pop = 0
                for fld in self.age_group_fields[i]:
                    total_pop += feat[fld]
                result[i] = [i, i+4, total_pop]
        return result
