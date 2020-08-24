"Define Beamline Modes"
def high_resolution():
	print("Resetting white beam slits")
	wb_slits.inboard.move(-9.6)
	wb_slits.outboard.move(-3.542180)
	
	print("Resetting Monochromator")
	sbm.yaw.move(0.0)
	sbm.roll.move(0.0)
	sbm.pitch.move(-0.05799)
	sbm.bend.move(1950)
	sbm.twist.move(-30)

	print("Resetting Mirror")
	Mirror_VFM.y_upstream.move(-0.7)
	Mirror_VFM.y_downstream_inboard.move(-0.0202)
	Mirror_VFM.y_downstream_outboard.move(0.3199)
	Mirror_VFM.bend_upstream.move(60)
	Mirror_VFM.bend_downstream.move(60)

	print("Resetting BDM Slits")
	#bdm_slits.top.move(999.957)
	#bdm_slits.bottom.move(-94363.970)
	#bdm_slits.inboard.move(-7600.960)
	#bdm_slits.outboard.move(-4100.075)

	print("Resetting OCM Slits")
	ocm_slits.top.move(-1065)
	ocm_slits.bottom.move(1955.0)
	ocm_slits.outboard.move(435.959)
	ocm_slits.inboard.move(-294.037)
	OCM_table.upstream_jack.move(4.14225)
	OCM_table.downstream_jack.move(-4.1700)
	OCM_table.X.move(-8.44701)
	print("Ready to go !")

def high_flux1():
	print("Resetting white beam slits")
	wb_slits.inboard.move(-14.05)
	wb_slits.outboard.move(-7.125)
	
	print("Resetting Monochromator")
	sbm.yaw.move(0.0)
	sbm.roll.move(0.0)
	sbm.pitch.move(-0.06569)
	sbm.bend.move(2509)
	sbm.twist.move(0)

	print("Resetting Mirror")
	Mirror_VFM.y_upstream.move(-0.7)
	Mirror_VFM.y_downstream_inboard.move(-0.0202)
	Mirror_VFM.y_downstream_outboard.move(0.3199)
	Mirror_VFM.bend_upstream.move(60)
	Mirror_VFM.bend_downstream.move(60)

	print("Resetting BDM Slits")
	#bdm_slits.top.move(999.957)
	#bdm_slits.bottom.move(-94363.970)
	#bdm_slits.inboard.move(-7600.960)
	#bdm_slits.outboard.move(-4100.075)

	print("Resetting OCM Slits")
	ocm_slits.top.move(-1995)
	ocm_slits.bottom.move(2005.0)
	ocm_slits.outboard.move(250.959)
	ocm_slits.inboard.move(50.963)
	OCM_table.upstream_jack.move(4.14225)
	OCM_table.downstream_jack.move(-4.1700)
	OCM_table.X.move(-8.44701)
	print("Ready to go !")


def high_flux2():
	print("Resetting white beam slits")
	wb_slits.inboard.move(-9.36)
	wb_slits.outboard.move(-3.473156)
	
	print("Resetting Monochromator")
	sbm.yaw.move(0.0)
	sbm.roll.move(0.0)
	sbm.pitch.move(-0.07719)
	sbm.bend.move(3000)
	sbm.twist.move(0.0000)

	print("Resetting Mirror")
	Mirror_VFM.y_upstream.move(-0.7)
	Mirror_VFM.y_downstream_inboard.move(-0.02)
	Mirror_VFM.y_downstream_outboard.move(0.32)
	Mirror_VFM.bend_upstream.move(65)
	Mirror_VFM.bend_downstream.move(65)

	print("Resetting BDM Slits")
	#bdm_slits.top.move(999.957)
	#bdm_slits.bottom.move(-94363.970)
	#bdm_slits.inboard.move(-7600.960)
	#bdm_slits.outboard.move(-4100.075)

	print("Resetting OCM Slits")
	ocm_slits.top.move(-2215.0)
	ocm_slits.bottom.move(2295.0)
	ocm_slits.outboard.move(380.959)
	ocm_slits.inboard.move(-49.037)
	OCM_table.upstream_jack.move(4.14225)
	OCM_table.downstream_jack.move(-4.1700)
	OCM_table.X.move(-8.44701)
	print("Ready to go !")

def saxs():
	print("Resetting white beam slits")
	wb_slits.inboard.move(-13.6)
	wb_slits.outboard.move(-7.54218)
	
	print("Resetting Monochromator")
	sbm.yaw.move(0.0)
	sbm.roll.move(0.0)
	sbm.pitch.move(-0.05149)
	sbm.bend.move(1550)
	sbm.twist.move(-30)

	print("Resetting Mirror")
	Mirror_VFM.y_upstream.move(-0.7)
	Mirror_VFM.y_downstream_inboard.move(-0.02)
	Mirror_VFM.y_downstream_outboard.move(0.32)
	Mirror_VFM.bend_upstream.move(10)
	Mirror_VFM.bend_downstream.move(10)

	print("Resetting BDM Slits")
	#bdm_slits.top.move(999.957)
	#bdm_slits.bottom.move(-94363.970)
	#bdm_slits.inboard.move(-7600.960)
	#bdm_slits.outboard.move(-4100.075)

	print("Resetting OCM Slits")
	ocm_slits.top.move(-1065.0)
	ocm_slits.bottom.move(1955.0)
	ocm_slits.outboard.move(635.959)
	ocm_slits.inboard.move(-94.037)
	OCM_table.upstream_jack.move(4.14225)
	OCM_table.downstream_jack.move(-4.1700)
	OCM_table.X.move(-8.44701)
	print("Ready to go !")

#test mode for 1 mm beam on mono
def test():
	print("Resetting white beam slits")
	wb_slits.inboard.move(-13.6)
	wb_slits.outboard.move(-7.62)
	
	print("Resetting Monochromator")
	sbm.yaw.move(0.0)
	sbm.roll.move(0.0)
	sbm.pitch.move(-0.06689)
	sbm.bend.move(2300)
	sbm.twist.move(0.0000)

	print("Resetting Mirror")
	Mirror_VFM.y_upstream.move(-0.7)
	Mirror_VFM.y_downstream_inboard.move(-0.02)
	Mirror_VFM.y_downstream_outboard.move(0.32)
	Mirror_VFM.bend_upstream.move(70)
	Mirror_VFM.bend_downstream.move(70)

	print("Resetting BDM Slits")
	#bdm_slits.top.move(999.957)
	#bdm_slits.bottom.move(-94363.970)
	#bdm_slits.inboard.move(-7600.960)
	#bdm_slits.outboard.move(-4100.075)

	print("Resetting OCM Slits")
	ocm_slits.top.move(-2065.0)
	ocm_slits.bottom.move(2055.0)
	ocm_slits.outboard.move(635.959)
	ocm_slits.inboard.move(-344.037)
	OCM_table.upstream_jack.move(4.14225)
	OCM_table.downstream_jack.move(-4.1700)
	OCM_table.X.move(-8.44701)
	print("Ready to go !")

def BDM_plot():
	from mpl_toolkits.mplot3d import Axes3D
	from matplotlib import pylab as pl
	from PIL import Image
	import numpy as np
	import pylab	
	
	img = Image.open('/nsls2/xf28id1/BDM_camera/BDM_ROI_000.tiff').convert('L')
	z   = np.asarray(img)
	mydata = z[375:450:1, 550:850:1]#y and x
	#mydata = z[164:300:1, 200:1000:1]
	fig = pl.figure(facecolor='w')
	ax1 = fig.add_subplot(1,2,1)
	im = ax1.imshow(mydata,interpolation='nearest',cmap=pl.cm.jet)
	ax1.set_title('2D')

	ax2 = fig.add_subplot(1,2,2,projection='3d')
	x,y = np.mgrid[:mydata.shape[0],:mydata.shape[1]]
	ax2.plot_surface(x,y,mydata,cmap=pl.cm.jet,rstride=1,cstride=1,linewidth=0.,antialiased=False)
	ax2.set_title('3D')
	#ax2.set_zlim3d(0,100)
	pl.show()

#def temp()
#	Det_1_Z.move(1674.44155)
#	Grid_X.move(32)
#	Grid_Y.move(41.75)
#	Grid_Z.move(830.39405)

 #Mirror_VFM.y_upstream.move(-2.3695)
 #Mirror_VFM.y_downstream_inboard.move(-1.5492)
 #Mirror_VFM.y_downstream_outboard.move(-1.2505)

