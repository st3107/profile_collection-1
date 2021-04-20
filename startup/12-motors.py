from ophyd import (Device, Component as Cpt,
                   EpicsSignal, EpicsSignalRO, EpicsMotor)

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

# Spinner Goniohead motors, add by HZ
Spinnergo_X = EpicsMotor('XF:28ID1B-ES{Stg:Smpl-Ax:X}Mtr', name='Spinnergo_X', labels=['positioners'])
Spinnergo_Y = EpicsMotor('XF:28ID1B-ES{Stg:Smpl-Ax:Y}Mtr', name='Spinnergo_Y', labels=['positioners'])
Spinnergo_Z = EpicsMotor('XF:28ID1B-ES{Stg:Smpl-Ax:Z}Mtr', name='Spinnergo_Z', labels=['positioners'])
Spinnergo_Ry = EpicsMotor('XF:28ID1B-ES{Stg:Smpl-Ax:Ry}Mtr', name='Spinnergo_Ry', labels=['positioners'])

Tomo_spinner = EpicsMotor('XF:28ID1B-ES{Smpl:Chngr-Ax:YRot}Mtr', name='Tomo_spinner', labels=['positiioners'])


#ECS diffractometer Added by MA
ECS_Sam_tth = EpicsMotor('XF:28ID1B-ES{ECS-Ax:2Th1}Mtr', name='ECS_Sam_tth', labels=['positioners'])
ECS_An_tth = EpicsMotor('XF:28ID1B-ES{ECS-Ax:2Th2}Mtr', name='ECS_An_tth', labels=['positioners'])

#detector for ECS - DO and MA
ECS_det1 = EpicsSignalRO(  'XF:28IDC-BI:1{IM:1}:C4_1' ,name='ECS_det1')

## Huber Stack
mStackY = EpicsMotor('XF:28IDD-ES:2{Stg:Stack-Ax:Yfine}Mtr', name='mStackY')
mStackX = EpicsMotor('XF:28IDD-ES:2{Stg:Stack-Ax:Xfine}Mtr', name='mStackX')
mStackZ = EpicsMotor('XF:28IDD-ES:2{Stg:Stack-Ax:Z}Mtr', name='mStackZ')
mRoll = EpicsMotor('XF:28IDD-ES:2{Stg:Stack-Ax:Roll}Mtr', name='mRoll')
mPitch = EpicsMotor('XF:28IDD-ES:2{Stg:Stack-Ax:Pitch}Mtr', name='mPitch')
mPhi = EpicsMotor('XF:28IDD-ES:2{Stg:Stack-Ax:Phi}Mtr', name='mPhi')
mYBase = EpicsMotor('XF:28IDD-ES:2{Stg:Stack-Ax:Y}Mtr', name='mYBase')
mXBase = EpicsMotor('XF:28IDD-ES:2{Stg:Stack-Ax:Xbase}Mtr', name='mXBase')

# Dexela
mDexelaPhi = EpicsMotor('XF:28IDD-ES:2{Stg:Stack-Ax:Htth}Mtr', name='mDexelaPhi')

# Questar X
mQuestarX = EpicsMotor('XF:28IDD-ES:2{Cam:Mnt-Ax:X}Mtr', name='mQuestarX')

# Hexapods Z
mHexapodsZ = EpicsMotor('XF:28IDD-ES:2{Det:Dexela-Ax:Z}Mtr', name='mHexapodsZ')

# Beamstops
mBeamStopY = EpicsMotor('XF:28IDD-ES:2{BS-Ax:X}Mtr', name='mBeamStopY')

# Slits
mSlitsYGap = EpicsMotor('XF:28IDD-ES:2{Slt-Ax:YGap}Mtr', name='mSlitsYGap')
mSlitsYCtr = EpicsMotor('XF:28IDD-ES:2{Slt-Ax:YCtr}Mtr', name='mSlitsYGap')
mSlitsXGap = EpicsMotor('XF:28IDD-ES:2{Slt-Ax:XGap}Mtr', name='mSlitsXGap')
mSlitsXCtr = EpicsMotor('XF:28IDD-ES:2{Slt-Ax:XCtr}Mtr', name='mSlitsXGap')
mSlitsTop = EpicsMotor('XF:28IDD-ES:2{Slt-Ax:T}Mtr', name='mSlitsTop')
mSlitsBottom = EpicsMotor('XF:28IDD-ES:2{Slt-Ax:B}Mtr', name='mSlitsBottom')
mSlitsOutboard = EpicsMotor('XF:28IDD-ES:2{Slt-Ax:O}Mtr', name='mSlitsOutboard')
mSlitsInboard = EpicsMotor('XF:28IDD-ES:2{Slt-Ax:I}Mtr', name='mSlitsInboard')

# Smartpod
sSmartPodUnit = EpicsSignal('XF:28IDD-ES:2{SPod:1}Unit-SP', name='sSmartPodUnit')
sSmartPodTrasX = EpicsSignal('XF:28IDD-ES:2{SPod:1-Ax:1}Pos-SP', name='sSmartPodTrasX')
sSmartPodTrasY = EpicsSignal('XF:28IDD-ES:2{SPod:1-Ax:2}Pos-SP', name='sSmartPodTrasY')
sSmartPodTrasZ = EpicsSignal('XF:28IDD-ES:2{SPod:1-Ax:3}Pos-SP', name='sSmartPodTrasZ')
sSmartPodRotX = EpicsSignal('XF:28IDD-ES:2{SPod:1-Ax:1}Rot-SP', name='sSmartPodRotX')
sSmartPodRotY = EpicsSignal('XF:28IDD-ES:2{SPod:1-Ax:2}Rot-SP', name='sSmartPodRotY')
sSmartPodRotZ = EpicsSignal('XF:28IDD-ES:2{SPod:1-Ax:3}Rot-SP', name='sSmartPodRotZ')
sSmartPodSync = EpicsSignal('XF:28IDD-ES:2{SPod:1}Sync-Cmd', name='sSmartPodSync')
sSmartPodMove = EpicsSignal('XF:28IDD-ES:2{SPod:1}Move-Cmd', name='sSmartPodMove')

# Sigray
mSigrayX = EpicsMotor('XF:28IDD-ES:2{Stg:Sigray-Ax:X}Mtr', name='mSigrayX')
mSigrayY = EpicsMotor('XF:28IDD-ES:2{Stg:Sigray-Ax:Y}Mtr', name='mSigrayY')
mSigrayZ = EpicsMotor('XF:28IDD-ES:2{Stg:Sigray-Ax:Z}Mtr', name='mSigrayZ')
mSigrayPitch = EpicsMotor('XF:28IDD-ES:2{Stg:Sigray-Ax:Pitch}Mtr', name='mSigrayPitch')
mSigrayYaw = EpicsMotor('XF:28IDD-ES:2{Stg:Sigray-Ax:Yaw}Mtr', name='mSigrayYaw')

FastShutter = EpicsMotor('XF:28IDC-ES:1{Sh2:Exp-Ax:5}Mtr', name='shctl1')

pdu1 = EpicsSignal('XF:28IDD-CT{PDU:1}Sw:1-Sel', name='pdu1')
pdu2 = EpicsSignal('XF:28IDD-CT{PDU:1}Sw:2-Sel', name='pdu2')
pdu3 = EpicsSignal('XF:28IDD-CT{PDU:1}Sw:3-Sel', name='pdu3')
pdu4 = EpicsSignal('XF:28IDD-CT{PDU:1}Sw:4-Sel', name='pdu4')

