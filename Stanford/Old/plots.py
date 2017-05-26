		
		
		
		#for i,(j,k) in enumerate(zip(ev.photons_end.pos[detected],endPosRotated)):
		#	print i,j-k
		endPosRotated[:,0] = endPosRotated[:,0] - ap.xshift
		endPosRotated[:,2] = endPosRotated[:,2] - ap.zshift
		#print "Test endPosRotated (before rotation):", endPosRotated[0], endPosRotated[1]
		#antirotation
		for x in range(0,len(endPosRotated)):
			endPosRotated[x] = np.dot(d1.antiRotation, endPosRotated[x])
		
		tempxpos = endPosRotated[:,0]
		tempzpos = endPosRotated[:,2]
		
		#BIlocx and BIlocz if you want the center to be oriented to bismuth source rather than LXE Cell "cap" (center for setup)
		#tempxpos[:] = [x - xshift for x in tempxpos]
		#tempzpos[:] = [z - zshift for z in tempzpos]
		
		#time to rotate back into correct orientation....this will make plots symmetrical on axes (rather than rotated)
		tempxposMax = max(tempxpos[:])
		tempzposMax = max(tempzpos[:])
		tempxposmin = min(tempxpos[:])
		tempzposmin = min(tempzpos[:])

		#Position Radius v Time
		fig = plt.figure(figsize=(10, 10))
		tempList = np.sqrt(tempxpos*tempxpos+tempzpos*tempzpos)
		maxTempList = max(tempList[:])
		maxTimeDetected = max(ev.photons_end.t[detected])
		plt.scatter(tempList, ev.photons_end.t[detected], marker="x")
		plt.axis((0,maxTempList+(maxTempList*.2),0,maxTimeDetected+(maxTimeDetected*.2)))
		plt.xlabel('Final Position: Radius from Center of Detector')
		plt.ylabel('Time Elapsed Before Detection')
		plt.title('Teflon Reflectivity ; Demonstration of Sphere Reflectance')
		plt.plot(marker='x')
		#if(arg_list[3]):
			#pass 
			#plt.show()

		#Heat Map of Detection Locations
		fig = plt.figure(figsize=(10, 10))
		rangeX = max(tempxpos[:])-min(tempxpos[:])
		rangeZ = max(tempzpos[:])-min(tempzpos[:])
		rangeSquare = int(rangeX*rangeZ)
		
		print "  X Detection Positions: 			Min: ", min(tempxpos[:])
		print "						Max: ", max(tempxpos[:])
		print "						Mean:", float(float(sum(tempxpos[:]))/float(len(tempxpos)))
		print "						Std: ", np.std(tempxpos)
		print "---------------------------------------------------------------------"
		print "  Z Detection Positions: 			Min: ",min(tempzpos[:])
		print "						Max: ", max(tempzpos[:])
		print "						Mean:", float(float(sum(tempzpos[:]))/float(len(tempzpos)))
		print "						Std: ", np.std(tempzpos)
		
		plt.hist(tempxpos, bins=130) 
		plt.axis((tempxposmin-2, tempxposMax+2, tempzposmin-2, tempzposMax+2))
		plt.xlabel('Final X-Position (m)')
		plt.ylabel('Final Z-Position (m)')
		degrees = d1.degRot*180.0/np.pi
		plt.title('Heat Map; Repositioned and Rotated %s Degrees' % degrees)
		#if(arg_list[3]):
			#plt.show()

		#Angular Distribution: Radius of Location vs Angle of Incidence
		detectedDirections = ev.photons_end.dir[detected]
		print "---------------------------------------------------------------------"
		print ("  Detected Photon Directions Shape:		"), detectedDirections.shape

		listPi = np.tile(np.pi/2,numDetected)
		
		anglesFromPlane = listPi[:]-np.arcsin(np.absolute(detectedDirections[:,1])/((detectedDirections[:,0]**2+detectedDirections[:,1]**2+detectedDirections[:,2]**2)**(1/2)))
		anglesFromPlane[:] = [(x*180/(np.pi)) for x in anglesFromPlane]		#conversion to degrees
		print "---------------------------------------------------------------------"
		print "  Angles From Plane: 				Min: ", min(anglesFromPlane[:])
		print "						Max: ", max(anglesFromPlane[:])
		print "						Mean:", float(float(sum(anglesFromPlane[:]))/float(len(anglesFromPlane)))
		print "						Std: ", np.std(anglesFromPlane)

		#NOW to compare to landing positions on detector, x radius from center, y detection angles

		tempList = np.sqrt(tempxpos*tempxpos+tempzpos*tempzpos)
		maxTempList = max(tempList[:])
		plt.scatter(anglesFromPlane, tempList)
		plt.axis((0,90, 0,maxTempList+(maxTempList*.2)))
		plt.ylabel('Final Position: Radius from Center of Detector')
		plt.xlabel('Angle in Degrees')
		plt.title('Radius from Center of Detector vs. Photon Angle from Plane Normal')
		if(arg_list[3]):
			plt.show()
		
		x = anglesFromPlane
		y = tempList

		nullfmt   = NullFormatter()         			# no labels

		left, width = 0.1, 0.65							# definitions for the axes
		bottom, height = 0.1, 0.65
		bottom_h = left_h = left+width+0.02
		
		rect_scatter = [left, bottom, width, height]
		rect_histx = [left, bottom_h, width, 0.2]
		rect_histy = [left_h, bottom, 0.2, height]
		
		plt.figure(1, figsize=(10,10))					# start with a rectangular Figure
		axScatter = plt.axes(rect_scatter)
		axHistx = plt.axes(rect_histx)
		axHisty = plt.axes(rect_histy)
		axHistx.xaxis.set_major_formatter(nullfmt)		# no labels
		axHisty.yaxis.set_major_formatter(nullfmt)
		axScatter.scatter(x, y)							# the scatter plot:

		binwidth = 1									# now determine nice limits by hand:
		xymax = np.max( [np.max(np.fabs(x)), np.max(np.fabs(y))] )
		lim = ( int(xymax/binwidth) + 1) * binwidth

		axScatter.set_xlim( (0, 90) )
		axScatter.set_ylim( (0, maxTempList+maxTempList*.1) )
		bins = np.arange(0, lim + binwidth, binwidth)
		axHistx.hist(x, bins=bins)
		axHisty.hist(y, bins=20, orientation='horizontal')
		axHistx.set_xlim( axScatter.get_xlim() )
		axHisty.set_ylim( axScatter.get_ylim() )
		if(arg_list[3]):
			plt.show()
