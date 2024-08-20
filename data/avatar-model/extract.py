from __future__ import print_function
import os
import sys
import numpy as np
import pickle
from scipy.sparse import csc_matrix  # Ensure we're using scipy directly

print("OpenARK SMPL Model Converter Utility v0.2, created by Alex Yu 2018-19")
print("This utility converts SMPL pickled model files (.pkl) to PCL point cloud files (.pcd) + an easy-to-parse skeleton information file.\n")

if len(sys.argv) < 2:
    print("Usage: python extract.py pkl_file_name [dest_dir=pwd]")
    sys.exit(0)

SRC_PATH = sys.argv[1]
DEST_DIR = sys.argv[2] if len(sys.argv) >= 3 else ""

if DEST_DIR and not os.path.exists(DEST_DIR):
    os.makedirs(DEST_DIR)

MODEL_FILE = os.path.join(DEST_DIR, 'model.pcd')
SKEL_FILE = os.path.join(DEST_DIR, 'skeleton.txt')
JREG_FILE = os.path.join(DEST_DIR, 'joint_regressor.txt')
SHAPEKEY_DIR = os.path.join(DEST_DIR, 'shapekey')

if not os.path.exists(SHAPEKEY_DIR):
    os.makedirs(SHAPEKEY_DIR)

def write_pcd(path, data):
    with open(path, 'w') as f:
        f.write("VERSION .7\nFIELDS x y z\nSIZE 4 4 4\nTYPE F F F\nCOUNT 1 1 1\n")
        f.write("WIDTH " + str(data.shape[0]) + "\nHEIGHT 1\nVIEWPOINT 0 0 0 1 0 0 0\n")
        f.write("POINTS " + str(data.shape[0]) + "\nDATA ascii\n")
        np.savetxt(f, data, fmt="%.18f")

def write_skel(path, joints, data):
    with open(path, 'w') as f:
        f.write("%s %s\n" % (joints.shape[0], data.shape[0]))
        names = ["PELVIS", "R_HIP", "L_HIP", "SPINE1", "R_KNEE", "L_KNEE", "SPINE2", "R_ANKLE", "L_ANKLE", "SPINE3", "R_FOOT", "L_FOOT", "NECK", "R_COLLAR", "L_COLLAR", "HEAD", "R_SHOULDER", "L_SHOULDER", "R_ELBOW", "L_ELBOW", "R_WRIST", "L_WRIST", "R_HAND", "L_HAND"]
        parents = [-1, 0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 9, 9, 12, 13, 14, 16, 17, 18, 19, 20, 21]
        for i in range(joints.shape[0]):
            f.write("%s %s %s %.18f %.18f %.18f\n" % (i, parents[i], names[i], joints[i][0], joints[i][1], joints[i][2]))
        for row in data:
            nonzero = [i for i in range(row.shape[0]) if row[i] > 0]
            f.write("%s" % len(nonzero))
            for i in nonzero:
                f.write(" %s %.18f" % (i, row[i]))
            f.write("\n")

def write_jreg(path, data):
    with open(path, 'w') as f:
        f.write('%s\n' % data.shape[0])
        data_rows = csc_matrix(data)
        for i in range(data_rows.shape[0]):
            row = data_rows[i]
            f.write(str(row.nnz))
            for j in range(row.nnz):
                f.write(' %s %.18f' % (row.indices[j], row.data[j]))
            f.write('\n')

# Handle the pickle loading without `chumpy`
with open(SRC_PATH, 'rb') as f:
    try:
        d = pickle.load(f, encoding='latin1')
    except UnicodeDecodeError:
        print("UnicodeDecodeError: The file might be using a different encoding.")
        sys.exit(1)
    except ModuleNotFoundError as e:
        if "chumpy" in str(e):
            print("Bypassing chumpy import issue")
            sys.modules['chumpy'] = None
            d = pickle.load(f, encoding='latin1')
        else:
            raise

# Process the data
print("Writing model template...")
write_pcd(MODEL_FILE, d['v_template'])

print("Writing skeleton...")
write_skel(SKEL_FILE, d['J'], d['weights'])

print("Writing joint regressor...")
write_jreg(JREG_FILE, d['J_regressor'])

print("Writing shape shapekeys...")
shapedirs = d['shapedirs']
for i in range(shapedirs.shape[2]):
    path = os.path.join(SHAPEKEY_DIR, "shape%03d.pcd" % i)
    write_pcd(path, shapedirs[:, :, i])
    if i % 5 == 4:
        print("%s of %s shape shapekeys written" % (i + 1, shapedirs.shape[2]))

print("All done.")
