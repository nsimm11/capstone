#!/usr/bin/env python

###
### This file is generated automatically by SALOME v9.9.0 with dump python functionality
###

import sys
import numpy as np
import salome

salome.salome_init()
import salome_notebook
notebook = salome_notebook.NoteBook()
sys.path.insert(0, r'/home/noah/Downloads/SALOME-9.9.0-native-UB20.04-SRC/Capstone')

###
### SHAPER component
###

from salome.shaper import model

model.begin()
partSet = model.moduleDocument()
model.end()

###
### SHAPERSTUDY component
###

###
### GEOM component
###

import GEOM
from salome.geom import geomBuilder
import math
import SALOMEDS

def flatten(li):
	flat_li = [item for sublist in li for item in sublist]
	return flat_li

def calcDistTubeLocs(len_header, distTubeSpacing, num_distTubes, dia_distTubes):

	len_internal = (num_distTubes-1) * distTubeSpacing + 2*dia_distTubes/2

	len_external = (len_header - len_internal)/2

	x_locs = []

	for i in range(len(num_distTubes)):
		x_locs.append(len_external + dia_distTubes/2 + i * (distTubeSpacing))

	return x_locs

def buildSAME(dia_inlet, len_inlet, dia_header, len_header, num_distTubes, distTubeSpacing, dia_distTubes):

	geompy = geomBuilder.New()

	O = geompy.MakeVertex(0, 0, 0)
	OX = geompy.MakeVectorDXDYDZ(1, 0, 0)
	OY = geompy.MakeVectorDXDYDZ(0, 1, 0)
	OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)
	
	#Generate Inlet Pipe
	Cylinder_1 = geompy.MakeCylinder(O, OX, dia_inlet, len_inlet)

	#Generate Inlet Box
	Vertex_1 = geompy.MakeVertex(len_inlet, -0.089, -0.089)
	Vertex_2 = geompy.MakeVertex(0.04+len_inlet, 0.089, 0.089)
	Box_1 = geompy.MakeBoxTwoPnt(Vertex_1, Vertex_2)

	#Generate Header Pipe
	Vertex_3 = geompy.MakeVertex(0.04+len_inlet, 0, 0)
	Cylinder_2 = geompy.MakeCylinder(Vertex_3, OX, dia_header, len_header)

	distCylinder = []

	loc_distTube = calcDistTubeLocs(len_header, distTubeSpacing, num_distTubes, dia_distTubes)

	for i in range(len(num_distTubes)):
		Vertex = geompy.MakeVertex(loc_distTube[i], 0, (dia_header/2 - 0.01))
		Cylinder = geompy.MakeCylinder(Vertex, OZ, 0.01905, 0.1497)
		distCylinder.append(Cylinder)
	
	headerComps = [Cylinder_1, Box_1, Cylinder_2, distCylinder]
	headerComps = flatten(headerComps)
	Fuse_1 = geompy.MakeFuseList(headerComps, True, True)

	Vertex_7 = geompy.MakeVertex(0.5, -0.2, 0.2)
	Vertex_8 = geompy.MakeVertex(0, 0, -0.2)
	
	Vertex_1000 = geompy.MakeVertex(-1, 0, 0)
	Vector_1 = geompy.MakeVector(O, Vertex_1000)

	Box_2 = geompy.MakeBoxTwoPnt(Vertex_7, Vertex_8)

	vertex_cols = [[],[],[]]
	cut_cyls = [[],[],[]]
	fuse_cyls = [[],[],[]]

	col_x = [0.4082, 0.332, 0.2558]

	for i in range(1,6):
		for j in range(len(col_x)):
			new_vert = geompy.MakeVertex(col_x[j] + 0.00635, 0, 0.0508 + 0.0254*i)
			new_cut_cyls = geompy.MakeCylinder(new_vert, OX, 0.00635, 0.01905)
			new_fuse_cyls = geompy.MakeCylinder(new_vert, OX, 0.003175, 0.0195)
			
			vertex_cols[j].append(new_vert)
			cut_cyls[j].append(new_cut_cyls)
			fuse_cyls[j].append(new_fuse_cyls)
			
			new_vert = geompy.MakeVertex(col_x[j] - 0.00635, 0, 0.0508 + 0.0254*i)
			new_cut_cyls = geompy.MakeCylinder(new_vert, Vector_1, 0.00635, 0.01905)
			new_fuse_cyls = geompy.MakeCylinder(new_vert, Vector_1, 0.003175, 0.0195)
			
			vertex_cols[j].append(new_vert)
			cut_cyls[j].append(new_cut_cyls)
			fuse_cyls[j].append(new_fuse_cyls)

	flat_cut_cyls = [item for sublist in cut_cyls for item in sublist]
	Cut_1 = geompy.MakeCutList(Fuse_1, flat_cut_cyls, True)

	geompy.addToStudy( Cut_1, 'Cut_1' )

	flat_fuse_cyls = [item for sublist in fuse_cyls for item in sublist]
	flat_fuse_cyls.append(Cut_1)

	Fuse_2 = geompy.MakeFuseList(flat_fuse_cyls, True, True)

	geompy.addToStudy( Fuse_2, 'Fuse_2' )

	geompy.addToStudy( O, 'O' )
	geompy.addToStudy( OX, 'OX' )
	geompy.addToStudy( OY, 'OY' )
	geompy.addToStudy( OZ, 'OZ' )
	geompy.addToStudy( Vertex_2, 'Vertex_2' )
	geompy.addToStudy( Vertex_3, 'Vertex_3' )
	geompy.addToStudy( Cylinder_2, 'Cylinder_2' )
	geompy.addToStudy( Cylinder_1, 'Cylinder_1' )
	geompy.addToStudy( Vertex_1, 'Vertex_1' )
	geompy.addToStudy( Box_1, 'Box_1' )
	geompy.addToStudy( Vertex_5, 'Vertex_5' )
	geompy.addToStudy( Vertex_4, 'Vertex_4' )
	geompy.addToStudy( Cylinder_3, 'Cylinder_3' )
	geompy.addToStudy( Vertex_6, 'Vertex_6' )
	geompy.addToStudy( Cylinder_4, 'Cylinder_4' )
	geompy.addToStudy( Cylinder_5, 'Cylinder_5' )
	geompy.addToStudy( Fuse_1, 'Fuse_1' )
	geompy.addToStudy( Vertex_7, 'Vertex_7' )
	geompy.addToStudy( Vertex_8, 'Vertex_8' )
	geompy.addToStudy( Box_2, 'Box_2' )

	flat_vertex_cols = [item for sublist in vertex_cols for item in sublist]
	for i in range(len(flat_vertex_cols)):
		geompy.addToStudy(flat_vertex_cols[i], ('Vertex_' + str(i+9)) )

	for i in range(len(flat_cut_cyls)):
		geompy.addToStudy(flat_cut_cyls[i], ('Cylinder_' + str(i+6)))

	for i in range(len(flat_fuse_cyls)):
		geompy.addToStudy(flat_fuse_cyls[i], ('Cylinder_' + str(i+6+len(flat_cut_cyls))))

	"""
	geompy.addToStudy( Vertex_9, 'Vertex_9' )
	geompy.addToStudy( Vertex_10, 'Vertex_10' )
	geompy.addToStudy( Vertex_11, 'Vertex_11' )
	geompy.addToStudy( Vertex_12, 'Vertex_12' )
	geompy.addToStudy( Vertex_13, 'Vertex_13' )
	geompy.addToStudy( Vertex_14, 'Vertex_14' )
	geompy.addToStudy( Vertex_15, 'Vertex_15' )
	geompy.addToStudy( Vertex_16, 'Vertex_16' )
	geompy.addToStudy( Vertex_17, 'Vertex_17' )
	geompy.addToStudy( Vertex_18, 'Vertex_18' )
	geompy.addToStudy( Vertex_19, 'Vertex_19' )
	geompy.addToStudy( Vector_1, 'Vector_1' )
	geompy.addToStudy( Cylinder_6, 'Cylinder_6' )
	geompy.addToStudy( Cylinder_7, 'Cylinder_7' )
	geompy.addToStudy( Cylinder_8, 'Cylinder_8' )
	geompy.addToStudy( Cylinder_9, 'Cylinder_9' )
	geompy.addToStudy( Cylinder_10, 'Cylinder_10' )
	geompy.addToStudy( Cylinder_11, 'Cylinder_11' )
	geompy.addToStudy( Cylinder_12, 'Cylinder_12' )
	geompy.addToStudy( Cylinder_13, 'Cylinder_13' )
	geompy.addToStudy( Cylinder_14, 'Cylinder_14' )
	geompy.addToStudy( Cylinder_15, 'Cylinder_15' )
	geompy.addToStudy( Cylinder_16, 'Cylinder_16' )
	geompy.addToStudy( Cut_1, 'Cut_1' )
	geompy.addToStudy( Cylinder_17, 'Cylinder_17' )
	geompy.addToStudy( Cylinder_18, 'Cylinder_18' )
	geompy.addToStudy( Cylinder_19, 'Cylinder_19' )
	geompy.addToStudy( Cylinder_20, 'Cylinder_20' )
	geompy.addToStudy( Cylinder_21, 'Cylinder_21' )
	geompy.addToStudy( Cylinder_22, 'Cylinder_22' )
	geompy.addToStudy( Cylinder_23, 'Cylinder_23' )
	geompy.addToStudy( Cylinder_24, 'Cylinder_24' )
	geompy.addToStudy( Cylinder_25, 'Cylinder_25' )
	geompy.addToStudy( Cylinder_26, 'Cylinder_26' )
	geompy.addToStudy( Fuse_2, 'Fuse_2' )
	"""

	if salome.sg.hasDesktop():
	salome.sg.updateObjBrowser()
