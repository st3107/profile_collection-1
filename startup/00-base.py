# Make ophyd listen to pyepics.
import nslsii
import time
from bluesky.utils import ts_msg_hook

# See docstring for nslsii.configure_base() for more details
# this command takes away much of the boilerplate for settting up a profile
# (such as setting up best effort callbacks etc)
nslsii.configure_base(get_ipython().user_ns, 'pdf', pbar=True, bec=True,
                      magics=True, mpl=True)

# disable plotting for now
# bec.disable_plots()
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

# RE.msg_hook = ts_msg_hook

RE.md['facility'] = 'NSLS-II'
RE.md['group'] = 'PDF'
RE.md['beamline_id'] = '28-ID-1'
RE.md['cycle'] = '2018-1'

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

# get_user_info()

from bluesky.magics import BlueskyMagics
from ophyd import EpicsSignal, EpicsSignalRO


def which_pvs(cls=None):
    ''' returns list of all existing pv's.
        cls : class, optional
            the class of PV's to search for
            defaults to [Device, Signal]
    '''
    if cls is None:
        cls = [Device, Signal]
    user_ns = get_ipython().user_ns

    obj_list = list()
    for key, obj in user_ns.items():
        # ignore objects beginning with "_"
        # (mainly for ipython stored objs from command line
        # return of commands)
        # also check its a subclass of desired classes
        if not key.startswith("_") and isinstance(obj, tuple(cls)):
            obj_list.append((key, obj))

    return obj_list


def print_all_pvs():
    cols = ["Python name", "Ophyd Name"]
    print("{:20s} \t {:20s}".format(*cols))
    print("="*40)
    obj_list = which_pvs()
    for name, obj in obj_list:
        print("{:20s} \t {:20s}".format(name, obj.name))
        try:
            if not isinstance(obj, EpicsMotor):
                for comp in obj.component_names:
                    print("    {}".format(comp))
        except AttributeError:
            pass


def print_all_pv_values():
    cols = ["Python name", "Time stamp", "Value"]
    print("{:40s} \t {:20s} \t\t\t {:20s}".format(*cols))
    print("="*120)
    obj_list = which_pvs()
    for name, obj in obj_list:
        try:
            ret = obj.read()
        except AttributeError:
            pass

        for key, val in ret.items():
            print("{:40s} \t {:20s} \t {}".format(key, time.ctime(val['timestamp']), val['value']))
