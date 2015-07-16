# ovpnCNcheck
an OpenVPN tls-verify script

Source: http://robert.penz.name/21/ovpncncheck-an-openvpn-tls-verify-script/

ovpnCNcheck — an OpenVPN tls-verify script

February 2, 2008

If you’ve running an OpenVPN server you may have asked yourself how you can decide which clients can connect even if they got signed by the same CA. A common case would arises if you provide more than one OpenVPN server but not all clients should be able to connect to every one. Sure it would be possible to use a separate CA for each server but that would not be flexible. The clients would need more than one certificate/key pair and if you want to enable/disable access to a certain server for a client you need to generate/revoke the client certificate. Not a good idea!

I’ve therefore written two scripts with solve this problem. These scripts check if the peer is in the allowed user list by checking the CN (common name) of the X.509 certificate against a provided text file. For example in OpenVPN, you could use the directive:

tls-verify "/usr/local/sbin/ovpnCNcheck.py /etc/openvpn/userlist.txt"

This would cause the connection to be dropped unless the client common name is within the userlist.txt. The bash script will just check if a common name is in one of the lines (one CN per line) and the python version parses the provided regular expressions. Every line should hold one regular expression in this case which can also be just one common name (don’t forget to escape stuff like .?^()[]\ with a \). Empty lines or ones which start with a # are ignored. The bash version works also on a â€œout of the boxâ€ OpenWRT installation.

Python version: ovpncncheck.py
Bash version: ovpncncheck.sh

Hope it helps you!
