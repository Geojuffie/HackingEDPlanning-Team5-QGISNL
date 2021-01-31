import os

from qgis.PyQt.QtWidgets import QAction, QMessageBox
from qgis.PyQt.uic import loadUi

from qgis.PyQt.QtGui import QIcon

from qgis.gui import (
    QgsMapLayerComboBox,
    QgsFieldComboBox
)
from qgis.core import (
    QgsVectorLayer
)




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


    def update_field_combo(self):
        layer = self.calculate_ages_dialog.combo_pop_layer.currentLayer()
        if isinstance(layer, QgsVectorLayer):
            self.calculate_ages_dialog.combo_pop_name.setLayer(layer)
        else:
            print('here :)')
            self.calculate_ages_dialog.combo_pop_name.clear()
