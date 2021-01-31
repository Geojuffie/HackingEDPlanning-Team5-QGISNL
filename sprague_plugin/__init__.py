# encoding: utf-8
#-----------------------------------------------------------
# Copyright (C) 2021 Team QGIS-NL
#-----------------------------------------------------------
# Licensed under the terms of
# Creative Commons Legal Code
# CC0 1.0 Universal
#---------------------------------------------------------------------

from .sprague_plugin import SpraguePlugin

def classFactory(iface):
    return SpraguePlugin(iface)
