# wisconsin-autonomous

The methods I used to build this program was color detection using HSV color space and contour detection. I converted the original picture from BGR to HSV, which made detecting the cones more effective. I used contour detection to identify the exact regions where the cones were located.

A technique that I tried for this program that wasn't effective was drawing lines between consecutive centroids, which assumed that all the cones were placed in a perfectly straight line. This didn't work as well because the cones were not placed in a linear path, so the line wasn't able to go through every cone.

The libraries that I used in this program are OpenCV and NumPy. 


