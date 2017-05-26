from chroma import make, view
from chroma.geometry import Geometry, Material, Solid, Surface, Mesh
from chroma import optics
from chroma.transform import make_rotation_matrix
from chroma.demo.optics import glass, water, vacuum
from chroma.demo.optics import black_surface, r7081hqe_photocathode
from chroma.loader import create_geometry_from_obj
from chroma.detector import Detector
from chroma.pmt import build_pmt
from chroma.event import Photons
from chroma.sim import Simulation
from chroma.sample import uniform_sphere
import lensmaterials as lm
import numpy as np
from chroma.transform import make_rotation_matrix, get_perp, rotate, rotate_matrix, normalize
from matplotlib.ticker import NullFormatter
import time
import sys, getopt #ako
from chroma.stl import mesh_from_stl
import setupMaterials as sm
import arguments as main 


print "====================================================================="

#if __name__ == "__main__":
main.main(sys.argv[1:])
from chroma.sim import Simulation
from chroma import sample
from chroma.event import Photons
import chroma.event as chromaev
from chroma.loader import load_bvh
from chroma.generator import vertex
from chroma.io.root import RootWriter
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
#import photonModifierBB180 as pmBB180

print "====================================================================="
print "  Numpy version:				", np.__version__
print "====================================================================="
print "  LXE TEST SETUP SIMULATION"
print "====================================================================="
#creation of detector!!!! In this code, we add the detector upon choosing which one below
setup = Detector(lm.vacuum)
print "  Blank Vacuum Setup Created..."
#for photon bomb location
demoSetup = Detector(lm.vacuum)
#Photon Bomb Position (In View Model, look for "location", a yellow solid)


while(True):
	a = mesh_from_stl("/home/exo/chroma_env/stanford/LXE Cell/LXE CELL ASSY - CF 12 BLANK ASSY CF 275-1 CF 12 BLANK WELD ASSY CF 275-1 CF 12 BLANK-1.STL")
	aS = Solid(a, sm.fullAbsorb, lm.vacuum, sm.steelSurface)
	setup.add_solid(aS, displacement=(0,0,0))
	
	b = mesh_from_stl("/home/exo/chroma_env/stanford/LXE Cell/LXE CELL ASSY - CF 12 BLANK ASSY CF 275-1 IME WAFER IN MOUNT-1 ANODE MOUNTING PLATE V2-1.STL")
	bS = Solid(b, sm.fullAbsorb, lm.vacuum, sm.steelSurface)
	setup.add_solid(bS, displacement=(0,0,0))
	
	c = mesh_from_stl("/home/exo/chroma_env/stanford/LXE Cell/LXE CELL ASSY - CF 12 BLANK ASSY CF 275-1 IME WAFER IN MOUNT-1 CERAMIC INTERFACE BOARD ASSY-1 CERAMIC INTERFACE BOARD-1.STL")
	cS = Solid(c, sm.fullAbsorb, lm.vacuum, sm.steelSurface)
	setup.add_solid(cS, displacement=(0,0,0))
	
	d = mesh_from_stl("/home/exo/chroma_env/stanford/LXE Cell/LXE CELL ASSY - CF 12 BLANK ASSY CF 275-1 IME WAFER IN MOUNT-1 CERAMIC INTERFACE BOARD ASSY-1 CERAMIC INTERFACE BOARD TRACE-1.STL")
	dS = Solid(d, sm.fullAbsorb, lm.vacuum, sm.steelSurface)
	setup.add_solid(dS, displacement=(0,0,0))
	
	e = mesh_from_stl("/home/exo/chroma_env/stanford/LXE Cell/LXE CELL ASSY - CF 12 BLANK ASSY CF 275-1 IME WAFER IN MOUNT-1 CERAMIC INTERFACE BOARD ASSY-2 CERAMIC INTERFACE BOARD-1.STL")
	eS = Solid(e, sm.fullAbsorb, lm.vacuum, sm.steelSurface)
	setup.add_solid(eS, displacement=(0,0,0))
	
	f = mesh_from_stl("/home/exo/chroma_env/stanford/LXE Cell/LXE CELL ASSY - CF 12 BLANK ASSY CF 275-1 IME WAFER IN MOUNT-1 CERAMIC INTERFACE BOARD ASSY-2 CERAMIC INTERFACE BOARD TRACE-1.STL")
	fS = Solid(f, sm.fullAbsorb, lm.vacuum, sm.steelSurface)
	setup.add_solid(fS, displacement=(0,0,0))
	
	g = mesh_from_stl("/home/exo/chroma_env/stanford/LXE Cell/LXE CELL ASSY - CF 12 BLANK ASSY CF 275-1 IME WAFER IN MOUNT-1 SUPPORTED READOUT W ANODE PADS-1 QUARTZ WAFER-1.STL")
	gS = Solid(g, sm.fullAbsorb, lm.vacuum, sm.steelSurface)
	setup.add_solid(gS, displacement=(0,0,0))
	
	h = mesh_from_stl("/home/exo/chroma_env/stanford/LXE Cell/LXE CELL ASSY - CF 12 BLANK ASSY CF 275-1 IME WAFER IN MOUNT-1 SUPPORTED READOUT W ANODE PADS-1 WIRE BOND PAD-1.STL")
	hS = Solid(h, sm.fullAbsorb, lm.vacuum, sm.steelSurface)
	setup.add_solid(hS, displacement=(0,0,0))
	
	i = mesh_from_stl("/home/exo/chroma_env/stanford/LXE Cell/LXE CELL ASSY - CF 12 SPOOL CUSTOM-1 CF 12 FLANGE-1.STL")
	iS = Solid(i, sm.fullAbsorb, lm.vacuum, sm.steelSurface)
	setup.add_solid(iS, displacement=(0,0,0))
	
	j = mesh_from_stl("/home/exo/chroma_env/stanford/LXE Cell/LXE CELL ASSY - CF 12 SPOOL CUSTOM-1 CF 12 FLANGE-2.STL")
	jS = Solid(j, sm.fullAbsorb, lm.vacuum, sm.steelSurface)
	setup.add_solid(jS, displacement=(0,0,0))
	
	k = mesh_from_stl("/home/exo/chroma_env/stanford/LXE Cell/LXE CELL ASSY - CF 12 SPOOL CUSTOM-1 CF 12 TUBE-1.STL")
	kS = Solid(k, sm.fullAbsorb, lm.vacuum, sm.steelSurface)
	setup.add_solid(kS, displacement=(0,0,0))
	
	l = mesh_from_stl("/home/exo/chroma_env/stanford/LXE Cell/LXE CELL ASSY - reducer_w_viewport_assy-1 CATHODE ASSY W FILLER BLOCKS-1 CATHODE ASSY-1 #4-40 X 0.25 SCREW BU-402-NA-1.STL")
	lS = Solid(l, sm.fullAbsorb, lm.vacuum, sm.steelSurface)
	setup.add_solid(lS, displacement=(0,0,0))
	
	m = mesh_from_stl("/home/exo/chroma_env/stanford/LXE Cell/LXE CELL ASSY - reducer_w_viewport_assy-1 CATHODE ASSY W FILLER BLOCKS-1 CATHODE ASSY-1 #4 VENTED WASHER 96861A200-1.STL")
	mS = Solid(m, sm.fullAbsorb, lm.vacuum, sm.steelSurface)
	setup.add_solid(mS, displacement=(0,0,0))
	
	BIsourceM = mesh_from_stl("/home/exo/chroma_env/stanford/LXE Cell/LXE CELL ASSY - reducer_w_viewport_assy-1 CATHODE ASSY W FILLER BLOCKS-1 CATHODE ASSY-1 Bi Source-1.STL")
	BIsourceS = Solid(BIsourceM, sm.fullAbsorb, lm.vacuum, sm.steelSurface)
	#setup.add_solid(BIsourceS, displacement=(0,0,0))
	demoSetup.add_solid(BIsourceS, displacement=(0,0,0))
	
	BItriangCent = BIsourceM.get_triangle_centers()
	#print BItriangCent [:,0], BItriangCent [:,1], BItriangCent [:,2]
	BIlocx = np.mean(BItriangCent[:,0])
	BIlocy = np.mean(BItriangCent[:,1])
	BIlocz = np.mean(BItriangCent[:,2])
	print "====================================================================="
	print "  Bismuth Source Triangle Centers		x:",BIlocx
	print "						y:",BIlocy
	print "						z:",BIlocz
	print "====================================================================="
	
	o = mesh_from_stl("/home/exo/chroma_env/stanford/LXE Cell/LXE CELL ASSY - reducer_w_viewport_assy-1 CATHODE ASSY W FILLER BLOCKS-1 CATHODE ASSY-1 CATHODE MESH-1.STL")
	oS = Solid(o, sm.fullAbsorb, lm.vacuum, sm.steelSurface)
	setup.add_solid(oS, displacement=(0,0,0))
	
	p = mesh_from_stl("/home/exo/chroma_env/stanford/LXE Cell/LXE CELL ASSY - reducer_w_viewport_assy-1 CATHODE ASSY W FILLER BLOCKS-1 CATHODE ASSY-1 CATHODE SUPPORT RING BOTTOM-1.STL")
	pS = Solid(p, sm.fullAbsorb, lm.vacuum, sm.steelSurface)
	setup.add_solid(pS, displacement=(0,0,0))
	
	q = mesh_from_stl("/home/exo/chroma_env/stanford/LXE Cell/LXE CELL ASSY - reducer_w_viewport_assy-1 CATHODE ASSY W FILLER BLOCKS-1 CATHODE ASSY-1 CATHODE SUPPORT RING TOP-1.STL")
	qS = Solid(q, sm.fullAbsorb, lm.vacuum, sm.steelSurface)
	setup.add_solid(qS, displacement=(0,0,0))
	
	r = mesh_from_stl("/home/exo/chroma_env/stanford/LXE Cell/LXE CELL ASSY - reducer_w_viewport_assy-1 CATHODE ASSY W FILLER BLOCKS-1 FILLER BLOCK-1.STL")
	rS = Solid(r, sm.fullAbsorb, lm.vacuum, sm.steelSurface)
	setup.add_solid(rS, displacement=(0,0,0))
	
	s = mesh_from_stl("/home/exo/chroma_env/stanford/LXE Cell/LXE CELL ASSY - reducer_w_viewport_assy-1 REDUCER WELD ASSY-1 reducer_CF12_CF6-1.STL")
	sS = Solid(s, sm.fullAbsorb, lm.vacuum, sm.steelSurface)
	setup.add_solid(sS, displacement=(0,0,0))
	
	t = mesh_from_stl("/home/exo/chroma_env/stanford/LXE Cell/LXE CELL ASSY - reducer_w_viewport_assy-1 viewport_6in_w_bolts-1 viewport_6in_MDC_9722009-1 0194605B-1.STL")
	tS = Solid(t, sm.fullAbsorb, lm.vacuum, sm.steelSurface)
	setup.add_solid(tS, displacement=(0,0,0))
	
	u = mesh_from_stl("/home/exo/chroma_env/stanford/LXE Cell/LXE CELL ASSY - reducer_w_viewport_assy-1 viewport_6in_w_bolts-1 viewport_6in_MDC_9722009-1 1004603A-1 0194303C-1.STL")
	uS = Solid(u, sm.fullAbsorb, lm.vacuum, sm.steelSurface)
	setup.add_solid(uS, displacement=(0,0,0))
	
	v = mesh_from_stl("/home/exo/chroma_env/stanford/LXE Cell/LXE CELL ASSY - reducer_w_viewport_assy-1 viewport_6in_w_bolts-1 viewport_6in_MDC_9722009-1 1004603A-1 1002204A-1.STL")
	vS = Solid(v, sm.fullAbsorb, lm.vacuum, sm.steelSurface)
	setup.add_solid(vS, displacement=(0,0,0))
	demoSetup.add_solid(vS, displacement=(0,0,0))
	
	#rgbM = mesh_from_stl("/home/exo/chroma_env/stanford/LXE Cell/RGB-HD/RGB-HD - SiPM 2x6 .045in with Plate-1.STL")
	#rgbS1 = Solid(rgbM, sm.fullAbsorb, lm.ls, surface = lm.fulldetect, color = 0x33de22de)
	#rgbS2 = Solid(rgbM, sm.fullAbsorb, lm.ls, surface = lm.fulldetect, color = 0x33de22de)
	#rgbS3 = Solid(rgbM, sm.fullAbsorb, lm.ls, surface = lm.fulldetect, color = 0x33de22de)
	
	
	triangleCenters = v.get_triangle_centers()
	#triangleCenters [:,0], triangleCenters [:,1], triangleCenters [:,2]
	meanX = np.mean(triangleCenters[:,0])
	meanY = np.mean(triangleCenters[:,1])
	meanZ = np.mean(triangleCenters[:,2])
	print "  Cap Triangle Centers				x:" ,meanX
	print "						y:",meanY
	print "						z:",meanZ
	print "====================================================================="
	print "  Adjusted Bismuth center 			x:",BIlocx-meanX
	print "  (oriented to cap) 				z:",BIlocz-meanZ
	print "====================================================================="
	#general reference shift Chroma to STL
	xshift = meanX
	zshift = meanZ
	#center of detector, in respect to chroma axes
	
	largePMT = Solid (make.box (200, .5, 200), sm.fullAbsorb, lm.ls, surface = lm.fulldetect, color = 0x33de22de)
	testSiPM = Solid (make.box (10, .5, 10), sm.fullAbsorb, lm.ls, surface = lm.fulldetect, color = 0x33de22de)
	testSiPMCover = Solid (make.box (10.25, .5, 10.25), sm.fullAbsorb, lm.ls, surface = lm.fulldetect, color = 0x0033CC)
	displacement = (meanX,meanY-10,meanZ)
	
	#Now we need to reajust for location in detector 
	#triangleCentersRGB = rgbM.get_triangle_centers()
	#rgbX = np.mean(triangleCentersRGB[:,0])
	#rgbY = np.mean(triangleCentersRGB[:,1])
	#rgbZ = np.mean(triangleCentersRGB[:,2])
	#print "rgb x y z", rgbX, rgbY, rgbZ
	#diffRGBX = rgbX - meanX
	#diffRGBY = rgbY - meanY
	#diffRGBZ = rgbZ - meanZ
	#print "diffRGB x y z", diffRGBX, diffRGBY, diffRGBZ
	#subtract by these to get RGB in cap location
	'''
	print "Detector Choice?"
	try:
		detectChoice = raw_input("Large pmt ('l'), SiPM ('s'), or RGB's: ")
	except:
		print "OK then..."
	'''
	detectChoice='l'
		
	if detectChoice == 's':
		print "Input detector positions in setup reference frame"
		print "(origin = cap triangle centers; look to adjusted Bi centers above)"
		print "Note: optimum position is ~x=7, ~z=-40"
		print "Height from base y (0 is touching)"
		while (True):
			try:
				mode1=float(raw_input('X pos:'))
				SiPMshiftx = mode1 + meanX
				break;
			except ValueError:
					print ("Not a number.")
		while (True):
			try:
				mode2=float(raw_input('Z pos:'))
				SiPMshiftz = mode2 + meanZ
				break;
			except ValueError:
					print ("Not a number.")
		while (True):
			try:
				mode3=float(raw_input('Y pos (Height from Base):'))
				yadd = mode3
				break;
			except ValueError:
					print ("Not a number.")			
		
		SiPMshifty = meanY+3.7+yadd
		
		print "Chroma location of SiPM; x,y,z:", SiPMshiftx, SiPMshifty, SiPMshiftz
		#oriented around center of conflat flange...at say x=20 and z=0, rotation needs to be 0,and x=0 z=20, rotation needs to be pi/2 cc, so we use basic rotation (arctan(y/x))
		degRot = float(np.arctan(float(mode2)/float(mode1)))
		
		"""
		distanceFromBiX = BIlocx - SiPMshiftx
		distanceFromBiY = BIlocy - SiPMshifty
		distanceFromBiZ = BIlocz - SiPMshiftz
		#rotation matrices for each
		rotXY = np.arctan(float(distanceFromBiZ)/float(distanceFromBiY))
		rotZY = np.arctan(float(distanceFromBiX)/float(distanceFromBiY))
		print "Lift rotations:", rotXY, rotZY
		rotationXY = [[np.cos(rotXY),-np.sin(rotXY), 0],[np.sin(rotXY),np.cos(rotXY),0],[0,0,1]]
		antiDegRotXY = -rotXY
		antiRotationXY = [[np.cos(antiDegRotXY),-np.sin(antiDegRotXY), 0],[np.sin(antiDegRotXY),np.cos(antiDegRotXY),0],[0,0,1]]
		rotationZY = [[1,0,0],[0,np.cos(rotZY),-np.sin(rotZY)],[0,np.sin(rotZY),np.cos(rotZY)]]
		antiDegRotZY = -rotZY
		antiRotationZY = [[1,0,0],[0,np.cos(antiDegRotZY),-np.sin(antiDegRotZY)],[0,np.sin(antiDegRotZY),np.cos(antiDegRotZY)]]
		"""
		
		#degRot = 0
		print "Degrees to Rotate around Y axis:", degRot*180.0/np.pi
		
		rotation = [[np.cos(degRot),0,-np.sin(degRot)],[0,1,0],[np.sin(degRot),0,np.cos(degRot)]]
		antiDegRot = -degRot
		antiRotation = [[np.cos(antiDegRot),0,-np.sin(antiDegRot)],[0,1,0],[np.sin(antiDegRot),0,np.cos(antiDegRot)]]
		
		
		
		print "Rotation matrix XZ:", rotation
		
		#print "Rotation matrix XY:", rotationXY
		#print "Rotation matrix ZY:", rotationZY
		#totRotation = np.dot(rotationXY, rotationZY)
		#totRotation = np.dot(rotation, totRotation)
		
		totRotation = rotation
		print "totRotation shape:", np.shape(totRotation)
		print "totRotation:", totRotation
		makeRotation = make_rotation_matrix (degRot, (0,1,0))
		print "maeRotation matrix:", makeRotation #wow, of course this existed...look at transform!
		
		setup.add_pmt(testSiPM,totRotation, displacement = (SiPMshiftx,SiPMshifty,SiPMshiftz))
		demoSetup.add_solid(testSiPM, totRotation, displacement = (SiPMshiftx,SiPMshifty,SiPMshiftz))
		setup.add_solid(testSiPMCover,totRotation, displacement = (SiPMshiftx,SiPMshifty-.25,SiPMshiftz))
		demoSetup.add_solid(testSiPMCover, totRotation, displacement = (SiPMshiftx,SiPMshifty-.05,SiPMshiftz))
		print
		fromSourceDistance = np.sqrt((SiPMshiftx-BIlocx)**2+(SiPMshifty+.5-BIlocy)**2+(SiPMshiftz-BIlocz)**2)
		print "Distance of SiPM from Bi Source", fromSourceDistance
		
	elif detectChoice == 'l':
		mode1,mode2 = 1,0
		degRot = float(np.arctan(float(mode2)/float(mode1)))
		#degRot = 0
		print "Degrees to Rotate:", degRot*180.0/np.pi
		
		rotation = [[np.cos(degRot),0,-np.sin(degRot)],[0,1,0],[np.sin(degRot),0,np.cos(degRot)]]
		antiDegRot = -degRot
		antiRotation = [[np.cos(antiDegRot),0,-np.sin(antiDegRot)],[0,1,0],[np.sin(antiDegRot),0,np.cos(antiDegRot)]]

		setup.add_pmt(largePMT,rotation= None, displacement = (meanX,meanY+4,meanZ))
		demoSetup.add_solid(largePMT, displacement = (meanX,meanY+4,meanZ))
	
	else:
		print "RGB DETECTORS CHOSEN"
		print "Input detector positions in setup reference frame"
		print "(origin = cap triangle centers; look to adjusted Bi centers above)"
		print "Note: optimum position is ~x=7, ~z=-40"
		print "Height from base y (0 is touching)"
		while (True):
			try:
				mode1=float(raw_input('X pos:'))
				RGBshiftx = mode1
				break;
			except ValueError:
					print ("Not a number.")
		while (True):
			try:
				mode2=float(raw_input('Z pos:'))
				RGBshiftz = mode2
				break;
			except ValueError:
					print ("Not a number.")
		while (True):
			try:
				mode3=float(raw_input('Y pos (Height from Base):'))
				yadd = mode3
				break;
			except ValueError:
					print ("Not a number.")			
		
		RGBshifty = 3.7+yadd #to get to cap inner surface height 3.5
		
		RGBshiftx = RGBshiftx - diffRGBX
		RGBshifty = RGBshifty - diffRGBY
		RGBshiftz = RGBshiftz - diffRGBZ
		
		print "Chroma location of RGB; x,y,z:", RGBshiftx, RGBshifty, RGBshiftz
		#oriented around center of conflat flange...at say x=20 and z=0, rotation needs to be 0,and x=0 z=20, rotation needs to be pi/2 cc, so we use basic rotation (arctan(y/x))
		degRot = float(np.arctan(float(mode2)/float(mode1)))
		degRot = degRot + np.pi/2.0
		#degRot = 0
		print "Degrees to Rotate around Y axis:", degRot*180.0/np.pi
		
		rotation = [[np.cos(degRot),0,-np.sin(degRot)],[0,1,0],[np.sin(degRot),0,np.cos(degRot)]]
		antiDegRot = -degRot
		antiRotation = [[np.cos(antiDegRot),0,-np.sin(antiDegRot)],[0,1,0],[np.sin(antiDegRot),0,np.cos(antiDegRot)]]
		
		print "Rotation matrix XZ:", rotation
		totRotation = rotation
		print "totRotation shape:", np.shape(totRotation)
		print "totRotation:", totRotation
		makeRotation = make_rotation_matrix (degRot, (0,1,0))
		print "maeRotation matrix:", makeRotation #wow, of course this existed...look at transform!
		
		#we must create amounts to move RGB 2 and 3
		
		moveRGBz = 3*np.sin(degRot)
		moveRGBx = 3*np.cos(degRot)
		
		#setup.add_pmt(rgbS1,totRotation, displacement = (RGBshiftx,RGBshifty,RGBshiftz))
		#demoSetup.add_solid(rgbS1, totRotation, displacement = (RGBshiftx,RGBshifty,RGBshiftz))
		
		setup.add_pmt(rgbS2,totRotation, displacement = (RGBshiftx+moveRGBx,RGBshifty,RGBshiftz+moveRGBz))
		demoSetup.add_solid(rgbS1, totRotation, displacement = (RGBshiftx+moveRGBx,RGBshifty,RGBshiftz+moveRGBz))
		
		setup.add_pmt(rgbS3,totRotation, displacement = (RGBshiftx-moveRGBx,RGBshifty,RGBshiftz-moveRGBz))
		demoSetup.add_solid(rgbS1, totRotation, displacement = (RGBshiftx-moveRGBx,RGBshifty,RGBshiftz-moveRGBz))
		
		print
		fromSourceDistance = np.sqrt((RGBshiftx-BIlocx)**2+(RGBshifty+.5-BIlocy)**2+(RGBshiftz-BIlocz)**2)
		print "Distance of SiPM from Bi Source", fromSourceDistance
	break


print "Mesh Imports Successful"
demoSetup.flatten()
setup.flatten()

#view (demoSetup)
#view (setup)

setup.bvh = load_bvh(setup)
sim = Simulation(setup, geant4_processes=0)


#PHOTONS Creation Types

# photon bomb, isotropic from position center
def photon_bomb(n,wavelength,pos):
    pos = np.tile(pos,(n,1))
    dir = uniform_sphere(n)
    pol = np.cross(dir,uniform_sphere(n))
    wavelengths = np.repeat(wavelength,n)
    print np.shape(pos)
    print np.shape(dir)
    print np.shape(pol)
    print np.shape(wavelengths)
    return Photons(pos,dir,pol,wavelengths)

#defines disk with photons coming randomly out of the disk surface, in any direction
def photon_area_bomb(n, diameter, wavelength, x, y, z):
    radii = np.random.uniform(0, diameter/2, n)
    angles = np.random.uniform(0, 2*np.pi, n)
    points = np.empty((n,3))
    points[:,0] = np.sqrt(diameter/2)*np.sqrt(radii)*np.cos(angles) + x
    points[:,1] = np.repeat(y, n)
    points[:,2] = np.sqrt(diameter/2)*np.sqrt(radii)*np.sin(angles) + z
    pos = points
    #print "Ten Points of Photon Start Positions"
    #print points[:10]
    dir = uniform_sphere(n)
    pol = np.cross(dir, uniform_sphere(n))
    wavelengths = np.repeat(wavelength, n)
    return Photons(pos, dir, pol, wavelengths)


# write it to a root file
from chroma.io.root import RootWriter
subName = ""
fileName = ('LXEdata%s.root' % subName) #naming file
f1 = RootWriter(fileName)

# pause to separate e-s from photon bomb
# print 'Press enter to continue'


'''
while (True):
	try:
    		mode=int(raw_input('Number of Photons to Simulate: '))
		break;
	except ValueError:
    		print ("Not a number.")
'''
mode=1000

numPhotons = mode


#numPhotons = 10000

start_time1 = time.time()
#Point Bomb
photonbomb = photon_bomb(numPhotons,150,(BIlocx,BIlocy,BIlocz))

#Area Bomb (Realistic)
#photonareabomb = photon_area_bomb(numPhotons, 10, 178, xshift, yshift, zshift)
print("--- %s seconds photonbomb method ---" % (time.time() - start_time1))
start_time2 = time.time()

#note -- may want to try to mimic the source better. Choose random point on a filled disk, and random direction to simulate photon. This would make it seem more like the radioactive source, which has an area dimension to the surface (around 1 cm? check next time go into lab). Look above for code

#bomb type?? check
for ev in sim.simulate(photonbomb, keep_photons_beg=True,keep_photons_end=True, run_daq=True,max_steps=100):
	print "Time Elapsed for First Simulation:", (time.time()-start_time2)
	print len(ev.photons_end)
	detected = (ev.photons_end.flags & (0x1 << 2)).astype(bool)
	numDetected = len(ev.photons_end[detected])
	#print "Elevation from Base:", yadd, "mm"
	print "Center Location on Plate (x, y):", mode1, mode2
	print "Num Detected:", numDetected
	detectPerc = float(float(numDetected)/float(numPhotons))
	print "Detection Percentage:", detectPerc
	SiPMPDE = .15
	print "SiPM PDE Used:", SiPMPDE
	probDetect = float(SiPMPDE * float(numDetected))
	print "Realistic SiPM Detection Amount (Accounting for PDE):", probDetect
	print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
	print "Bi207 Betay Decay Energy: ~12000 photons/decay"
	singleDecayNum = float(12000.0 * detectPerc)
	print "Hit Detectors per Decay:", singleDecayNum
	print "Possible Detection (PDE) vs Dark Rate:", singleDecayNum * SiPMPDE, "vs. 2-3 dark hits/cm^2"

	print "Events Written to File"
	
	print "Starting Plots"
	
	
	####PLOTS########PLOTS########PLOTS########PLOTS########PLOTS########PLOTS########PLOTS########PLOTS####
	
	#tempxpos/tempzpos lists of positions, accounting for shift in detector from simulation center
	endPosRotated = ev.photons_end.pos[detected]
	endPosRotated[:,0] = endPosRotated[:,0] - xshift
	endPosRotated[:,2] = endPosRotated[:,2] - zshift
	print "Test endPosRotated (before rotation):", endPosRotated[0], endPosRotated[1]
	#antirotation
	for x in range(0,len(endPosRotated)):
		endPosRotated[x] = np.dot(antiRotation, endPosRotated[x])
	
	tempxpos = endPosRotated[:,0]
	tempzpos = endPosRotated[:,2]
	
	#BIlocx and BIlocz if you want the center to be oriented to bismuth source rather than LXE Cell "cap" (center for setup)
	#tempxpos[:] = [x - xshift for x in tempxpos]
	#tempzpos[:] = [z - zshift for z in tempzpos]
	
	#time to rotate back into correct orientation....this will make plots symmetrical on axes (rather than rotated)

	
	tempxposMax = max(tempxpos[:])
	tempzposMax = max(tempzpos[:])
	tempxposmin = min(tempxpos[:])
	tempzposmin = min(tempzpos[:])
	
	#plt.scatter(ev.photons_end.pos[detected][:,0], ev.photons_end.pos[detected][:,2])
	
	#X v Z Individual Hits
		#fig = plt.figure(figsize=(6, 6))
	#plt.scatter(tempxpos, tempzpos)
		#plt.axis((-50, 50, -50, 50))
		#plt.xlabel('Final X-Position (mm)')
		#plt.ylabel('Final Z-Position (mm)')
		#plt.title('Hit Detection Locations')
		#plt.show()

	print "Position Radius v Time"
	#Position Radius v Time
	fig = plt.figure(figsize=(5, 12))
	tempList = np.sqrt(tempxpos*tempxpos+tempzpos*tempzpos)
	maxTempList = max(tempList[:])
	maxTimeDetected = max(ev.photons_end.t[detected])
	plt.scatter(tempList, ev.photons_end.t[detected])
	plt.axis((0,maxTempList+(maxTempList*.2),0,maxTimeDetected+(maxTimeDetected*.2)))
	plt.xlabel('Final Position: Radius from Center of Detector')
	plt.ylabel('Time Elapsed Before Detection')
	plt.title('Teflon Reflectivity ; Demonstration of Sphere Reflectance')
	#plt.show()
	print "Done."
	
	print "Heat Map of Detected Positions"
	#Heat Map of Detection Locations
	fig = plt.figure(figsize=(7.8, 6))
	rangeX = max(tempxpos[:])-min(tempxpos[:])
	rangeZ = max(tempzpos[:])-min(tempzpos[:])
	rangeSquare = int(rangeX*rangeZ)
	print
	print "X detection positions: max, min, mean, std"
	print max(tempxpos[:]), min(tempxpos[:]), float(float(sum(tempxpos[:]))/float(len(tempxpos))), np.std(tempxpos)
	print "Z detection positions: max, min, mean, std"
	print max(tempzpos[:]), min(tempzpos[:]), float(float(sum(tempzpos[:]))/float(len(tempzpos))), np.std(tempzpos)
	
	plt.hist(tempxpos, bins=130) 
	#akoedit:plt.hist(tempxpos, tempzpos, bins=130) 
        #150?
	plt.axis((tempxposmin-2, tempxposMax+2, tempzposmin-2, tempzposMax+2))
	plt.xlabel('Final X-Position (m)')
	plt.ylabel('Final Z-Position (m)')
	degrees = degRot*180.0/np.pi
	plt.title('Heat Map; Repositioned and Rotated %s Degrees' % degrees)
	#plt.colorbar()
	#plt.show()
	print "Done."

	print "Angular Distribution"
	#Angular Distribution: Radius of Location vs Angle of Incidence
	#We need to graph the appropiate angle distribution that photons hit the detector at. We can get this by crossing the photon vectors with the 

	detectedDirections = ev.photons_end.dir[detected]
	print ("Detected Photon Directions Shape: "), detectedDirections.shape

	listPi = np.tile(np.pi/2,numDetected)
	
	anglesFromPlane = listPi[:]-np.arcsin(np.absolute(detectedDirections[:,1])/((detectedDirections[:,0]**2+detectedDirections[:,1]**2+detectedDirections[:,2]**2)**(1/2)))
	#conversion to degrees
	anglesFromPlane[:] = [(x*180/(np.pi)) for x in anglesFromPlane]
	
	print "anglesFromPlane: max, min, mean, std"
	print max(anglesFromPlane[:]), min(anglesFromPlane[:]), float(float(sum(anglesFromPlane[:]))/float(len(anglesFromPlane))), np.std(anglesFromPlane)
	
	#testAngles = np.arcsin((hello[:,1])/(hello[:,0]**2+hello[:,1]**2+hello[:,2]**2)**(1/2))
	#print detectedDirections
	#print detectedDirections.shape
	#print testAngles
	#print anglesFromPlane
	#NOW to compare to landing positions on detector, x radius from center, y detection angles

	tempList = np.sqrt(tempxpos*tempxpos+tempzpos*tempzpos)
	#tempListBounce = np.sqrt(tempxposBounce*tempxposBounce+tempzposBounce*tempzposBounce)
	maxTempList = max(tempList[:])
	plt.scatter(anglesFromPlane, tempList)
	plt.axis((0,90, 0,maxTempList+(maxTempList*.2)))
	plt.ylabel('Final Position: Radius from Center of Detector')
	plt.xlabel('Angle in Degrees')
	plt.title('Radius from Center of Detector vs. Photon Angle from Plane Normal')
	#plt.show()
	print "Done."
	
	print "Scatter Plot, Histogram of Each Axis"
	#Histogram with Scatter Plots
	# the random data
	x = anglesFromPlane
	#y = tempListBounce
	y = tempList

	nullfmt   = NullFormatter()         # no labels

	# definitions for the axes
	left, width = 0.1, 0.65
	bottom, height = 0.1, 0.65
	bottom_h = left_h = left+width+0.02

	rect_scatter = [left, bottom, width, height]
	rect_histx = [left, bottom_h, width, 0.2]
	rect_histy = [left_h, bottom, 0.2, height]

	# start with a rectangular Figure
	plt.figure(1, figsize=(7.8,6))

	axScatter = plt.axes(rect_scatter)
	axHistx = plt.axes(rect_histx)
	axHisty = plt.axes(rect_histy)

	# no labels
	axHistx.xaxis.set_major_formatter(nullfmt)
	axHisty.yaxis.set_major_formatter(nullfmt)

	# the scatter plot:
	axScatter.scatter(x, y)

	# now determine nice limits by hand:
	binwidth = 1
	xymax = np.max( [np.max(np.fabs(x)), np.max(np.fabs(y))] )
	lim = ( int(xymax/binwidth) + 1) * binwidth

	axScatter.set_xlim( (0, 90) )
	axScatter.set_ylim( (0, maxTempList+maxTempList*.1) )

	bins = np.arange(0, lim + binwidth, binwidth)
	axHistx.hist(x, bins=bins)
	axHisty.hist(y, bins=20, orientation='horizontal')

	axHistx.set_xlim( axScatter.get_xlim() )
	axHisty.set_ylim( axScatter.get_ylim() )

	#plt.show()
	print "Done."
		
	#f1.write_event(ev)   

	
	                   		
	
f1.close()
print "File closed."




