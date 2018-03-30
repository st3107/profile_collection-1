from bluesky.callbacks import CallbackBase

import os
import os.path

import yaml

import threading


class SoftLinkCallBack(CallbackBase):
    ''' Create data soft links.

        This callback creates softlinks of your data.
    '''
    def __init__(self, db, data_keys, data_info_keys, root='/SHARE/user_data'):
        '''
            db : the database to read from
            data_keys : data keys to create soft links for
            data_info_keys : data that you want to save into filename
        '''
        self.db = db
        self.start_uid = None
        self.start_doc = None
        self.descriptors = dict()
        self.data_keys = data_keys
        self.data_info_keys = data_info_keys
        self.root = root


    def start(self, doc):
        self.start_doc = doc 
        self.start_uid = doc['uid']

    def descriptor(self, doc):
        self.descriptors[doc['uid']] = dict(doc)

    def event(self, doc):
        data_dict = doc['data'] 
        descriptor_uid = doc['descriptor']

        stream_name = self.descriptors[descriptor_uid]['name']
        
        print("Got name : {}".format(stream_name))
        print("data dict : {}".format(data_dict))
        for data_key in self.data_keys:
            print("looking for {}".format(data_key))
            if data_key in data_dict:
                datum_id = data_dict[data_key]
                file_list = get_file_list(datum_id, db)
                for filepath in file_list:
                    root = self.root
                    PI = str(self.start_doc.get('Proposal ID', "None"))
                    data_dirname = root + "/" + PI
                    suffix = filepath.split(".")[-1]
                    sample_name = str(self.start_doc.get("sample_name", "NoSample"))
                    wavelength = str(self.start_doc.get("wavelength", "NoWavelength"))
                    out_filename = sample_name + "_" + wavelength
                    for key in self.data_info_keys:
                        out_filename = out_filename + "{}=".format(key)+str(data_dict.get(key, "No{}".format(key)))
                    out_filename = out_filename + "_" + stream_name
                    out_filepath = data_dirname + "/" + out_filename
                    os.makedirs(data_dirname, exist_ok=True)
                    dst = out_filepath + "." + suffix
                    dst_md = out_filepath + ".txt"
                    src = filepath
                    # checking file existence
                    if os.path.isfile(dst):
                        num = 0
                        collision = True
                        while(collision):
                            new_dst = out_filepath + "." + str(num) + "." + suffix
                            new_dst_md = out_filepath + "." + str(num) + ".txt"
                            collision = os.path.isfile(new_dst)
                            print("softlinkcallback : collision with {}".format(dst))
                            print("Trying new file: {}".format(new_dst))
                            num += 1 
                        dst = new_dst
                        dst_md = new_dst_md
                    print("soft linking {} to {}".format(src, dst))
                    print("Writing metadata to {}".format(dst_md))
                    os.symlink(src, dst)
                    yaml.dump(self.start_doc, open(dst_md, "w"), default_flow_style=False)
                    
                    

                    


    def stop(self, doc):
        ''' clear the start data.'''
        self.start_uid = None
        self.start_doc = None
        self.descriptors = dict()


def get_handler(datum_id, db):
    '''
        Get a file handler from the database.

        datum_id : the datum uid (from db.table() usually...)
        db : the databroker instance (db = Broker.named("pdf") for example)

    '''
    resource = db.reg.resource_given_datum_id(datum_id)
    datums = list(db.reg.datum_gen_given_resource(resource))
    handler = db.reg.get_spec_handler(resource['uid'])
    return handler
    
def get_file_list(datum_id, db):
    resource = db.reg.resource_given_datum_id(datum_id)
    datums = db.reg.datum_gen_given_resource(resource)
    handler = db.reg.get_spec_handler(resource['uid'])
    datum_kwarg_list = [datum['datum_kwargs'] for datum in datums if datum['datum_id'] == datum_id]

    return handler.get_file_list(datum_kwarg_list)




# this call back will create soft links for PE
data_keys = [pe1.image.name]
data_info_keys = [Det_1_Z.name]

soft_link_callback = SoftLinkCallBack(db, data_keys, data_info_keys, root='/SHARE/user_data')

RE.subscribe(soft_link_callback)
