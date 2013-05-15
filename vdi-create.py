#!/usr/bin/env python

import sys
import XenAPI
from pprint import pprint
import inspect

if __name__ == "__main__":
    url = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]

    session = XenAPI.Session(url)
    session.xenapi.login_with_password(username,password)
    for sr_ref in session.xenapi.SR.get_all():
        if ( session.xenapi.SR.get_record(sr_ref).get('type') == 'nfs' and
           session.xenapi.SR.get_record(sr_ref).get('uuid') == 'a20e4bcc-1d90-5d13-4669-ea80ec2cf287' ):
           pprint(session.xenapi.SR.get_record(sr_ref).get('name_label'))
           vdi_spec = {
               'name_label': 'test_vdi',
               'name_description': 'test_vdi',
               'SR': sr_ref,
               'virtual_size': '2048',
               'type': 'user',
               'sharable': False,
               'read_only': False,
               'other_config': dict()
           }
           session.xenapi.VDI.create(vdi_spec)
