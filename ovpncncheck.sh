#!/bin/sh


#    ovpnCNcheck -- an OpenVPN tls-verify script
#    """""""""""""""""""""""""""""""""""""""""""
#
#    This script checks if the peer is in the allowed
#    user list by checking the CN (common name) of the
#    X509 certificate against a provided text file.
#
#    For example in OpenVPN, you could use the directive
#    (as one line):
#
#    tls-verify "/usr/local/sbin/ovpnCNcheck.py
#                /etc/openvpn/userlist.txt"
#
#    This would cause the connection to be dropped unless
#    the client common name is within the userlist.txt.
#
#    Special care has been taken to ensure that this script
#    also works on openwrt systems where only busybox is
#    available 
#
#    Written by Robert Penz <robert@penz.name> under the GPL 2
#    Parts are copied from the verify-cn sample OpenVPN
#    tls-verify script.


[ $# -eq 3 ] || { echo usage: ovpnCNcheck.sh userfile certificate_depth X509_NAME_oneline ; exit 255 ; }

# $2 -> certificate_depth
if [ $2 -eq 0 ] ; then
        # $3 -> X509_NAME_oneline
        # $1 -> cn we are looking for
        grep -q "^`expr match "$3" ".*/CN=\([^/][^/]*\)"`$" "$1" && exit 0
        exit 1
fi

exit 0
