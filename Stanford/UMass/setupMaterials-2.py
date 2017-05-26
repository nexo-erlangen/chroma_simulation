from chroma.geometry import Material, Solid, Surface
import numpy as np

#CHECK!
teflon = Material('teflon')
teflon.set('refractive_index', 1.38)
teflon.set('absorption_length', 1)
teflon.set('scattering_length', 0)
teflon.density = 2.2
teflon.composition = {'F' : .9969, 'C' : .00063}


steel= Material('steel')
steel.set('refractive_index', 1.29)
steel.set('absorption_length', 0)
steel.set('scattering_length', 0)
steel.density = 8.05
steel.composition = {'C' : .0008, 'Mg' : .02, 'P' : .0004, 'S' : .0003, 'Si' : .0075, 'Ni' : .08, 'Cr' : .18, 'Fe' : .711}

copper= Material('copper')
copper.set('refractive_index', 1.3)
copper.set('absorption_length', 0)
copper.set('scattering_length',0)
copper.density = 8.96
copper.composition = {'Cu' : 1.00}

fulldetect = Surface('fulldetect')
fulldetect.set('detect', 1.0)

nothing = Surface('nothing')
nothing.set('detect', 0)
nothing.set('absorb', 0)
nothing.set('reflect_diffuse', 0)
nothing.set('reflect_specular', 0)

fullAbsorb= Material('fullAbsorb')
fullAbsorb.set('absorb', 1)
fullAbsorb.set('refractive_index', 1.5)
fullAbsorb.set('absorption_length', 0)
fullAbsorb.set('scattering_length', 0)
fullAbsorb.density = 1


###Teflon Parameters
teflonSurface = Surface('teflonSurface')
#PERCENTAGE of full absorb
teflonSurface.set('absorb', 0.1) #all values set to this before minute adjustmets
teflonReflArray = np.array([(175.0, 0.46), (260.0,  0.94),
              (270.0,  0.95), (280.0,  0.95), (290.0,  0.95), (300.0,  .95),
              (310.0, 0.96), (320.0, 0.98), (330.0, 0.98), (340.0, 0.98),
              (350.0, 0.98), (360.0, 0.99), (370.0, 0.99), (380.0, 0.99),
              (390.0, 0.99), (400.0, 0.99), (410.0, 0.99), (420.0, 0.99),
              (430.0, 0.99), (440.0, 0.99), (450.0, 0.99), (460.0, 0.99),
              (470.0, 0.99), (480.0, 0.99), (490.0, 0.99), (500.0, 0.99),
              (510.0, 0.99), (520.0, 0.99), (530.0, 0.99), (540.0, 0.99),
              (550.0, 0.99), (560.0,  0.99), (570.0,  0.99), (580.0,  0.99),
              (590.0,  0.99), (600.0,  0.99), (610.0,  0.99), (620.0,  0.99),
              (630.0, 0.99), (640.0,  0.99), (650.0,  0.99), (660.0,  0.99),
              (670.0,  0.99), (680.0,  0.99), (690.0,  0.99), (700.0,  0.99),
              (710.0,  0.99)])
#in array, it sets each row value, then goes to the next row. calling a column will point to the values of that column, ex. in the form array[:,1], or all values in the second column

#figure 1.12 of Reflective Materials Thesis, table XIX
teflonAbsorbArray = teflonReflArray
teflonAbsorbArray[:,1] = 1.00-teflonAbsorbArray[:,1]

teflonSurface.set('absorb', teflonAbsorbArray[:,1], teflonAbsorbArray[:,0])
#teflonSurface.set('absorb', 1)
teflonSurface.set('reflect_diffuse', .42/.46)
#teflonSurface.set('reflect_diffuse', 1.00)
teflonSurface.set('reflect_specular', .039/.46)
#teflonSurface.set('reflect_specular', 0.00)
###



steelSurface = Surface('steelSurface')
steelSurface.set('absorb', 1)
steelSurface.set('reflect_diffuse', 0.00)
steelSurface.set('reflect_specular', 0.00)


quartz= Material('quartz')
quartzRefraction = np.array([(178.0, 1.6), (210.0,  1.54), (245.0,  1.51), (210.0,  1.54),
              (280.0,  1.49), (315.0, 1.48), (385.0,  1.47), (420.0,  1.47),
              (430.0, 1.30), (440.0, 1.30), (450.0, 1.30), (460.0, 1.30),
              (470.0, 1.30), (480.0, 1.30), (490.0, 1.30), (500.0, 1.30),
              (510.0, 1.30), (520.0, 1.30), (530.0, 1.30), (540.0, 1.30),
              (550.0, 1.30), (560.0, 1.30), (570.0, 1.30), (580.0, 1.30),
              (590.0, 1.30), (600.0, 1.30), (610.0, 1.30), (620.0, 1.30),
              (630.0, 0.99), (640.0, 1.30), (650.0, 1.30), (660.0, 1.30),
              (670.0, 1.30), (680.0, 1.30), (690.0, 1.30), (700.0, 1.30),
              (710.0, 1.30)])
quartz.set('refractive_index', quartzRefraction[:,1], quartzRefraction[:,0])

#9.49122 normal ?????
quartz.set('absorption_length', 9.49122)
#using the graph from, we can estimate that the filter has around a ~90% transmittence with 1mm quartz window. Therefore, we can calculate the amount it takes for the trasmittence to go down by a factor of 1/e. 
#1/e^(1mm/x) = .9 ,=> x= 9.49122mm (when filter is 9.49122mm, transmittance is 1/e)
quartz.set('scattering_length',1e6)
quartz.density = 2.65
#2.65?


quartzSurface = Surface('quartzSurface')
quartzSurface.set('absorb', 0)
quartzSurface.set('reflect_specular', 0)
quartzSurface.transmissive = 0

#filter properties
BB180Surface = Surface('BB180Surface')
BB180transmit = np.array([(160.0, 0.001), (170, .25), (175,  .33), (176.0,  .35)
		, (180.0,  .36), (184.0,  .35), (185.0,  .35), (189.0,  .30)
		, (190.0,  .29), (200.0,  .17), (205.0,  .11), (210.0,  .075)
		, (220.0,  .04), (240.0,  .02), (260.0,  .005)]) #http://www.pelhamresearchoptical.com/broadband.html
BB180absorb = BB180transmit
#BB180absorb[:,1] = 1-BB180absorb[:,1]

BB180Surface.set('absorb', BB180absorb[:,1], BB180absorb[:,0])
BB180Surface.set('reflect_diffuse', 0.00)
BB180Surface.set('reflect_specular', 0.00)

#CHECK! Transformation of transmission array into material absorption length
BB180 = Material('BB180')
BB180.set('refractive_index', 1)#infinitely wrong
BB180transDist = BB180absorb
BB180transDist [:,1] = 4/(np.log((1/BB180transDist[:,1])))
BB180.set('absorption_length', BB180transDist[:,1], BB180transDist[:,0])
BB180.set('scattering_length', 1e6)
BB180.density = 2.2


