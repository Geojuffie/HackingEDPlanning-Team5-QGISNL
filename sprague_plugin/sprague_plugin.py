import os

from PyQt5.QtWidgets import QAction, QMessageBox
from qgis.PyQt.QtGui import QIcon




class SpraguePlugin:

    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        print(self.plugin_dir)


    def initGui(self):
        icon_fn = os.path.join(self.plugin_dir, 'iiep_logo.png')
        icon = QIcon(icon_fn)
        self.action = QAction(icon, 'Open Sprague panel', self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        self.iface.addToolBarIcon(self.action)


    def unload(self):
        self.iface.removeToolBarIcon(self.action)
        del self.action


    def run(self):
        QMessageBox.information(None, u'Sprague plugin', u'Do something useful here')
