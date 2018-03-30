"Define motors related to optics"

from ophyd import EpicsMotor, Device
from ophyd import Component as Cpt


class Slits(Device):
    top = Cpt(EpicsMotor, '-Ax:T}Mtr')
    bottom = Cpt(EpicsMotor, '-Ax:B}Mtr')
    inboard = Cpt(EpicsMotor, '-Ax:I}Mtr')
    outboard = Cpt(EpicsMotor, '-Ax:O}Mtr')
    """ TODO later:
    xc = Cpt(EpicsMotor, '-Ax:XCtr}Mtr')
    xg = Cpt(EpicsMotor, '-Ax:XGap}Mtr')
    yc = Cpt(EpicsMotor, '-Ax:YCtr}Mtr')
    yg = Cpt(EpicsMotor, '-Ax:YGap}Mtr')
    """

ocm_slits = Slits('XF:28ID1B-OP{Slt:2', name='ocm_slits')  # OCM Slits
bdm_slits = Slits('XF:28ID1A-OP{Slt:1', name='bdm_slits')  # BD Slits


# Shutters:
fs = EpicsSignal('XF:28ID1B-OP{PSh:1-Det:2}Cmd', name='fs')  # fast shutter
