from myimports import * 

Usetup = Detector(mat.LXenon)

print "  Creating Blank Vacuum Setup:			Done"
path = "/home/chroma/chroma_env/stanford/new/UMass/"

green = 0xff00
blue = 0x0000ff
red = 0xFF0000

distance =-2.5

a = mesh_from_stl(path+"sourceMegasm_setdist_15.9mm_APD_Disk_wdrill-1.STL")
aS = Solid(a, mat.fullAbsorb, mat.LXenon, surf.steelSurface, blue)
#Usetup.add_solid(aS, displacement=(0,distance,0))

b = mesh_from_stl(path+"sourceMegasm_setdist_15.9mm_APD_Disk_wdrill-2.STL")
bS = Solid(b, mat.fullAbsorb, mat.LXenon, surf.steelSurface,blue)
Usetup.add_solid(bS, displacement=(0,0,0))

c = mesh_from_stl(path+"sourceMegasm_setdist_15.9mm - cylinder-1.STL")
cS = Solid(c, mat.fullAbsorb, mat.LXenon, surf.steelSurface, green)
#Usetup.add_solid(cS, displacement=(0,0,0))

e = mesh_from_stl(path+"sourceMegasm_setdist_15.9mm - MEG Complete-5 .24 SiPM Single (1)-1.STL")
eS = Solid(e, mat.silicon, mat.LXenon, data.top(e, surf.fulldetect, surf.steelSurface), data.top(e, red, blue))
Usetup.add_solid(eS, displacement=(0,0,0))

g = mesh_from_stl(path+"sourceMegasm_setdist_15.9mm - MEG Complete-5 .24 SiPM Single (1)-2.STL")
gS = Solid(g, mat.silicon, mat.LXenon, data.top(g, surf.fulldetect, surf.steelSurface), data.top(g, red, blue))
Usetup.add_solid(gS, displacement=(0,0,0))

i = mesh_from_stl(path+"sourceMegasm_setdist_15.9mm - MEG Complete-5 .24 SiPM Single (1)-3.STL")
iS = Solid(i, mat.silicon, mat.LXenon, data.top(i, surf.fulldetect, surf.steelSurface), data.top(i, red, blue))
Usetup.add_solid(iS, displacement=(0,0,0))

j = mesh_from_stl(path+"sourceMegasm_setdist_15.9mm - MEG Complete-5 .24 SiPM Single (1)-4.STL")
jS = Solid(j, mat.silicon, mat.LXenon, data.top(j, surf.fulldetect, surf.steelSurface), data.top(j, red, blue))
Usetup.add_solid(jS, displacement=(0,0,0))

k = mesh_from_stl(path+"sourceMegasm_setdist_15.9mm - MEG Complete-5 MEG Base-1.STL")
kS = Solid(k, mat.fullAbsorb, mat.LXenon, surf.steelSurface, blue)
Usetup.add_solid(kS, displacement=(0,0,0))

m = mesh_from_stl(path+"sourceMegasm_setdist_15.9mm - MEG Complete-5 MEG SO2-1.STL")
mS = Solid(m, mat.quartz, data.bottom(m, mat.silicon, mat.LXenon),  color=data.bottom(m, red, green))
#Usetup.add_solid(mS, displacement=(0,0,0))

o = mesh_from_stl(path+"sourceMegasm_setdist_15.9mm - Source-1 sourcelayer1-1.STL")
oS = Solid(o, mat.fullAbsorb, mat.LXenon, surf.steelSurface, green )
Usetup.add_solid(oS, displacement=(0,distance,0))

p = mesh_from_stl(path+"sourceMegasm_setdist_15.9mm - Source-1 sourcelayer2-1.STL")
pS = Solid(p, mat.fullAbsorb, mat.LXenon, surf.steelSurface, green)
Usetup.add_solid(pS, displacement=(0,distance,0))

q = mesh_from_stl(path+"sourceMegasm_setdist_15.9mm - Source-1 sourcelayer3-1.STL")
qS = Solid(q, mat.fullAbsorb, mat.LXenon, surf.steelSurface, red)
#Usetup.add_solid(qS, displacement=(0,0,0))

s = mesh_from_stl(path+"sourceMegasm_setdist_15.9mm - threadedrod-1.STL")
sS = Solid(s, mat.fullAbsorb, mat.LXenon, surf.steelSurface, green)
Usetup.add_solid(sS, displacement=(0,0,0))


t = mesh_from_stl(path+"sourceMegasm_setdist_15.9mm - threadedrod-2.STL")
tS = Solid(t, mat.fullAbsorb, mat.LXenon, surf.steelSurface, green)
Usetup.add_solid(tS, displacement=(0,10,0))
