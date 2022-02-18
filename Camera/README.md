# Camera Package
UAV deployable camera package for monitoring hydrology and performing edge computing. 
<p align="center">
<img src="V1.0/pics/v1-module.png" alt="drawing" width="600"/>
</p>
<p align="center">
Figure 1: Camera Package installed underneath a structure.
</p>

## Modular Components
The major components of this package are:
1. Control Board (Raspberry Pi)
2. Camera (PiCam v2.1)
3. Electropermanent Magnet
4. Radio Chip (NRF)

## NRFCommunicate

NRFCommunicate wraps a basic NRF circuit-python package. The goal is to create a plug-and-play library not just for uploading data, but also for communication between sensor packages.


## V1
1.	Powered off battery (not battery monitoring)
1.	Begins program on startup
1.	Takes picture whenever it gets a signal from the NRF
1.	Images stored on a SD card on the PI (not sure how to extract data)
1.	Has the electro permanent magnet that can turn on and off with a signal from the NRF (need to see if we can integrates this with the controller from the gauge sensor)
 








