from chroma import make, view
from chroma.geometry import Solid, Geometry
from chroma.transform import make_rotation_matrix
from chroma.demo.optics import glass, water, vacuum, r7081hqe_photocathode
from chroma.demo.optics import black_surface
import numpy as np

np.set_printoptions(threshold='nan')

def build_pd(radius, heigth, radius2, nsteps):
	outside_mesh = make.cylinder(radius, heigth, radius2, nsteps)
	inside_mesh = make.cylinder(radius-glass_thickness*2, heigth-glass_thickness*2, 
					radius2-glass_thickness*2, nsteps)
	outside_solid = Solid(outside_mesh,glass,water)    
	z = inside_mesh.get_triangle_centers()[:,1]
	top = z == max(z)
	inside_surface = np.where(top,r7081hqe_photocathode,black_surface)
	inside_color = np.where(top,0xff0000,0x33ffffff)
	inside_solid = Solid(inside_mesh,vacuum,glass,surface=inside_surface,color=inside_color)
	return outside_solid + inside_solid

radius, radius2 = 100,100
heigth = 500 
glass_thickness = 10
nsteps = 500 


def build_detector():
	g = Geometry(water)
	rotation = make_rotation_matrix(np.pi,(0,-1,-1))
	g.add_solid(build_pd(radius,heigth,radius2,nsteps),rotation=rotation,displacement=(0,0,250))
	world = Solid(make.box(200,400,400),water,vacuum,color=0x33ffffff)
	xaxis = Solid(make.box(100,5,5),water,vacuum,color=0xff0000)		#red xaxis
	yaxis = Solid(make.box(5,100,5),water,vacuum,color=0x01df01)		#green yaxis
	zaxis = Solid(make.box(5,5,100),water,vacuum,color=0x0000ff)		#blue zaxis	
	g.add_solid(xaxis,displacement=(50,0,0))
	g.add_solid(yaxis,displacement=(0,50,0))
	g.add_solid(zaxis,displacement=(0,0,50))
	g.add_solid(Solid(make.box(5,5,5),water,vacuum,color=0x33ffffff),displacement=(0,0,700))
	return g
	
if __name__ == '__main__':
	print("======Simulation started===============")

	from chroma.sim import Simulation
	from chroma.sample import uniform_sphere
	from chroma.event import Photons
	from chroma.loader import load_bvh
	from chroma.generator import vertex
	import matplotlib.pyplot as plt
	g = build_detector()
	g.flatten()
	view (g)
	g.bvh = load_bvh(g)
	sim = Simulation(g)

	def photon_bomb(n,wavelength,pos):
	    pos = np.tile(pos,(n,1))
	    dir = uniform_sphere(n)
	    pol = np.cross(dir,uniform_sphere(n))
	    wavelengths = np.repeat(wavelength,n)
	    return Photons(pos,dir,pol,wavelengths)


	f=open("histogram.dat", "a")
	for ev in sim.simulate([photon_bomb(50000,400,(0,0,550))],
                           keep_photons_beg=True,keep_photons_end=True,
                           run_daq=False,max_steps=100):
		
		detected = (ev.photons_end.flags & (0x1 << 2)).astype(bool)
		print "Number of photons: \t\t", len(ev.photons_end)
		print "Number of photons detected: \t", len(ev.photons_end[detected])
		print "data type of detected is: \t", type(detected) 
		print "its dimensions are: \t\t", np.shape(detected) 
		#print type(ev.photons_beg.pos) 
		#print np.shape(ev.photons_beg.pos) 
		#print (ev.photons_beg.pos)

		print("Der Datentyp von flags lautet:")
		print type(ev.photons_end.flags) 
		print np.shape(ev.photons_end.flags) 
		
		plt.hist(ev.photons_beg.pos[detected],100)
		plt.xlabel('Position (mm)')
		plt.title('Photon Start and End Vertices')
		plt.legend(["x position", "y position", "z position"])
		histo=str(ev.photons_beg.pos[detected])		
		f.write(histo)
		plt.show()

		plt.hist(ev.photons_end.pos[detected],100)
		plt.xlabel('Position (ns)')
		plt.title('Photon Start and End Vertices')
		plt.legend(["x position", "y position", "z position"])
		plt.show()
	f.close()

	print("======Simulation finished==============")








