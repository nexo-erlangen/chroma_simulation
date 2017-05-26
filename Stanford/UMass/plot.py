from matplotlib.ticker import NullFormatter
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns
from scipy.stats import *
from ROOT import gROOT, TCanvas, TF1, TH1F, TFile, TTree, TH2F, gStyle


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
	xymax = np.max([np.max(np.fabs(x)), np.max(np.fabs(y))])
	lim = (int(xymax/binwidth)+1) * binwidth
	axScatter.set_xlim(0, max(x)+2)
	axScatter.set_ylim(0, max(y)+2)
	bins = np.arange(0, lim + binwidth, binwidth)
	axHistx.hist(x, bins=bins)
	axHisty.hist(y, bins=bins, orientation='horizontal')
	axHistx.set_xlim(axScatter.get_xlim())
	axHisty.set_ylim(axScatter.get_ylim())
	plt.show()
	
def histogram(data, xlabel, bin_nr):
	fig = plt.figure(figsize=(10,8))
	sns.axlabel(xlabel, "counts [#]")
	sns.distplot(data, bins=bin_nr, kde=False, rug=True, norm_hist=False)
	plt.show()	
	
def event_display(numPhotons, photon_track, vertex, o_center, v_center, BIloc):
	fig = plt.figure(figsize=(15, 10))
	ax = fig.add_subplot(111, projection='3d')
	for i in range(numPhotons):
		X,Y,Z = photon_track[:,i,0].tolist(), photon_track[:,i,1].tolist(), photon_track[:,i,2].tolist()
		X.insert(0, BIloc[0])
		Y.insert(0, BIloc[1])
		Z.insert(0, BIloc[2])
		ax.plot(X,Y,Z, color='b')	
		ax.scatter(X,Y,Z , c='r', s=.5)		
	ax.plot_wireframe(o_center[::20,0], o_center[::20,1], o_center[::20,2], color='g')
	ax.plot_wireframe(v_center[::20,0], v_center[::20,1], v_center[::20,2], color='g')
	ax.scatter(vertex[:,0], vertex[:,1], vertex[:,2], c='y', s=5)	
	ax.set_xlabel('X Label')
	ax.set_ylabel('Y Label')
	ax.set_zlabel('Z Label')
	ax.view_init(elev=3., azim=0)
	plt.savefig('event_display.pdf') 
	plt.show()	
	
def color_map(hist):
	c1 = TCanvas( 'c1', 'Example with Formula', 200, 10, 700, 500 )	
	gStyle.SetPalette(1)
	gStyle.SetOptStat(0)
	gStyle.SetNumberContours(64)
	hist.Draw("colz")
	hist.GetXaxis().SetTitle("radius [cm]")
	hist.GetYaxis().SetTitle("distance from center [cm]")
	c1.SaveAs("heatmap.pdf")	
