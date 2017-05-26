from myimports import * 

import add_parts as ap
path = "/home/chroma/chroma_env/stanford/new/LXECell_standoff/"

green = 0xff00
blue = 0x0000ff

def ChooseDetector(Choice):
	if Choice == 'pmt':
		pmt = mesh_from_stl(path+"pmt_window2.stl")
		pmtS = Solid(pmt, mat.quartz, data.bottom(pmt,mat.MSuprasil,mat.LXenon), data.radius_bottom(pmt, surf.fulldetect, None), data.radius_bottom(pmt, green, blue))
		#ap.demoSetup.add_pmt(pmtS,rotation = make_rotation_matrix(np.pi,(0,0,1)), displacement = (ap.meanX,ap.meanY-((ap.thickness+10.0)/2),ap.meanZ))
		ap.setup.add_pmt(pmtS,rotation = make_rotation_matrix(np.pi,(0,0,1)), displacement = (ap.meanX,ap.meanY-((ap.thickness+0.0)/2),ap.meanZ))
		
