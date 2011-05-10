import IMP.domino

# create a model and some particles, they are just used as markers here
m= IMP.Model()
ps= [IMP.Particle(m) for i in range(0,10)]

# create a subset with a few of the particles
ss= IMP.domino.Subset([ps[3], ps[5], ps[7]])

file_name= IMP.create_temporary_file_name("assignments", "hdf5")

print "File name is", file_name

# open the file and clear any existing contents
rt= IMP.rmf.HDF5Group(file_name, True)

# add a data set to store it in, it must have dimension 2
data_set= rt.add_child_index_data_set("node_1_assignments", 2)

# create a list of assignments
asl=[]
for i in range(0,5):
    for j in range(0,5):
        for k in range(0,5):
            asl.append(IMP.domino.Assignment([i,j,k]))
IMP.domino.set_assignments(data_set, asl, ss, ps)

# to check, we can read it back immediately
back_asl= IMP.domino.get_assignments(data_set, ss, ps)

if back_asl==asl:
    print "They match!"
else:
    print "They don't match :-("


# More interestingly, we can create a new model and read back the assignments for that
mp= IMP.Model()
psp= [IMP.Particle(mp) for i in range(0,10)]

# create a subset with a few of the particles
ssp= IMP.domino.Subset([psp[3], psp[5], psp[7]])

print "Note the subsets are differently ordered (most of the time): ", ss, ssp

back_aslp= IMP.domino.get_assignments(data_set, ssp, psp)

# however, the states are demuxed so they match
print [str(a) for a in back_aslp]
