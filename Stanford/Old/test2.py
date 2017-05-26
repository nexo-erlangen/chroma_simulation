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
import numpy as np
from chroma.transform import make_rotation_matrix, get_perp, rotate, rotate_matrix, normalize
#from scipy import stats
from matplotlib.ticker import NullFormatter
#import pyparsing
import time

from chroma.stl import mesh_from_stl
import setupMaterials as sm

#if __name__ == '__main__':
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

import photonModifierBB180 as pmBB180

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

print "Numpy version:", np.__version__

print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
print
print "LXE TEST SETUP SiPM OPTIMIZATION LXECELL"
print
#creation of detector!!!! In this code, we add the detector upon choosing which one below
setup = Detector(lm.vacuum)
print "Blank Vacuum Setup Created..."
#for photon bomb location
demoSetup = Detector(lm.vacuum)
#Photon Bomb Position (In View Model, look for "location", a yellow solid)

print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"


