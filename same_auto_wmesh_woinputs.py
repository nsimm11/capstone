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

num_distTubes = 3

def calcPipeNum(num_distTube):
	if num_distTube % 2 == 0:
		col_loc = int(num_distTube/2)
		num_faces_pipe = 42*col_loc+1 +7
	else:
	        col_loc = int((num_distTube/2) - 0.1)
	        num_faces_pipe = 42*col_loc + 21 + 7
    
	return num_faces_pipe

def buildWallsMapping(num_distTube, Faces):
	faces_distTube = []
	faces_outlet = []
	total = 7
	num_faces_pipe = calcPipeNum(num_distTube)
	for i in range(num_distTube):
		for j in range(1,43):
			total = total + 1
			if total == num_faces_pipe:
				faces_distTube.append(Faces[total])
				total = total + 1

			if j < 6 or j > 37:
				
				faces_outlet.append(Faces[total])

			elif (j > 5 and j < 21) or (j > 22 and j <38):
				faces_distTube.append(Faces[total])

			elif j > 20 and j < 23:
				faces_distTube.append(Faces[total])
    
	return faces_distTube, faces_outlet
    	
    	    
def buildFaceMapping(num_distTube, Faces):
    faces_inlet = [Faces[0]]
    
    inletWalls = []
    for k in range(1,8):
    	inletWalls.append(Faces[k])
    
    faces_distTube, faces_outlet = buildWallsMapping(num_distTube, Faces)
    
    faces_walls_nonFlat = [inletWalls, faces_distTube, [Faces[-1]]]
    
    faces_walls = [item for sublist in faces_walls_nonFlat for item in sublist]
    
    return faces_inlet, faces_outlet, faces_walls
    
    

geompy = geomBuilder.New()

O = geompy.MakeVertex(0, 0, 0)
OX = geompy.MakeVectorDXDYDZ(1, 0, 0)
OY = geompy.MakeVectorDXDYDZ(0, 1, 0)
OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)
Cylinder_1 = geompy.MakeCylinder(O, OX, 0.0508, 0.127)
Vertex_1 = geompy.MakeVertex(0.127, -0.089, -0.089)
Vertex_2 = geompy.MakeVertex(0.167, 0.089, 0.089)
Box_1 = geompy.MakeBoxTwoPnt(Vertex_1, Vertex_2)
Vertex_3 = geompy.MakeVertex(0.167, 0, 0)
Cylinder_2 = geompy.MakeCylinder(Vertex_3, OX, 0.0508, 0.33)
Vertex_4 = geompy.MakeVertex(0.4082, 0, 0.0408)
Vertex_5 = geompy.MakeVertex(0.332, 0, 0.0408)
Vertex_6 = geompy.MakeVertex(0.2558, 0, 0.0408)
Cylinder_3 = geompy.MakeCylinder(Vertex_4, OZ, 0.01905, 0.1497)
Cylinder_4 = geompy.MakeCylinder(Vertex_5, OZ, 0.01905, 0.1497)
Cylinder_5 = geompy.MakeCylinder(Vertex_6, OZ, 0.01905, 0.1497)
Fuse_1 = geompy.MakeFuseList([Cylinder_1, Box_1, Cylinder_2, Cylinder_3, Cylinder_4, Cylinder_5], True, True)
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
print(np.shape(flat_fuse_cyls))
Fuse_2 = geompy.MakeFuseList(flat_fuse_cyls, True, True)

geompy.addToStudy( Fuse_2, 'Fuse_2' )

Faces = geompy.ExtractShapes(Fuse_2, geompy.ShapeType["FACE"], True)

faces_inlet, faces_outlet, faces_walls = buildFaceMapping(num_distTubes, Faces)

print(faces_outlet)

Auto_group_for_inlet = geompy.CreateGroup(Fuse_2, geompy.ShapeType["FACE"])

geompy.UnionList(Auto_group_for_inlet, faces_inlet)

Auto_group_for_outlet = geompy.CreateGroup(Fuse_2, geompy.ShapeType["FACE"])

geompy.UnionList(Auto_group_for_outlet, faces_outlet)

Auto_group_for_walls = geompy.CreateGroup(Fuse_2, geompy.ShapeType["FACE"])

geompy.UnionList(Auto_group_for_walls, faces_walls)

flat_vertex_cols = [item for sublist in vertex_cols for item in sublist]
for i in range(len(flat_vertex_cols)):
	geompy.addToStudy(flat_vertex_cols[i], ('Vertex_' + str(i+9)) )

for i in range(len(flat_cut_cyls)):
	geompy.addToStudy(flat_cut_cyls[i], ('Cylinder_' + str(i+6)))

for i in range(len(flat_fuse_cyls)):
	geompy.addToStudy(flat_fuse_cyls[i], ('Cylinder_' + str(i+6+len(flat_cut_cyls))))

for i in range(len(Faces)):
	geompy.addToStudyInFather(Fuse_2, Faces[i], ("Face_" + str(i+1)))

geompy.addToStudyInFather( Fuse_2, Auto_group_for_outlet, 'Auto_group_for_outlet' )
geompy.addToStudyInFather( Fuse_2, Auto_group_for_inlet, 'Auto_group_for_inlet' )
geompy.addToStudyInFather( Fuse_2, Auto_group_for_walls, 'Auto_group_for_walls' )


###
### SMESH component
###

import  SMESH, SALOMEDS
from salome.smesh import smeshBuilder

smesh = smeshBuilder.New()
#smesh.SetEnablePublish( False ) # Set to False to avoid publish in study if not needed or in some particular situations:
                                 # multiples meshes built in parallel, complex and numerous mesh edition (performance)

Mesh_1 = smesh.Mesh(Fuse_2,'Mesh_1')
NETGEN_1D_2D_3D = Mesh_1.Tetrahedron(algo=smeshBuilder.NETGEN_1D2D3D)
NETGEN_3D_Parameters_1 = NETGEN_1D_2D_3D.Parameters()
NETGEN_3D_Parameters_1.SetMaxSize( 0.005 )
NETGEN_3D_Parameters_1.SetMinSize( 0.001 )
NETGEN_3D_Parameters_1.SetSecondOrder( 0 )
NETGEN_3D_Parameters_1.SetOptimize( 1 )
NETGEN_3D_Parameters_1.SetFineness( 2 )
NETGEN_3D_Parameters_1.SetChordalError( -1 )
NETGEN_3D_Parameters_1.SetChordalErrorEnabled( 0 )
NETGEN_3D_Parameters_1.SetUseSurfaceCurvature( 1 )
NETGEN_3D_Parameters_1.SetFuseEdges( 1 )
NETGEN_3D_Parameters_1.SetQuadAllowed( 0 )
NETGEN_3D_Parameters_1.SetCheckChartBoundary( 3 )
NETGEN_1D_2D = Mesh_1.Triangle(algo=smeshBuilder.NETGEN_1D2D,geom=Faces[0])
NETGEN_2D_Parameters_1 = NETGEN_1D_2D.Parameters()
NETGEN_2D_Parameters_1.SetMaxSize( 0.001 )
NETGEN_2D_Parameters_1.SetMinSize( 0.0005 )
NETGEN_2D_Parameters_1.SetSecondOrder( 0 )
NETGEN_2D_Parameters_1.SetOptimize( 1 )
NETGEN_2D_Parameters_1.SetFineness( 2 )
NETGEN_2D_Parameters_1.SetChordalError( -1 )
NETGEN_2D_Parameters_1.SetChordalErrorEnabled( 0 )
NETGEN_2D_Parameters_1.SetUseSurfaceCurvature( 1 )
NETGEN_2D_Parameters_1.SetFuseEdges( 1 )
NETGEN_2D_Parameters_1.SetQuadAllowed( 0 )
NETGEN_2D_Parameters_1.SetWorstElemMeasure( 22059 )
NETGEN_2D_Parameters_1.SetUseDelauney( 128 )
NETGEN_2D_Parameters_1.SetCheckChartBoundary( 3 )
Viscous_Layers_2D_1 = NETGEN_1D_2D.ViscousLayers2D(20,12,1.25,[],0)
isDone = Mesh_1.Compute()
outlet = Mesh_1.GroupOnGeom(Auto_group_for_outlet,'outlet',SMESH.FACE)
[ outlet ] = Mesh_1.GetGroups()
inlet = Mesh_1.GroupOnGeom(Faces[0],'inlet',SMESH.FACE)
[ outlet, inlet ] = Mesh_1.GetGroups()
walls = Mesh_1.GroupOnGeom(Auto_group_for_walls,'walls',SMESH.FACE)
[ outlet, inlet, walls ] = Mesh_1.GetGroups()

Sub_mesh_1 = NETGEN_1D_2D.GetSubMesh()

## Set names of Mesh objects
smesh.SetName(Sub_mesh_1, 'Sub-mesh_1')
smesh.SetName(NETGEN_1D_2D_3D.GetAlgorithm(), 'NETGEN 1D-2D-3D')
smesh.SetName(NETGEN_1D_2D.GetAlgorithm(), 'NETGEN 1D-2D')
smesh.SetName(inlet, 'inlet')
smesh.SetName(outlet, 'outlet')
smesh.SetName(walls, 'walls')

smesh.SetName(Mesh_1.GetMesh(), 'Mesh_1')
smesh.SetName(NETGEN_2D_Parameters_1, 'NETGEN 2D Parameters_1')
smesh.SetName(NETGEN_3D_Parameters_1, 'NETGEN 3D Parameters_1')
smesh.SetName(Viscous_Layers_2D_1, 'Viscous Layers 2D_1')


if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser()
