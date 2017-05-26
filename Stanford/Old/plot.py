from matplotlib.ticker import NullFormatter
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def scatter_hist(x,y):
	fig = plt.figure(figsize=(10, 10))
	
	plt.clf()

	nullfmt = NullFormatter()

	left, width = 0.1, 0.65				
	bottom, height = 0.1, 0.65
	bottom_h = left_h = left+width+0.02

	rect_scatter = [left, bottom, width, height]
	rect_histx = [left, bottom_h, width, 0.2]
	rect_histy = [left_h, bottom, 0.2, height]

	plt.figure(1, figsize=(10,10))			
	axScatter = plt.axes(rect_scatter)
	axHistx = plt.axes(rect_histx)
	axHisty = plt.axes(rect_histy)
	axHistx.xaxis.set_major_formatter(nullfmt)	
	axHisty.yaxis.set_major_formatter(nullfmt)
	axScatter.scatter(x, y)						
	binwidth = 1						
	xymax = np.max( [np.max(np.fabs(x)), np.max(np.fabs(y))] )
	lim = ( int(xymax/binwidth) + 1) * binwidth

	axScatter.set_xlim(0, max(x)+2)
	axScatter.set_ylim(0, max(y)+2)
	bins = np.arange(0, lim + binwidth, binwidth)
	axHistx.hist(x, bins=bins)
	axHisty.hist(y, bins=bins, orientation='horizontal')
	axHistx.set_xlim( axScatter.get_xlim() )
	axHisty.set_ylim( axScatter.get_ylim() )
	plt.show()
