# MVSEC-NIGHTL21

https://user-images.githubusercontent.com/939553/122247023-57b18e80-cec7-11eb-8ac9-ed6bb88c1095.mp4

## Citation

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4967574.svg)](https://doi.org/10.5281/zenodo.4967574)

When use this dataset, please cite:

```bibtex
@InProceedings{Hu_2021_CVPR,
    author    = {Hu, Yuhuang and Liu, Shih-Chii and Delbruck, Tobi},
    title     = {v2e: From Video Frames to Realistic DVS Events},
    booktitle = {Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR) Workshops},
    month     = {June},
    year      = {2021},
    pages     = {1312-1321}
}
```

## Parent dataset: MVSEC

MVSEC-NIGHTL21 is derived dataset of "The Multi Vehicle Stereo Event Camera Dataset" which is available here: https://daniilidis-group.github.io/mvsec/

Please also cite the original MVSEC paper:

+ Zhu, A. Z., Thakur, D., Ozaslan, T., Pfrommer, B., Kumar, V., & Daniilidis, K. (2018). The Multi Vehicle Stereo Event Camera Dataset: An Event Camera Dataset for 3D Perception. IEEE Robotics and Automation Letters, 3(3), 2032-2039.

## Usage

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1qL8LoCZ-mm_O8K3aMDo22M3KSUtaK0cp?usp=sharing)

### Data Description

### MVSEC at night condition

We used `outdoor_night1_data.hdf5` of the MVSEC dataset.
The dataset is recorded with dual camera, we use the `left` camera.
In the HDF5 archive, the relevant dataset can be accessed as following:

```python
mvsec_data = h5py.File(mvsec_data_path, "r")

# raw frame
frame_data = mvsec_data["davis"]["left"]["image_raw"]
# frame timestamps
frame_ts = mvsec_data["davis"]["left"]["image_raw_ts"]

# raw events 
events_data = mvsec_data["davis"]["left"]["events"]

# event indices that corresponds to the frame
frame_event_inds = mvsec_data["davis"]["left"]["image_raw_event_inds"]
```

For visualization in this repository, we only used the raw frames.

### MVSEC-NIGHTL21 Labels

In the validation set, there are 400 frames. The list of the frame indices is in [`frame_list.txt`](./frame_list.txt).

Among these 400 frames, 368 frames are labeled. The frames that don't have labels are listed in [`frames_that_dont_have_labels.txt`](./frames_that_dont_have_labels.txt).
We labelled `car` in these frames.

The labelled groundtruths are stored in `.txt` files and can be found in [`mvsec_nightl21_labels`](./mvsec_nightl21_labels).

Each labeled car is in the format `car x_min y_min x_max y_max`. For example:

```
car 48 112 143 170
```

means `x_min=48, y_min=112`, and `x_max=143, y_max=170`.


### Visualization

1. Install dependency
    ```
    pip install h5py
    pip install matplotlib
    pip install opencv-python
    ```

2. Clone this repository
    ```
    git clone https://github.com/SensorsINI/MVSEC-NIGHTL21
    cd MVSEC-NIGHTL21
    ```

3. Download the `outdoor_night1_data.hdf5` from MVSEC dataset, available [here](https://drive.google.com/drive/folders/1rwyRk26wtWeRgrAx_fgPc-ubUzTFThkV)

4. Run The Visualization
    ```
     python visualize_mvsec_nightl21.py --mvsec_data /path/to/outdoor_night1_data.hdf5 --gt_root ./mvsec_nightl21_labels
    ```

    If everything works, you should see a video that annotates the cars.


## Contact

Yuhuang Hu  
yuhuang.hu@ini.uzh.ch
