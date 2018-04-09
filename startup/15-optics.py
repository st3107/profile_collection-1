"Define motors related to optics"

from ophyd import EpicsMotor, Device
from ophyd import Component as Cpt


class Slits(Device):
    top = Cpt(EpicsMotor, 'T}Mtr')
    bottom = Cpt(EpicsMotor, 'B}Mtr')
    inboard = Cpt(EpicsMotor, 'I}Mtr')
    outboard = Cpt(EpicsMotor, 'O}Mtr')
    ''' TODO : Add later
    xc = Cpt(EpicsMotor, 'XCtr}Mtr')
    xg = Cpt(EpicsMotor, 'XGap}Mtr')
    yc = Cpt(EpicsMotor, 'YCtr}Mtr')
    yg = Cpt(EpicsMotor, 'YGap}Mtr')
    '''

ocm_slits = Slits('XF:28ID1B-OP{Slt:2-Ax:', name='ocm_slits')  # OCM Slits
bdm_slits = Slits('XF:28ID1A-OP{Slt:1-Ax:', name='bdm_slits')  # BD Slits

class SideBounceMono(Device):
    x_wedgemount = Cpt(EpicsMotor, "X}Mtr")
    y_wedgemount = Cpt(EpicsMotor, "Y}Mtr")
    yaw = Cpt(EpicsMotor, "Yaw}Mtr")
    pitch = Cpt(EpicsMotor, "Pitch}Mtr")
    roll = Cpt(EpicsMotor, "Roll}Mtr")
    bend = Cpt(EpicsMotor, "Bend}Mtr")
    twist = Cpt(EpicsMotor, "Twist}Mtr")

sbm = SideBounceMono("XF:28ID1A-OP{Mono:SBM-Ax:", name='sbm')
# Shutters:
fs = EpicsSignal('XF:28ID1B-OP{PSh:1-Det:2}Cmd', name='fs')  # fast shutter
