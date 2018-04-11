import ophyd
from ophyd import (Device, Component as Cpt,
                   EpicsSignal, EpicsSignalRO, EpicsMotor)

Det_1_X = EpicsMotor('XF:28ID1B-ES{Det:1-Ax:X}Mtr', name='Det_1_X')
Det_1_Y = EpicsMotor('XF:28ID1B-ES{Det:1-Ax:Y}Mtr', name='Det_1_Y')
Det_1_Z = EpicsMotor('XF:28ID1B-ES{Det:1-Ax:Z}Mtr', name='Det_1_Z')

Det_2_X = EpicsMotor('XF:28ID1B-ES{Det:2-Ax:X}Mtr', name='Det_2_X')
Det_2_Y = EpicsMotor('XF:28ID1B-ES{Det:2-Ax:Y}Mtr', name='Det_2_Y')
Det_2_Z = EpicsMotor('XF:28ID1B-ES{Det:2-Ax:Z}Mtr', name='Det_2_Z')

Grid_X = EpicsMotor('XF:28ID1B-ES{Env:1-Ax:X}Mtr', name='Grid_X')
Grid_Y = EpicsMotor('XF:28ID1B-ES{Env:1-Ax:Y}Mtr', name='Grid_Y')
Grid_Z = EpicsMotor('XF:28ID1B-ES{Env:1-Ax:Z}Mtr', name='Grid_Z')

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

