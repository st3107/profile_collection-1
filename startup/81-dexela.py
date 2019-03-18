import os
import ophyd
from hxntools.detectors.dexela import (DexelaDetector, DexelaTiffPlugin)
from ophyd import (AreaDetector, CamBase, TIFFPlugin, Component as Cpt,
                    HDF5Plugin, Device, StatsPlugin, ProcessPlugin,
                    ROIPlugin, EpicsSignal)
from databroker.assets.handlers import HandlerBase
from ophyd.areadetector.filestore_mixins import (FileStoreIterativeWrite,
                                                 FileStoreHDF5IterativeWrite,
                                                 FileStoreTIFFSquashing,
                                                 FileStoreTIFF,
                                                 FileStoreHDF5, new_short_uid,
                                                 FileStoreBase
                                                 )
from ophyd.areadetector import (AreaDetector, PixiradDetectorCam, ImagePlugin,
                                TIFFPlugin, StatsPlugin, HDF5Plugin,
                                ProcessPlugin, ROIPlugin, TransformPlugin,
                                OverlayPlugin)
from ophyd.areadetector.trigger_mixins import SingleTrigger
from enum import Enum


class XPDDMode(Enum):
    step = 1
    fly = 2


class XPDDDexelaTiffPlugin(TIFFPlugin,FileStoreIterativeWrite ):
    pass


class XPDDDexelaDetector(SingleTrigger, DexelaDetector):
    total_points = Cpt(Signal, value=1, doc="The total number of points to be taken")
    tiff = Cpt(XPDDDexelaTiffPlugin, 'TIFF1:',
               read_attrs=[],
               configuration_attrs=[],
               write_path_template='Z:\\dex_data\\%Y\\%m\\%d\\',
               #write_path_template='Z:dex_data\\%Y\\%m\\%d\\',
               read_path_template='/nsls2/xf28id2/dex_data/%Y/%m/%d/',
               root='/nsls2/xf28id2/dex_data/')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._mode = XPDDMode.step

    def stage(self):
        self.cam.stage_sigs['image_mode'] = 'Single'
        self.cam.stage_sigs['trigger_mode'] = 'Int. Software'
        if self._mode is XPDDMode.fly:
            self.cam.stage_sigs['trigger_mode'] = 'Ext. Edge Single'
        return super().stage()

    def unstage(self):
        try:
            ret = super().unstage()
        finally:
            self._mode = XPDDMode.step
        return ret


dexela = XPDDDexelaDetector('XF:28IDD-ES:2{Det:DEX}', name='dexela')
dexela.read_attrs = ['tiff']
