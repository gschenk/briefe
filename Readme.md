Repository for Business Letters
following DIN 5008 and DIN 676

Recipient and sender data may be
stored in the 'private' directory.

Using yaml address entries. The python
script 'enterAdress.py' may be used
to generate these. Each entrie is in
its own filename. The filename without
extension serves as a handle to identify
the addressee.

The first line in the 'brief.tex' file
must be the handle of the addressee. The
scritp 'readAddr.py' uses this handle to
generate latex statements that specify
the address and salutation of the recipient
based on the respective .yaml address file.


*Care must be taken not to make
branches where these were filled
with private data public.*


The repo of python scripts can be found on github:
git@github.com:gschenk/address-stuff.git
