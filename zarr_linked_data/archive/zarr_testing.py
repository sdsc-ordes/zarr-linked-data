import zarr
import random
import numpy as np


# ----------------------------------------------
###### ARCHIVE COMMENT
# ----------------------------------------------
# The goal of this script was to explore zarr functionalities. 
# It led to the creation of the fake data pipeline 
# in fake_data_flow.py
# ----------------------------------------------




# Question:
# is user responsible of consistent chunk size? You can put any value and there is never a problem
# Notes:
# ~1
# for accesing a group within a hierarchy, the open function finds the hierarchy file and the group file but when opening and writing into it, it generates a group.zarr file
# example: finds experience1 because it is in lab.zarr but also creates a zarr file for it (so extra zarr file created)
# ~2
# Can store as MongoDB, SQLite

# *********************************************
# Exploring Zarr tutorial
# --------------------------
# Create Zarr objects
# z1 = zarr.zeros((10000, 5000), chunks=(1000, 500), dtype='i4')
# zarr.save('data/z1.zarr', z1)
# array1 = np.arange(10)
# zarr.save('data/z2.zarr', array1)
# zarr.load('data/z2.zarr')
# print(z1.shape)

# *********************************************
# Assembling building blocks
# here the goal is to understand the shapes of the Zarr arrays
# also support orthogonal indexing, masks,
# conclusion: same manner of assembly as numpy arrays
# --------------------------
# chemicals = np.arange(10000000, dtype='i4').reshape(10000, 1000)
# chem_lib = zarr.array(chemicals, chunks=(1000, 100))
# print(chem_lib.shape)
# chem_lib.append(chemicals)
# small_chem_lib = np.vstack([chemicals, chemicals])
# # assemble 1 way
# chem_lib1 = chem_lib
# chem_lib1.append(small_chem_lib, axis=0)
# print("Stacked horizontally! " + str(chem_lib1.shape))
# # assemble another way
# chem_lib = zarr.array(chemicals, chunks=(1000, 100))
# chem_lib.append(chemicals)
# chem_lib2 = chem_lib
# chem_lib2.append(small_chem_lib, axis=1)
# print("Stacked vertically! " + str(chem_lib2.shape))

# *********************************************
# Assembling building blocks with a HIERARCHY
# ---------------------------------------------
# By Hand
# lab = zarr.group()
# robot1 = lab.create_group('robot1')
# robot2 = lab.create_group('robot1')
# experience1 = robot1.create_group('experience1')
# chemicals1 = experience1.create_dataset('chemicals1', shape=(4000, 1000), chunks=(400,100), dtype='i4')
# chemicals2 = experience1.create_dataset('chemicals2', shape=(9000, 1000), chunks=(900,100), dtype='i4')

# Iteratively
lab = zarr.group()
# Try to make a zarr iteratively
# generate a random number of experiences
num_robots = random.randint(3, 10)
for r in range(1, num_robots):
    robot_name = "robot" + str(r)
    locals()[robot_name] = lab.create_group(robot_name)
    # generate a random number of experiences
    num_experiences = random.randint(2, 5)
    # For each robot add the random number of experiences
    for e in range(1, num_experiences):
        exp_name = "experience" + str(e)
        locals()[exp_name] = locals()[robot_name].create_group(exp_name)
        # generate a random number of datasets
        num_datasets = random.randint(2, 10)
        # For each experience add the random number of chemical datasets used
        for d in range(1, num_datasets):
            num_chemicals = random.randint(1000, 10000)
            dataset_name = "chemicals" + str(d)
            locals()[dataset_name] = locals()[exp_name].create_dataset(
                dataset_name,
                shape=(num_chemicals, 1000),
                chunks=(num_chemicals / 10, 100),
                dtype="i4",
            )


# Create metadata
lab.attrs["professor"] = "John Doe"
lab.attrs["location"] = "EPFL"
lab.attrs["description"] = "This is a top notch chemistry lab."

experience1.attrs["researcher"] = "Bob Richard"


print(lab.tree())
print(lab.info)
# print(lab['robot1/experience1/chemicals1'])
print(sorted(lab.attrs))
print(sorted(experience1.attrs))
print("professor" in lab.attrs)
# zarr.save('data/lab.zarr', lab)
# test = zarr.open('data/experience1.zarr', mode='w')
# Note for test, find it because it is in lab.zarr but also creates a zarr file for it (so extra zarr file created)
