import os
import ophyd
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


# monkey patch for trailing slash problem (from XPD's profile, see
# https://github.com/NSLS-II-XPD/profile_collection/blob/master/startup/80-areadetector.py#L17-L32)
def _ensure_trailing_slash(path):
    """
    'a/b/c' -> 'a/b/c/'
    EPICS adds the trailing slash itself if we do not, so in order for the
    setpoint filepath to match the readback filepath, we need to add the
    trailing slash ourselves.
    """
    newpath = os.path.join(path, '')
    if newpath[0] != '/' and newpath[-1] == '/':
        # make it a windows slash
        newpath = newpath[:-1]
    return newpath

ophyd.areadetector.filestore_mixins._ensure_trailing_slash = _ensure_trailing_slash

class BulkDexela(HandlerBase):
    HANDLER_NAME = 'DEXELA_FLY_V1'
    def __init__(self, resource_fn):
        self._handle = h5py.File(resource_fn, 'r')

    def __call__(self):
        return self._handle['entry/instrument/detector/data'][:]

db.reg.register_handler(BulkDexela.HANDLER_NAME, BulkDexela,
                        overwrite=True)


class FileStoreBulkReadable(FileStoreIterativeWrite):
    def _reset_data(self):
        self._datum_uids.clear()
        self._point_counter = itertools.count()
    def bulk_read(self, timestamps):
        image_name = self.image_name
        uids = [self.generate_datum(self.image_name, ts, {}) for ts in timestamps]
        # clear so unstage will not save the images twice:
        self._reset_data()
        return {image_name: uids}
    @property
    def image_name(self):
        return self.parent._image_name

class DexelaTiffPlugin(TIFFPlugin, FileStoreBulkReadable, FileStoreTIFF,
                               Device):
    def mode_external(self):
        total_points = self.parent.mode_settings.total_points.get()
        self.stage_sigs[self.num_capture] = total_points

    def get_frames_per_point(self):
        mode = self.parent.mode_settings.mode.get()
        if mode == 'external':
            return 1
        else:
            return self.parent.cam.num_images.get()


class DexelaDetectorCam(CamBase):
    acquire_gain = Cpt(EpicsSignal, 'DEXAcquireGain')
    acquire_offset = Cpt(EpicsSignal, 'DEXAcquireOffset')
    binning_mode = Cpt(SignalWithRBV, 'DEXBinningMode')
    corrections_dir = Cpt(EpicsSignal, 'DEXCorrectionsDir', string=True)
    current_gain_frame = Cpt(EpicsSignal, 'DEXCurrentGainFrame')
    current_offset_frame = Cpt(EpicsSignal, 'DEXCurrentOffsetFrame')
    defect_map_available = Cpt(EpicsSignal, 'DEXDefectMapAvailable')
    defect_map_file = Cpt(EpicsSignal, 'DEXDefectMapFile', string=True)
    full_well_mode = Cpt(SignalWithRBV, 'DEXFullWellMode')
    gain_available = Cpt(EpicsSignal, 'DEXGainAvailable')
    gain_file = Cpt(EpicsSignal, 'DEXGainFile', string=True)
    load_defect_map_file = Cpt(EpicsSignal, 'DEXLoadDefectMapFile')
    load_gain_file = Cpt(EpicsSignal, 'DEXLoadGainFile')
    load_offset_file = Cpt(EpicsSignal, 'DEXLoadOffsetFile')
    num_gain_frames = Cpt(EpicsSignal, 'DEXNumGainFrames')
    num_offset_frames = Cpt(EpicsSignal, 'DEXNumOffsetFrames')
    offset_available = Cpt(EpicsSignal, 'DEXOffsetAvailable')
    offset_constant = Cpt(SignalWithRBV, 'DEXOffsetConstant')
    offset_file = Cpt(EpicsSignal, 'DEXOffsetFile', string=True)
    save_gain_file = Cpt(EpicsSignal, 'DEXSaveGainFile')
    save_offset_file = Cpt(EpicsSignal, 'DEXSaveOffsetFile')
    serial_number = Cpt(EpicsSignal, 'DEXSerialNumber')
    software_trigger = Cpt(EpicsSignal, 'DEXSoftwareTrigger')
    use_defect_map = Cpt(EpicsSignal, 'DEXUseDefectMap')
    use_gain = Cpt(EpicsSignal, 'DEXUseGain')
    use_offset = Cpt(EpicsSignal, 'DEXUseOffset')


class DexelaDetector(AreaDetector):
    cam = Cpt(DexelaDetectorCam, 'cam1:',
            read_attrs=[],
            configuration_attrs=['image_mode', 'trigger_mode',
                                'acquire_time', 'acquire_period'],
            )

class XPDDDexelaDetector(SingleTrigger, DexelaDetector):
    total_points = Cpt(Signal, value=1, doc="The total number of points to be taken")
    tiff1 = Cpt(DexelaTiffPlugin, 'TIFF1:',
               read_attrs=[],
               configuration_attrs=[],
               write_path_template='Z:\\%Y\\%m\\%d\\',
               read_path_template='/nsls2/xf28id2/XF05ID1/dexela/%Y/%m/%d/',
               root='/nsls2/xf05id1/XF05ID1/dexela/')
    # this is used as a latch to put the xspress3 into 'bulk' mode
    # for fly scanning.  Do this is a signal (rather than as a local variable
    # or as a method so we can modify this as part of a plan
    fly_next = Cpt(Signal, value=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._mode = XPDDMode.step

    def stage(self):
        # do the latching
        if self.fly_next.get():
            self.fly_next.put(False)
            self._mode = XPDDMode.fly

        self.cam.stage_sigs['image_mode'] = 'Multiple'
        if self._mode is XPDDMode.fly:
            self.cam.stage_sigs['trigger_mode'] = 'Ext. Edge Single'
        else:
            self.cam.stage_sigs['trigger_mode'] = 'Int. Fixed Rate'


        return super().stage()

    def unstage(self):
        try:
            ret = super().unstage()
        finally:
            self._mode = XPDDMode.step
        return ret


dexela = XPDDDexelaDetector('XF:28IDD-ES:2{Dex:DEX}', name='dexela')
dexela.read_attrs = ['tiff1']
