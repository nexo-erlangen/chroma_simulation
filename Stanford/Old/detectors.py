from myimports import * 

import add_parts as ap

def ChooseDetector(Choice):
	if Choice == 'pmt':
		largePMT = Solid (make.cylinder (6.7, .01), mat.fullAbsorb, mat.quartz, surface = surf.fulldetect, color=0xff0000) 	#red
		PMT_glas = Solid (make.cylinder (7.8, .01), mat.quartz, mat.vacuum, color=0xCCFF00)	#green
		#PMT_mesh = Mesh(largePMT)
		#pmt_center = PMT_mesh.get_triangle_centers()
		ap.setup.add_pmt(largePMT,rotation= None, displacement = (ap.meanX,ap.bottomY-.02,ap.meanZ))
		ap.setup.add_pmt(PMT_glas,rotation= None, displacement = (ap.meanX,ap.bottomY-.01,ap.meanZ))
		ap.demoSetup.add_solid(largePMT, rotation= None, displacement = (ap.meanX,ap.bottomY-4.01,ap.meanZ))
		ap.demoSetup.add_pmt(PMT_glas,rotation= None, displacement = (ap.meanX,ap.bottomY,ap.meanZ))
