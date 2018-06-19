import ophyd
from ophyd import (Device, Component as Cpt,
                   EpicsSignal, EpicsSignalRO, EpicsMotor)
from nslsii.devices import TwoButtonShutter
#import nslsii.devices

Det_1_X = EpicsMotor('XF:28ID1B-ES{Det:1-Ax:X}Mtr', name='Det_1_X', labels=['positioners'])
Det_1_Y = EpicsMotor('XF:28ID1B-ES{Det:1-Ax:Y}Mtr', name='Det_1_Y', labels=['positioners'])
Det_1_Z = EpicsMotor('XF:28ID1B-ES{Det:1-Ax:Z}Mtr', name='Det_1_Z', labels=['positioners'])

Det_2_X = EpicsMotor('XF:28ID1B-ES{Det:2-Ax:X}Mtr', name='Det_2_X', labels=['positioners'])
Det_2_Y = EpicsMotor('XF:28ID1B-ES{Det:2-Ax:Y}Mtr', name='Det_2_Y', labels=['positioners'])
Det_2_Z = EpicsMotor('XF:28ID1B-ES{Det:2-Ax:Z}Mtr', name='Det_2_Z', labels=['positioners'])

Grid_X = EpicsMotor('XF:28ID1B-ES{Env:1-Ax:X}Mtr', name='Grid_X', labels=['positioners'])
Grid_Y = EpicsMotor('XF:28ID1B-ES{Env:1-Ax:Y}Mtr', name='Grid_Y', labels=['positioners'])
Grid_Z = EpicsMotor('XF:28ID1B-ES{Env:1-Ax:Z}Mtr', name='Grid_Z', labels=['positioners'])

# Beam stop motors
class BeamStop(Device):
    x = Cpt(EpicsMotor, 'X}Mtr')
    y = Cpt(EpicsMotor, 'Y}Mtr')

BStop1 = BeamStop('XF:28ID1B-ES{BS:1-Ax:', name='BStop1')
BStop2 = BeamStop('XF:28ID1B-ES{BS:2-Ax:', name='BStop2')

# OCM table widget
class OCMTable(Device):
    ocm_y_upstream = Cpt(EpicsMotor, 'YU}Mtr')
    ocm_y_downstream = Cpt(EpicsMotor, 'YD}Mtr')
    ocm_x_table = Cpt(EpicsMotor, 'X}Mtr')

OCM_table = OCMTable('XF:28ID1B-ES{OCM-Ax:', name='OCM_table')

ECS_tel_guide = EpicsMotor('XF:28ID1B-ES{ECS-Ax:X}Mtr', name='ECS_tel_guide')


class ECS(Device):
    laser_y = Cpt(EpicsMotor, 'Lsr:1-Ax:Y}Mtr')
    reflective_foil_x = Cpt(EpicsMotor, 'Foil:1-Ax:X}Mtr')
    filter_wheel_1_phi = Cpt(EpicsMotor, 'Fltr:Whl1-Ax:Phi}Mtr')
    filter_wheel_2_phi = Cpt(EpicsMotor, 'Fltr:Whl2-Ax:Phi}Mtr')

ECS_laser_foil_filter = ECS('XF:28ID1B-ES{', name='ECS_laser_foil_filter')


class FilterBank(Device):
    flt1 = Cpt(EpicsSignal, '1}Cmd:Opn-Cmd', string=True)
    flt2 = Cpt(EpicsSignal, '2}Cmd:Opn-Cmd', string=True)
    flt3 = Cpt(EpicsSignal, '3}Cmd:Opn-Cmd', string=True)
    flt4 = Cpt(EpicsSignal, '4}Cmd:Opn-Cmd', string=True)

class FilterBankTwoButtonShutter(Device):
    flt1 = Cpt(TwoButtonShutter, '1}')
    flt2 = Cpt(TwoButtonShutter, '2}')
    flt3 = Cpt(TwoButtonShutter, '3}')
    flt4 = Cpt(TwoButtonShutter, '4}')

fb = FilterBank('XF:28ID1B-OP{Fltr:', name='fb')
fb_two_button_shutters = FilterBankTwoButtonShutter('XF:28ID1B-OP{Fltr:', name='fb_two_button_shutters')

