# Stone detection

A project on detecting stone impurity on scanned image of a bag of rice and counting the number of found impurities.

The project is  GUI application in Python. The GUI provides an interface for the User to select the image through a file explorer and then compare it with a generated image showing the found inpurity.

## Implementation
The project implements
* Image manipulation using Numpy an Pillow
* Image pixel traversal algorithm - done by first converting the image to a Numpy array and then applying the algorithm on it to spot changes in Pixel color and mark the portion of the image that has those changes.

## Usage
To preview how the project works, you can clone the repository and launch the build executable file on a windows machine.
