#!/usr/bin/env python

'''
    ovpnCNcheck -- an OpenVPN tls-verify script
    """""""""""""""""""""""""""""""""""""""""""
    
    This script checks if the peer is in the allowed
    user list by checking the CN (common name) of the 
    X509 certificate against a provided text file.
    
    For example in OpenVPN, you could use the directive
    (as one line):
    
    tls-verify "/usr/local/sbin/ovpnCNcheck.py
                /etc/openvpn/userlist.txt"

    This would cause the connection to be dropped unless
    the client common name is within the userlist.txt.
    Every line should hold one regular expression which
    can also be just one common name (don't forget to escape
    stuff like .?^()[]\ with a \).
    Empty or lines which start with a # are ignored.
    
    Written by Robert Penz <robert@penz.name> under the GPL 2
    Parts are copied from the verify-cn sample OpenVPN
    tls-verify script.
'''

# Version 0.1
# Initial Release


import sys
import re


def matchCommonName(userListFile, cn):
    """ reads the user list file and tries to match every regex """
    for rawLine in open(userListFile,"r").readlines():
        line = rawLine.strip().rstrip("\n")
        if not line or line[0] == "#":
            continue
        
        if re.compile(line).match(cn):
            return True
    return False

def main():
    # we only work with 3 parameters
    if len(sys.argv) != 4:
        print __doc__
        sys.exit(-1)

    # Parse out arguments:
    # userListFile -- Path of the file with the allowed users
    #                 taken from the argument to the tls-verify directive
    #                 in the OpenVPN config file.
    # depth        -- The current certificate chain depth.  In a typical
    #                 bi-level chain, the root certificate will be at level
    #                 1 and the client certificate will be at level 0.
    #                 This script will be called separately for each level.
    # x509         -- the X509 subject string as extracted by OpenVPN from
    #                 the client's provided certificate.
    (userListFile, depth, x509) = sys.argv[1:]

    if depth == "0":
        # If depth is zero, we know that this is the final
        # certificate in the chain (i.e. the client certificate),
        # and the one we are interested in examining.
        # If so, parse out the common name substring in
        # the X509 subject string.

        found = re.compile(r"/CN=(?P<cn>[^/]+)").search(x509)
        if found:
            # Accept the connection if the X509 common name
            # string matches a regex
            if matchCommonName(userListFile, found.group("cn")):
                sys.exit(0)
            
	# Authentication failed -- Either we could not parse
        # the X509 subject string, or the common name in the
        # subject string didn't match the user list regexes
        sys.exit(1)

    # If depth is nonzero, tell OpenVPN to continue processing
    # the certificate chain.
    sys.exit(0)

if __name__ == '__main__':
    main()

