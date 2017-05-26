from myimports import *
from array import array
start_begin = time.time() 
print 
print "====================================================================="
arg_list = arg.main(sys.argv[1:])
print "====================================================================="
print "  Start Simulation				Done"
print "====================================================================="
#***************************************************************************
print "hallo" 
print "hallo" 
#***************************************************************************
import add_parts as ap			#import components of the Stanford LXe Setup 
import detectors as det			#import chosen detector
import photon_types as pht 		#import photon creation types 
import propagate_single as prop
#***************************************************************************
print "====================================================================="
print "  Mesh Imports					Successful"
print "====================================================================="
#***************************************************************************
det.ChooseDetector(arg_list[1])
ap.demoSetup.flatten()
ap.setup.flatten()
if(arg_list[2]):
	#view (ap.demoSetup)
	view (ap.setup)
ap.setup.bvh = load_bvh(ap.setup)
sim = Simulation(ap.setup, geant4_processes=0)
#***************************************************************************
numPhotons = arg_list[0]
start_time1 = time.time()
start_time2 = time.time()
"====================initializing root components======================"
runs = 100
radius = array('d', [0] )
mean_coll = 0
event = array('i', [0])
zdir = array('d', [0])
photon_nr = array('d', [0])
gROOT.Reset()
f1 = TFile("data.root", "RECREATE") 
t = TTree("data","data")
t.Branch("event", event, "event/I")
t.Branch("radius", radius, "radius/D")
t.Branch("zdir", zdir, "zdir/D")
t.Branch("photon_nr", photon_nr, "photon_nr/D")

"====================start step by steps simulation===================="
nr_hits = np.zeros((runs))
doRandom = prop.getRandom()
point_zero = data.get_center(ap.o)
#steps = 38
steps = 38
#steps2 = 50
steps2 = 35
incr = .2
schreiben = open("data.dat",'w')
hist = TH2F("hist", "light collection map", steps, 0, steps*incr, steps, 0, steps*incr) 
for k in range(steps):
	for j in range(steps2):
		photonbomb = pht.photon_bomb(numPhotons,175,(point_zero[0]+radius[0], point_zero[1]+1.85-zdir[0], point_zero[2]))
		for i in range(runs):
			photons, photon_track = prop.propagate_photon(photonbomb, numPhotons, 100, ap.setup, doRandom[0], doRandom[1], doRandom[2])
			detected = (photons.flags & (0x1 << 2)).astype(bool) 
			absorbB = (photons.flags & (0x1 << 1)).astype(bool) 
			absorbS = (photons.flags & (0x1 << 3)).astype(bool) 
			specular = (photons.flags & (0x1 << 6)).astype(bool) 
			diffuse = (photons.flags & (0x1 << 5)).astype(bool) 
			nr_hits[i] = len(photons.pos[detected])
			photon_nr[0] = (nr_hits[i]*.15/numPhotons)
			mean_coll += photon_nr[0]
			t.Fill()
			event[0] = event[0]+ 1 
		mean_coll /= runs 
		schreiben.write("%f\t" % radius[0])
		schreiben.write("%f\t" % zdir[0])
		schreiben.write("%f\n" % mean_coll)
		#print "  Numbers	", radius[0], "\t", zdir[0], "\t", i, "\t", nr_hits[i]*.15*22000/numPhotons, "\t", mean_coll, "\t", len(photons.pos[absorbB]), "\t", len(photons.pos[absorbS]), "\t", len(photons.pos[diffuse]), "\t", len(photons.pos[specular])
		print "  Numbers	", radius[0], "\t", zdir[0], "\t", nr_hits[i]*.15*22000/numPhotons, "\t", mean_coll 
		hist.Fill(radius[0], zdir[0], mean_coll)
		radius[0] += incr
	zdir[0] += incr
	radius[0] = 0
hist.Write()
plot.color_map(hist)
t.Write()
f1.Close()
schreiben.close()

pos_all = radius = array('d', [0,0,0] )
vertex = photons.pos[detected] 
messung_dir = photons.dir[detected]
angles = data.incident_angle(messung_dir) 
BIloc = [ap.BIlocx, ap.BIlocy, ap.BIlocz]
v_center = ap.v.get_triangle_centers()
if(arg_list[3]):
	plot.event_display(numPhotons, photon_track, vertex, ap.o_center, v_center, BIloc)


plot.histogram(nr_hits,"Number of photons",10)
plot.histogram(angles,"Incident angles",90)	


plot.scatter_hist(angles,angles)

endPosRotated = photons.pos[absorbB]
endPosRotated2 = photons.pos[absorbS]
endPosRotated3 = photons.pos[diffuse]
endPosRotated4 = photons.pos[specular]
	
fig = plt.figure(figsize=(20, 15))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(endPosRotated[:,0], endPosRotated[:,1], endPosRotated[:,2], c='r')
ax.scatter(endPosRotated2[:,0], endPosRotated2[:,1], endPosRotated2[:,2], c='g')
ax.scatter(endPosRotated3[:,0], endPosRotated3[:,1], endPosRotated3[:,2], c='b')
ax.scatter(endPosRotated4[:,0], endPosRotated4[:,1], endPosRotated4[:,2], c='k')
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')
#ax.title('Position of detection for photons')
#plt.plot(marker='x')
plt.show()
	

	
	
	
	
	
	
	
	
	
	
	
	
	
	
#photonbomb = pht.photon_bomb(numPhotons,175,(point_zero[0]+radius[0], point_zero[1]+1.85-zdir[0], point_zero[2]))
			
#for ev in sim.simulate(photonbomb, keep_photons_beg=True,keep_photons_end=True, run_daq=True, max_steps=100):
	##print "  Time Elapsed for First Simulation:		", (time.time()-start_time2)
	#detected = (ev.photons_end.flags & (0x1 << 2)).astype(bool)
	#transmit = (ev.photons_end.flags & (0x1 << 8)).astype(bool)
	#absorb = (ev.photons_end.flags & (0x1 << 3)).astype(bool) 
	#numDetected = len(ev.photons_end[detected])
	#photon_pos_absorb = ev.photons_end.pos[absorb]
	##print "  Center Location on Plate (x, y):		", d1.mode1,",", d1.mode2
	#print "  Number of Detected Photons:			", numDetected
	#detectPerc = float(float(numDetected)/float(numPhotons))
	#print "  Detection Percentage:				", detectPerc
	#SiPMPDE = .15
	#print "  SiPM PDE Used:				", SiPMPDE
	#probDetect = float(SiPMPDE * float(numDetected))
	#print "  Realistic SiPM Detection Amount (incl. PDE):	", probDetect
	#print "====================================================================="
	#print "  Bi207 Beta Decay Energy: 			~12000 photons/decay"
	#singleDecayNum = float(22000.0 * detectPerc)
	#print "  Hit Detectors per Decay:			", singleDecayNum
	#print "  Poss. Detection vs. DR [1/cm^2]:		", singleDecayNum * SiPMPDE, "vs. 2-3"
	#print "====================================================================="
	#print "  Writing Events to File 			Done"
	#print "====================================================================="
	#print "  Starting Plots				Done"
	#print "====================================================================="
	
	#####PLOTS########PLOTS########PLOTS########PLOTS########PLOTS########PLOTS########
	
	##tempxpos/tempzpos lists of positions, accounting for shift in detector from simulation center
	#endPosRotated = ev.photons_end.pos[absorb]
	#endTrans = ev.photons_end.pos[transmit]
	#fig = plt.figure(figsize=(20, 15))
	#ax = fig.add_subplot(111, projection='3d')
	#ax.scatter(ev.photons_end.pos[:,0], ev.photons_end.pos[:,1], ev.photons_end.pos[:,2])
	#ax.set_xlabel('X Label')
	#ax.set_ylabel('Y Label')
	#ax.set_zlabel('Z Label')
	##ax.title('Teflon Reflectivity ; Demonstration of Sphere Reflectance')
	##plt.plot(marker='x')
	#if(arg_list[3]):
		#plt.show()
		
	#fig = plt.figure(figsize=(20, 15))
	#ax = fig.add_subplot(111, projection='3d')
	#ax.scatter(endPosRotated[:,0], endPosRotated[:,1], endPosRotated[:,2])
	#ax.set_xlabel('X Label')
	#ax.set_ylabel('Y Label')
	#ax.set_zlabel('Z Label')
	##ax.title('Position of detection for photons')
	##plt.plot(marker='x')
	#if(arg_list[3]):
		#plt.show()
		
	#fig = plt.figure(figsize=(20, 15))
	#ax = fig.add_subplot(111, projection='3d')
	#ax.scatter(endTrans[:,0], endTrans[:,1], endTrans[:,2])
	#ax.set_xlabel('X Label')
	#ax.set_ylabel('Y Label')
	#ax.set_zlabel('Z Label')
	##ax.title('Position of detection for photons')
	##plt.plot(marker='x')
	##if(arg_list[3]):
	##	plt.show()
		

print "====================================================================="
print "  Finish Simulation				Done" 
print "  Time elapsed					", time.time()-start_begin, "sec" 
print "====================================================================="
print 
