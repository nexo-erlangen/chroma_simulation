from chroma.geometry import Geometry, Material, Solid, Surface, Mesh
from chroma.stl import mesh_from_stl
from chroma.detector import Detector
from chroma.transform import make_rotation_matrix
import Materials as mat
import Surfaces as surf
import numpy as np
import data as data
import colors as col



class LXeSetup(object):
	
	def __init__(self, setup, cell_path, sipm_path, detector_choice="pmt"):
		self.outside_material = "vacuum"
		self.detector_choice = detector_choice 
		self.cell_path = cell_path
		self.sipm_path = sipm_path
		self.setup = setup 
		self.window_xmean = 0
		self.window_ymean = 0
		self.window_zmean = 0
		self.window_thickness = 0
		self.cathode_mesh = ""
		self.cf12_blank = ""
		self.reducer = ""
		self.reducer_radius = ""
		self.window = "" 
		self.flange_top = "" 
		self.flange_top_radius = ""
		self.wafer = ""
		self.runs = 1
		self.step_xz = 3.
		self.step_y = 3. 
	
	def getRadius(self, center):
		radius = [np.sqrt(pow(x,2) + pow(y,2)) for x,y in zip(center[:,0],center[:,2])]
		return radius
		
	def getSourceLocations(self):
		locs = []

		cell_dist = abs(np.min(self.cf12_blank[:,1])-np.max(self.reducer[:,1]))
		pmt_dist = abs(np.max(self.reducer[:,1]) - np.max(self.window[:,1]))
		print "  Distance in z within cell:			", cell_dist 
		print "  Distance in z within reducer:			", pmt_dist 

		for ii in range(int(cell_dist/self.step_y)+1):
			for jj in range(int(np.min(self.flange_top_radius)*2/self.step_xz)):
				for kk in range(int(np.min(self.flange_top_radius)*2/self.step_xz)):
					event = [np.min(self.flange_top_radius)-kk*self.step_xz, np.min(self.cf12_blank[:,1])-.1-ii*self.step_y, np.min(self.flange_top_radius)-jj*self.step_xz]
					if(np.sqrt(pow(event[0],2) + pow(event[2],2)) < np.min(self.flange_top_radius)):
						locs.append(event)

		for ii in range(int(pmt_dist/self.step_y)+1):
			for jj in range(int(np.min(self.reducer_radius)*2/self.step_xz)):
				for kk in range(int(np.min(self.reducer_radius)*2/self.step_xz)):
					event = [np.min(self.reducer_radius)-kk*self.step_xz, np.max(self.reducer[:,1])-.1-ii*self.step_y, np.min(self.reducer_radius)-jj*self.step_xz]
					if(np.sqrt(pow(event[0],2) + pow(event[2],2)) < np.min(self.reducer_radius)):
						locs.append(event)
						
		return np.asarray(locs) 
		
	def build_cell(self):
		print "  Creating Blank Vacuum Setup:			Done"

		a = mesh_from_stl(self.cell_path+"LXE CELL ASSY with standoffs_CF 12 BLANK_190.stl")
		aS = Solid(a, mat.fullAbsorb, data.bottom(a,mat.LXenon,mat.fullAbsorb), color = data.bottom(a,col.grey,col.white))
		self.setup.add_solid(aS, displacement=(0,0,0))
		a_center = a.get_triangle_centers()
		self.cf12_blank = a.get_triangle_centers()

		b = mesh_from_stl(self.cell_path+"LXE CELL ASSY with standoffs_ANODE MOUNTING PLATE V2_282.stl")
		bS = Solid(b, mat.fullAbsorb, mat.LXenon, surf.steelSurface,col.grey)
		self.setup.add_solid(bS, displacement=(0,0,0))

		c = mesh_from_stl(self.cell_path+"LXE CELL ASSY with standoffs_CERAMIC INTERFACE BOARD_307.stl")
		cS = Solid(c, mat.fullAbsorb, mat.LXenon, surf.steelSurface, col.grey)
		self.setup.add_solid(cS, displacement=(0,0,0))

		e = mesh_from_stl(self.cell_path+"LXE CELL ASSY with standoffs_CERAMIC INTERFACE BOARD_368.stl")
		eS = Solid(e, mat.fullAbsorb, mat.LXenon, surf.steelSurface, col.grey)
		self.setup.add_solid(eS, displacement=(0,0,0))

		g = mesh_from_stl(self.cell_path+"LXE CELL ASSY with standoffs_QUARTZ WAFER_429.stl")
		gS = Solid(g, mat.fullAbsorb, mat.LXenon, surf.steelSurface, col.grey)
		self.setup.add_solid(gS, displacement=(0,0,0))
		self.wafer = g.get_triangle_centers()

		i = mesh_from_stl(self.cell_path+"LXE CELL ASSY with standoffs_CF 12 FLANGE_1.stl")
		iS = Solid(i, mat.fullAbsorb, data.inner_radius(i,mat.LXenon,mat.fullAbsorb), surf.steelSurface, data.inner_radius(i,col.grey,col.white))
		self.setup.add_solid(iS, displacement=(0,0,0))
		self.flange_top = i.get_triangle_centers() 
		self.flange_top_radius = self.getRadius(self.flange_top)

		j = mesh_from_stl(self.cell_path+"LXE CELL ASSY with standoffs_CF 12 FLANGE_3.stl")
		jS = Solid(j, mat.fullAbsorb, data.inner_radius(j,mat.LXenon,mat.fullAbsorb), surf.steelSurface, data.inner_radius(j,col.grey,col.white))
		self.setup.add_solid(jS, displacement=(0,0,0))

		k = mesh_from_stl(self.cell_path+"LXE CELL ASSY with standoffs_CF 12 TUBE_2.stl")
		kS = Solid(k, mat.fullAbsorb, data.inner_radius(k,mat.LXenon,mat.fullAbsorb), surf.steelSurface, data.inner_radius(k,col.grey,col.white))
		self.setup.add_solid(kS, displacement=(0,0,0))

		BIsourceM = mesh_from_stl(self.cell_path+"LXE CELL ASSY with standoffs_Bi Source_132.stl")
		BIsourceS = Solid(BIsourceM, mat.LXenon, mat.LXenon,  color=col.blue)
		self.setup.add_solid(BIsourceS, displacement=(-1,0,5))

		BItriangCent = BIsourceM.get_triangle_centers()

		BIlocx = np.mean(BItriangCent[:,0])
		BIlocy = np.mean(BItriangCent[:,1])
		BIlocz = np.mean(BItriangCent[:,2])

		o = mesh_from_stl(self.cell_path+"LXE CELL ASSY with standoffs_CATHODE MESH_82.stl")
		oS = Solid(o, mat.fullAbsorb, mat.LXenon, surf.steelSurface)
		self.setup.add_solid(oS, displacement=(0,0,0))
		o_center = o.get_triangle_centers()
		self.cathode_mesh = o.get_triangle_centers()
		o_radius = [np.sqrt(pow(x,2) + pow(y,2)) for x,y in zip(o_center[:,0],o_center[:,2])]


		p = mesh_from_stl(self.cell_path+"LXE CELL ASSY with standoffs_CATHODE SUPPORT RING BOTTOM_83.stl")
		pS = Solid(p, mat.fullAbsorb, mat.LXenon, surf.steelSurface)
		self.setup.add_solid(pS, displacement=(0,0,0))
		p_center = p.get_triangle_centers()

		q = mesh_from_stl(self.cell_path+"LXE CELL ASSY with standoffs_CATHODE SUPPORT RING TOP_81.stl")
		qS = Solid(q, mat.fullAbsorb, mat.LXenon, surf.steelSurface)
		self.setup.add_solid(qS, displacement=(0,0,0))

		s = mesh_from_stl(self.cell_path+"LXE CELL ASSY with standoffs_reducer_CF12_CF6_14.stl")
		self.reducer = s.get_triangle_centers()
		self.reducer_radius = self.getRadius(self.reducer)
		
		s_top = max(self.reducer[:,1])
		s_MIn = np.where((self.reducer[:,1]>=(s_top+.05*s_top))| ((np.sqrt(pow(self.reducer[:,0],2) + pow(self.reducer[:,2],2))) < (min(self.getRadius(self.reducer))+.05*min(self.getRadius(self.reducer)))), mat.LXenon, mat.vacuum)
		s_MInC = np.where((self.reducer[:,1]>=(s_top+.05*s_top)) | ((np.sqrt(pow(self.reducer[:,0],2) + pow(self.reducer[:,2],2))) < (min(self.getRadius(self.reducer))+.05*min(self.getRadius(self.reducer)))),col.grey,col.white)
		sS = Solid(s, mat.fullAbsorb, s_MIn, surf.steelSurface, color = s_MInC)
		self.setup.add_solid(sS, displacement=(0,0,0))

		t = mesh_from_stl(self.cell_path+"LXE CELL ASSY with standoffs_0194605B_22.stl")
		tS = Solid(t, mat.fullAbsorb, data.inner_radius(t,mat.LXenon,mat.vacuum), surf.steelSurface, data.inner_radius(t,col.grey,col.white))
		self.setup.add_solid(tS, displacement=(0,0,0))

		u = mesh_from_stl(self.cell_path+"LXE CELL ASSY with standoffs_0194303C_20.stl")
		uS = Solid(u, mat.fullAbsorb, data.inner_radius(u,mat.LXenon,mat.vacuum), surf.steelSurface, data.inner_radius(u,col.grey,col.white))
		self.setup.add_solid(uS, displacement=(0,0,0))

		v = mesh_from_stl(self.cell_path+"LXE CELL ASSY with standoffs_1002204A_21.stl")
		vS = Solid(v, mat.MSuprasil, data.top(v,mat.LXenon,mat.quartz), color = data.top(v,col.grey,col.white))
		v_center = v.get_triangle_centers()
		self.window = v.get_triangle_centers()
		thickness = abs(min(self.window[0:,1])-max(self.window[0:,1])) 
		#print "  Thickness:		", thickness
		#print "  Distance:		", abs(np.mean(v_tra[0:,1])-np.mean(BItriangCent[0:,1])) 
		self.setup.add_solid(vS, displacement=(0,0,0))

		meanX = np.mean(self.window[:,0])
		meanY = np.mean(self.window[:,1])
		bottomY = np.min(self.window[:,1])
		meanZ = np.mean(self.window[:,2])


		
		self.window_xmean = np.mean(self.window[:,0])
		self.window_ymean = np.mean(self.window[:,1])
		self.window_zmean = np.mean(self.window[:,2])
		self.window_thickness = thickness
		
		print "  Mesh Imports:					Successful"
		print "====================================================================="

	def ChooseDetector(self):
		if self.detector_choice == 'pmt':
			pmt = mesh_from_stl(self.cell_path+"pmt.stl")
			pmtS = Solid(pmt, mat.quartz, data.bottom(pmt,mat.MSuprasil,mat.LXenon), data.radius_bottom(pmt, surf.fulldetect, None), data.radius_bottom(pmt, col.grey, col.white))
			self.setup.add_pmt(pmtS,rotation = make_rotation_matrix(np.pi,(0,0,1)), displacement = (self.window_xmean ,self.window_ymean -((self.window_thickness+0.0)/2),self.window_zmean))
		
		if self.detector_choice == 'sipm':	
			c1 = mesh_from_stl(self.sipm_path+"LXe Assembly - 6er SiPM Ceramic Carrier v4-1 Ceramic carrier-1 Ceramic carrier-1.STL")
			c2 = mesh_from_stl(self.sipm_path+"LXe Assembly - 6er SiPM Ceramic Carrier v4_2-1 Ceramic carrier_2-1 Ceramic carrier_2-1.STL")
			c3 = mesh_from_stl(self.sipm_path+"LXe Assembly - 6er SiPM Ceramic Carrier v4_3-1 Ceramic carrier_3-1 Ceramic carrier_3-1.STL")
			c4 = mesh_from_stl(self.sipm_path+"LXe Assembly - 6er SiPM Ceramic Carrier v4_4-1 Ceramic carrier_4-1 Ceramic carrier_4-1.STL")
			c5 = mesh_from_stl(self.sipm_path+"LXe Assembly - 3er SiPM Ceramic Carrier v2-1 Ceramic carrier_5-1 Ceramic carrier_5-1.STL")
			c6 = mesh_from_stl(self.sipm_path+"LXe Assembly - 3er SiPM Ceramic Carrier v2_2-1 Ceramic carrier_6-1 Ceramic carrier_6-1.STL")
			c7 = mesh_from_stl(self.sipm_path+"LXe Assembly - 3er SiPM Ceramic Carrier v2_3-1 Ceramic carrier_7-1 Ceramic carrier_7-1.STL")
			c8 = mesh_from_stl(self.sipm_path+"LXe Assembly - 3er SiPM Ceramic Carrier v2_4-1 Ceramic carrier_8-1 Ceramic carrier_8-1.STL")

			SUM = c1+c2+c3+c4+c5+c6+c7+c8 
			sumV = SUM.get_triangle_centers()

			steel = mesh_from_stl(self.sipm_path+"LXe Assembly - Steel Carrier-1.STL")
			steelS = Solid(steel, mat.fullAbsorb, mat.LXenon, color = col.black)
			self.setup.add_solid(steelS, displacement=(np.mean(self.cathode_mesh[:,0])-np.mean(sumV[:,0]),np.mean(self.cathode_mesh[:,1])-np.mean(sumV[:,1])-3,np.mean(self.cathode_mesh[:,2])-np.mean(sumV[:,2])))

			c1S = Solid(c1, mat.fullAbsorb, mat.LXenon, color = col.white)
			c2S = Solid(c2, mat.fullAbsorb, mat.LXenon, color = col.white)
			c3S = Solid(c3, mat.fullAbsorb, mat.LXenon, color = col.white)
			c4S = Solid(c4, mat.fullAbsorb, mat.LXenon, color = col.white)
			c5S = Solid(c5, mat.fullAbsorb, mat.LXenon, color = col.white)
			c6S = Solid(c6, mat.fullAbsorb, mat.LXenon, color = col.white)
			c7S = Solid(c7, mat.fullAbsorb, mat.LXenon, color = col.white)
			c8S = Solid(c8, mat.fullAbsorb, mat.LXenon, color = col.white)

			self.setup.add_solid(c1S, displacement=(np.mean(self.cathode_mesh[:,0])-np.mean(sumV[:,0]),np.mean(self.cathode_mesh[:,1])-np.mean(sumV[:,1])-3,np.mean(self.cathode_mesh[:,2])-np.mean(sumV[:,2])))
			self.setup.add_solid(c2S, displacement=(np.mean(self.cathode_mesh[:,0])-np.mean(sumV[:,0]),np.mean(self.cathode_mesh[:,1])-np.mean(sumV[:,1])-3,np.mean(self.cathode_mesh[:,2])-np.mean(sumV[:,2])))
			self.setup.add_solid(c3S, displacement=(np.mean(self.cathode_mesh[:,0])-np.mean(sumV[:,0]),np.mean(self.cathode_mesh[:,1])-np.mean(sumV[:,1])-3,np.mean(self.cathode_mesh[:,2])-np.mean(sumV[:,2])))
			self.setup.add_solid(c4S, displacement=(np.mean(self.cathode_mesh[:,0])-np.mean(sumV[:,0]),np.mean(self.cathode_mesh[:,1])-np.mean(sumV[:,1])-3,np.mean(self.cathode_mesh[:,2])-np.mean(sumV[:,2])))
			self.setup.add_solid(c5S, displacement=(np.mean(self.cathode_mesh[:,0])-np.mean(sumV[:,0]),np.mean(self.cathode_mesh[:,1])-np.mean(sumV[:,1])-3,np.mean(self.cathode_mesh[:,2])-np.mean(sumV[:,2])))
			self.setup.add_solid(c6S, displacement=(np.mean(self.cathode_mesh[:,0])-np.mean(sumV[:,0]),np.mean(self.cathode_mesh[:,1])-np.mean(sumV[:,1])-3,np.mean(self.cathode_mesh[:,2])-np.mean(sumV[:,2])))
			self.setup.add_solid(c7S, displacement=(np.mean(self.cathode_mesh[:,0])-np.mean(sumV[:,0]),np.mean(self.cathode_mesh[:,1])-np.mean(sumV[:,1])-3,np.mean(self.cathode_mesh[:,2])-np.mean(sumV[:,2])))
			self.setup.add_solid(c8S, displacement=(np.mean(self.cathode_mesh[:,0])-np.mean(sumV[:,0]),np.mean(self.cathode_mesh[:,1])-np.mean(sumV[:,1])-3,np.mean(self.cathode_mesh[:,2])-np.mean(sumV[:,2])))


			s1 = mesh_from_stl(self.sipm_path+"LXe Assembly - 3er SiPM Ceramic Carrier v2_2-1 Ceramic carrier_6-1 SiPM Gold Pad (2)_6-1 Component42_2-1.STL")
			s2 = mesh_from_stl(self.sipm_path+"LXe Assembly - 3er SiPM Ceramic Carrier v2_2-1 Ceramic carrier_6-1 SiPM Gold Pad (4)_6-1 Component46_2-1.STL")
			s3 = mesh_from_stl(self.sipm_path+"LXe Assembly - 3er SiPM Ceramic Carrier v2_2-1 Ceramic carrier_6-1 SiPM Gold Pad (5)_6-1 Component48_2-1.STL")
			s4 = mesh_from_stl(self.sipm_path+"LXe Assembly - 3er SiPM Ceramic Carrier v2_3-1 Ceramic carrier_7-1 SiPM Gold Pad (2)_7-1 Component42_2-1.STL")
			s5 = mesh_from_stl(self.sipm_path+"LXe Assembly - 3er SiPM Ceramic Carrier v2_3-1 Ceramic carrier_7-1 SiPM Gold Pad (4)_7-1 Component46_2-1.STL")
			s6 = mesh_from_stl(self.sipm_path+"LXe Assembly - 3er SiPM Ceramic Carrier v2_3-1 Ceramic carrier_7-1 SiPM Gold Pad (5)_7-1 Component48_2-1.STL")
			s7 = mesh_from_stl(self.sipm_path+"LXe Assembly - 3er SiPM Ceramic Carrier v2_4-1 Ceramic carrier_8-1 SiPM Gold Pad (2)_8-1 Component42_2-1.STL")
			s8 = mesh_from_stl(self.sipm_path+"LXe Assembly - 3er SiPM Ceramic Carrier v2_4-1 Ceramic carrier_8-1 SiPM Gold Pad (4)_8-1 Component46_2-1.STL")
			s9 = mesh_from_stl(self.sipm_path+"LXe Assembly - 3er SiPM Ceramic Carrier v2_4-1 Ceramic carrier_8-1 SiPM Gold Pad (5)_8-1 Component48_2-1.STL")
			s10 = mesh_from_stl(self.sipm_path+"LXe Assembly - 3er SiPM Ceramic Carrier v2-1 Ceramic carrier_5-1 SiPM Gold Pad (2)_5-1 Component42_2-1.STL")
			s11 = mesh_from_stl(self.sipm_path+"LXe Assembly - 3er SiPM Ceramic Carrier v2-1 Ceramic carrier_5-1 SiPM Gold Pad (4)_5-1 Component46_2-1.STL")
			s12 = mesh_from_stl(self.sipm_path+"LXe Assembly - 3er SiPM Ceramic Carrier v2-1 Ceramic carrier_5-1 SiPM Gold Pad (5)_5-1 Component48_2-1.STL")
			s13 = mesh_from_stl(self.sipm_path+"LXe Assembly - 6er SiPM Ceramic Carrier v4_2-1 Ceramic carrier_2-1 SiPM Gold Pad (1)_2-1 Component40-1.STL")
			s14 = mesh_from_stl(self.sipm_path+"LXe Assembly - 6er SiPM Ceramic Carrier v4_2-1 Ceramic carrier_2-1 SiPM Gold Pad (2)_2-1 Component42-1.STL")
			s15 = mesh_from_stl(self.sipm_path+"LXe Assembly - 6er SiPM Ceramic Carrier v4_2-1 Ceramic carrier_2-1 SiPM Gold Pad (3)_2-1 Component44-1.STL")
			s16 = mesh_from_stl(self.sipm_path+"LXe Assembly - 6er SiPM Ceramic Carrier v4_2-1 Ceramic carrier_2-1 SiPM Gold Pad (4)_2-1 Component46-1.STL")
			s17 = mesh_from_stl(self.sipm_path+"LXe Assembly - 6er SiPM Ceramic Carrier v4_2-1 Ceramic carrier_2-1 SiPM Gold Pad (5)_2-1 Component48-1.STL")
			s18 = mesh_from_stl(self.sipm_path+"LXe Assembly - 6er SiPM Ceramic Carrier v4_2-1 Ceramic carrier_2-1 SiPM Gold Pad_2-1 Component30-1.STL")
			s19 = mesh_from_stl(self.sipm_path+"LXe Assembly - 6er SiPM Ceramic Carrier v4_3-1 Ceramic carrier_3-1 SiPM Gold Pad (1)_3-1 Component40-1.STL")
			s20 = mesh_from_stl(self.sipm_path+"LXe Assembly - 6er SiPM Ceramic Carrier v4_3-1 Ceramic carrier_3-1 SiPM Gold Pad (2)_3-1 Component42-1.STL")
			s21 = mesh_from_stl(self.sipm_path+"LXe Assembly - 6er SiPM Ceramic Carrier v4_3-1 Ceramic carrier_3-1 SiPM Gold Pad (3)_3-1 Component44-1.STL")
			s22 = mesh_from_stl(self.sipm_path+"LXe Assembly - 6er SiPM Ceramic Carrier v4_3-1 Ceramic carrier_3-1 SiPM Gold Pad (4)_3-1 Component46-1.STL")
			s23 = mesh_from_stl(self.sipm_path+"LXe Assembly - 6er SiPM Ceramic Carrier v4_3-1 Ceramic carrier_3-1 SiPM Gold Pad (5)_3-1 Component48-1.STL")
			s24 = mesh_from_stl(self.sipm_path+"LXe Assembly - 6er SiPM Ceramic Carrier v4_3-1 Ceramic carrier_3-1 SiPM Gold Pad_3-1 Component30-1.STL")
			s25 = mesh_from_stl(self.sipm_path+"LXe Assembly - 6er SiPM Ceramic Carrier v4_4-1 Ceramic carrier_4-1 SiPM Gold Pad (1)_4-1 Component40-1.STL")
			s26 = mesh_from_stl(self.sipm_path+"LXe Assembly - 6er SiPM Ceramic Carrier v4_4-1 Ceramic carrier_4-1 SiPM Gold Pad (2)_4-1 Component42-1.STL")
			s27 = mesh_from_stl(self.sipm_path+"LXe Assembly - 6er SiPM Ceramic Carrier v4_4-1 Ceramic carrier_4-1 SiPM Gold Pad (3)_4-1 Component44-1.STL")
			s28 = mesh_from_stl(self.sipm_path+"LXe Assembly - 6er SiPM Ceramic Carrier v4_4-1 Ceramic carrier_4-1 SiPM Gold Pad (4)_4-1 Component46-1.STL")
			s29 = mesh_from_stl(self.sipm_path+"LXe Assembly - 6er SiPM Ceramic Carrier v4_4-1 Ceramic carrier_4-1 SiPM Gold Pad (5)_4-1 Component48-1.STL")
			s30 = mesh_from_stl(self.sipm_path+"LXe Assembly - 6er SiPM Ceramic Carrier v4_4-1 Ceramic carrier_4-1 SiPM Gold Pad_4-1 Component30-1.STL")
			s31 = mesh_from_stl(self.sipm_path+"LXe Assembly - 6er SiPM Ceramic Carrier v4-1 Ceramic carrier-1 SiPM Gold Pad (1)-1 Component40-1.STL")
			s32 = mesh_from_stl(self.sipm_path+"LXe Assembly - 6er SiPM Ceramic Carrier v4-1 Ceramic carrier-1 SiPM Gold Pad (2)-1 Component42-1.STL")
			s33 = mesh_from_stl(self.sipm_path+"LXe Assembly - 6er SiPM Ceramic Carrier v4-1 Ceramic carrier-1 SiPM Gold Pad (3)-1 Component44-1.STL")
			s34 = mesh_from_stl(self.sipm_path+"LXe Assembly - 6er SiPM Ceramic Carrier v4-1 Ceramic carrier-1 SiPM Gold Pad (4)-1 Component46-1.STL")
			s35 = mesh_from_stl(self.sipm_path+"LXe Assembly - 6er SiPM Ceramic Carrier v4-1 Ceramic carrier-1 SiPM Gold Pad (5)-1 Component48-1.STL")
			s36 = mesh_from_stl(self.sipm_path+"LXe Assembly - 6er SiPM Ceramic Carrier v4-1 Ceramic carrier-1 SiPM Gold Pad-1 Component30-1.STL")

			s1S = Solid(s1, mat.fullAbsorb, mat.LXenon, surface = surf.fulldetect, color = col.gold)
			s2S = Solid(s2, mat.fullAbsorb, mat.LXenon, surface = surf.fulldetect, color = col.gold)
			s3S = Solid(s3, mat.fullAbsorb, mat.LXenon, surface = surf.fulldetect, color = col.gold)
			s4S = Solid(s4, mat.fullAbsorb, mat.LXenon, surface = surf.fulldetect, color = col.gold)
			s5S = Solid(s5, mat.fullAbsorb, mat.LXenon, surface = surf.fulldetect, color = col.gold)
			s6S = Solid(s6, mat.fullAbsorb, mat.LXenon, surface = surf.fulldetect, color = col.gold)
			s7S = Solid(s7, mat.fullAbsorb, mat.LXenon, surface = surf.fulldetect, color = col.gold)
			s8S = Solid(s8, mat.fullAbsorb, mat.LXenon, surface = surf.fulldetect, color = col.gold)
			s9S = Solid(s9, mat.fullAbsorb, mat.LXenon, surface = surf.fulldetect, color = col.gold)
			s10S = Solid(s10, mat.fullAbsorb, mat.LXenon, surface = surf.fulldetect, color = col.gold)
			s11S = Solid(s11, mat.fullAbsorb, mat.LXenon, surface = surf.fulldetect, color = col.gold)
			s12S = Solid(s12, mat.fullAbsorb, mat.LXenon, surface = surf.fulldetect, color = col.gold)
			s13S = Solid(s13, mat.fullAbsorb, mat.LXenon, surface = surf.fulldetect, color = col.gold)
			s14S = Solid(s14, mat.fullAbsorb, mat.LXenon, surface = surf.fulldetect, color = col.gold)
			s15S = Solid(s15, mat.fullAbsorb, mat.LXenon, surface = surf.fulldetect, color = col.gold)
			s16S = Solid(s16, mat.fullAbsorb, mat.LXenon, surface = surf.fulldetect, color = col.gold)
			s17S = Solid(s17, mat.fullAbsorb, mat.LXenon, surface = surf.fulldetect, color = col.gold)
			s18S = Solid(s18, mat.fullAbsorb, mat.LXenon, surface = surf.fulldetect, color = col.gold)
			s19S = Solid(s19, mat.fullAbsorb, mat.LXenon, surface = surf.fulldetect, color = col.gold)
			s20S = Solid(s20, mat.fullAbsorb, mat.LXenon, surface = surf.fulldetect, color = col.gold)
			s21S = Solid(s21, mat.fullAbsorb, mat.LXenon, surface = surf.fulldetect, color = col.gold)
			s22S = Solid(s22, mat.fullAbsorb, mat.LXenon, surface = surf.fulldetect, color = col.gold)
			s23S = Solid(s23, mat.fullAbsorb, mat.LXenon, surface = surf.fulldetect, color = col.gold)
			s24S = Solid(s24, mat.fullAbsorb, mat.LXenon, surface = surf.fulldetect, color = col.gold)
			s25S = Solid(s25, mat.fullAbsorb, mat.LXenon, surface = surf.fulldetect, color = col.gold)
			s26S = Solid(s26, mat.fullAbsorb, mat.LXenon, surface = surf.fulldetect, color = col.gold)
			s27S = Solid(s27, mat.fullAbsorb, mat.LXenon, surface = surf.fulldetect, color = col.gold)
			s28S = Solid(s28, mat.fullAbsorb, mat.LXenon, surface = surf.fulldetect, color = col.gold)
			s29S = Solid(s29, mat.fullAbsorb, mat.LXenon, surface = surf.fulldetect, color = col.gold)
			s30S = Solid(s30, mat.fullAbsorb, mat.LXenon, surface = surf.fulldetect, color = col.gold)
			s31S = Solid(s31, mat.fullAbsorb, mat.LXenon, surface = surf.fulldetect, color = col.gold)
			s32S = Solid(s32, mat.fullAbsorb, mat.LXenon, surface = surf.fulldetect, color = col.gold)
			s33S = Solid(s33, mat.fullAbsorb, mat.LXenon, surface = surf.fulldetect, color = col.gold)
			s34S = Solid(s34, mat.fullAbsorb, mat.LXenon, surface = surf.fulldetect, color = col.gold)
			s35S = Solid(s35, mat.fullAbsorb, mat.LXenon, surface = surf.fulldetect, color = col.gold)
			s36S = Solid(s36, mat.fullAbsorb, mat.LXenon, surface = surf.fulldetect, color = col.gold)

			self.setup.add_solid(s1S, displacement=(np.mean(self.cathode_mesh[:,0])-np.mean(sumV[:,0]),np.mean(self.cathode_mesh[:,1])-np.mean(sumV[:,1])-3,np.mean(self.cathode_mesh[:,2])-np.mean(sumV[:,2])))
			self.setup.add_solid(s2S, displacement=(np.mean(self.cathode_mesh[:,0])-np.mean(sumV[:,0]),np.mean(self.cathode_mesh[:,1])-np.mean(sumV[:,1])-3,np.mean(self.cathode_mesh[:,2])-np.mean(sumV[:,2])))
			self.setup.add_solid(s3S, displacement=(np.mean(self.cathode_mesh[:,0])-np.mean(sumV[:,0]),np.mean(self.cathode_mesh[:,1])-np.mean(sumV[:,1])-3,np.mean(self.cathode_mesh[:,2])-np.mean(sumV[:,2])))
			self.setup.add_solid(s4S, displacement=(np.mean(self.cathode_mesh[:,0])-np.mean(sumV[:,0]),np.mean(self.cathode_mesh[:,1])-np.mean(sumV[:,1])-3,np.mean(self.cathode_mesh[:,2])-np.mean(sumV[:,2])))
			self.setup.add_solid(s5S, displacement=(np.mean(self.cathode_mesh[:,0])-np.mean(sumV[:,0]),np.mean(self.cathode_mesh[:,1])-np.mean(sumV[:,1])-3,np.mean(self.cathode_mesh[:,2])-np.mean(sumV[:,2])))
			self.setup.add_solid(s6S, displacement=(np.mean(self.cathode_mesh[:,0])-np.mean(sumV[:,0]),np.mean(self.cathode_mesh[:,1])-np.mean(sumV[:,1])-3,np.mean(self.cathode_mesh[:,2])-np.mean(sumV[:,2])))
			self.setup.add_solid(s7S, displacement=(np.mean(self.cathode_mesh[:,0])-np.mean(sumV[:,0]),np.mean(self.cathode_mesh[:,1])-np.mean(sumV[:,1])-3,np.mean(self.cathode_mesh[:,2])-np.mean(sumV[:,2])))
			self.setup.add_solid(s8S, displacement=(np.mean(self.cathode_mesh[:,0])-np.mean(sumV[:,0]),np.mean(self.cathode_mesh[:,1])-np.mean(sumV[:,1])-3,np.mean(self.cathode_mesh[:,2])-np.mean(sumV[:,2])))
			self.setup.add_solid(s9S, displacement=(np.mean(self.cathode_mesh[:,0])-np.mean(sumV[:,0]),np.mean(self.cathode_mesh[:,1])-np.mean(sumV[:,1])-3,np.mean(self.cathode_mesh[:,2])-np.mean(sumV[:,2])))
			self.setup.add_solid(s10S, displacement=(np.mean(self.cathode_mesh[:,0])-np.mean(sumV[:,0]),np.mean(self.cathode_mesh[:,1])-np.mean(sumV[:,1])-3,np.mean(self.cathode_mesh[:,2])-np.mean(sumV[:,2])))
			self.setup.add_solid(s11S, displacement=(np.mean(self.cathode_mesh[:,0])-np.mean(sumV[:,0]),np.mean(self.cathode_mesh[:,1])-np.mean(sumV[:,1])-3,np.mean(self.cathode_mesh[:,2])-np.mean(sumV[:,2])))
			self.setup.add_solid(s12S, displacement=(np.mean(self.cathode_mesh[:,0])-np.mean(sumV[:,0]),np.mean(self.cathode_mesh[:,1])-np.mean(sumV[:,1])-3,np.mean(self.cathode_mesh[:,2])-np.mean(sumV[:,2])))
			self.setup.add_solid(s13S, displacement=(np.mean(self.cathode_mesh[:,0])-np.mean(sumV[:,0]),np.mean(self.cathode_mesh[:,1])-np.mean(sumV[:,1])-3,np.mean(self.cathode_mesh[:,2])-np.mean(sumV[:,2])))
			self.setup.add_solid(s14S, displacement=(np.mean(self.cathode_mesh[:,0])-np.mean(sumV[:,0]),np.mean(self.cathode_mesh[:,1])-np.mean(sumV[:,1])-3,np.mean(self.cathode_mesh[:,2])-np.mean(sumV[:,2])))
			self.setup.add_solid(s15S, displacement=(np.mean(self.cathode_mesh[:,0])-np.mean(sumV[:,0]),np.mean(self.cathode_mesh[:,1])-np.mean(sumV[:,1])-3,np.mean(self.cathode_mesh[:,2])-np.mean(sumV[:,2])))
			self.setup.add_solid(s16S, displacement=(np.mean(self.cathode_mesh[:,0])-np.mean(sumV[:,0]),np.mean(self.cathode_mesh[:,1])-np.mean(sumV[:,1])-3,np.mean(self.cathode_mesh[:,2])-np.mean(sumV[:,2])))
			self.setup.add_solid(s17S, displacement=(np.mean(self.cathode_mesh[:,0])-np.mean(sumV[:,0]),np.mean(self.cathode_mesh[:,1])-np.mean(sumV[:,1])-3,np.mean(self.cathode_mesh[:,2])-np.mean(sumV[:,2])))
			self.setup.add_solid(s18S, displacement=(np.mean(self.cathode_mesh[:,0])-np.mean(sumV[:,0]),np.mean(self.cathode_mesh[:,1])-np.mean(sumV[:,1])-3,np.mean(self.cathode_mesh[:,2])-np.mean(sumV[:,2])))
			self.setup.add_solid(s19S, displacement=(np.mean(self.cathode_mesh[:,0])-np.mean(sumV[:,0]),np.mean(self.cathode_mesh[:,1])-np.mean(sumV[:,1])-3,np.mean(self.cathode_mesh[:,2])-np.mean(sumV[:,2])))
			self.setup.add_solid(s20S, displacement=(np.mean(self.cathode_mesh[:,0])-np.mean(sumV[:,0]),np.mean(self.cathode_mesh[:,1])-np.mean(sumV[:,1])-3,np.mean(self.cathode_mesh[:,2])-np.mean(sumV[:,2])))
			self.setup.add_solid(s21S, displacement=(np.mean(self.cathode_mesh[:,0])-np.mean(sumV[:,0]),np.mean(self.cathode_mesh[:,1])-np.mean(sumV[:,1])-3,np.mean(self.cathode_mesh[:,2])-np.mean(sumV[:,2])))
			self.setup.add_solid(s22S, displacement=(np.mean(self.cathode_mesh[:,0])-np.mean(sumV[:,0]),np.mean(self.cathode_mesh[:,1])-np.mean(sumV[:,1])-3,np.mean(self.cathode_mesh[:,2])-np.mean(sumV[:,2])))
			self.setup.add_solid(s23S, displacement=(np.mean(self.cathode_mesh[:,0])-np.mean(sumV[:,0]),np.mean(self.cathode_mesh[:,1])-np.mean(sumV[:,1])-3,np.mean(self.cathode_mesh[:,2])-np.mean(sumV[:,2])))
			self.setup.add_solid(s24S, displacement=(np.mean(self.cathode_mesh[:,0])-np.mean(sumV[:,0]),np.mean(self.cathode_mesh[:,1])-np.mean(sumV[:,1])-3,np.mean(self.cathode_mesh[:,2])-np.mean(sumV[:,2])))
			self.setup.add_solid(s25S, displacement=(np.mean(self.cathode_mesh[:,0])-np.mean(sumV[:,0]),np.mean(self.cathode_mesh[:,1])-np.mean(sumV[:,1])-3,np.mean(self.cathode_mesh[:,2])-np.mean(sumV[:,2])))
			self.setup.add_solid(s26S, displacement=(np.mean(self.cathode_mesh[:,0])-np.mean(sumV[:,0]),np.mean(self.cathode_mesh[:,1])-np.mean(sumV[:,1])-3,np.mean(self.cathode_mesh[:,2])-np.mean(sumV[:,2])))
			self.setup.add_solid(s27S, displacement=(np.mean(self.cathode_mesh[:,0])-np.mean(sumV[:,0]),np.mean(self.cathode_mesh[:,1])-np.mean(sumV[:,1])-3,np.mean(self.cathode_mesh[:,2])-np.mean(sumV[:,2])))
			self.setup.add_solid(s28S, displacement=(np.mean(self.cathode_mesh[:,0])-np.mean(sumV[:,0]),np.mean(self.cathode_mesh[:,1])-np.mean(sumV[:,1])-3,np.mean(self.cathode_mesh[:,2])-np.mean(sumV[:,2])))
			self.setup.add_solid(s29S, displacement=(np.mean(self.cathode_mesh[:,0])-np.mean(sumV[:,0]),np.mean(self.cathode_mesh[:,1])-np.mean(sumV[:,1])-3,np.mean(self.cathode_mesh[:,2])-np.mean(sumV[:,2])))
			self.setup.add_solid(s30S, displacement=(np.mean(self.cathode_mesh[:,0])-np.mean(sumV[:,0]),np.mean(self.cathode_mesh[:,1])-np.mean(sumV[:,1])-3,np.mean(self.cathode_mesh[:,2])-np.mean(sumV[:,2])))
			self.setup.add_solid(s31S, displacement=(np.mean(self.cathode_mesh[:,0])-np.mean(sumV[:,0]),np.mean(self.cathode_mesh[:,1])-np.mean(sumV[:,1])-3,np.mean(self.cathode_mesh[:,2])-np.mean(sumV[:,2])))
			self.setup.add_solid(s32S, displacement=(np.mean(self.cathode_mesh[:,0])-np.mean(sumV[:,0]),np.mean(self.cathode_mesh[:,1])-np.mean(sumV[:,1])-3,np.mean(self.cathode_mesh[:,2])-np.mean(sumV[:,2])))
			self.setup.add_solid(s33S, displacement=(np.mean(self.cathode_mesh[:,0])-np.mean(sumV[:,0]),np.mean(self.cathode_mesh[:,1])-np.mean(sumV[:,1])-3,np.mean(self.cathode_mesh[:,2])-np.mean(sumV[:,2])))
			self.setup.add_solid(s34S, displacement=(np.mean(self.cathode_mesh[:,0])-np.mean(sumV[:,0]),np.mean(self.cathode_mesh[:,1])-np.mean(sumV[:,1])-3,np.mean(self.cathode_mesh[:,2])-np.mean(sumV[:,2])))
			self.setup.add_solid(s35S, displacement=(np.mean(self.cathode_mesh[:,0])-np.mean(sumV[:,0]),np.mean(self.cathode_mesh[:,1])-np.mean(sumV[:,1])-3,np.mean(self.cathode_mesh[:,2])-np.mean(sumV[:,2])))
			self.setup.add_solid(s36S, displacement=(np.mean(self.cathode_mesh[:,0])-np.mean(sumV[:,0]),np.mean(self.cathode_mesh[:,1])-np.mean(sumV[:,1])-3,np.mean(self.cathode_mesh[:,2])-np.mean(sumV[:,2])))


