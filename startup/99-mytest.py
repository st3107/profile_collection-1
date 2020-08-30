import logging
logger = logging.getLogger()#('ophyd')
with open("/tmp/this_junk2.txt",'w') as file:
    file.write(repr(logger.handlers))
