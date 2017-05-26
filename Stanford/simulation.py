import sys, getopt, time, os, datetime
from chroma.detector import Detector
from chroma.loader import load_bvh
from chroma import view
from chroma.sim import Simulation
import Materials as mat
import cell as cell
import arguments as arg
import photon_types as pht 
import plot as plot
import propagate_single as prop
import numpy as np
import matplotlib.pyplot as plt
from array import array
import ROOT

now = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
path = "/Dropbox/Stanford/data/"+str(now)
home = os.path.expanduser('~')
dir = home + path

start_begin = time.time() 
arg_list = arg.main(sys.argv[1:])

print "====================================================================="
print "  Start Simulation:				Done"

numPhotons = arg_list[0]





path = "/home/exo/Dropbox/Stanford/LXECell_standoff/"
path2 = "/home/exo/Dropbox/Stanford/SiPM/"
cell_path = "/home/exo/Dropbox/Stanford/LXECell_standoff/"
sipm_path = "/home/exo/Dropbox/Stanford/SiPM/"

setup = Detector(mat.vacuum)
Setup = cell.LXeSetup(setup, cell_path = cell_path, sipm_path = sipm_path, detector_choice = arg_list[1])
Setup.build_cell()
Setup.ChooseDetector()
Setup.setup.flatten()
Setup.setup.bvh = load_bvh(Setup.setup)
if(arg_list[2]):
	view(Setup.setup)
sim = Simulation(Setup.setup, geant4_processes=0)

locss = Setup.getSourceLocations()
print "  Number of photon sources:			", len(locss[:,0])

if(arg_list[3]):
	fig = plt.figure(figsize=(20, 15))
	ax = fig.add_subplot(111, projection='3d')
	ax.plot_wireframe(Setup.cathode_mesh[::20,0], Setup.cathode_mesh[::20,1], Setup.cathode_mesh[::20,2], color='r')
	ax.plot_wireframe(Setup.wafer[:,0], Setup.wafer[:,1], Setup.wafer[:,2], color='b')
	ax.plot_wireframe(Setup.window[::20,0], Setup.window[::20,1], Setup.window[::20,2], color='g')
	ax.plot_wireframe(Setup.cf12_blank[::20,0], Setup.cf12_blank[::20,1], Setup.cf12_blank[::20,2], color='k')
	ax.scatter(locss[:,0] ,locss[:,1], locss[:,2])
	ax.set_xlabel('X Label')
	ax.set_ylabel('Y Label')
	ax.set_zlabel('Z Label')
	ax.view_init(elev=0., azim=0.)
	plt.show()


events = []	
for ii in range(len(locss[:,0])):
	photonbomb = pht.photon_bomb(numPhotons,175,locss[ii,:])
	events.append(photonbomb)

hits = np.zeros((int(Setup.runs), len(locss[:,0]), 4))

if(arg_list[4]):
	os.mkdir(dir, 0755)
	radius = array('d', [0] )
	mean_coll = 0
	run = array('i', [0])
	xpos = array('d', [0])
	ypos = array('d', [0])
	zpos = array('d', [0])
	photon_nr = array('d', [0])
	ROOT.gROOT.Reset()
	f1 = ROOT.TFile(dir+"/photons-"+str(numPhotons)+"_det-"+str(arg_list[1])+"_runs-"+str(Setup.runs)+".root", "RECREATE") 
	t = ROOT.TTree("data","data")
	t.Branch("run", run, "run/I")
	t.Branch("xpos", radius, "xpos/D")
	t.Branch("ypos", ypos, "ypos/D")
	t.Branch("zpos", zpos, "zpos/D")
	t.Branch("photon_nr", photon_nr, "photon_nr/D")	


photon_end_position = []

if(arg_list[4]):
	for ii in range(Setup.runs):
		print ii
		for ind, ev in enumerate(sim.simulate(events, keep_photons_beg=True,keep_photons_end=True, run_daq=True, max_steps=100)):
			detected = (ev.photons_end.flags & (0x1 << 2)).astype(bool)
			transmit = (ev.photons_end.flags & (0x1 << 8)).astype(bool)
			absorb = (ev.photons_end.flags & (0x1 << 3)).astype(bool) 
			numDetected = len(ev.photons_end[detected])
			
			test = ev.photons_end.pos[detected]
			photon_end_position = photon_end_position.append(test)
			photon_pos_absorb = ev.photons_end.pos[absorb]
			#print "  Counter:	", ind, "	", numDetected, "	", round(float(locss[ind,0]),2), "	", round(float(locss[ind,1]),2), "	", round(float(locss[ind,2]),2)
			detectPerc = float(float(numDetected)/float(numPhotons))
			SiPMPDE = .15
			probDetect = float(SiPMPDE * float(numDetected))
			singleDecayNum = float(22000.0 * detectPerc)
			hits[ii,ind,3] = numDetected
			hits[ii,ind,0] = locss[ind,0]
			hits[ii,ind,1] = locss[ind,1]
			hits[ii,ind,2] = locss[ind,2]
			xpos[0] = locss[ind,0]
			ypos[0] = locss[ind,1]
			zpos[0] = locss[ind,2]
			run[0] = ii 
			photon_nr[0] = numDetected
			t.Fill()
			#if(arg_list[3]):
				#endPosRotated = ev.photons_end.pos[absorb]
				#endTrans = ev.photons_end.pos[transmit]
				#fig = plt.figure(figsize=(20, 15))
				#ax = fig.add_subplot(111, projection='3d')
				#ax.scatter(ev.photons_end.pos[:,0], ev.photons_end.pos[:,1], ev.photons_end.pos[:,2])
				#ax.set_xlabel('X Label')
				#ax.set_ylabel('Y Label')
				#ax.set_zlabel('Z Label')
		
			
				#fig = plt.figure(figsize=(20, 15))
				#ax = fig.add_subplot(111, projection='3d')
				#ax.scatter(endPosRotated[:,0], endPosRotated[:,1], endPosRotated[:,2])
				#ax.set_xlabel('X Label')
				#ax.set_ylabel('Y Label')
				#ax.set_zlabel('Z Label')

			
				#fig = plt.figure(figsize=(20, 15))
				#ax = fig.add_subplot(111, projection='3d')
				#ax.scatter(endTrans[:,0], endTrans[:,1], endTrans[:,2])
				#ax.set_xlabel('X Label')
				#ax.set_ylabel('Y Label')
				#ax.set_zlabel('Z Label')
				#plt.show()
			#print "---------------------------------------------------------------------"

print len(photon_end_position[:,0])
plot.hist_3D(photon_end_position)


t.Write()
f1.Close()
#plot.histogram(hits, xlabel = "detected photons", bin_nr = 100)
print "  Finish Simulation				Done" 
print "  Time elapsed					", time.time()-start_begin, "sec" 
print "=====================================================================\n"
