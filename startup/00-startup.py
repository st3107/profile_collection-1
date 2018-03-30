# Make ophyd listen to pyepics.
import nslsii

# See docstring for nslsii.configure_base() for more details
# this command takes away much of the boilerplate for settting up a profile
# (such as setting up best effort callbacks etc)
nslsii.configure_base(get_ipython().user_ns, 'pdf', pbar=True, bec=True,
                      magics=True, mpl=True, epics_context=True)

# disable plotting for now
bec.disable_plots()
# Optional: set any metadata that rarely changes.
# RE.md['beamline_id'] = 'YOUR_BEAMLINE_HERE'


# At the end of every run, verify that files were saved and
# print a confirmation message.
#from bluesky.callbacks.broker import verify_files_saved, post_run
# RE.subscribe(post_run(verify_files_saved, db), 'stop')

# Uncomment the following lines to turn on verbose messages for
# debugging.
# import logging
# ophyd.logger.setLevel(logging.DEBUG)
# logging.basicConfig(level=logging.DEBUG)


RE.md['facility'] = 'NSLS-II'
RE.md['group'] = 'PDF'
RE.md['beamline_id'] = '28-ID-1'

def get_user_info():
    ''' This function prompts the user for basic info and 
        adds it to RE.md.

        All data in RE.md gets saved in each start document for each run.

    '''

    print("Please enter the following information for your scan")

    PI_name = input("Enter PI Name: ")
    prop_ID = input("Enter Proposal ID: ")
    wavelength = input("Enter wavelength: ")
    
    RE.md['PI Name'] = PI_name
    RE.md['Proposal ID'] = prop_ID
    RE.md['wavelength'] = wavelength
