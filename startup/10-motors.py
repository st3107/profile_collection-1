from ophyd import EpicsMotor
import ophyd
from ophyd import EpicsSignal

Det_1_X = EpicsMotor('XF:28ID1B-ES{Det:1-Ax:X}Mtr', name='Det_1_X')
Det_1_Y = EpicsMotor('XF:28ID1B-ES{Det:1-Ax:Y}Mtr', name='Det_1_Y')
Det_1_Z = EpicsMotor('XF:28ID1B-ES{Det:1-Ax:Z}Mtr', name='Det_1_Z')

Det_2_X = EpicsMotor('XF:28ID1B-ES{Det:2-Ax:X}Mtr', name='Det_2_X')
Det_2_Y = EpicsMotor('XF:28ID1B-ES{Det:2-Ax:Y}Mtr', name='Det_2_Y')
Det_2_Z = EpicsMotor('XF:28ID1B-ES{Det:2-Ax:Z}Mtr', name='Det_2_Z')

Grid_X = EpicsMotor('XF:28ID1B-ES{Env:1-Ax:X}Mtr', name='Grid_X')
Grid_Y = EpicsMotor('XF:28ID1B-ES{Env:1-Ax:Y}Mtr', name='Grid_Y')
Grid_Z = EpicsMotor('XF:28ID1B-ES{Env:1-Ax:Z}Mtr', name='Grid_Z')

