"""Plan to run a XRD map "fly-scan" over a large sample."""
import uuid

import numpy as np
import itertools
import bluesky.preprocessors as bpp
import bluesky.plan_stubs as bps
from ophyd import Signal


def _extarct_motor_pos(mtr):
    ret = yield from bps.read(mtr)
    if ret is None:
        return None
    return next(
        itertools.chain(
            (ret[k]["value"] for k in mtr.hints.get("fields", [])),
            (v["value"] for v in ret.values()),
        )
    )


def xrd_map(
    dets,
    fly_motor,
    fly_start,
    fly_stop,
    fly_pixels,
    step_motor,
    step_start,
    step_stop,
    step_pixels,
    dwell_time,
    *,
    dark_plan=None,
    md=None,
    backoff=0,
    snake=True,
):
    """
    Collect a 2D XRD map by "flying" in one direction.



    Parameters
    ----------
    dets : List[OphydObj]

    fly_motor : Movable
       The motor that will be moved continuously during collection
       (aka "flown")

    fly_start, fly_stop : float
       The start and stop position of the "fly" direction

    fly_pixels : int
       The target number of pixels in the "fly" direction

    step_motor : Movable
       The "slow" axis

    step_start, stop_stop : float
       The first and last position for the slow direction

    step_pixels : int
       How many pixels in the slow direction

    dwell_time : float
       How long in s to dwell in each pixel.  combined with *fly_pixels*
       this will be used to compute the motor velocity

    dark_plan : Plan or None
       If not None, will be passed the detector list at the end of every
       fast pass to inject logic to collect dark frames.

    md : Optional[Dict[str, Any]]
       User-supplied meta-data

    backoff : float
       How far to move beyond the fly dimensions to get up to speed

    snake : bool
       If we should "snake" or "typewriter" the fly axis

    """
    plan_args_cache = {
        k: v
        for k, v in locals().items()
        if k not in ("dets", "fly_motor", "step_motor")
    }

    # TODO input validation

    # round dwell time to nearest 10th of a second
    dwell_time = np.round(dwell_time, 1)

    # set up metadata
    _md = {}
    _md = {
        "detectors": [det.name for det in dets],
        "plan_args": plan_args_cache,
        "map_size": (fly_pixels, step_pixels),
        "hints": {},
    }
    _md["hints"].setdefault(
        "dimensions", [((fly_motor.name,), "primary"), ((step_motor.name,), "primary")]
    )
    _md.update(md or {})
    # soft signal to use for tracking pixel edges
    # TODO put better metadata on these
    px_start = Signal(name=f"start_{fly_motor.name}")
    px_stop = Signal(name=f"stop_{fly_motor.name}")

    # TODO either think more carefully about how to compute this
    # or get the gating working below.
    speed = abs(fly_stop - fly_start) / (fly_pixels * dwell_time)

    @bpp.set_run_key_decorator(f"xrd_map_{uuid.uuid4()}")
    @bpp.stage_decorator(dets)
    @bpp.run_decorator(md=_md)
    def inner():
        _fly_start, _fly_stop = fly_start, fly_stop
        _backoff = backoff

        for step in np.linspace(step_start, step_stop, step_pixels):
            # TODO maybe go to a "move velocity here?
            yield from bps.abs_set(step_motor, step, group="pre_fly")
            yield from bps.abs_set(fly_motor, _fly_start - _backoff, group="pre_fly")

            # take the dark while we might be waiting for motor movement
            if dark_plan:
                yield from dark_plan(dets)

            # wait for the pre-fly motion to stop
            yield from bps.wait(group="pre_fly")

            yield from bps.abs_set(fly_motor, _fly_stop + _backoff, group="fly")
            # TODO gate starting to take data on motor position
            for j in range(fly_pixels):
                for d in dets:
                    yield from bps.trigger(d, group="fly_pixel")
                # grab motor position right after we trigger
                start_pos = yield from _extarct_motor_pos(fly_motor)
                yield from bps.mv(px_start, start_pos)
                # wait for frame to finish
                yield from bps.wait(group="fly_pixel")
                # grab the motor position
                stop_pos = yield from _extarct_motor_pos(fly_motor)
                yield from bps.mv(px_stop, stop_pos)
                # generate the event
                yield from bps.create("primary")
                for obj in dets + [px_start, px_stop, step_motor]:
                    yield from bps.read(obj)
                yield from bps.save()

            if snake:
                # if snaking, flip these for the next pass through
                _fly_start, _fly_stop = _fly_stop, _fly_start
                _backoff = -_backoff

    yield from bps.configure(fly_motor, {"velocity": speed})
    yield from inner()
