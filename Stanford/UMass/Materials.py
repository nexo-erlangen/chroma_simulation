from chroma.geometry import Material, Solid, Surface
import numpy as np
#***************************************************************************
MSuprasil = Material('MSuprasil')
MSuprasil.set('refractive_index', 1.57)
MSuprasil.set('absorption_length', 1.152736998)
#MSuprasil.set('absorption_length', .52736998)
MSuprasil.set('scattering_length', 1e6)
MSuprasil.density = 2.2
#***************************************************************************
teflon = Material('teflon')
teflon.set('refractive_index', 1.38)
teflon.set('absorption_length', 1)
teflon.set('scattering_length', 0)
teflon.density = 2.2
teflon.composition = {'F' : .9969, 'C' : .00063} 
#***************************************************************************
steel= Material('steel')
steel.set('refractive_index', 1.29)
steel.set('absorption_length', 0)
steel.set('scattering_length', 0)
steel.density = 8.05
steel.composition = {'C' : .0008, 'Mg' : .02, 'P' : .0004, 'S' : .0003, 'Si' : .0075, 'Ni' : .08, 'Cr' : .18, 'Fe' : .711}
#***************************************************************************
copper= Material('copper')
copper.set('refractive_index', 1.3)
copper.set('absorption_length', 0)
copper.set('scattering_length',0)
copper.density = 8.96
copper.composition = {'Cu' : 1.00}
#***************************************************************************
ls = Material('ls')
ls.set('refractive_index', 1.5)
ls.set('absorption_length', 1e6)
ls.set('scattering_length', 1e6)
ls.density = 0.780
#***************************************************************************
vacuum = Material('vac')
vacuum.set('refractive_index', 1.0)
vacuum.set('absorption_length', 1e6)
vacuum.set('scattering_length', 1e6)
ls.density = 1
#***************************************************************************
lensmat = Material('lensmat')
lensmat.set('refractive_index', 2.0)
lensmat.set('absorption_length', 1e6)
lensmat.set('scattering_length', 1e6)
#***************************************************************************
blackhole = Material('blackhole')
blackhole.set('refractive_index', 1.0)
blackhole.set('absorption_length', 1e-15)
blackhole.set('scattering_length', 1e6)
#***************************************************************************
LXenon = Material('LXenon')
LXenon.set('refractive_index', 1.69)
LXenon.set('absorption_length', 364)
LXenon.set('scattering_length', 400.0)
LXenon.density = 2.942
#***************************************************************************
fullAbsorb= Material('fullAbsorb')
fullAbsorb.set('absorb', 1)
fullAbsorb.set('refractive_index', 1.5)
fullAbsorb.set('absorption_length', 0)
fullAbsorb.set('scattering_length', 0)
fullAbsorb.density = 1
#***************************************************************************
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
#quartz.set('refractive_index', quartzRefraction[:,1], quartzRefraction[:,0])
quartz.set('refractive_index', 1.6)
quartz.set('absorption_length', .949122)
#using the graph from, we can estimate that the filter has around a ~90% transmittence with 1mm quartz window. Therefore, we can calculate the amount it takes for the trasmittence to go down by a factor of 1/e. 
#1/e^(1mm/x) = .9 ,=> x= 9.49122mm (when filter is 9.49122mm, transmittance is 1/e)
quartz.set('scattering_length',1e6)
quartz.density = 2.65
#***************************************************************************
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
#***************************************************************************
BB180 = Material('BB180')
BB180.set('refractive_index', 1)#infinitely wrong
BB180transDist = BB180absorb
BB180transDist [:,1] = 4/(np.log((1/BB180transDist[:,1])))
BB180.set('absorption_length', BB180transDist[:,1], BB180transDist[:,0])
BB180.set('scattering_length', 1e6)
BB180.density = 2.2 
#***************************************************************************
SiO2 = Material('SiO2')
SiO2.set('refractive_index', 1.698)
SiO2.set('absorption_length', 364)
SiO2.set('scattering_length', 400.0)
SiO2.density = 2.942
#***************************************************************************
silicon = Material('silicon')
silicon.set('refractive_index', 0.9)
silicon.set('absorption_length', 364)
silicon.set('scattering_length', 400.0)
silicon.density = 2.942


