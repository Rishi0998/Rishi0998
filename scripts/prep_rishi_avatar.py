import numpy as np
from PIL import Image

# Load current_avatar.png
im = Image.open('current_avatar.png').convert('RGB')
arr = np.array(im, dtype=float)

# Background color in current_avatar.png is around [114, 89, 119]
bg_color = np.array([114.0, 89.0, 119.0])
dist = np.sqrt(np.sum((arr - bg_color)**2, axis=-1))

# Mask background pixels
is_bg = dist < 30.0

# In grayscale, background should be pure white (255) so it becomes spaces in ASCII
gray = np.mean(arr, axis=-1)
# Push background to 255
gray[is_bg] = 255.0

# Also increase contrast of hair and glasses
prepped = Image.fromarray(gray.astype(np.uint8))
prepped.save('source-prepped.png')
print('Successfully prepped avatar -> source-prepped.png')
