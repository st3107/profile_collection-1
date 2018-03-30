# main plans

def acquisition_plan(dets, motors, fs, sample_name, images_per_set=None):
    '''
        This is testing a simple acquisition plan.
        Here we open shutter, take an image, close shutter, take a dark then
            stop.
        dets : dets to read from
        motors: motors to take readings from
            (for later use)
        fs : the fast shutter
        sample_name : the sample name
    '''
    def myplan():
        for det in dets:
            if images_per_set is not None:
                yield from bps.abs_set(det.images_per_set, images_per_set)

        # open fast shutter
        yield from bps.abs_set(fs,1)
        # for the motors, trigger() won't be called since it doesn't exist
        yield from trigger_and_read(dets + motors, name='primary')
        # close fast shutter, now take a dark
        yield from bps.abs_set(fs,0)
        yield from trigger_and_read(dets + motors, name='dark')

        
    yield from bpp.run_wrapper(bpp.stage_wrapper(myplan(), dets),md=dict(sample_name=sample_name))
    
