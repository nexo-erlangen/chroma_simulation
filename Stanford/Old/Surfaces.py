from chroma.geometry import Material, Solid, Surface
import numpy as np
#***************************************************************************
fulldetect = Surface('fulldetect')
fulldetect.set('detect', 1.0)
#***************************************************************************
SSuprasil = Surface('SSuprasil')
SSuprasil.set('absorb', 0)
SSuprasil.set('reflect_specular', 0)
SSuprasil.transmissive = 1
#***************************************************************************
teflonSurface = Surface('teflonSurface')
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
teflonAbsorbArray = teflonReflArray
teflonAbsorbArray[:,1] = 1.00-teflonAbsorbArray[:,1]
teflonSurface.set('absorb', teflonAbsorbArray[:,1], teflonAbsorbArray[:,0])
teflonSurface.set('reflect_diffuse', .42/.46)
teflonSurface.set('reflect_specular', .039/.46)
#***************************************************************************
steelSurface = Surface('steelSurface')
steelSurface.set('absorb', 1)
steelSurface.set('reflect_diffuse', 0.00)
steelSurface.set('reflect_specular', 0.00)
#***************************************************************************
nothing = Surface('nothing')
nothing.set('detect', 0)
nothing.set('absorb', 0)
nothing.set('reflect_diffuse', 0)
nothing.set('reflect_specular', 0)
nothing.transmissive = 1
#***************************************************************************
quartzSurface = Surface('quartzSurface')
quartzSurface.set('absorb', 0)
quartzSurface.set('detect', 0)
quartzSurface.set('reflect_specular', 0)
quartzSurface.set('reflect_diffuse', 0)
#quartzSurface.transmissive = 1
#***************************************************************************
