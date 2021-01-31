# encoding: utf-8
#-----------------------------------------------------------
# Copyright (C) 2021 Team QGIS-NL
#-----------------------------------------------------------
# Licensed under the terms of
# Creative Commons Legal Code
# CC0 1.0 Universal
#---------------------------------------------------------------------

from PyQt5.QtWidgets import QAction, QMessageBox

def classFactory(iface):
    return SpraguePlugin(iface)


class SpraguePlugin:
    def __init__(self, iface):
        self.iface = iface

    def initGui(self):
        self.action = QAction(u'Go!', self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        self.iface.addToolBarIcon(self.action)

    def unload(self):
        self.iface.removeToolBarIcon(self.action)
        del self.action

    def run(self):
        QMessageBox.information(None, u'Sprague plugin', u'Do something useful here')
