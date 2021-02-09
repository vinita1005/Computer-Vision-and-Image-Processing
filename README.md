# Computer-Vision-and-Image-Processing
Implementation of various computer vision and image processing algorithms

Developed an image processing system to produce panorama images from a set of images.
Algorithms implemented:
1. ORB for detecting key points.
2. Good feature extraction by calculating hamming distances.
3. Ransac algorithm for feature matching.
4. Calculating homography matrix.
5. Opencv WarpPerspective to warp one image onto another using the homography matrix.
6. Cropping the final panorama by calculating the max black pixel coordintates.

# Some examples:

Data given: 3 images for horizontal alignment


<img src="https://github.com/vinita1005/Computer-Vision-and-Image-Processing/blob/panorama/panorama_results/data/nevada.jpg" width="300" height="200">
<img src="https://github.com/vinita1005/Computer-Vision-and-Image-Processing/blob/panorama/panorama_results/data/nevada2.jpg" width="300" height="200">
<img src="https://github.com/vinita1005/Computer-Vision-and-Image-Processing/blob/panorama/panorama_results/data/nevada3.jpg" width="300" height="200">

Panaroma:

<img src="https://github.com/vinita1005/Computer-Vision-and-Image-Processing/blob/panorama/panorama_results/data/panorama.jpg" width="500" height="300">

Data given: 3 images for vertical alignment

<img src="https://github.com/vinita1005/Computer-Vision-and-Image-Processing/blob/panorama/panorama_results/extra2/shanghai-20.png" width="300" height="200">
<img src="https://github.com/vinita1005/Computer-Vision-and-Image-Processing/blob/panorama/panorama_results/extra2/shanghai-22.png" width="300" height="200">
<img src="https://github.com/vinita1005/Computer-Vision-and-Image-Processing/blob/panorama/panorama_results/extra2/shanghai-23.png" width="300" height="200">

Panaroma:

<img src="https://github.com/vinita1005/Computer-Vision-and-Image-Processing/blob/panorama/panorama_results/extra2/panorama.jpg" width="400" height="400">

Data given: 5 images for horizontal alignment


<img src="https://github.com/vinita1005/Computer-Vision-and-Image-Processing/blob/panorama/panorama_results/extra3/fishbowl-a.png" width="300" height="200">
<img src="https://github.com/vinita1005/Computer-Vision-and-Image-Processing/blob/panorama/panorama_results/extra3/fishbowl-b.png" width="300" height="200">
<img src="https://github.com/vinita1005/Computer-Vision-and-Image-Processing/blob/panorama/panorama_results/extra3/fishbowl-c.png" width="300" height="200">
<img src="https://github.com/vinita1005/Computer-Vision-and-Image-Processing/blob/panorama/panorama_results/extra3/fishbowl-d.png" width="300" height="200">
<img src="https://github.com/vinita1005/Computer-Vision-and-Image-Processing/blob/panorama/panorama_results/extra3/fishbowl-e.png" width="300" height="200">

Panaroma:


<img src="https://github.com/vinita1005/Computer-Vision-and-Image-Processing/blob/panorama/panorama_results/extra3/panorama.jpg" width="600" height="300">
