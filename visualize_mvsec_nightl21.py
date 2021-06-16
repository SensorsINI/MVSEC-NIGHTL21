"""Visualize MVSEC NIGHTL 21 Labels.

Author: Yuhuang Hu
Email : yuhuang.hu@ini.uzh.ch
"""

import os
import glob
import argparse

import numpy as np
import h5py

import matplotlib.pyplot as plt
import matplotlib.patches as patches

import cv2

parser = argparse.ArgumentParser()

parser.add_argument("--mvsec_data", type=str)
parser.add_argument("--gt_root", type=str)

parser.add_argument("--colab", action="store_true")

args = parser.parse_args()

# load mvsec data
mvsec_data = h5py.File(args.mvsec_data, "r")

frame_data = mvsec_data["davis"]["left"]["image_raw"]

# load labels
gt_files = sorted(glob.glob(os.path.join(args.gt_root, "*.txt")))
gt_idx = {int(os.path.basename(path)[:-4].split("_")[-1]): path
          for path in gt_files}

# load frame list
frame_list = np.loadtxt("./frame_list.txt", dtype=np.int16)

v_writer = None

for frame_idx in frame_list:

    # load frame
    frame = frame_data[frame_idx][()][..., np.newaxis]
    frame = np.concatenate((frame, frame, frame), axis=-1)

    fig = plt.figure(figsize=(5, 5))
    ax = plt.subplot(111)
    plt.imshow(frame)
    plt.axis("off")
    plt.title("Frame ID {}".format(frame_idx))

    if frame_idx in gt_idx:
        # there is a label, draw
        gt = np.loadtxt(gt_idx[frame_idx], usecols=(1, 2, 3, 4))
        if gt.ndim == 1:
            gt = gt[np.newaxis, ...]
    else:
        gt = None

    if gt is not None:
        for box in gt:
            box = box.astype(int)
            box[box < 0] = 0
            rect = patches.Rectangle(
                (box[0], box[1]), box[2]-box[0], box[3]-box[1],
                linewidth=3, edgecolor='r', facecolor='none')
            ax.add_patch(rect)

    plt.tight_layout()
    fig.canvas.draw()

    # save as video
    #  plt.show()

    data = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
    data = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))

    #  print("Saving Frame {} to video".format(frame_idx))

    if args.colab:
        if v_writer is None:
            fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
            v_writer = cv2.VideoWriter(
                "./output.mp4", fourcc, 30, (data.shape[1], data.shape[0]))

        v_writer.write(cv2.cvtColor(data, cv2.COLOR_BGR2RGB))
        print("\rWriting frame {}".format(frame_idx), end="")
    else:
        cv2.imshow("MVSEC-NIGHTL21 Visualization",
                   cv2.cvtColor(data, cv2.COLOR_BGR2RGB))
        cv2.waitKey(1)

    plt.cla()
    fig.clear()
    plt.close()
    del fig
