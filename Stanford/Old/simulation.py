from myimports import *
start_begin = time.time() 
print 
print "====================================================================="
arg_list = arg.main(sys.argv[1:])
print "====================================================================="
print "  Start Simulation				Done"
print "====================================================================="
#***************************************************************************
from myimports import * 
#***************************************************************************
import add_parts as ap			#import components of the LXe Setup 
import detectors as det		#import chosen detector
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
	view (ap.setup)
	view (ap.demoSetup)
ap.setup.bvh = load_bvh(ap.setup)
sim = Simulation(ap.setup, geant4_processes=0)
#***************************************************************************
numPhotons = arg_list[0]
start_time1 = time.time()
photonbomb = pht.photon_bomb(numPhotons,175,(ap.BIlocx,ap.BIlocy,ap.BIlocz))
start_time2 = time.time()
##***************************************************************************
#runs = 500
#nr_hits = np.zeros((runs))
#doRandom = prop.getRandom()
#for eg in range(runs):
	#photons, photon_track = prop.propagate_photon(photonbomb, numPhotons, 20, ap.setup, doRandom[0], doRandom[1], doRandom[2])
	#detected = (photons.flags & (0x1 << 2)).astype(bool) 
	#nr_hits[eg] = len(photons.pos[detected])*.15 
	##print "  Number of photons detected			", nr_hits[eg]
	
#fig = plt.figure(figsize=(20, 10))
#sns.distplot(nr_hits, bins=20, kde=False, rug=True)
#plt.show()	


#photons, photon_track = prop.propagate_photon(photonbomb, numPhotons, 20, ap.setup) 

#print "  Number of photons detected			", len(photons.pos[detected])
#messung = photons.pos[detected] 
#messung_dir = photons.dir[detected]
#angles = data.incident_angle(messung_dir) 


#if(arg_list[3]):
	#fig = plt.figure(figsize=(20, 10))
	#ax = fig.add_subplot(111, projection='3d')
	#for i in range(numPhotons):
		#X,Y,Z = photon_track[:,i,0].tolist(), photon_track[:,i,1].tolist(), photon_track[:,i,2].tolist()
		#X.insert(0, ap.BIlocx)
		#Y.insert(0, ap.BIlocy)
		#Z.insert(0, ap.BIlocz)
		#ax.plot(X,Y,Z, 'b')	
		#ax.scatter(X,Y,Z ,color='r', s=.5)		
	#ax.plot_wireframe(ap.o_center[::200,0], ap.o_center[::200,1], ap.o_center[::200,2], color = 'g')
	#ax.plot_wireframe(ap.v_center[::20,0], ap.v_center[::20,1], ap.v_center[::20,2], color = 'g')
	#ax.scatter(messung[:,0], messung[:,1], messung[:,2], color='c', s=5)	
	#ax.set_xlabel('X Label')
	#ax.set_ylabel('Y Label')
	#ax.set_zlabel('Z Label')
	#ax.view_init(elev=3., azim=0)
	#plt.savefig('event_display.pdf') 
	#plt.show()	
	
	#print "hallo"
	
	
	#fig = plt.figure(figsize=(15, 10))	
	#plt.hist(angles, bins=50) 
	#plt.xlabel('Incident angle ')
	#plt.ylabel('frequency [#]')
	#plt.title('Histogram of incident angles')
	#plt.savefig('incident_angle.pdf') 
	##plt.show()
	
	#print "hallo"
	
	#fig = plt.figure(figsize=(20, 10))
	#sns.distplot(angles, bins=10, kde=False, rug=True)
	##plt.show()
	
	#print "hallo"

	#plot.scatter_hist(angles,angles)
	
if(arg_list[4]):	
	for ev in sim.simulate(photonbomb, keep_photons_beg=True,keep_photons_end=True, run_daq=True, max_steps=100):
		#print "  Time Elapsed for First Simulation:		", (time.time()-start_time2)
		detected = (ev.photons_end.flags & (0x1 << 2)).astype(bool)
		transmit = (ev.photons_end.flags & (0x1 << 8)).astype(bool)
		numDetected = len(ev.photons_end[detected])
		print "  Number of Detected Photons:			", numDetected
		detectPerc = float(float(numDetected)/float(numPhotons))
		print "  Detection Percentage:				", detectPerc
		SiPMPDE = .15
		print "  SiPM PDE Used:				", SiPMPDE
		probDetect = float(SiPMPDE * float(numDetected))
		print "  Realistic SiPM Detection Amount (incl. PDE):	", probDetect
		print "====================================================================="
		print "  Bi207 Beta Decay Energy: 			~12000 photons/decay"
		singleDecayNum = float(22000.0 * detectPerc)
		print "  Hit Detectors per Decay:			", singleDecayNum
		print "  Poss. Detection vs. DR [1/cm^2]:		", singleDecayNum * SiPMPDE, "vs. 2-3"
		print "====================================================================="
		print "  Writing Events to File 			Done"
		print "====================================================================="
		print "  Starting Plots				Done"
		print "====================================================================="
		
		####PLOTS########PLOTS########PLOTS########PLOTS########PLOTS########PLOTS########
		
		#tempxpos/tempzpos lists of positions, accounting for shift in detector from simulation center
		endPosRotated = ev.photons_end.pos[detected]
		endTrans = ev.photons_end.pos[transmit]
		fig = plt.figure(figsize=(20, 15))
		ax = fig.add_subplot(111, projection='3d')
		ax.scatter(ev.photons_end.pos[:,0], ev.photons_end.pos[:,1], ev.photons_end.pos[:,2])
		ax.set_xlabel('X Label')
		ax.set_ylabel('Y Label')
		ax.set_zlabel('Z Label')
		#ax.title('Teflon Reflectivity ; Demonstration of Sphere Reflectance')
		#plt.plot(marker='x')
		if(arg_list[3]):
			plt.show()
			
		fig = plt.figure(figsize=(20, 15))
		ax = fig.add_subplot(111, projection='3d')
		ax.scatter(endPosRotated[:,0], endPosRotated[:,1], endPosRotated[:,2])
		ax.set_xlabel('X Label')
		ax.set_ylabel('Y Label')
		ax.set_zlabel('Z Label')
		#ax.title('Position of detection for photons')
		#plt.plot(marker='x')
		if(arg_list[3]):
			plt.show()
			
		fig = plt.figure(figsize=(20, 15))
		ax = fig.add_subplot(111, projection='3d')
		ax.scatter(endTrans[:,0], endTrans[:,1], endTrans[:,2])
		ax.set_xlabel('X Label')
		ax.set_ylabel('Y Label')
		ax.set_zlabel('Z Label')
		#ax.title('Position of detection for photons')
		#plt.plot(marker='x')
		#if(arg_list[3]):
		#	plt.show()
		

print "====================================================================="
print "  Finish Simulation				Done" 
print "  Time elapsed					", time.time()-start_begin, "sec" 
print "====================================================================="
print 
