#!/usr/bin/python
from __future__ import print_function

import sys
import base64
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import Encoding


def parse_ca_certs(ca_str):
    ca_certs = set()

    cert = ""

    for line in ca_str.splitlines():
        cert += line + '\n'
        if '-----END CERTIFICATE-----' in line:
            ca_certs.add(x509.load_pem_x509_certificate(str.encode(cert), default_backend()))
            cert = ""

    return ca_certs


current_ca_encoded = sys.argv[1]
target_ca_encoded = sys.argv[2]

current_certs = parse_ca_certs(base64.b64decode(current_ca_encoded))
new_certs = parse_ca_certs(base64.b64decode(target_ca_encoded))

additional_certs = set()

for new_cert in new_certs:
    if new_cert not in (c for c in current_certs if c.serial_number == new_cert.serial_number):
        additional_certs.add(new_cert)

# No additional certificates found - print and exit
if not additional_certs:
    print("", end='')
    sys.exit(0)

current_certs.update(additional_certs)

for cert in current_certs:
    print(cert.public_bytes(Encoding.PEM), end='')
