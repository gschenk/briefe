A LaTeX Business Letter Template
================================

Repository for Business Letters
following DIN 5008 and DIN 676

Using the letter options of the KOMA
project by Markus Kohm:
http://www.komascript.de/

Address Database Function
-------------------------

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

solarized branch
----------------

This branch allows to change the colour scheme of
the output pdf to solarized. Due to reduced contrast
it may be easier to read when ambient light is not
very bright.

The solarized colour scheme was developed by
Ethan Schoonover and can be found at:
http://ethanschoonover.com/solarized

The *solarized.sty* package accepts the options
*dark* and *light* no option renders the letter
unchanged, ie black on white.

The repo of python scripts can be found on github:
git@github.com:gschenk/address-stuff.git
