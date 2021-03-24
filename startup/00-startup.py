###############################################################################
# TODO: remove this block once https://github.com/bluesky/ophyd/pull/959 is
# merged/released.
from datetime import datetime
from ophyd.signal import EpicsSignalBase, EpicsSignal, DEFAULT_CONNECTION_TIMEOUT

def print_now():
    return datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S.%f')

def wait_for_connection_base(self, timeout=DEFAULT_CONNECTION_TIMEOUT):
    '''Wait for the underlying signals to initialize or connect'''
    if timeout is DEFAULT_CONNECTION_TIMEOUT:
        timeout = self.connection_timeout
    # print(f'{print_now()}: waiting for {self.name} to connect within {timeout:.4f} s...')
    start = time.time()
    try:
        self._ensure_connected(self._read_pv, timeout=timeout)
        # print(f'{print_now()}: waited for {self.name} to connect for {time.time() - start:.4f} s.')
    except TimeoutError:
        if self._destroyed:
            raise DestroyedError('Signal has been destroyed')
        raise

def wait_for_connection(self, timeout=DEFAULT_CONNECTION_TIMEOUT):
    '''Wait for the underlying signals to initialize or connect'''
    if timeout is DEFAULT_CONNECTION_TIMEOUT:
        timeout = self.connection_timeout
    # print(f'{print_now()}: waiting for {self.name} to connect within {timeout:.4f} s...')
    start = time.time()
    self._ensure_connected(self._read_pv, self._write_pv, timeout=timeout)
    # print(f'{print_now()}: waited for {self.name} to connect for {time.time() - start:.4f} s.')

EpicsSignalBase.wait_for_connection = wait_for_connection_base
EpicsSignal.wait_for_connection = wait_for_connection
###############################################################################

from ophyd.signal import EpicsSignalBase
# EpicsSignalBase.set_default_timeout(timeout=10, connection_timeout=10)  # old style
EpicsSignalBase.set_defaults(timeout=10, connection_timeout=10)  # new style

# Make ophyd listen to pyepics.
import nslsii

# See docstring for nslsii.configure_base() for more details
# this command takes away much of the boilerplate for settting up a profile
# (such as setting up best effort callbacks etc)
nslsii.configure_base(get_ipython().user_ns, 'xpdd', pbar=True, bec=True,
                      magics=True, mpl=True, epics_context=False)

# IMPORTANT : This is needed to read old data
# db.reg.set_root_map({'/direct/XF28ID1':'/direct/XF28ID2'})

# At the end of every run, verify that files were saved and
# print a confirmation message.
from bluesky.callbacks.broker import verify_files_saved, post_run
# RE.subscribe(post_run(verify_files_saved, db), 'stop')

# Uncomment the following lines to turn on verbose messages for
# debugging.
# import logging
# ophyd.logger.setLevel(logging.DEBUG)
# logging.basicConfig(level=logging.DEBUG)


RE.md['facility'] = 'NSLS-II'
RE.md['group'] = 'XPD'
RE.md['beamline_id'] = '28-ID-D'

import subprocess


def show_env():
    # this is not guaranteed to work as you can start IPython without hacking
    # the path via activate
    proc = subprocess.Popen(["conda", "list"], stdout=subprocess.PIPE)
    out, err = proc.communicate()
    a = out.decode('utf-8')
    b = a.split('\n')
    print(b[0].split('/')[-1][:-1])
