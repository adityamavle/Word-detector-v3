import torch

# Check the default CUDA device
device = torch.cuda.current_device()
print("Default CUDA device:", device)

# Set the default CUDA device
#torch.cuda.set_device(1)  # Set to device index 1

