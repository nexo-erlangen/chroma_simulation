from myimports import * 

def propagate_photon(photon_type, numPhotons, nr_steps, geometry, nthreads_per_block, max_blocks, rng_states):
	gpu_photons = gpu.GPUPhotons(photon_type);
	gpu_geometry = gpu.GPUGeometry(geometry)
	photon_track = np.zeros((nr_steps, numPhotons, 3))
	sim_time = np.zeros((nr_steps))
	for i in range(nr_steps):
		start_sim = time.time()
		gpu_photons.propagate(gpu_geometry, rng_states, nthreads_per_block=nthreads_per_block, max_blocks=max_blocks, max_steps=1)
		photons = gpu_photons.get()
		photon_track[i,:,0] = photons.pos[:,0] 
		photon_track[i,:,1] = photons.pos[:,1] 
		photon_track[i,:,2] = photons.pos[:,2]
		#absorb = (photons.flags & (0x1 << 3)).astype(bool) 
		sim_time [i] = time.time() - start_sim
		#print  len(photons.pos[absorb])
	#return photons, photon_track
	return photons
	
def simulate_single(photon_type, numPhotons, runs):
	doRandom = getRandom()


def getRandom():
	nthreads_per_block = 64
	max_blocks = 1024
	rng_states = gpu.get_rng_states(nthreads_per_block*max_blocks, seed=0)
	doRandom = [nthreads_per_block, max_blocks, rng_states]
	return doRandom  
