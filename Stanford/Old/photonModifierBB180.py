from chroma import make, view
from chroma.geometry import Geometry, Material, Solid, Surface, Mesh
from chroma import optics
from chroma.transform import make_rotation_matrix
from chroma.demo.optics import glass, water, vacuum
from chroma.demo.optics import black_surface, r7081hqe_photocathode
from chroma.loader import create_geometry_from_obj
from chroma.detector import Detector
from chroma.pmt import build_pmt
from chroma.event import Photons #!!!
from chroma.sim import Simulation
from chroma.sample import uniform_sphere
import lensmaterials as lm
import numpy as np
from matplotlib.ticker import NullFormatter
#import pyparsing
import time
from chroma.stl import mesh_from_stl
import setupMaterials as sm
from chroma.sim import Simulation
from chroma import sample
from chroma.event import Photons
import chroma.event as chromaev
from chroma.loader import load_bvh
from chroma.generator import vertex
from chroma.io.root import RootWriter
from chroma.io.root import RootReader
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from chroma.rootimport import ROOT

#from transmissionPoints import SiO2transmit

#Read the files
#Write the arrays
#import arrays to wavelengthShiftBB
BB180transmit = np.array([(160.0, 0.001), (170, .25), (175,  .33), (176.0,  .35), (180.0,  .36), (184.0,  .35), (185.0,  .35), (189.0,  .30), (190.0,  .29), (200.0,  .17), (205.0,  .11), (210.0,  .075), (220.0,  .04), (240.0,  .02), (260.0,  .005)]) #http://www.pelhamresearchoptical.com/broadband.html
test = False #Debugging purposes, or just halt in part 1 of simulation. Runs it from this point (see bottom)


def find_nearest_lower(array, wav):#one dimensional array, wavelength to find lower value. If same as wavelenght on array, returns array value
	numRows = 0
	#number of rows in array given...
	for y in array:
		numRows = numRows + 1 
	x=0
	#index values x from 0 to numRows-1
	while (x < numRows):
		temp = array[x]
		#if wav to test is less than wavelength value in array index x
		if ((wav-temp)<=0):
			#print "Returned index", x-1
			#returns lower value of x
			return x-1
		x = x+1
	#return last index value in array, since wav is greater than all array wavelength values
	return x-1
	
#for an individual wavelength, give an associated transmission percentage and return that float (oblivious to shift)
#new method can be chosen for different transmission curves
def transmitPercentBB180(wavelength): 

	transmitArray = BB180transmit 
	transmitWav = transmitArray[:,0]
	
	#simply put, creating a linear function between upper and lower points on transmission curve and finding value of wavelength on the line
	lowerIndex = find_nearest_lower(transmitWav, wavelength)
	#if wavelength is lower than all wavelength points in array
	if (lowerIndex < 0):
		return transmitArray [0,1]
	upperIndex = lowerIndex+1
	if (upperIndex > (len(transmitArray[:,0])-1)):
		return transmitArray [lowerIndex,1]
		
	diffWav = wavelength-transmitArray[lowerIndex,0]
	diffPerc = transmitArray[upperIndex,1]-transmitArray[lowerIndex,1]
	slopeDiff = transmitArray[upperIndex,0]-transmitArray[lowerIndex,0]
	#slope between points
	diffPercSlope = diffPerc/slopeDiff
	#percentage transmittance of lower index, plus slope times wavelength difference from wavelength to wavelength in array
	newPercent = transmitArray[lowerIndex,1]+diffWav*diffPercSlope
	
	return newPercent
	
#"shifts" photon wavelengths, and filters photons, depending on the array list BB180
def wavelengthShiftBB180(initPhotons):
	initDirs = initPhotons.dir
	initWavs = initPhotons.wavelengths
	initPos = initPhotons.pos
	initPol = initPhotons.pol
	mods = initPhotons #photons to change
	
	#getting the angle of incidence -- pi/2 - inverse sin of (y/(x^2+y^2+z^2)^(1/2)), this returns angle from norm, which is pi/2
	listHalfPi = np.tile(np.pi/2,len(initPhotons))
	initAngles = listHalfPi[:]-np.arcsin((initDirs[:,1])/((initDirs[:,0]**2+initDirs[:,1]**2+initDirs[:,2]**2)**(1/2)))
	#conversion to degrees
	initAngles = [(x*180/(np.pi)) for x in initAngles]
	
	#shifting the wavelengths
	#For this process, we assume that the shift from 0 to 45 degrees is linear, where 0 is 0 shift and 45 is 10nm wafelength shift right (towards larger wavelengths)
	#It may be better suited to filter photons before, and then on those leftover do the calculations
	initShifts = initAngles
	initShifts =  [(x/45 * 10) for x in initShifts]
	
	#conversion of wavelengths with shift amounts, initShifts
	tempWavs = initWavs 
	tempWavs[:] = tempWavs[:]+initShifts[:] #corresponding photon wavelengths shifted to the right appropiately, simulating the percentage transmittance shift left
	print 

	print "Number of tempWavelengths (same as number of initPhotons:", len(tempWavs)
	
	#Now associating each photon a transmission percentage, which is based upon its temporary wavelength and BB180 transmission curve
	transmitPerc= initPhotons.wavelengths
	print tempWavs[:20]
	for x in range(len(tempWavs)):
		wav = tempWavs[x]
		perc = transmitPercentBB180(wav) #appropiate percentages for each wavelength
		transmitPerc[x] = perc
	
	for x in range(0,20):
		print "Transmit Perc for photon", x,":", transmitPerc[x]

	dieRoll = np.random.uniform(0, 1,len(initDirs))
	marked = np.tile(1, len(initDirs))
	print marked
	for x in range(0,len(initDirs)):
		#print "For wavlength", tempWavs[x], ":", dieRoll[x], ">=", transmitPerc[x], "?", 
		if(dieRoll[x] >= transmitPerc[x]):
			marked[x] = 0
			#print "Yes: to remove"
		#else:
			#print "No: to stay"
	print float(float(np.sum(marked))/(len(marked)))
	#something = np.delete(photonMods, 3)
	for y in range(0, len(marked)):
		backVal = len(marked)-(y+1)
		if (marked[backVal] == 0):
			initDirs = np.delete(initDirs, backVal, 0)
			initWavs = np.delete(initWavs, backVal)
			initPos = np.delete(initPos, backVal, 0)
			initPol = np.delete(initPol, backVal, 0)
		if (backVal == 0):
			print 
			print "Original Photon List Length:", len(initPhotons)
			print "Modified Photon List Length:", len(initWavs)
	print np.shape(initDirs)
	print np.shape(initPos)
	print np.shape(initPol)
	print np.shape(initWavs)
	
	beforeRef = Photons(initPos,initDirs,initPol,initWavs)
	afterRef = photonReflection(0,beforeRef)
	return afterRef
	
#perfect reflection, depending on percentage...very basic at this stage, hopefully percentage is a factor of incidence angle
def photonReflection (percentage, initPhotons):
	initDirs = initPhotons.dir
	initWavs = initPhotons.wavelengths
	initPos = initPhotons.pos
	initPol = initPhotons.pol
	
	photonLen = len(initWavs)
	dieRoll = np.random.uniform(0, 1,photonLen)
	for x in range (0, photonLen):
		if (dieRoll[x] < percentage):
			initDirs[x,1] = -initDirs[x,1]
	
	return Photons(initPos,initDirs,initPol,initWavs)
		
	
def photonMods(importFile): #returns modified photons for new simulation
	from chroma.io.root import RootWriter
	from chroma.io.root import RootReader
	fRead = RootReader(importFile)
	fWrite = RootWriter('modifiedData.root')
	
	for ev in fRead:
		#Seperating Detected Photon Properties from photons that do not hit the filter "detector"
		detected = (ev.photons_end.flags & (0x1 << 2)).astype(bool)
		detectedDirections = ev.photons_end.dir[detected]
		detectedPositions = ev.photons_end.pos[detected]
		detectedWavelengths = ev.photons_end.wavelengths[detected]
		detectedPols = ev.photons_end.pol[detected]
	
		initDetected = Photons(detectedPositions, detectedDirections, detectedPols, detectedWavelengths)
		#list of photons to wavelengthShift, which returns list of photons that "make it through" the filter
		
		modifiedPhotons = wavelengthShiftBB180(initDetected)
		return modifiedPhotons
		
	
	
def letsSimulate1(fileName):
	"""#Material Properties
	print ("Material Properties test (check setupMaterials.py).") #Un-comment to display

	print ("BB Material absorption length")
	print sm.BB180.absorption_length
	print ("Quartz Material absorption length")
	print sm.quartz.absorption_length
	print ("Teflon Surface absorption")
	print sm.teflonSurface.absorb

	try:
		blah=raw_input("Press ENTER to Continue to simulation...")
	except:
		print ('OK then...')
	"""
	print
	print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
	print ("2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2")
	print ("Simulation Teflon Sphere Setup PART TWO")
	print
	#creation of detector!!!! In this code, we add the detector upon choosing which one below
	setup = Detector(lm.vacuum)
	print ("Blank Vacuum Setup Created...")
	#for photon bomb location
	demoSetup = Detector(lm.vacuum)
	#Photon Bomb Position (In View Model, look for "location", a yellow solid)

	print
	print ("Choose one of the following detectors (YOU ONLY HAVE ONE CHOICE NOW, AND THAT IS THE LAST CHOICE)")
	print ("2x2mm SiPM, Full Detector, No Filter, No Quartz Window, No Viewmodel.")
	print
	print ("--------------------------------------------------------")
	print 
	print ("What SiPM do you want to load?")
	print ("'a' - 2mmx2mm")
	print ("'b' - 1cmx1cm")
	print ("'c' - Super-5")
	print ("'d' - MEG")
	print ("'e' - PMT R9875p")
	#more choices in the future...will have to convert to newly oriented teflon sphere (where square opening sides are parallel with axis).

	
	while (True): #IMPORTING MESHES FROM STL's. While is just for collapsing in editor and false choices
		try:
			choice=raw_input()
		except:
			print ('OK then...')
			
		if (choice == 'a'): #2mmx2mm
			print ("Loading 2mmx2mm")
			detectorChoice = "2mmx2mm"
			detector = mesh_from_stl("/media/LUPIN/Double Beta Decay/Solid Works/STL Files/New Oriented Sphere Files/Chroma Assembly 2mmx2mm/Chroma Assembly 2mmx2mm - 2x2 cm Assembly-1 Simple 2x2 mm detector-1.STL")

			ceramicSubM = mesh_from_stl("/media/LUPIN/Double Beta Decay/Solid Works/STL Files/New Oriented Sphere Files/Chroma Assembly 2mmx2mm/Chroma Assembly 2mmx2mm - 2x2 cm Assembly-1 Simple Ceramic Substrate-1.STL")
			conflatFlangeM = mesh_from_stl("/media/LUPIN/Double Beta Decay/Solid Works/STL Files/New Oriented Sphere Files/Chroma Assembly 2mmx2mm/Chroma Assembly 2mmx2mm - Conflat Flange Main part-1.STL")
			copperPlateM = mesh_from_stl("/media/LUPIN/Double Beta Decay/Solid Works/STL Files/New Oriented Sphere Files/Chroma Assembly 2mmx2mm/Chroma Assembly 2mmx2mm - Copper Plate Attached Lower Ring-1.STL")
			filterCylinderM = mesh_from_stl("/media/LUPIN/Double Beta Decay/Solid Works/STL Files/New Oriented Sphere Files/Chroma Assembly 2mmx2mm/Chroma Assembly 2mmx2mm - Filter-1.STL")
			insertM = mesh_from_stl("/media/LUPIN/Double Beta Decay/Solid Works/STL Files/New Oriented Sphere Files/Chroma Assembly 2mmx2mm/Chroma Assembly 2mmx2mm - Insertion .785 inch-1.STL")
			steelBaseM = mesh_from_stl("/media/LUPIN/Double Beta Decay/Solid Works/STL Files/New Oriented Sphere Files/Chroma Assembly 2mmx2mm/Chroma Assembly 2mmx2mm - Simple-1.STL")
			teflonSphereM = mesh_from_stl("/media/LUPIN/Double Beta Decay/Solid Works/STL Files/New Oriented Sphere Files/Chroma Assembly 2mmx2mm/Chroma Assembly 2mmx2mm - Teflon Sphere 3-8 inch_4.5diameter Revised 2-1.STL")
			quartzWindowM = mesh_from_stl("/media/LUPIN/Double Beta Decay/Solid Works/STL Files/New Oriented Sphere Files/Chroma Assembly 2mmx2mm/Chroma Assembly 2mmx2mm - Glass-1.STL")
			
			#solid Creations
			ceramicSubS = Solid(ceramicSubM, sm.fullAbsorb, lm.vacuum, sm.steelSurface, color = 0xdaa520)
			conflatFlangeS = Solid(conflatFlangeM, sm.fullAbsorb, lm.vacuum, sm.steelSurface)
			copperPlateS = Solid(copperPlateM, sm.fullAbsorb, lm.vacuum, sm.steelSurface)
			quartzWindowS = Solid(quartzWindowM, sm.quartz, lm.vacuum, surface = None)
			filterCylinderS = Solid(filterCylinderM, sm.BB180, lm.vacuum, surface = None, color = 0x33ff4040) #angle of incidence
			insertS = Solid(insertM, sm.fullAbsorb, lm.vacuum, sm.steelSurface)
			steelBaseS = Solid(steelBaseM, sm.fullAbsorb, lm.vacuum, sm.steelSurface)
			teflonSphereS = Solid(teflonSphereM, sm.teflon, lm.vacuum, sm.teflonSurface)
			#Notes on teflon properties
			#changed surface to steel(full absorb surface), and  results make sense.
			#changed back to sm.teflonSurface, absorb must be set before diffuse/specular!!!! Of course, it is so obvious now! The hat goes on the head!
			
			setup.add_solid(ceramicSubS, displacement=(0,0,0))
			setup.add_solid(insertS, displacement=(0,0,0))
			sipmS = Solid(detector, sm.fullAbsorb, lm.vacuum, surface = lm.fulldetect, color = 0x8a2be2)
			setup.add_pmt(sipmS,rotation= None, displacement = (0,0,0))
			
			#This is a small square solid that is used in orienting the photon start location in the demo setup
			location = Solid (make.box (.5, .5, .5), lm.vacuum, lm.vacuum, sm.nothing, 0x33ffff00)
			
			print "Average of Triangle Centers (to get estimate pmt location) from Teflon Sphere: x,y,z coordinates"
			triangleCenters = teflonSphereM.get_triangle_centers()
			print triangleCenters [:,0], triangleCenters [:,1], triangleCenters [:,2]
			meanX = np.mean(triangleCenters[:,0])
			meanY = np.mean(triangleCenters[:,1])
			meanZ = np.mean(triangleCenters[:,2])
			print "x:",meanX, "y:",meanY, "z:",meanZ
			print

			#General Center Photon Bomb Location, Orientation of setup
			xshift = meanX
			yshiftDetector = meanY
			yshift = 10
			zshift = meanZ

			#LARGE pmt, variable placement (input parameter below)
			largePMT = Solid (make.box (100, 1.0, 100), sm.fullAbsorb, lm.ls, surface = lm.fulldetect, color = 0x33de22de)
			sourceCylinder = Solid (make.cylinder(5, 1), sm.fullAbsorb, lm.ls, surface = sm.steelSurface, color = 0x33bb00ee)

			#used in orientation only, x y and z axes for small adjustments of photon start locations
			testPMTx = Solid (make.box (5, .5, .5), glass, lm.ls, surface = lm.fulldetect)
			testPMTy = Solid (make.box (.5, 10, .5), glass, lm.ls, surface = lm.fulldetect)
			testPMTz = Solid (make.box (.5, .5, 15), lm.ls, lm.ls, surface = lm.fulldetect)
			
			#DEMO####
			#for adjustments, and so you can see detector location and other things
			#demo setup, for bomb location and modification
			#demoSetup.add_solid(ceramicSubS, displacement=(0,0,0))
			#demoSetup.add_solid(conflatFlangeS, displacement=(0,0,0))
			demoSetup.add_solid(copperPlateS, displacement=(0,0,0))
			#demoSetup.add_solid(filterCylinderS, displacement=(0,0,0))
			demoSetup.add_solid(insertS, displacement=(0,0,0))
			#demoSetup.add_solid(steelBaseS, displacement=(0,0,0))
			#demoSetup.add_solid(teflonSphereS, displacement=(0,0,0))
			#demoSetup.add_solid(quartzWindowS, displacement=(0,0,0))

			#orientation and position axis
			demoSetup.add_solid(testPMTx, displacement=(xshift+20,120,zshift+20))
			demoSetup.add_solid(testPMTy, displacement=(xshift+20,120,zshift+20))
			demoSetup.add_solid(testPMTz, displacement=(xshift+20,120,zshift+20))

			demoSetup.add_pmt(sipmS,rotation= None, displacement = (0,0,0))
			demoSetup.add_solid(sourceCylinder, displacement=(xshift,yshift,zshift))



			demoSetup.add_solid(location,rotation= None, displacement = (xshift-.25,yshift-.51,zshift-.25))
			#setup.add_solid(location,rotation= None, displacement = (xshift-.25,yshift-.51,zshift-.25))
			#-.25 to get small location square centered, .51 so it doesn't interfere with simulation photons
			########
			
			print ("Successfully 2mmx2mm'ed")
			break

		elif (choice == 'b'): #1cmx1cm
			print ("Loading 1cmx1cm")
			detectorChoice = "1cmx1cm"
			detector = mesh_from_stl("/media/LUPIN/Double Beta Decay/Solid Works/STL Files/New Oriented Sphere Files/Chroma Assembly 1cmx1cm/Chroma Assembly 1cmx1cm - 2x2 cm Assembly-1 Simple 2x2 mm detector-1.STL")
			
			ceramicSubM = mesh_from_stl("/media/LUPIN/Double Beta Decay/Solid Works/STL Files/New Oriented Sphere Files/Chroma Assembly 1cmx1cm/Chroma Assembly 1cmx1cm - 2x2 cm Assembly-1 Simple Ceramic Substrate-1.STL")
			conflatFlangeM = mesh_from_stl("/media/LUPIN/Double Beta Decay/Solid Works/STL Files/New Oriented Sphere Files/Chroma Assembly 1cmx1cm/Chroma Assembly 1cmx1cm - Conflat Flange Main part-1.STL")
			copperPlateM = mesh_from_stl("/media/LUPIN/Double Beta Decay/Solid Works/STL Files/New Oriented Sphere Files/Chroma Assembly 1cmx1cm/Chroma Assembly 1cmx1cm - Copper Plate Attached Lower Ring-1.STL")
			filterCylinderM = mesh_from_stl("/media/LUPIN/Double Beta Decay/Solid Works/STL Files/New Oriented Sphere Files/Chroma Assembly 1cmx1cm/Chroma Assembly 1cmx1cm - Filter-1.STL")
			insertM = mesh_from_stl("/media/LUPIN/Double Beta Decay/Solid Works/STL Files/New Oriented Sphere Files/Chroma Assembly 1cmx1cm/Chroma Assembly 1cmx1cm - Insertion .785 inch-1.STL")
			steelBaseM = mesh_from_stl("/media/LUPIN/Double Beta Decay/Solid Works/STL Files/New Oriented Sphere Files/Chroma Assembly 1cmx1cm/Chroma Assembly 1cmx1cm - Simple-1.STL")
			teflonSphereM = mesh_from_stl("/media/LUPIN/Double Beta Decay/Solid Works/STL Files/New Oriented Sphere Files/Chroma Assembly 1cmx1cm/Chroma Assembly 1cmx1cm - Teflon Sphere 3-8 inch_4.5diameter Revised 2-1.STL")
			quartzWindowM = mesh_from_stl("/media/LUPIN/Double Beta Decay/Solid Works/STL Files/New Oriented Sphere Files/Chroma Assembly 1cmx1cm/Chroma Assembly 1cmx1cm - Glass-1.STL")

			#solid Creations
			ceramicSubS = Solid(ceramicSubM, sm.fullAbsorb, lm.vacuum, sm.steelSurface, color = 0xdaa520)
			conflatFlangeS = Solid(conflatFlangeM, sm.fullAbsorb, lm.vacuum, sm.steelSurface)
			copperPlateS = Solid(copperPlateM, sm.fullAbsorb, lm.vacuum, sm.steelSurface)
			quartzWindowS = Solid(quartzWindowM, sm.quartz, lm.vacuum, surface = None)
			filterCylinderS = Solid(filterCylinderM, sm.BB180, lm.vacuum, surface = None, color = 0x33ff4040) #angle of incidence
			insertS = Solid(insertM, sm.fullAbsorb, lm.vacuum, sm.steelSurface)
			steelBaseS = Solid(steelBaseM, sm.fullAbsorb, lm.vacuum, sm.steelSurface)
			teflonSphereS = Solid(teflonSphereM, sm.teflon, lm.vacuum, sm.teflonSurface)
			#Notes on teflon properties
			#changed surface to steel(full absorb surface), and  results make sense.
			#changed back to sm.teflonSurface, absorb must be set before diffuse/specular!!!! Of course, it is so obvious now! The hat goes on the head!
			
			setup.add_solid(ceramicSubS, displacement=(0,0,0))
			setup.add_solid(insertS, displacement=(0,0,0))
			sipmS = Solid(detector, sm.fullAbsorb, lm.vacuum, surface = lm.fulldetect, color = 0x8a2be2)
			setup.add_pmt(sipmS,rotation= None, displacement = (0,0,0))
			
			#This is a small square solid that is used in orienting the photon start location in the demo setup
			location = Solid (make.box (.5, .5, .5), lm.vacuum, lm.vacuum, sm.nothing, 0x33ffff00)
			
			print "Average of Triangle Centers (to get estimate pmt location) from Teflon Sphere: x,y,z coordinates"
			triangleCenters = teflonSphereM.get_triangle_centers()
			print triangleCenters [:,0], triangleCenters [:,1], triangleCenters [:,2]
			meanX = np.mean(triangleCenters[:,0])
			meanY = np.mean(triangleCenters[:,1])
			meanZ = np.mean(triangleCenters[:,2])
			print "x:",meanX, "y:",meanY, "z:",meanZ
			print

			#General Center Photon Bomb Location, Orientation of setup
			xshift = meanX
			yshiftDetector = meanY
			yshift = 10
			zshift = meanZ

			#LARGE pmt, variable placement (input parameter below)
			largePMT = Solid (make.box (100, 1.0, 100), sm.fullAbsorb, lm.ls, surface = lm.fulldetect, color = 0x33de22de)
			sourceCylinder = Solid (make.cylinder(5, 1), sm.fullAbsorb, lm.ls, surface = sm.steelSurface, color = 0x33bb00ee)

			#used in orientation only, x y and z axes for small adjustments of photon start locations
			testPMTx = Solid (make.box (5, .5, .5), glass, lm.ls, surface = lm.fulldetect)
			testPMTy = Solid (make.box (.5, 10, .5), glass, lm.ls, surface = lm.fulldetect)
			testPMTz = Solid (make.box (.5, .5, 15), lm.ls, lm.ls, surface = lm.fulldetect)
			
			#DEMO####
			#for adjustments, and so you can see detector location and other things
			#demo setup, for bomb location and modification
			#demoSetup.add_solid(ceramicSubS, displacement=(0,0,0))
			#demoSetup.add_solid(conflatFlangeS, displacement=(0,0,0))
			demoSetup.add_solid(copperPlateS, displacement=(0,0,0))
			#demoSetup.add_solid(filterCylinderS, displacement=(0,0,0))
			demoSetup.add_solid(insertS, displacement=(0,0,0))
			#demoSetup.add_solid(steelBaseS, displacement=(0,0,0))
			#demoSetup.add_solid(teflonSphereS, displacement=(0,0,0))
			#demoSetup.add_solid(quartzWindowS, displacement=(0,0,0))

			#orientation and position axis
			demoSetup.add_solid(testPMTx, displacement=(xshift+20,120,zshift+20))
			demoSetup.add_solid(testPMTy, displacement=(xshift+20,120,zshift+20))
			demoSetup.add_solid(testPMTz, displacement=(xshift+20,120,zshift+20))

			demoSetup.add_pmt(sipmS,rotation= None, displacement = (0,0,0))
			demoSetup.add_solid(sourceCylinder, displacement=(xshift,yshift,zshift))



			demoSetup.add_solid(location,rotation= None, displacement = (xshift-.25,yshift-.51,zshift-.25))
			#setup.add_solid(location,rotation= None, displacement = (xshift-.25,yshift-.51,zshift-.25))
			#-.25 to get small location square centered, .51 so it doesn't interfere with simulation photons
			########
			
			print ("Successfully 1cmx1cm'ed")
			break

		elif (choice == 'c'): #Super-5
			print ("Loading Super-5")
			detectorChoice = "Super-5"
			detector1 = mesh_from_stl("/media/LUPIN/Double Beta Decay/Solid Works/STL Files/New Oriented Sphere Files/Chroma Assembly Super-5/Chroma Assembly Super-5 - Super-5 Assembly-1 .180x.180x.005in-1.STL")
			detector2 = mesh_from_stl("/media/LUPIN/Double Beta Decay/Solid Works/STL Files/New Oriented Sphere Files/Chroma Assembly Super-5/Chroma Assembly Super-5 - Super-5 Assembly-1 .180x.180x.005in-2.STL")
			detector3 = mesh_from_stl("/media/LUPIN/Double Beta Decay/Solid Works/STL Files/New Oriented Sphere Files/Chroma Assembly Super-5/Chroma Assembly Super-5 - Super-5 Assembly-1 .180x.180x.005in-3.STL")
			detector4 = mesh_from_stl("/media/LUPIN/Double Beta Decay/Solid Works/STL Files/New Oriented Sphere Files/Chroma Assembly Super-5/Chroma Assembly Super-5 - Super-5 Assembly-1 .180x.180x.005in-4.STL")
			detector5 = mesh_from_stl("/media/LUPIN/Double Beta Decay/Solid Works/STL Files/New Oriented Sphere Files/Chroma Assembly Super-5/Chroma Assembly Super-5 - Super-5 Assembly-1 .180x.180x.005in-5.STL")
			
			sipmS1 = Solid(detector1, sm.fullAbsorb, lm.vacuum, surface = lm.fulldetect, color = 0x8a2be2)
			sipmS2 = Solid(detector2, sm.fullAbsorb, lm.vacuum, surface = lm.fulldetect, color = 0x8a2be2)
			sipmS3 = Solid(detector3, sm.fullAbsorb, lm.vacuum, surface = lm.fulldetect, color = 0x8a2be2)
			sipmS4 = Solid(detector4, sm.fullAbsorb, lm.vacuum, surface = lm.fulldetect, color = 0x8a2be2)
			sipmS5 = Solid(detector5, sm.fullAbsorb, lm.vacuum, surface = lm.fulldetect, color = 0x8a2be2)
			
			ceramicSubM = mesh_from_stl("/media/LUPIN/Double Beta Decay/Solid Works/STL Files/New Oriented Sphere Files/Chroma Assembly 1cmx1cm/Chroma Assembly 1cmx1cm - 2x2 cm Assembly-1 Simple Ceramic Substrate-1.STL")
			conflatFlangeM = mesh_from_stl("/media/LUPIN/Double Beta Decay/Solid Works/STL Files/New Oriented Sphere Files/Chroma Assembly Super-5/Chroma Assembly Super-5 - Conflat Flange Main part-1.STL")
			copperPlateM = mesh_from_stl("/media/LUPIN/Double Beta Decay/Solid Works/STL Files/New Oriented Sphere Files/Chroma Assembly Super-5/Chroma Assembly Super-5 - Copper Plate Attached Lower Ring-1.STL")
			filterCylinderM = mesh_from_stl("/media/LUPIN/Double Beta Decay/Solid Works/STL Files/New Oriented Sphere Files/Chroma Assembly Super-5/Chroma Assembly Super-5 - Filter-1.STL")
			insertM = mesh_from_stl("/media/LUPIN/Double Beta Decay/Solid Works/STL Files/New Oriented Sphere Files/Chroma Assembly Super-5/Chroma Assembly Super-5 - Insertion .785 inch-1.STL")
			steelBaseM = mesh_from_stl("/media/LUPIN/Double Beta Decay/Solid Works/STL Files/New Oriented Sphere Files/Chroma Assembly Super-5/Chroma Assembly Super-5 - Simple-1.STL")
			teflonSphereM = mesh_from_stl("/media/LUPIN/Double Beta Decay/Solid Works/STL Files/New Oriented Sphere Files/Chroma Assembly 1cmx1cm/Chroma Assembly 1cmx1cm - Teflon Sphere 3-8 inch_4.5diameter Revised 2-1.STL")
			quartzWindowM = mesh_from_stl("/media/LUPIN/Double Beta Decay/Solid Works/STL Files/New Oriented Sphere Files/Chroma Assembly Super-5/Chroma Assembly Super-5 - Glass-1.STL")

			#general non detector solid Creations
			ceramicSubS = Solid(ceramicSubM, sm.fullAbsorb, lm.vacuum, sm.steelSurface, color = 0xdaa520)
			conflatFlangeS = Solid(conflatFlangeM, sm.fullAbsorb, lm.vacuum, sm.steelSurface)
			copperPlateS = Solid(copperPlateM, sm.fullAbsorb, lm.vacuum, sm.steelSurface)
			quartzWindowS = Solid(quartzWindowM, sm.quartz, lm.vacuum, surface = None)
			filterCylinderS = Solid(filterCylinderM, sm.BB180, lm.vacuum, surface = None, color = 0x33ff4040) #angle of incidence
			insertS = Solid(insertM, sm.fullAbsorb, lm.vacuum, sm.steelSurface)
			steelBaseS = Solid(steelBaseM, sm.fullAbsorb, lm.vacuum, sm.steelSurface)
			teflonSphereS = Solid(teflonSphereM, sm.teflon, lm.vacuum, sm.teflonSurface)
			#Notes on teflon properties
			#changed surface to steel(full absorb surface), and  results make sense.
			#changed back to sm.teflonSurface, absorb must be set before diffuse/specular!!!! Of course, it is so obvious now! The hat goes on the head!
			
			setup.add_pmt(sipmS1,rotation= None, displacement = (0,0,0))
			setup.add_pmt(sipmS2,rotation= None, displacement = (0,0,0))
			setup.add_pmt(sipmS3,rotation= None, displacement = (0,0,0))
			setup.add_pmt(sipmS4,rotation= None, displacement = (0,0,0))
			setup.add_pmt(sipmS5,rotation= None, displacement = (0,0,0))
			
			#This is a small square solid that is used in orienting the photon start location in the demo setup
			location = Solid (make.box (.5, .5, .5), lm.vacuum, lm.vacuum, sm.nothing, 0x33ffff00)
			
			print "Average of Triangle Centers (to get estimate pmt location) from Teflon Sphere: x,y,z coordinates"
			triangleCenters = teflonSphereM.get_triangle_centers()
			print triangleCenters [:,0], triangleCenters [:,1], triangleCenters [:,2]
			meanX = np.mean(triangleCenters[:,0])
			meanY = np.mean(triangleCenters[:,1])
			meanZ = np.mean(triangleCenters[:,2])
			print "x:",meanX, "y:",meanY, "z:",meanZ
			print

			#General Center Photon Bomb Location, Orientation of setup
			xshift = meanX
			yshiftDetector = meanY
			yshift = 10
			zshift = meanZ

			#LARGE pmt, variable placement (input parameter below)
			largePMT = Solid (make.box (100, 1.0, 100), sm.fullAbsorb, lm.ls, surface = lm.fulldetect, color = 0x33de22de)
			sourceCylinder = Solid (make.cylinder(5, 1), sm.fullAbsorb, lm.ls, surface = sm.steelSurface, color = 0x33bb00ee)

			#used in orientation only, x y and z axes for small adjustments of photon start locations
			testPMTx = Solid (make.box (5, .5, .5), glass, lm.ls, surface = lm.fulldetect)
			testPMTy = Solid (make.box (.5, 10, .5), glass, lm.ls, surface = lm.fulldetect)
			testPMTz = Solid (make.box (.5, .5, 15), lm.ls, lm.ls, surface = lm.fulldetect)
			
			#DEMO####
			#for adjustments, and so you can see detector location and other things
			#demo setup, for bomb location and modification
			#demoSetup.add_solid(ceramicSubS, displacement=(0,0,0))
			#demoSetup.add_solid(conflatFlangeS, displacement=(0,0,0))
			demoSetup.add_solid(copperPlateS, displacement=(0,0,0))
			#demoSetup.add_solid(filterCylinderS, displacement=(0,0,0))
			#demoSetup.add_solid(steelBaseS, displacement=(0,0,0))
			#demoSetup.add_solid(teflonSphereS, displacement=(0,0,0))
			#demoSetup.add_solid(quartzWindowS, displacement=(0,0,0))

			#orientation and position axis
			demoSetup.add_solid(testPMTx, displacement=(xshift+20,120,zshift+20))
			demoSetup.add_solid(testPMTy, displacement=(xshift+20,120,zshift+20))
			demoSetup.add_solid(testPMTz, displacement=(xshift+20,120,zshift+20))

			demoSetup.add_pmt(sipmS1,rotation= None, displacement = (0,0,0))
			demoSetup.add_pmt(sipmS2,rotation= None, displacement = (0,0,0))
			demoSetup.add_pmt(sipmS3,rotation= None, displacement = (0,0,0))
			demoSetup.add_pmt(sipmS4,rotation= None, displacement = (0,0,0))
			demoSetup.add_pmt(sipmS5,rotation= None, displacement = (0,0,0))
			
			demoSetup.add_solid(sourceCylinder, displacement=(xshift,yshift,zshift))



			demoSetup.add_solid(location,rotation= None, displacement = (xshift-.25,yshift-.51,zshift-.25))
			#setup.add_solid(location,rotation= None, displacement = (xshift-.25,yshift-.51,zshift-.25))
			#-.25 to get small location square centered, .51 so it doesn't interfere with simulation photons
			########
			
			print ("Successfully Super-5'ed")
			break
			
		elif (choice == 'd'): #MEG
			print ("Loading MEG")
			detectorChoice = "MEG"
			detector1 = mesh_from_stl("/media/LUPIN/Double Beta Decay/Solid Works/STL Files/New Oriented Sphere Files/Chroma Assembly MEG/Chroma Assembly MEG - MEG Complete-1 .24 SiPM Single-1.STL")
			detector2 = mesh_from_stl("/media/LUPIN/Double Beta Decay/Solid Works/STL Files/New Oriented Sphere Files/Chroma Assembly MEG/Chroma Assembly MEG - MEG Complete-1 .24 SiPM Single-2.STL")
			detector3 = mesh_from_stl("/media/LUPIN/Double Beta Decay/Solid Works/STL Files/New Oriented Sphere Files/Chroma Assembly MEG/Chroma Assembly MEG - MEG Complete-1 .24 SiPM Single-3.STL")
			detector4 = mesh_from_stl("/media/LUPIN/Double Beta Decay/Solid Works/STL Files/New Oriented Sphere Files/Chroma Assembly MEG/Chroma Assembly MEG - MEG Complete-1 .24 SiPM Single-4.STL")
			
			MEGbase = mesh_from_stl("/media/LUPIN/Double Beta Decay/Solid Works/STL Files/New Oriented Sphere Files/Chroma Assembly MEG/Chroma Assembly MEG - MEG Complete-1 MEG Base-1.STL")
			MEGSO2Window = mesh_from_stl("/media/LUPIN/Double Beta Decay/Solid Works/STL Files/New Oriented Sphere Files/Chroma Assembly MEG/Chroma Assembly MEG - MEG Complete-1 MEG SO2-1.STL")

			sipmS1 = Solid(detector1, sm.fullAbsorb, lm.vacuum, surface = lm.fulldetect, color = 0x8a2be2)
			sipmS2 = Solid(detector2, sm.fullAbsorb, lm.vacuum, surface = lm.fulldetect, color = 0x8a2be2)
			sipmS3 = Solid(detector3, sm.fullAbsorb, lm.vacuum, surface = lm.fulldetect, color = 0x8a2be2)
			sipmS4 = Solid(detector4, sm.fullAbsorb, lm.vacuum, surface = lm.fulldetect, color = 0x8a2be2)
			
			MEGbaseS = Solid(MEGbase, sm.fullAbsorb, lm.vacuum, sm.steelSurface, color = 0xdaa520)
			MEGSO2Window = Solid(MEGSO2Window, sm.quartz, lm.vacuum, surface = None, color = 0x00FF00) #Change from quartz properties to SO2
			
			ceramicSubM = mesh_from_stl("/media/LUPIN/Double Beta Decay/Solid Works/STL Files/New Oriented Sphere Files/Chroma Assembly 1cmx1cm/Chroma Assembly 1cmx1cm - 2x2 cm Assembly-1 Simple Ceramic Substrate-1.STL")
			conflatFlangeM = mesh_from_stl("/media/LUPIN/Double Beta Decay/Solid Works/STL Files/New Oriented Sphere Files/Chroma Assembly MEG/Chroma Assembly MEG - Conflat Flange Main part-1.STL")
			copperPlateM = mesh_from_stl("/media/LUPIN/Double Beta Decay/Solid Works/STL Files/New Oriented Sphere Files/Chroma Assembly MEG/Chroma Assembly MEG - Copper Plate Attached Lower Ring-1.STL")
			filterCylinderM = mesh_from_stl("/media/LUPIN/Double Beta Decay/Solid Works/STL Files/New Oriented Sphere Files/Chroma Assembly MEG/Chroma Assembly MEG - Filter-1.STL")
			steelBaseM = mesh_from_stl("/media/LUPIN/Double Beta Decay/Solid Works/STL Files/New Oriented Sphere Files/Chroma Assembly MEG/Chroma Assembly MEG - Simple-1.STL")
			teflonSphereM = mesh_from_stl("/media/LUPIN/Double Beta Decay/Solid Works/STL Files/New Oriented Sphere Files/Chroma Assembly MEG/Chroma Assembly MEG - Teflon Sphere 3-8 inch_4.5diameter Revised 2-1.STL")
			quartzWindowM = mesh_from_stl("/media/LUPIN/Double Beta Decay/Solid Works/STL Files/New Oriented Sphere Files/Chroma Assembly MEG/Chroma Assembly MEG - Glass-1.STL")
			
			#solid Creations
			ceramicSubS = Solid(ceramicSubM, sm.fullAbsorb, lm.vacuum, sm.steelSurface, color = 0xdaa520)
			conflatFlangeS = Solid(conflatFlangeM, sm.fullAbsorb, lm.vacuum, sm.steelSurface)
			copperPlateS = Solid(copperPlateM, sm.fullAbsorb, lm.vacuum, sm.steelSurface)
			quartzWindowS = Solid(quartzWindowM, sm.quartz, lm.vacuum, surface = None)
			filterCylinderS = Solid(filterCylinderM, sm.BB180, lm.vacuum, surface = None, color = 0x33ff4040) #angle of incidence
			steelBaseS = Solid(steelBaseM, sm.fullAbsorb, lm.vacuum, sm.steelSurface)
			teflonSphereS = Solid(teflonSphereM, sm.teflon, lm.vacuum, sm.teflonSurface)
			#Notes on teflon properties
			#changed surface to steel(full absorb surface), and  results make sense.
			#changed back to sm.teflonSurface, absorb must be set before diffuse/specular!!!! Of course, it is so obvious now! The hat goes on the head!

			setup.add_pmt(sipmS1,rotation= None, displacement = (0,0,0))
			setup.add_pmt(sipmS2,rotation= None, displacement = (0,0,0))
			setup.add_pmt(sipmS3,rotation= None, displacement = (0,0,0))
			setup.add_pmt(sipmS4,rotation= None, displacement = (0,0,0))
			setup.add_solid(MEGbaseS, displacement=(0,0,0))
			setup.add_solid(MEGSO2Window, displacement=(0,0,0))
			
			#This is a small square solid that is used in orienting the photon start location in the demo setup
			location = Solid (make.box (.5, .5, .5), lm.vacuum, lm.vacuum, sm.nothing, 0x33ffff00)
			
			print "Average of Triangle Centers (to get estimate pmt location) from Teflon Sphere: x,y,z coordinates"
			triangleCenters = teflonSphereM.get_triangle_centers()
			print triangleCenters [:,0], triangleCenters [:,1], triangleCenters [:,2]
			meanX = np.mean(triangleCenters[:,0])
			meanY = np.mean(triangleCenters[:,1])
			meanZ = np.mean(triangleCenters[:,2])
			print "x:",meanX, "y:",meanY, "z:",meanZ
			print

			#General Center Photon Bomb Location, Orientation of setup
			xshift = meanX
			yshiftDetector = meanY
			yshift = 10
			zshift = meanZ

			#LARGE pmt, variable placement (input parameter below)
			largePMT = Solid (make.box (100, 1.0, 100), sm.fullAbsorb, lm.ls, surface = lm.fulldetect, color = 0x33de22de)
			sourceCylinder = Solid (make.cylinder(5, 1), sm.fullAbsorb, lm.ls, surface = sm.steelSurface, color = 0x33bb00ee)

			#used in orientation only, x y and z axes for small adjustments of photon start locations
			testPMTx = Solid (make.box (5, .5, .5), glass, lm.ls, surface = lm.fulldetect)
			testPMTy = Solid (make.box (.5, 10, .5), glass, lm.ls, surface = lm.fulldetect)
			testPMTz = Solid (make.box (.5, .5, 15), lm.ls, lm.ls, surface = lm.fulldetect)
			
			#DEMO####
			#for adjustments, and so you can see detector location and other things
			#demo setup, for bomb location and modification
			#demoSetup.add_solid(ceramicSubS, displacement=(0,0,0))
			#demoSetup.add_solid(conflatFlangeS, displacement=(0,0,0))
			#demoSetup.add_solid(copperPlateS, displacement=(0,0,0))
			#demoSetup.add_solid(filterCylinderS, displacement=(0,0,0))
			#demoSetup.add_solid(steelBaseS, displacement=(0,0,0))
			#demoSetup.add_solid(teflonSphereS, displacement=(0,0,0))
			#demoSetup.add_solid(quartzWindowS, displacement=(0,0,0))

			#orientation and position axis
			demoSetup.add_solid(testPMTx, displacement=(xshift+20,120,zshift+20))
			demoSetup.add_solid(testPMTy, displacement=(xshift+20,120,zshift+20))
			demoSetup.add_solid(testPMTz, displacement=(xshift+20,120,zshift+20))

			demoSetup.add_pmt(sipmS1,rotation= None, displacement = (0,0,0))
			demoSetup.add_pmt(sipmS2,rotation= None, displacement = (0,0,0))
			demoSetup.add_pmt(sipmS3,rotation= None, displacement = (0,0,0))
			demoSetup.add_pmt(sipmS4,rotation= None, displacement = (0,0,0))
			demoSetup.add_solid(sourceCylinder, displacement=(xshift,yshift,zshift))



			demoSetup.add_solid(location,rotation= None, displacement = (xshift-.25,yshift-.51,zshift-.25))
			#setup.add_solid(location,rotation= None, displacement = (xshift-.25,yshift-.51,zshift-.25))
			#-.25 to get small location square centered, .51 so it doesn't interfere with simulation photons
			########
			
			print ("Successfully MEG'ed")
			break
			
		elif (choice == 'e'): #PMT Hamamatsu R9875p 8mm diameter
			print ("Loading R9875p PMT")
			detectorChoice = "R9875p PMT"
			detector = mesh_from_stl("/media/LUPIN/Double Beta Decay/Solid Works/STL Files/New Oriented Sphere Files/Chroma Assembly PMT/Chroma Assembly R9875p - PMT Assembly with Insert-1 PMT Assembly-1 Detector 8mm-1.STL")
			
			ceramicSubM = mesh_from_stl("/media/LUPIN/Double Beta Decay/Solid Works/STL Files/New Oriented Sphere Files/Chroma Assembly PMT/Chroma Assembly R9875p - PMT Assembly with Insert-1 PMT Assembly-1 House PMT-1.STL")
			conflatFlangeM = mesh_from_stl("/media/LUPIN/Double Beta Decay/Solid Works/STL Files/New Oriented Sphere Files/Chroma Assembly PMT/Chroma Assembly R9875p - Conflat Flange Main part-1.STL")
			copperPlateM = mesh_from_stl("/media/LUPIN/Double Beta Decay/Solid Works/STL Files/New Oriented Sphere Files/Chroma Assembly PMT/Chroma Assembly R9875p - Copper Plate Attached Lower Ring-1.STL")
			filterCylinderM = mesh_from_stl("/media/LUPIN/Double Beta Decay/Solid Works/STL Files/New Oriented Sphere Files/Chroma Assembly PMT/Chroma Assembly R9875p - Filter-1.STL")
			insertM = mesh_from_stl("/media/LUPIN/Double Beta Decay/Solid Works/STL Files/New Oriented Sphere Files/Chroma Assembly PMT/Chroma Assembly R9875p - PMT Assembly with Insert-1 Combined Raiser Hamamatsu-1.STL")
			steelBaseM = mesh_from_stl("/media/LUPIN/Double Beta Decay/Solid Works/STL Files/New Oriented Sphere Files/Chroma Assembly PMT/Chroma Assembly R9875p - Simple-1.STL")
			teflonSphereM = mesh_from_stl("/media/LUPIN/Double Beta Decay/Solid Works/STL Files/New Oriented Sphere Files/Chroma Assembly PMT/Chroma Assembly R9875p - Teflon Sphere 3-8 inch_4.5diameter Revised 2-1.STL")
			quartzWindowM = mesh_from_stl("/media/LUPIN/Double Beta Decay/Solid Works/STL Files/New Oriented Sphere Files/Chroma Assembly PMT/Chroma Assembly R9875p - Glass-1.STL")

			#solid Creations
			ceramicSubS = Solid(ceramicSubM, sm.fullAbsorb, lm.vacuum, sm.steelSurface, color = 0xdaa520)
			conflatFlangeS = Solid(conflatFlangeM, sm.fullAbsorb, lm.vacuum, sm.steelSurface)
			copperPlateS = Solid(copperPlateM, sm.fullAbsorb, lm.vacuum, sm.steelSurface)
			quartzWindowS = Solid(quartzWindowM, sm.quartz, lm.vacuum, surface = None)

			filterCylinderS = Solid(filterCylinderM, sm.fullAbsorb, lm.vacuum, surface = lm.fulldetect, color = 0x920000) #angle of incidence, filters are now PMT's in this code
			
			insertS = Solid(insertM, sm.fullAbsorb, lm.vacuum, sm.steelSurface)
			steelBaseS = Solid(steelBaseM, sm.fullAbsorb, lm.vacuum, sm.steelSurface)
			teflonSphereS = Solid(teflonSphereM, sm.teflon, lm.vacuum, sm.teflonSurface)
			#Notes on teflon properties
			#changed surface to steel(full absorb surface), and  results make sense.
			#changed back to sm.teflonSurface, absorb must be set before diffuse/specular!!!! Of course, it is so obvious now! The hat goes on the head!
			
			setup.add_solid(ceramicSubS, displacement=(0,0,0))
			setup.add_solid(insertS, displacement=(0,0,0))
			sipmS = Solid(detector, sm.fullAbsorb, lm.vacuum, surface = lm.fulldetect, color = 0x8a2be2)
			setup.add_pmt(sipmS,rotation= None, displacement = (0,0,0))
			
			#This is a small square solid that is used in orienting the photon start location in the demo setup
			location = Solid (make.box (.5, .5, .5), lm.vacuum, lm.vacuum, sm.nothing, 0x33ffff00)
			
			print "Average of Triangle Centers (to get estimate pmt location) from Teflon Sphere: x,y,z coordinates"
			triangleCenters = teflonSphereM.get_triangle_centers()
			print triangleCenters [:,0], triangleCenters [:,1], triangleCenters [:,2]
			meanX = np.mean(triangleCenters[:,0])
			meanY = np.mean(triangleCenters[:,1])
			meanZ = np.mean(triangleCenters[:,2])
			print "x:",meanX, "y:",meanY, "z:",meanZ
			print

			#General Center Photon Bomb Location, Orientation of setup
			xshift = meanX
			yshiftDetector = meanY
			yshift = 10
			zshift = meanZ

			#LARGE pmt, variable placement (input parameter below)
			largePMT = Solid (make.box (100, 1.0, 100), sm.fullAbsorb, lm.ls, surface = lm.fulldetect, color = 0x33de22de)
			sourceCylinder = Solid (make.cylinder(5, 1), sm.fullAbsorb, lm.ls, surface = sm.steelSurface, color = 0x33bb00ee)

			#used in orientation only, x y and z axes for small adjustments of photon start locations
			testPMTx = Solid (make.box (5, .5, .5), glass, lm.ls, surface = lm.fulldetect)
			testPMTy = Solid (make.box (.5, 10, .5), glass, lm.ls, surface = lm.fulldetect)
			testPMTz = Solid (make.box (.5, .5, 15), lm.ls, lm.ls, surface = lm.fulldetect)
			
			#DEMO####
			#for adjustments, and so you can see detector location and other things
			#demo setup, for bomb location and modification
			#demoSetup.add_solid(ceramicSubS, displacement=(0,0,0))
			#demoSetup.add_solid(conflatFlangeS, displacement=(0,0,0))
			demoSetup.add_solid(copperPlateS, displacement=(0,0,0))
			#demoSetup.add_solid(filterCylinderS, displacement=(0,0,0))
			demoSetup.add_solid(insertS, displacement=(0,0,0))
			#demoSetup.add_solid(steelBaseS, displacement=(0,0,0))
			#demoSetup.add_solid(teflonSphereS, displacement=(0,0,0))
			#demoSetup.add_solid(quartzWindowS, displacement=(0,0,0))

			#orientation and position axis
			demoSetup.add_solid(testPMTx, displacement=(xshift+20,120,zshift+20))
			demoSetup.add_solid(testPMTy, displacement=(xshift+20,120,zshift+20))
			demoSetup.add_solid(testPMTz, displacement=(xshift+20,120,zshift+20))

			demoSetup.add_pmt(sipmS,rotation= None, displacement = (0,0,0))
			demoSetup.add_solid(sourceCylinder, displacement=(xshift,yshift,zshift))



			demoSetup.add_solid(location,rotation= None, displacement = (xshift-.25,yshift-.51,zshift-.25))
			#setup.add_solid(location,rotation= None, displacement = (xshift-.25,yshift-.51,zshift-.25))
			#-.25 to get small location square centered, .51 so it doesn't interfere with simulation photons
			########
			
			print ("Successfully PMT R9875p'ed")
			break
			
		else:
			print("Incorrect choice. Please Choose Again")

	try:
		char=raw_input("Full setup? ('y' or 'n'): ")
	except:
		print ('OK then...')

	if (char == 'n'):
		try:
				char=raw_input("Filter? ('y' or 'n'): " )
		except:
				print ('OK then...')
		if (char == 'y'):
			setup.add_solid(filterCylinderS, displacement=(0,0,0))

	else:
		#y shift is up, xz is horizontal plane. 69.5, 10. 69 correct(?) position in source
		#edit: yshift and z shift are averaged from below, mean of photon detection positions

		#####ACTUAL setup, adding solid S parts
		setup.add_solid(conflatFlangeS, displacement=(0,0,0))
		#setup.add_solid(copperPlateS, displacement=(0,0,0))
		#FILTER PROPERTIES

		try:
				char=raw_input("Filter? ('y' or 'n'): " )
		except:
				print ('OK then...')
		if (char == 'y'):
			setup.add_solid(filterCylinderS, displacement=(0,0,0))
		#need properties
		setup.add_solid(steelBaseS, displacement=(0,0,0))

		#teflon sphere
		setup.add_solid(teflonSphereS, displacement=(0,0,0))

		#quartz window
		try:
				char=raw_input("Quartz Window? ('y' or 'n'): " )
		except:
				print ('OK then...')
		#if (char == 'y'):
			#setup.add_solid(quartzWindowS, displacement=(0,0,0))
		#MATERIALS NEED TO BE CHECKED

		

	##CHECK Detector Choice
	###
	print "Note: ALL selected detectors have been added earlier in the code. The large PMT is totally absorbing..."
	try:
		choice=raw_input("Large PMT Detector? ('y' or 'n'): ")
	except:
		print ('OK then...')

	if (choice == 'y'):
		print ("Large pmt height position?")
		print("(example positions: 110 above sphere, 40 above opening, Source Positon 10)")
		try:
			pmtHeight=float(raw_input('Large PMT Height: '))
		except ValueError:
			print ("Not a number")
		yshiftpmt = pmtHeight
		setup.add_pmt(largePMT,rotation= None, displacement = (xshift, yshiftpmt+.5, zshift))
		demoSetup.add_pmt(largePMT,rotation= None, displacement = (xshift, yshiftpmt+.5, zshift)) #+.5 for PMT thickness; nearest surface becomes yshiftpmt height exactly
	else:
		yshiftpmt = -100
		#SiPM size is 2x2 in setup

	#Now the fun begins
	demoSetup.flatten()
	setup.flatten()

	try:
		char=raw_input("Viewing Model? Real or demo ('r' or 'd'): ")
	except:
		print ('OK then...')

	if (char == 'r'):
		print ('Showing real.')
		view (setup)
	elif (char == 'd'):
		print ("Showing demo.")
		view (demoSetup)
	else:
		print ("Yeah, screw cool setup animations...")

	setup.bvh = load_bvh(setup)
	sim = Simulation(setup, geant4_processes=0)
	
	
	#####LISTEN
	#Now you have to take data from both files (the event created below, and the original)
	#You need to find a way to get the indices in respect to the ORIGINAL list...this may require you to modify the above methodology to allow this.
	#Have fun :...D
	
	
	# write it to a root file
	from chroma.io.root import RootWriter
	from chroma.io.root import RootWriter
	
	start_time1 = time.time()
	#MODDED PHOTONS! Loaded from fileName root class
	print "Starting Photon Mods"
	moddedPhotons = photonMods(fileName) #CHECK THE CLASS
	print "Modding Finished"
	print "ModdedPhoton shapes: pos, dir, pol, wavelengths:"
	print moddedPhotons.pos
	print moddedPhotons.dir
	print moddedPhotons.pol
	print moddedPhotons.wavelengths
	print "ModdedPhotons shapes:"
	print np.shape(moddedPhotons.pos)
	print np.shape(moddedPhotons.dir)
	print np.shape(moddedPhotons.pol)
	print np.shape(moddedPhotons.wavelengths)
	print
	
	print "Modded Photons Size:", len(moddedPhotons)
	
	print("--- %s seconds photonbomb method ---" % (time.time() - start_time1))
	start_time2 = time.time()
	
	importFile = fileName
	f2 = RootWriter('finalData.root')
	fRead = RootReader(importFile)
	

	for ev in fRead:
		numPhotonsTot = len(ev.photons_beg)
		detectedInit = (ev.photons_end.flags & (0x1 << 2)).astype(bool)
		numPhotonsFilt = len(ev.photons_end[detectedInit])
	
	
	for ev in sim.simulate(moddedPhotons, keep_photons_beg=True,keep_photons_end=True, run_daq=True,max_steps=100):
		print
		print "NOTE: (10mm)^2/(4*pi*(100mm)^2) ~ .0008, +teflon, -filter ~ .0005-.0006 ... It is in the right neighborhood."
		print
		print "Time Elapsed for Second Part of Simulation:", (time.time()-start_time2)
		print
		print ("<(~.~)> <(-'-)> d(^.^)b <(O-O)> <(^.^)> <($u$)> <(@.@)> ")
		print
		print "Detector Choice:", detectorChoice
		print "Total photons simulated, from first part:", numPhotonsTot
		print "Photons simulated that reached filter:", numPhotonsFilt

	#     # check photon start times
		photons_beg = ev.photons_beg
		photons_end = ev.photons_end
		numPhotons = len(ev.photons_beg)

		detected = (ev.photons_end.flags & (0x1 << 2)).astype(bool)
		detectedPhotonsLen = len(photons_end[detected])
				
		print "Photons simulated that survived filter:", numPhotons
		print "Photons simulated that were detected:", detectedPhotonsLen
		print
		a= float(float(numPhotons)/float(numPhotonsFilt))
		b= float(float(detectedPhotonsLen)/float(numPhotonsTot))
		print "Photon that survived filter/Photons that hit filter:", a
		print "Detected Photons/Total simulated Photons:", b
		#print ("First Ten Photons: Times, Flags")
		#print photons_end.t[:10]
		#print photons_end.flags[:10]
		
		smallAngle = np.tile(False, detectedPhotonsLen)
		
		x = 0
		minAngle = np.arctan(20.0/110)*180.0/np.pi
		print "Min Angle: ", minAngle, "degrees." 
		
		for direction in ev.photons_end[detected].dir:
			#listPi = np.tile(np.pi/2, detectedPhotonsLen)
			angle = (np.pi/2)-np.arcsin((direction[1])/((direction[0]**2+direction[1]**2+direction[2]**2)**(1/2)))
			angle = angle * 180.0/np.pi

			if (angle <= minAngle):
				smallAngle[x] = True
			x = x+1
			
		withinAnglePhotons = len(photons_end[smallAngle])
		print "Number of photons that are within angle:", withinAnglePhotons
		print "Percentage within Angle/Total Detected:", float(float(withinAnglePhotons)/float(detectedPhotonsLen))
		print
		print ("<(~.~)> <(-'-)> d(^.^)b <(O-O)> <(^.^)> <($u$)> <(@.@)> ")
		print

		f2.write_event(ev)
		
		#LOOOK AT MEEEEE try to get the small angle thing working	
		
		#detectedBounce = (ev.photons_end.flags != 4).astype(bool)
		bounciness = np.tile(False, numPhotons)
		
		for x in range (0, numPhotons):
			if (detected[x]):	
				if (photons_end.flags[x] != 4):
					bounciness[x] = True
					
					
		angleTotBounce = np.tile(False, numPhotons)
		print "Small Angle Tot Size:", len(angleTotBounce)
		print "numPhotons size", numPhotons
		print "detected bool len", len(detected)
		
		for x in range (0, numPhotons):
			if (detected[x]):
				direction2 = ev.photons_end[x].dir
				angle = (np.pi/2)-np.arcsin((direction2[1])/((direction2[0]**2+direction2[1]**2+direction2[2]**2)**(1/2)))
				angle = angle * 180.0/np.pi
				
				if (angle >= minAngle): #greater than supposes that photons are coming in at large, strange angles due to bouncing
					angleTotBounce[x] = True
		
		numTrue = 0
		for x in range(0,numPhotons):
			if angleTotBounce[x]:
				numTrue = numTrue +1
				
		print "Num True in angleTotBounce (this and angleTot should equalt total detected)", numTrue
		#print bounciness
		
		#For photons that appear to be from direct incidence....the problem is that smallAngle is too small (need to be from numPhotons)
		detectedBounce = angleTotBounce 
			
		#detectedBounce = bounciness
		print
		#print ("Detected Photons: Times, Flags")
		#print photons_end.t[detected]
		#print photons_end.flags[detected]
		if (yshiftpmt != -100):
			print ("PMT HEIGHT Y")
			print yshiftpmt
			print ("Height Above Light Source")
			print (yshiftpmt-yshift)
		print
		print("--- %s seconds simulation time ---" % (time.time() - start_time2))
		print ("Number of Photons Created: ")
		print (numPhotons)
		print


		if not detected.any():
			print ("Empty List: No Detected Photons")
		else:
			numDetected = len(ev.photons_end.t[detected])
		
		print "THE FOLLOWING DATA IS FOR A SIMULATION OF THROUGH FILTER PHOTONS ONLY...NOT IN RESPECT TO TOTAL PHOTONS"
		print
		numDetectedBounce = len(ev.photons_end.t[detectedBounce])
		print ("Total Detected Photons: "), numDetected
		print
		print ("Total Detected Photons NOT Direct Incident: "), numDetectedBounce
		print
		percentDetect = float(numDetected)/(numPhotons)
		print ("Detected/Total Photons:"), percentDetect
		print
		percentDetectBounce = float(numDetectedBounce)/(numPhotons)
		print ("Detected (NOT Straight Incidence)/Total Photons:"), percentDetectBounce
		print
		xavg = float(float(sum(photons_end.pos[detected][:,0]))/len(ev.photons_end.t[detected]))
		print ("Mean Position X Detected:"), xavg
		print
		zavg = float(float(sum(photons_end.pos[detected][:,2]))/len(ev.photons_end.t[detected]))
		print ("Mean Position Z Detected:"), zavg
		print
		print ("(Note: Setup is not oriented evenly on axis)")
		straightIncNum = 0
		for x in range (0, numPhotons):
			if (photons_end.flags[x] == 4):
				straightIncNum = straightIncNum+1
		print ("TEST: Total Bounce+Direct, Total detected - '' '':"), (straightIncNum+numDetectedBounce), numDetected-(straightIncNum+numDetectedBounce)
		percentStraightIncDet = float(straightIncNum)/(numDetected)
		print ("Number Uninterrupted Incidence (Tag == 4; No Scattering or Redirection): "), straightIncNum
		print
		print ("Uninterrupted Incidence/Total Detected Photons: "), percentStraightIncDet
		print
		percentStraightIncTot = float(straightIncNum)/(numPhotons) 
		print ("Uninterrupted Incidence/Total Photons: "), percentStraightIncTot


	####PLOTS########PLOTS########PLOTS########PLOTS########PLOTS########PLOTS########PLOTS########PLOTS####


		#tempxpos/tempzpos lists of positions, accounting for shift in detector from simulation center
		tempxpos = ev.photons_end.pos[detected][:,0]
		tempzpos = ev.photons_end.pos[detected][:,2]

		tempxpos[:] = [x - xshift for x in tempxpos]
		tempzpos[:] = [z - zshift for z in tempzpos]

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
		plt.show()
		
		#Heat Map of Detection Locations
		#Note: need to reorient actual detector (new STL File) so edges are parellel with axes, or else apply rotation matrix to detection location (ifffffy, because we don't exactly know the center of the detector, moreover the entire cetup mirror axis) 
		fig = plt.figure(figsize=(7.8, 6))
		rangeX = max(tempxpos[:])-min(tempxpos[:])
		rangeZ = max(tempzpos[:])-min(tempzpos[:])
		rangeSquare = int(rangeX*rangeZ)
		print
		print ("X Range of Detected Photons")
		print rangeX
		print ("Z Range of Detected Photons")
		print rangeZ
		print ("Ranges Squared")
		print rangeSquare
		plt.hist2d(tempxpos, tempzpos, bins=(130)) #150?
		plt.axis((tempxposmin-2, tempxposMax+2, tempzposmin-2, tempzposMax+2))
		plt.xlabel('Final X-Position (m)')
		plt.ylabel('Final Z-Position (m)')
		plt.title('Hit Detection Locations Heat Map')
		plt.colorbar()
		plt.show()


		#Angular Distribution: Radius of Location vs Angle of Incidence
		#We need to graph the appropiate angle distribution that photons hit the detector at. We can get this by crossing the photon vectors with the 

		detectedDirections = ev.photons_end.dir[detected]
		#detectedDirections = ev.photons_end.dir[detectedBounce]

		print ("detectedBounce Photons Shape: "), detectedDirections.shape
		#hello = np.array([[0,1,0],[1,0,0]])
		#print hello.shape
		#detectedDirectons = np.append(hello,detectedDirections, 0)
		listPi = np.tile(np.pi/2,numDetected)
		#listPi = np.tile(np.pi/2,numDetectedBounce)
		#print listPi
		anglesFromPlane = listPi[:]-np.arcsin((detectedDirections[:,1])/((detectedDirections[:,0]**2+detectedDirections[:,1]**2+detectedDirections[:,2]**2)**(1/2)))
		#conversion to degrees
		
		anglesFromPlane[:] = [(x*180/(np.pi)) for x in anglesFromPlane]
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
		plt.show()

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

		plt.show()
	
		#Writing txt file of array for root conversion
		f_handle = file('%s.txt' % detectorChoice , 'a')
		np.savetxt(f_handle, anglesFromPlane)
		f_handle.close()


		#Bounce#		#Bounce#		#Bounce#		#Bounce#		#Bounce#
		#FOLLOWING FOR PHOTONS NOT INCLUDING DIRECT INCIDENCE (BOUNCING PHOTONS)

		#TEMPXPOS/TEMPZPOS FOR BOUNCING PHOTONS NOW
		#tempxpos/tempzpos lists of positions, accounting for shift in detector from simulation center
		tempxpos =ev.photons_end.pos[detectedBounce][:,0]
		tempzpos =ev.photons_end.pos[detectedBounce][:,2]

		tempxpos[:] = [x - xshift for x in tempxpos]
		tempzpos[:] = [z - zshift for z in tempzpos]

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

		#Position Radius v Time
		fig = plt.figure(figsize=(5, 12))
		tempList = np.sqrt(tempxpos*tempxpos+tempzpos*tempzpos)
		maxTempList = max(tempList[:])
		maxTimeDetected = max(ev.photons_end.t[detectedBounce])
		plt.scatter(tempList, ev.photons_end.t[detectedBounce])
		plt.axis((0,maxTempList+(maxTempList*.2),0,maxTimeDetected+(maxTimeDetected*.2)))
		plt.xlabel('Final Position: Radius from Center of Detector')
		plt.ylabel('Time Elapsed Before Detection')
		plt.title('Teflon Reflectivity ; Demonstration of Sphere Reflectance')
		plt.show()
		
		#Heat Map of Detection Locations
		#Note: need to reorient actual detector (new STL File) so edges are parellel with axes, or else apply rotation matrix to detection location (ifffffy, because we don't exactly know the center of the detector, moreover the entire cetup mirror axis) 
		fig = plt.figure(figsize=(7.8, 6))
		rangeX = max(tempxpos[:])-min(tempxpos[:])
		rangeZ = max(tempzpos[:])-min(tempzpos[:])
		rangeSquare = int(rangeX*rangeZ)
		print
		print ("X Range of Detected Photons")
		print rangeX
		print ("Z Range of Detected Photons")
		print rangeZ
		print ("Ranges Squared")
		print rangeSquare
		plt.hist2d(tempxpos, tempzpos, bins=(130)) #150?
		plt.axis((tempxposmin-2, tempxposMax+2, tempzposmin-2, tempzposMax+2))
		plt.xlabel('Final X-Position (m)')
		plt.ylabel('Final Z-Position (m)')
		plt.title('Hit Detection Locations Heat Map')
		plt.colorbar()
		plt.show()


		#Angular Distribution: Radius of Location vs Angle of Incidence
		#We need to graph the appropiate angle distribution that photons hit the detector at. We can get this by crossing the photon vectors with the 

		detectedDirections = ev.photons_end.dir[detectedBounce]
		#detectedDirections = ev.photons_end.dir[detectedBounce]

		print ("detectedBounce Photons Shape: "), detectedDirections.shape
		#hello = np.array([[0,1,0],[1,0,0]])
		#print hello.shape
		#detectedDirectons = np.append(hello,detectedDirections, 0)
		listPi = np.tile(np.pi/2,numDetectedBounce)
		#print listPi
		anglesFromPlane = listPi[:]-np.arcsin((detectedDirections[:,1])/((detectedDirections[:,0]**2+detectedDirections[:,1]**2+detectedDirections[:,2]**2)**(1/2)))
		#conversion to degrees
		
		anglesFromPlane[:] = [(x*180/(np.pi)) for x in anglesFromPlane]
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
		plt.show()

		#This is for Histogram
		x = anglesFromPlane
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
		binwidth = 2
		xymax = np.max( [np.max(np.fabs(x)), np.max(np.fabs(y))] )
		lim = ( int(xymax/binwidth) + 1) * binwidth

		axScatter.set_xlim( (0, 90) )
		axScatter.set_ylim( (0, maxTempList+maxTempList*.1) )

		bins = np.arange(0, lim + binwidth, binwidth)
		axHistx.hist(x, bins=bins)
		axHisty.hist(y, bins=20, orientation='horizontal')

		axHistx.set_xlim( axScatter.get_xlim() )
		axHisty.set_ylim( axScatter.get_ylim() )

		plt.show()	
		
	f2.close()
	
	

if(test): 
	letsSimulate1('initial2000K.root') #testing with previous data set, to see if it is working
if __name__ == '__main__':
	letsSimulate1('initial2000K.root') #testing with previous data set, to see if it is working
print transmitPercentBB180(195)
