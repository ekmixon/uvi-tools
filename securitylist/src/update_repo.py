#!/usr/bin/env python

import securitylist
import sys
import os
import json

def main():

    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} output_dir input_dir namespace")
        print()
        sys.exit(1)

    namespace = sys.argv[3]
    dwf_path = sys.argv[2]
    data_path = sys.argv[1]
    securitylist.CVE.path = data_path

    dwf_files = []

    for root,d_names,f_names in os.walk(dwf_path):

        if '.git' in root:
            continue

        dwf_files.extend(os.path.join(root, i) for i in f_names if 'CVE-' in i)
    # We need to find a way to only pull in updates

    for f in dwf_files:
        with open(f) as fh:
            dwf_data = json.load(fh)

            the_id = dwf_data['CVE_data_meta']['ID']
            # We need to put these in the NVD namespace
            c = securitylist.CVE(the_id)
            c.add_data(namespace, dwf_data)
            if c.write():
                print(f)

if __name__ == "__main__":
    main()
