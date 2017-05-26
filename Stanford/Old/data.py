from matplotlib.ticker import NullFormatter
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D



def incident_angle(last_pos):
	angles = np.arccos(np.fabs(last_pos[:,1])/np.sqrt((last_pos[:,0]**2 + last_pos[:,1]**2 + last_pos[:,2]**2)))*(180/np.pi)
	return angles
