#!/usr/bin/env python

import sys
import XenAPI
from pprint import pprint

if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(1)
    url = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]

    session = XenAPI.Session(url)
    session.xenapi.login_with_password(username,password)
    for sr_ref in session.xenapi.SR.get_all():
        if session.xenapi.SR.get_record(sr_ref).get('type') == 'nfs':
           session.xenapi.SR.get_record(sr_ref).get('name_label')
