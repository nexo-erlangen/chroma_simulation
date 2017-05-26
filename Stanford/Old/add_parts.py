from myimports import * 

setup = Detector(mat.vacuum)
demoSetup = Detector(mat.vacuum)

print "  Creating Blank Vacuum Setup:			Done"
path = "/home/exo/Dropbox/Stanford/LXECell_standoff/"

green = 0xff00
blue = 0x0000ff
red = 0xff0000

a = mesh_from_stl(path+"LXE CELL ASSY with standoffs_CF 12 BLANK_190.stl")
aS = Solid(a, mat.fullAbsorb, mat.vacuum, surf.steelSurface)
setup.add_solid(aS, displacement=(0,0,0))

b = mesh_from_stl(path+"LXE CELL ASSY with standoffs_ANODE MOUNTING PLATE V2_282.stl")
bS = Solid(b, mat.fullAbsorb, mat.LXenon, surf.steelSurface)
setup.add_solid(bS, displacement=(0,0,0))

c = mesh_from_stl(path+"LXE CELL ASSY with standoffs_CERAMIC INTERFACE BOARD_307.stl")
cS = Solid(c, mat.fullAbsorb, mat.LXenon, surf.steelSurface)
setup.add_solid(cS, displacement=(0,0,0))

e = mesh_from_stl(path+"LXE CELL ASSY with standoffs_CERAMIC INTERFACE BOARD_368.stl")
eS = Solid(e, mat.fullAbsorb, mat.LXenon, surf.steelSurface)
setup.add_solid(eS, displacement=(0,0,0))

g = mesh_from_stl(path+"LXE CELL ASSY with standoffs_QUARTZ WAFER_429.stl")
gS = Solid(g, mat.fullAbsorb, mat.LXenon, surf.steelSurface)
setup.add_solid(gS, displacement=(0,0,0))
#demoSetup.add_solid(gS, displacement=(0,0,0))

i = mesh_from_stl(path+"LXE CELL ASSY with standoffs_CF 12 FLANGE_1.stl")
iS = Solid(i, mat.fullAbsorb, mat.vacuum, surf.steelSurface)
setup.add_solid(iS, displacement=(0,0,0))

j = mesh_from_stl(path+"LXE CELL ASSY with standoffs_CF 12 FLANGE_3.stl")
jS = Solid(j, mat.fullAbsorb, mat.vacuum, surf.steelSurface)
setup.add_solid(jS, displacement=(0,0,0))

k = mesh_from_stl(path+"LXE CELL ASSY with standoffs_CF 12 TUBE_2.stl")
kS = Solid(k, mat.fullAbsorb, mat.vacuum, surf.steelSurface)
setup.add_solid(kS, displacement=(0,0,0))

BIsourceM = mesh_from_stl(path+"LXE CELL ASSY with standoffs_Bi Source_132.stl")
BIsourceS = Solid(BIsourceM, mat.fullAbsorb, mat.vacuum, surf.steelSurface, color=0x3366FF)
demoSetup.add_solid(BIsourceS, displacement=(0,0,0))
setup.add_solid(BIsourceS, displacement=(-1,0,5))

BItriangCent = BIsourceM.get_triangle_centers()

BIlocx = np.mean(BItriangCent[:,0])
BIlocy = np.mean(BItriangCent[:,1])
BIlocz = np.mean(BItriangCent[:,2])
#print "====================================================================="
#print "  Bismuth Source Triangle Centers		x:",BIlocx
#print "						y:",BIlocy
#print "						z:",BIlocz

o = mesh_from_stl(path+"LXE CELL ASSY with standoffs_CATHODE MESH_82.stl")
oS = Solid(o, mat.fullAbsorb, mat.LXenon, surf.steelSurface)
setup.add_solid(oS, displacement=(0,0,0))
o_center = o.get_triangle_centers()

p = mesh_from_stl(path+"LXE CELL ASSY with standoffs_CATHODE SUPPORT RING BOTTOM_83.stl")
pS = Solid(p, mat.fullAbsorb, mat.LXenon, surf.steelSurface)
setup.add_solid(pS, displacement=(0,0,0))

q = mesh_from_stl(path+"LXE CELL ASSY with standoffs_CATHODE SUPPORT RING TOP_81.stl")
qS = Solid(q, mat.fullAbsorb, mat.LXenon, surf.steelSurface)
setup.add_solid(qS, displacement=(0,0,0))

s = mesh_from_stl(path+"LXE CELL ASSY with standoffs_reducer_CF12_CF6_14.stl")
s_center = s.get_triangle_centers()
r_min = min(np.sqrt(s_center[:,0]*s_center[:,0] + s_center[:,2]*s_center[:,2]))
s_MIn = np.where(np.sqrt(s_center[:,0]*s_center[:,0] + s_center[:,2]*s_center[:,2]) <= (r_min + 0.01*r_min), mat.LXenon, mat.vacuum)
s_MInC = np.where(np.sqrt(s_center[:,0]*s_center[:,0] + s_center[:,2]*s_center[:,2]) <= (r_min + 0.01*r_min),0x01df01, 0x0000ff)
sS = Solid(s, mat.fullAbsorb, s_MIn, surf.steelSurface, color = s_MInC)
setup.add_solid(sS, displacement=(0,0,0))
demoSetup.add_solid(sS, displacement=(0,0,0))

t = mesh_from_stl(path+"LXE CELL ASSY with standoffs_0194605B_22.stl")
tS = Solid(t, mat.fullAbsorb, mat.vacuum, surf.steelSurface)
setup.add_solid(tS, displacement=(0,0,0))

u = mesh_from_stl(path+"LXE CELL ASSY with standoffs_0194303C_20.stl")
uS = Solid(u, mat.fullAbsorb, mat.vacuum, surf.steelSurface)
setup.add_solid(uS, displacement=(0,0,0))

v = mesh_from_stl(path+"LXE CELL ASSY with standoffs_1002204A_21.stl")
v_center = v.get_triangle_centers()
top = max(v_center[:,1])
material_out = np.where(top, mat.LXenon, mat.vacuum)
vS = Solid(v, mat.MSuprasil, material_out)
setup.add_solid(vS, displacement=(0,0,0))
demoSetup.add_solid(vS, displacement=(0,0,0))

triangleCenters = v.get_triangle_centers()
meanX = np.mean(triangleCenters[:,0])
meanY = np.mean(triangleCenters[:,1])
bottomY = np.min(triangleCenters[:,1])
meanZ = np.mean(triangleCenters[:,2])

#print "---------------------------------------------------------------------"
#print "  Cap Triangle Centers				x:" ,meanX
#print "						y:",meanY
#print "						z:",meanZ
#print "---------------------------------------------------------------------"
#print "  Adjusted Bismuth center 			x:",BIlocx-meanX
#print "  (oriented to cap) 				z:",BIlocz-meanZ

xshift = meanX
zshift = meanZ

#a_center = a.get_triangle_centers()
#b_center = b.get_triangle_centers()
#c_center = c.get_triangle_centers()
#e_center = e.get_triangle_centers()
#g_center = g.get_triangle_centers()
#i_center = i.get_triangle_centers()
#j_center = j.get_triangle_centers()
#k_center = k.get_triangle_centers()

#p_center = p.get_triangle_centers()
#q_center = q.get_triangle_centers()
#s_center = s.get_triangle_centers()
#t_center = t.get_triangle_centers()
#u_center = u.get_triangle_centers()
