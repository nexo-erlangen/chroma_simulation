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
from matplotlib.ticker import NullFormatter
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
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import photonModifierBB180 as pmBB180

SiO2transmit = np.array([(0.3864673,	0),
		(0.3864473,	1),
		(0.3863874,	2),
		(0.3862897,	3),
		(0.3861606,	4),
		(0.3860147,	5),
		(0.3858778,	6),
		(0.385786,	7),
		(0.3857795,	8),
		(0.3858905,	9),
		(0.386123,	10),
		(0.3864269,	11),
		(0.386675,	12),
		(0.386692,	13),
		(0.38639,	14),
		(0.3859097,	15),
		(0.3855345,	16),
		(0.3854419,	17),
		(0.3855836,	18),
		(0.3856881,	19),
		(0.3854197,	20),
		(0.3848699,	21),
		(0.3844601,	22),
		(0.3842491,	23),
		(0.3839911,	24),
		(0.3834929,	25),
		(0.3829632,	26),
		(0.3824554,	27),
		(0.3817121,	28),
		(0.3809814,	29),
		(0.3804827,	30),
		(0.3795702,	31),
		(0.3781991,	32),
		(0.3775275,	33),
		(0.3767101,	34),
		(0.3747074,	35),
		(0.3736404,	36),
		(0.3727788,	37),
		(0.3701177,	38),
		(0.3688889,	39),
		(0.3675143,	40),
		(0.36414,	41),
		(0.3631918,	42),
		(0.3602859,	43),
		(0.3571988,	44),
		(0.3556828,	45),
		(0.3509055,	46),
		(0.3493993,	47),
		(0.3445829,	48),
		(0.3416961,	49),
		(0.3373335,	50),
		(0.3328372,	51),
		(0.3286165,	52),
		(0.3228861,	53),
		(0.3182046,	54),
		(0.311727,	55),
		(0.3058019,	56),
		(0.299092,	57),
		(0.2911381,	58),
		(0.2840369,	59),
		(0.2746745,	60),
		(0.2648165,	61),
		(0.256112,	62),
		(0.2439213,	63),
		(0.2268397,	64),
		(0.2187392,	65),
		(0.2064156,	66),
		(0.182743,	67),
		(0.1576836,	68),
		(0.1313601,	69),
		(0.0889181,	70),
		(0.0431303,	71),
		(0.0101323,	72),
		(8.59E-08,	73),
		(9.01E-12,	74),
		(2.53E-14,	75),
		(2.63E-16,	76),
		(6.09E-18,	77),
		(2.48E-19,	78),
		(1.57E-20,	79),
		(1.41E-21,	80),
		(1.73E-22,	81),
		(2.74E-23,	82),
		(5.50E-24,	83),
		(1.36E-24,	84),
		(4.03E-25,	85),
		(1.40E-25,	86),
		(5.56E-26,	87),
		(2.36E-26,	88),
		(9.02E-27,	89)])
BB180transmit = np.array([(160.0, 0.001), (170, .25), (175,  .33), (176.0,  .35), (180.0,  .36), (184.0,  .35), (185.0,  .35), (189.0,  .30), (190.0,  .29), (200.0,  .17), (205.0,  .11), (210.0,  .075), (220.0,  .04), (240.0,  .02), (260.0,  .005)]) #http://www.pelhamresearchoptical.com/broadband.html

