# AngleEye
 A convolutional model that recognizes the orientation of objects in an image.

## Detector.py
- This module detects object from an image.
- It only draws boxes around objects with the highest scores.
- Save the annotations if the model detects object correctly.
- Saved annotations will be used to crop images in Cropper.py.

## Cropper.py
- This module will annotated boxes from images.
- It will increase the accuracy during the angle recognition process.

## AngleEye.ipynb
- This module uses convolutional filters to determine the angle of the object's base.
- The comments in the code provide an explanation of how it works.

## AccuracyCheck.py
- This module checks the accuracy of AngleEye model.
  
