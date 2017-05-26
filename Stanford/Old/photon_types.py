from myimports import * 
#***************************************************************************
# photon bomb, isotropic from position center
def photon_bomb(n,wavelength,pos):
    pos = np.tile(pos,(n,1))
    dir = uniform_sphere(n)
    pol = np.cross(dir,uniform_sphere(n))
    wavelengths = np.repeat(wavelength,n)
    return Photons(pos,dir,pol,wavelengths)

#defines disk with photons coming randomly out of the disk surface, in any direction
def photon_area_bomb(n, diameter, wavelength, x, y, z):
    radii = np.random.uniform(0, diameter/2, n)
    angles = np.random.uniform(0, 2*np.pi, n)
    points = np.empty((n,3))
    points[:,0] = np.sqrt(diameter/2)*np.sqrt(radii)*np.cos(angles) + x
    points[:,1] = np.repeat(y, n)
    points[:,2] = np.sqrt(diameter/2)*np.sqrt(radii)*np.sin(angles) + z
    pos = points
    #print "Ten Points of Photon Start Positions"
    #print points[:10]
    dir = uniform_sphere(n)
    pol = np.cross(dir, uniform_sphere(n))
    wavelengths = np.repeat(wavelength, n)
    return Photons(pos, dir, pol, wavelengths)
