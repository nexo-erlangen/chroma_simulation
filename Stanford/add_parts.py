#from myimports import * 
from chroma.geometry import Geometry, Material, Solid, Surface, Mesh
from chroma.stl import mesh_from_stl
from chroma.detector import Detector
import Materials as mat
import Surfaces as surf
import numpy as np
import data as data
import colors as col



def BuildDetector(setup):
	print "  Creating Blank Vacuum Setup:			Done"
	path = "/home/exo/Dropbox/Stanford/LXECell_standoff/"
	path2 = "/home/exo/Dropbox/Stanford/SiPM/"


	a = mesh_from_stl(path+"LXE CELL ASSY with standoffs_CF 12 BLANK_190.stl")
	aS = Solid(a, mat.fullAbsorb, data.bottom(a,mat.LXenon,mat.fullAbsorb), color = data.bottom(a,col.grey,col.white))
	setup.add_solid(aS, displacement=(0,0,0))
	a_center = a.get_triangle_centers()

	b = mesh_from_stl(path+"LXE CELL ASSY with standoffs_ANODE MOUNTING PLATE V2_282.stl")
	bS = Solid(b, mat.fullAbsorb, mat.LXenon, surf.steelSurface,col.grey)
	setup.add_solid(bS, displacement=(0,0,0))

	c = mesh_from_stl(path+"LXE CELL ASSY with standoffs_CERAMIC INTERFACE BOARD_307.stl")
	cS = Solid(c, mat.fullAbsorb, mat.LXenon, surf.steelSurface, col.grey)
	setup.add_solid(cS, displacement=(0,0,0))

	e = mesh_from_stl(path+"LXE CELL ASSY with standoffs_CERAMIC INTERFACE BOARD_368.stl")
	eS = Solid(e, mat.fullAbsorb, mat.LXenon, surf.steelSurface, col.grey)
	setup.add_solid(eS, displacement=(0,0,0))

	g = mesh_from_stl(path+"LXE CELL ASSY with standoffs_QUARTZ WAFER_429.stl")
	gS = Solid(g, mat.fullAbsorb, mat.LXenon, surf.steelSurface, col.grey)
	setup.add_solid(gS, displacement=(0,0,0))
	g_center = g.get_triangle_centers()

	i = mesh_from_stl(path+"LXE CELL ASSY with standoffs_CF 12 FLANGE_1.stl")
	iS = Solid(i, mat.fullAbsorb, data.inner_radius(i,mat.LXenon,mat.fullAbsorb), surf.steelSurface, data.inner_radius(i,col.grey,col.white))
	setup.add_solid(iS, displacement=(0,0,0))
	i_center = i.get_triangle_centers() 
	i_radius = [np.sqrt(pow(x,2) + pow(y,2)) for x,y in zip(i_center[:,0],i_center[:,2])]

	j = mesh_from_stl(path+"LXE CELL ASSY with standoffs_CF 12 FLANGE_3.stl")
	jS = Solid(j, mat.fullAbsorb, data.inner_radius(j,mat.LXenon,mat.fullAbsorb), surf.steelSurface, data.inner_radius(j,col.grey,col.white))
	setup.add_solid(jS, displacement=(0,0,0))

	k = mesh_from_stl(path+"LXE CELL ASSY with standoffs_CF 12 TUBE_2.stl")
	kS = Solid(k, mat.fullAbsorb, data.inner_radius(k,mat.LXenon,mat.fullAbsorb), surf.steelSurface, data.inner_radius(k,col.grey,col.white))
	setup.add_solid(kS, displacement=(0,0,0))

	BIsourceM = mesh_from_stl(path+"LXE CELL ASSY with standoffs_Bi Source_132.stl")
	BIsourceS = Solid(BIsourceM, mat.LXenon, mat.LXenon,  color=col.blue)
	setup.add_solid(BIsourceS, displacement=(-1,0,5))

	BItriangCent = BIsourceM.get_triangle_centers()

	BIlocx = np.mean(BItriangCent[:,0])
	BIlocy = np.mean(BItriangCent[:,1])
	BIlocz = np.mean(BItriangCent[:,2])

	o = mesh_from_stl(path+"LXE CELL ASSY with standoffs_CATHODE MESH_82.stl")
	oS = Solid(o, mat.fullAbsorb, mat.LXenon, surf.steelSurface)
	setup.add_solid(oS, displacement=(0,0,0))
	o_center = o.get_triangle_centers()
	o_radius = [np.sqrt(pow(x,2) + pow(y,2)) for x,y in zip(o_center[:,0],o_center[:,2])]


	p = mesh_from_stl(path+"LXE CELL ASSY with standoffs_CATHODE SUPPORT RING BOTTOM_83.stl")
	pS = Solid(p, mat.fullAbsorb, mat.LXenon, surf.steelSurface)
	setup.add_solid(pS, displacement=(0,0,0))
	p_center = p.get_triangle_centers()

	q = mesh_from_stl(path+"LXE CELL ASSY with standoffs_CATHODE SUPPORT RING TOP_81.stl")
	qS = Solid(q, mat.fullAbsorb, mat.LXenon, surf.steelSurface)
	setup.add_solid(qS, displacement=(0,0,0))

	s = mesh_from_stl(path+"LXE CELL ASSY with standoffs_reducer_CF12_CF6_14.stl")
	s_center = s.get_triangle_centers()
	s_radius = [np.sqrt(pow(x,2) + pow(y,2)) for x,y in zip(s_center[:,0],s_center[:,2])]

	s_top = max(s_center[:,1])
	s_MIn = np.where((s_center[:,1]>=(s_top+.05*s_top))| ((np.sqrt(pow(s_center[:,0],2) + pow(s_center[:,2],2))) < (min(s_radius)+.05*min(s_radius))), mat.LXenon, mat.vacuum)
	s_MInC = np.where((s_center[:,1]>=(s_top+.05*s_top)) | ((np.sqrt(pow(s_center[:,0],2) + pow(s_center[:,2],2))) < (min(s_radius)+.05*min(s_radius))),col.grey,col.white)
	sS = Solid(s, mat.fullAbsorb, s_MIn, surf.steelSurface, color = s_MInC)
	setup.add_solid(sS, displacement=(0,0,0))

	t = mesh_from_stl(path+"LXE CELL ASSY with standoffs_0194605B_22.stl")
	tS = Solid(t, mat.fullAbsorb, data.inner_radius(t,mat.LXenon,mat.vacuum), surf.steelSurface, data.inner_radius(t,col.grey,col.white))
	setup.add_solid(tS, displacement=(0,0,0))

	u = mesh_from_stl(path+"LXE CELL ASSY with standoffs_0194303C_20.stl")
	uS = Solid(u, mat.fullAbsorb, data.inner_radius(u,mat.LXenon,mat.vacuum), surf.steelSurface, data.inner_radius(u,col.grey,col.white))
	setup.add_solid(uS, displacement=(0,0,0))

	v = mesh_from_stl(path+"LXE CELL ASSY with standoffs_1002204A_21.stl")
	vS = Solid(v, mat.MSuprasil, data.top(v,mat.LXenon,mat.quartz), color = data.top(v,col.grey,col.white))
	v_center = v.get_triangle_centers()
	thickness = abs(min(v_center[0:,1])-max(v_center[0:,1])) 
	#print "  Thickness:		", thickness
	#print "  Distance:		", abs(np.mean(v_tra[0:,1])-np.mean(BItriangCent[0:,1])) 
	setup.add_solid(vS, displacement=(0,0,0))

	triangleCenters = v.get_triangle_centers()
	meanX = np.mean(triangleCenters[:,0])
	meanY = np.mean(triangleCenters[:,1])
	bottomY = np.min(triangleCenters[:,1])
	meanZ = np.mean(triangleCenters[:,2])

	xshift = meanX
	zshift = meanZ



