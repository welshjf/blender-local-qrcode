=====================================
Local QR Code Generator Blender Addon
=====================================

Generate QR code meshes directly in Blender, with no need for an external
program or web service.

By Jacob Welsh

License: MIT/X11

Minimum required Blender version: 2.65

Blender Addons Catalog page (hopefully...):
http://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/Add_Mesh/Local_QR_Code_Generator

General information on addons:
http://wiki.blender.org/index.php/Doc:2.6/Manual/Extensions/Python/Add-Ons

Building
========

The addon is implemented in pure Python and consists of a single file plus
dependencies. So the only build step is the optional creation of a zip file
that bundles everything for easy installation into Blender.

The primary dependency is the python-qrcode_ library. Version 4.0.4 or newer is
strongly recommended for correctness; 5.0.1 is recommended for speed. It is
linked in ``deps/python-qrcode`` as a git submodule. This library requires
six_; since that's a single file and doesn't use git, it's reproduced in full
in ``deps/six.py``. Note that ``python-qrcode`` also normally requires
``pillow``, but that's not needed here as the addon doesn't use that part of
the code.

Once the dependencies are in place in ``deps``, update the version comments in
``bundle_hdr.py`` if necessary, then run ``./bundle.sh`` which will produce
``add_mesh_local_qrcode.zip``.

.. _python-qrcode: https://pypi.python.org/pypi/qrcode
.. _six: https://pypi.python.org/pypi/six

Installation
============

From the bundled zip file
-------------------------

In Blender, select File > User Preferences, Addons tab, Install from File
button. Navigate to ``add_mesh_local_qrcode.zip`` and install it. It should now
be listed as "Add Mesh: Local QR Code" under the "Add Mesh" category. Click the
checkbox on the right to enable it, and "Save User Settings" if you want it
enabled every time you run Blender.

Using shared libraries
----------------------

If your Blender is using a system-wide Python installation (e.g. from a Linux
distribution), you can install the dependencies in a standard Python 3
location, then install only ``add_mesh_local_qrcode.py`` in your Blender addons
directory as above.

Usage
=====

Add a new code through Add > Mesh > Local QR Code. It will be created in the XY
plane, oriented for scanning from the top. Once added, you can control the
following from the operator properties box in the tool shelf (the mesh will
update immediately):

* Data: the text to encode; more compact encodings such as number or
  alphanumeric will be detected automatically
* Invert: whether to create blocks for the background or foreground
* Fixed size: whether to scale the code to a fixed size of 2x2, or build it
  from 1x1 blocks
* Join blocks: whether to join vertices of adjacent blocks together; you might
  not want this for stylizations like adding space between each block
* Border size, in blocks
* Error correction: higher levels are more resistant to damage, but may
  be more difficult to scan due to the greater amount of data

Be sure to use a dark-colored foreground on a light background for your final
product to be able to scan the code.

Support
=======

Email me: jwelsh@welshcomputing.com

Report a bug: https://github.com/welshjf/blender-local-qrcode/issues

If you find this addon helpful, please consider donating bitcoin_:
1EAr1XZzd9a1RqSMtKDGDZs214ptT9WHtK

Thanks for downloading, and have a lot of fun!

.. _bitcoin: https://www.weusecoins.com/
