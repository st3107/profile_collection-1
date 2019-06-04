# ACQ SIDE - Edited by Chris 07_24
# ======================================================
import time

import numpy as np
import bluesky.plans as bp
import bluesky.plan_stubs as bps
import bluesky.preprocessors as bpp
from bluesky.utils import Msg, short_uid as _short_uid
from bluesky.preprocessors import subs_wrapper
from bluesky.simulators import summarize_plan
from bluesky.callbacks import LiveTable
from xpdacq.xpdacq_conf import xpd_configuration
from xpdacq.xpdacq import glbl, CustomizedRunEngine
from xpdacq.beamtime import (
    _configure_area_det,
    close_shutter_stub,
    open_shutter_stub,
)
from xpdacq.beamtime import _check_mini_expo


# Copied this from upstream, remove and import when new version of xpdAcq comes
# out
def configure_area_det_expo(exposure):
    det = xpd_configuration["area_det"]

    yield from bps.abs_set(
        det.cam.acquire_time, glbl["frame_acq_time"], wait=True
    )
    acq_time = det.cam.acquire_time.get()
    _check_mini_expo(exposure, acq_time)
    if hasattr(det, "images_per_set"):
        # compute number of frames
        num_frame = np.ceil(exposure / acq_time)
        yield from bps.abs_set(det.images_per_set, num_frame, wait=True)
    else:
        # The dexela detector does not support `images_per_set` so we just
        # use whatever the user asks for as the thing
        # TODO: maybe put in warnings if the exposure is too long?
        num_frame = 1
    computed_exposure = num_frame * acq_time

    # print exposure time
    print(
        "INFO: requested exposure time = {} - > computed exposure time"
        "= {}".format(exposure, computed_exposure)
    )
    return num_frame, acq_time, computed_exposure


save_kwargs = {}

shutter = xpd_configuration["shutter"]
sh_open = glbl["shutter_conf"]["open"]
sh_close = glbl["shutter_conf"]["close"]
sample_motor = spinner_goniohead.X

# experimental info
Tstart, Tstop, numT = 5, 15, 3
# Tstart1, Tstop1, numT1 = 150, 300, 11
# Tstart, Tstop, numT = 11, 17, 3
det_z_pos1, det_z_pos2 = 1195, 1995
_configure_area_det(600)

# special dict for cryostat experiment
sample1_name, sample1_pos, sample1_expo, sample1_wait = (
    "Sample1",
    -10.44,
    600,
    20,
)  # CHANGE as needed!!!!!
sample2_name, sample2_pos, sample2_expo, sample2_wait = (
    "Sample2",
    -8.44,
    600,
    20,
)  # CHANGE as needed!!!!!
sample3_name, sample3_pos, sample3_expo, sample3_wait = (
    "Sample3",
    -6.44,
    600,
    20,
)  # CHANGE as needed!!!!!
### NOTE: Sample positions must be evenly spaced


sub_sample_dict = {
    sample1_pos: {
        "name": sample1_name,
        "exposure": sample1_expo,
        "wait": sample1_wait,
    },
    sample2_pos: {
        "name": sample2_name,
        "exposure": sample2_expo,
        "wait": sample2_wait,
    },
    sample3_pos: {
        "name": sample3_name,
        "exposure": sample3_expo,
        "wait": sample3_wait,
    },
}

# this is tailored for xpdAn at this stage. Will be changed in the future
cryostat_sample_dict = {"sub_samples": sub_sample_dict}

# heating stage of cryostat
heater_dict = {(4, 30): 1, (30, 80): 2, (80, 600): 3}


# vendor blusky nd_per_step
def light_dark_nd_step(detectors, step, pos_cache):
    """
    Inner loop of an N-dimensional step scan
    This is the default function for ``per_step`` param`` in ND plans.
    Parameters
    ----------
    detectors : iterable
        devices to read
    step : dict
        mapping motors to positions in this step
    pos_cache : dict
        mapping motors to their last-set positions
    """

    def move():
        yield Msg("checkpoint")
        grp = _short_uid("set")
        for motor, pos in step.items():
            if pos == pos_cache[motor]:
                # This step does not move this motor.
                continue
            yield Msg("set", motor, pos, group=grp)
            pos_cache[motor] = pos
        yield Msg("wait", None, group=grp)

    motors = step.keys()
    yield from close_shutter_stub()
    yield from move()
    for k, v in sub_sample_dict.items():
        if np.abs(sample_motor.get().user_readback - k) < 1.5:
            inner_dict = v
            break
        else:
            inner_dict = {"exposure": .1, "wait": 1}
    print(inner_dict)
    yield from configure_area_det_expo(inner_dict["exposure"])

    # This is to make certain that the detector has properly configured the
    # exposure time, uncomment if waits don't work
    # yield from bps.sleep(10)

    yield from bps.trigger_and_read(
        list(detectors) + list(motors) + [shutter], name="dark"
    )
    yield from open_shutter_stub()

    t0 = time.time()
    yield from bps.trigger_and_read(list(detectors) + list(motors) + [shutter])
    t1 = time.time()
    print(
        "INFO: exposure time (plus minor message overhead) = {:.2f}".format(
            t1 - t0
        )
    )

    yield from close_shutter_stub()
    yield from bps.sleep(inner_dict["wait"])

# cryostat doesn't properly hint its temperature so we sideband this here
cryostat1.T.kind = 'hinted'

plan = bp.grid_scan(
    [pe1c, shutter, cryostat1, cryostat2, sample_motor],
    cryostat1,
    Tstart,
    Tstop,
    numT,
    Det_1_Z,
    det_z_pos1,
    det_z_pos2,
    2,
    False,
    # comment this line if you dont want to move detector
    sample_motor,
    sample1_pos,
    sample3_pos,
    3,
    False,
    per_step=light_dark_nd_step,

    # uncomment if cryostat is not hinted properly
    # md={
    #     "hints": {
    #         "gridding": "rectilinear",
    #         "dimensions": [
    #             [["cryostat1_T"], "primary"],
    #             [["spinner_goniohead_X"], "primary"],
    #             [["Det_1_Z"], "primary"],
    #         ],
    #     }
    # },
)

dummy_plan = bp.grid_scan(
    [pe1c, shutter, cryostat1, cryostat2, sample_motor],
    cryostat1,
    Tstart,
    Tstop,
    numT,
    Det_1_Z,
    det_z_pos1,
    det_z_pos2,
    2,
    False,
    # comment this line if you dont want to move detector
    sample_motor,
    sample1_pos,
    sample3_pos,
    3,
    False,
    per_step=light_dark_nd_step,
    md={
        "hints": {
            "gridding": "rectilinear",
            "dimensions": [
                [["cryostat1_T"], "primary"],
                [["spinner_goniohead_X"], "primary"],
                [["cryostat2_T"], "primary"],
            ],
        }
    },
)

# plan = bpp.subs_wrapper(plan, LiveTable([pe1c, shutter, Det_1_Z, cryostat1, sample_motor]))

# COPY this to your terminal, DO NOT run in script
"""
# prview the plan
summarize_plan(dummy_plan)
# execute the plan
xrun(cryostat_sample_dict, plan, subs=[LiveTable([pe1c, shutter, Det_1_Z, cryostat1, sample_motor])])
_configure_area_det(300)

"""

# AN SIDE
# =================================================================================
"""save_kwargs['string'] = (''
                         '{base_folder}/{folder_prefix}/'
                         '{analysis_stage}/'
                         '{human_timestamp}_'
                         '[temp_{raw_event[data][cryostat1_T]:1.2f}'
                         '{raw_descriptor[data_keys][cryostat1_T][units]}]_'
                         '[dx_{raw_event[data][diff_x]:1.3f}'
                         '{raw_descriptor[data_keys][diff_x][units]}]_'
                         '[dy_{raw_event[data][diff_y]:1.3f}'
                         '{raw_descriptor[data_keys][diff_y][units]}]_'
                         '[z_{raw_event[data][Det_1_Z]:1.3f}'
                         '{raw_descriptor[data_keys][Det_1_Z][units]}]_'
                         '[gx_{raw_event[data][spinner_goniohead_X]:1.3f}'
                         '{raw_descriptor[data_keys][spinner_goniohead_X][units]}]_'
                         '{raw_start[uid]:.6}_'
                         '{raw_event[seq_num]:04d}{ext}')
"""

"""Do not put T in file name
save_kwargs['string'] = (''
                         '{base_folder}/{folder_prefix}/'
                         '{analysis_stage}/'
                         '{human_timestamp}_'
                         '[temp_{raw_event[data][cryostat_T]:1.2f}'
                         '{raw_descriptor[data_keys][cryostat_T][units]}]_'
                         '[dx_{raw_event[data][diff_x]:1.3f}'
                         '{raw_descriptor[data_keys][diff_x][units]}]_'
                         '[dy_{raw_event[data][diff_y]:1.3f}'
                         '{raw_descriptor[data_keys][diff_y][units]}]_'
                         '[z_{raw_event[data][Det_1_Z]:1.3f}'
                         '{raw_descriptor[data_keys][Det_1_Z][units]}]_'
                         '[gx_{raw_event[data][spinner_goniohead_X]:1.3f}'
                         '{raw_descriptor[data_keys][spinner_goniohead_X][units]}]_'
                         '{raw_start[uid]:.6}_'
                         '{raw_event[seq_num]:04d}{ext}')
"""
"""'
cryostat1.T.kind = 'hinted'                                                                           

In [94]: cryostat1.T.kind                                                                                      
Out[94]: <Kind.hinted: 5>

In [95]: db[-1].start  
"""
