from ophyd.areadetector import ADComponent
from ophyd import PointGreyDetectorCam
from ophyd import SingleTrigger, ImagePlugin, HDF5Plugin
from ophyd import AreaDetector


class XPDDBlackFlyMode(Enum):
    step = 1

:
class XPDDBlackFlyTiffPlugin(TIFFPlugin, FileStoreTIFF, Device):
    pass


class XPDDBlackFlyDetector(SingleTrigger, AreaDetector):
    """PointGrey Black Fly detector(s) as used by 28-ID-D"""
    cam = ADComponent(PointGreyDetectorCam, "cam1:")
    image = ADComponent(ImagePlugin, "image1:")
    tiff = Cpt(XPDDBlackFlyTiffPlugin, 'TIFF1:',
               read_attrs=[],
               configuration_attrs=[],
               write_path_template='Z:blackfly_data\\',
               read_path_template='/nsls2/xf28id2/blackfly_data/%Y/%m/%d/',
               root='/nsls2/xf28id2/dex_data/')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._mode = XPDDBlackFlyMode.step

    def stage(self):
        self.cam.stage_sigs['image_mode'] = 'Single'
        self.cam.stage_sigs['trigger_mode'] = 'Int. Software'
        return super().stage()

    def unstage(self):
        try:
            ret = super().unstage()
        finally:
            self._mode = XPDDBlackflyMode.step
            return ret


blackfly = XPDDBlackFlyDetector('XF:28IDD-BI{Det-BlackFly}', name="blackfly_det")
blackfly.read_attrs = ['tiff']
