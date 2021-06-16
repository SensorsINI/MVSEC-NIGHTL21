"""Find correspondence between data and saved record."""

import os
import glob
import argparse
import shutil

import numpy as np
import h5py

import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()

parser.add_argument("--mvsec_data", type=str)
parser.add_argument("--saved_record_path", type=str)
parser.add_argument("--saved_gt_path", type=str)

parser.add_argument("--out_gt_path", type=str)

args = parser.parse_args()

# load mvsec data

mvsec_data = h5py.File(args.mvsec_data, "r")

frame_data = mvsec_data["davis"]["left"]["image_raw"]

# load saved record data
saved_files = sorted(glob.glob(os.path.join(args.saved_record_path, "*.npz")))


# load saved record data
saved_gt_files = sorted(glob.glob(os.path.join(args.saved_gt_path, "*.txt")))

# find anchor
#  data = np.load(saved_files[0])
#  first_saved_frame = data["img"]

#  for idx in range(frame_data.shape[0]):
#      temp_frame = frame_data[idx][()]
#
#      diff = (temp_frame-first_saved_frame).sum()
#
#      if diff == 0:
#          print("Found my frame: {}".format(idx))
#          break
#      else:
#          print("missed")

# Found idx = 1975

found_idx = 1975


def search_right_frame(ref, data, idx):
    frame = data[idx][()]

    if (ref-frame).sum() == 0:
        # found
        return idx
    else:
        return search_right_frame(ref, data, idx+1)


relations = {}
for file_path in saved_files:
    # load data
    data = np.load(file_path)
    saved_frame = data["img"]

    fn = os.path.basename(file_path)[:-4]

    # load mvsec frame
    found_idx = search_right_frame(saved_frame, frame_data, found_idx)

    #  print("{} -> {}".format(fn, found_idx))

    relations[fn] = found_idx

    print(found_idx)

#  print(relations)

# align label

#  if not os.path.isdir(args.out_gt_path):
#      os.makedirs(args.out_gt_path)
#
#  for file_path in saved_gt_files:
#      fn = os.path.basename(file_path)[:-4]
#
#      out_file_name = "gt_label_frame_{}.txt".format(relations[fn])
#      print(out_file_name)
#
#      out_path = os.path.join(args.out_gt_path, out_file_name)
#
#      # move to the new place
#      shutil.copyfile(file_path, out_path)

# find missing frame ids

#  gt_filenames = [os.path.basename(path)[:-4] for path in saved_gt_files]
#
#  print(len(gt_filenames))
#  print(len(relations.keys()))
#
#  num_missing_files = 0
#  for key in relations.keys():
#
#      if key not in gt_filenames:
#          print("Frame {}".format(relations[key]))
#          num_missing_files += 1
#
#  print("Number of missing files {}".format(num_missing_files))
