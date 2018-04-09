
'''
TODO :
    1. finish adding all motor PV's
    2. Add the prosilica detectors
    3. implement the two_distance_plan
    4. Verify filenames make sense
    5. Implement a grid scan (and retrieve data)
        (on monochromator pitch/yaw)
        count on what?

    Later:
    6. add temperature sensor
'''
def two_distance_plan(dets, motor, fs, sample_name, distances, images_per_set=None):
    '''
        This is testing a simple acquisition plan.
        Here we open shutter, take an image, close shutter, take a dark then
            stop.
        dets : dets to read from
        motor: the motor to move
            (for later use)
        fs : the fast shutter
        sample_name : the sample name
	distances : list
	    a list of distances desired
    '''
    def myplan():
        
        # set the number of images per set here
        # (only do this once)
        for det in dets:
            if images_per_set is not None:
                yield from bps.mov(det.images_per_set, images_per_set)

        # iterate over the distances for the motor "motor"
        for distance in distances:
            # move the motor to distance
            yield from bps.mov(motor, distance)
    
            # stage the detectors
            for det in dets:
                yield from bps.stage(det)
    
            # this is due to some strange race condition/bug
            # sleep to ensure that the detector is ready for acquisition
            yield from bps.sleep(1)

            # close fast shutter, now take a dark
            yield from bps.mov(fs,0)
            yield from trigger_and_read(dets + [motor], name='dark')
            # open fast shutter
            yield from bps.mov(fs,1)
            # for the motors, trigger() won't be called since it doesn't exist
            yield from trigger_and_read(dets + [motor], name='primary')
            for det in dets:
                yield from bps.unstage(det)

        
    yield from bpp.run_wrapper(myplan(), md=dict(sample_name=sample_name))
