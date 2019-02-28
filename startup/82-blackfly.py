from ophyd.areadetector import ADComponent
from ophyd import PointGreyDetectorCam
from ophyd import SingleTrigger, ImagePlugin, HDF5Plugin
from ophyd import AreaDetector


class XPDDBlackFlyDetector(SingleTrigger, AreaDetector):
    """PointGrey Black Fly detector(s) as used by 28-ID-D"""
    cam = ADComponent(PointGreyDetectorCam, "cam1:")
    image = ADComponent(ImagePlugin, "image1:")

blackfly_det = XPDDBlackFlyDetector('XF:28IDD-BI{Det-BlackFly}', name="blackfly_det")
