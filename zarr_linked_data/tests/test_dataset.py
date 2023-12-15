import numpy as np 

extracted_dataset = np.load("zarr_linked_data/data/results/dataset.npy")

print(extracted_dataset.shape)
print(extracted_dataset[1,10])