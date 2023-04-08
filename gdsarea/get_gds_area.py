#!/usr/bin/env python3
import gdspy


def get_gds_area(file, top_cell_name=None):
    gds = gdspy.GdsLibrary().read_gds(file)
    if top_cell_name is None:
        top_cells = gds.top_level()
    else:
        if top_cell_name not in gds.cells.keys():
            # raise ValueError("Top cell name not found in GDS file")
            return {"No such cells": [(0, 0), ]}, ValueError("Top cell name not found in GDS file")
        top_cells = [gds.cells[top_cell_name]]

    areas_by_cell_name = {}
    for cell in top_cells:
        d = cell.area(by_spec=True)
        areas_by_layer = sorted(d.items(), key=lambda x: x[0][0])
        areas_by_layer.append(("Total area", cell.area()))
        areas_by_cell_name[cell.name] = areas_by_layer

    return areas_by_cell_name, None
