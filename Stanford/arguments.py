import sys, getopt

def usage():
	print 
	print "  The minimum paramaters the simulation needs are:"
	print "  	(1) '-d <pmt/sipm>'	choosing the correct detector." 
	print "  	(2) '-n <#>'		number of photons to be simulated."
	print "  Additional options can be chosen:"
	print "  	(3) '-v' or '-view'	to view the setup before simulation."
	print "  	(4) '-a' 		to analyze the simulated photons."
	print "====================================================================="

def todo():
	print "  In order to check the manual type 'help'."
	print "  If you want to leave and try again just press enter."
	try:
		mode=raw_input('  >>>  ')
		if(mode == "help"):
			usage()
		else:
			sys.exit()
	except ValueError:
		sys.exit()

def main(argv):
	photon_nr = 10000
	detectChoice = "pmt"
	Show = False
	arg_nr = False
	arg_det = False 
	Plot = False
	Analysis = False
	try:
		opts, args = getopt.getopt(argv,"apvd:n:",["view","help","d=","n="])
	except getopt.GetoptError:
		print "  You have passed the wrong/or not enough arguments."
		usage()
		sys.exit()
	if not opts:
		print "  You haven't passed any arguments to the simulation. How is this supposed to work?"
		usage()
		sys.exit()
	for opt, arg in opts:
		if opt == "-help ":
			usage()
			sys.exit()
		elif opt == "-n":
			try:
				photon_nr = int(arg)
				arg_nr = True
			except:
				print "  You should take care of proper spacings betweens options and arguments."
				usage()
				sys.exit()
		elif opt == "-d":
				detectChoice = arg
				arg_det = True
		elif opt == "-v":
			Show = True
		elif opt == "-a":
			Analysis = True
		elif opt == "-p":
			Plot = True
	arg_list=(photon_nr, detectChoice, Show, Plot, Analysis)
	if (arg_nr and arg_det):
		print "\n====================================================================="
		print "  Number of photons: 				", arg_list[0]
		print "  Detector used: 				", arg_list[1]
		print "  View setup before simulation: 		", Show
		print "  View plots: 					", Plot
		print "  Analyze simulation: 				", Analysis
	else:
		if(arg_nr):
			print "  You haven't specified the detector to be used."
			todo()
		else:
			print "  You haven't specified the number of photons that should be simulated."
			todo()
		sys.exit()
	return (arg_list)
