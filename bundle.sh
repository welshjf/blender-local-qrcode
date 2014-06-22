#!/bin/bash
# Create a self-contained zip file for the Blender addon.
# Be sure to have the git submodule(s) initialized.

pkg=add_mesh_local_qrcode

[ -d $pkg ] && rm -rf $pkg
[ -f $pkg.zip ] && rm -f $pkg.zip
mkdir $pkg

# find closing } of bl_info declaration
cut_linenum=`sed -n -e '/^}/ {=; q}' $pkg.py`
(head -n $cut_linenum $pkg.py; cat bundle_hdr.py; tail -n +$((cut_linenum+1)) $pkg.py) > $pkg/__init__.py

mkdir $pkg/modules
cp -a deps/python-qrcode/qrcode $pkg/modules
cp -a deps/python-qrcode/LICENSE $pkg/modules/qrcode
cp -a deps/six.py $pkg/modules

zip -9 -r $pkg.zip $pkg
rm -rf $pkg
