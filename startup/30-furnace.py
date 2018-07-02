from ophyd import PVPositioner

# TODO : PV needs to be fixed for done signal
# (doesn't work on ramp down)
class LinkamFurnace(PVPositioner):
    readback = C(EpicsSignalRO, 'RAMP:LIMIT:SET.VAL')
    setpoint = C(EpicsSignal, 'RAMP:LIMIT:SET')
    done = C(EpicsSignalRO, 'STATUS')
    stop_signal = C(EpicsSignal, 'RAMP:CTRL:SET')
    temperature = C(EpicsSignal, "TEMP")

    def set(self, *args, timeout=None, **kwargs):
        
        return super().set(*args, timeout=timeout, **kwargs)

    def trigger(self):
        # There is nothing to do. Just report that we are done.
        # Note: This really should not necessary to do --
        # future changes to PVPositioner may obviate this code.
        status = DeviceStatus(self)
        status._finished()
        return status

# To allow for sample temperature equilibration time, increase
# the `settle_time` parameter (units: seconds).
linkam_furnace = LinkamFurnace('XF:28ID1-ES{LINKAM}:', name='cs700',
                                   settle_time=0)
linkam_furnace.done_value = 3
linkam_furnace.stop_value = 0
linkam_furnace.setpoint.kind = "read"
linkam_furnace.readback.kind = "read"
linkam_furnace.readback.name = 'temperature'
linkam_furnace.setpoint.name = 'temperature_setpoint'
