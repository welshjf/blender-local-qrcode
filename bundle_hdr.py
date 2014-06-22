
#
# BUNDLE HEADER
#
# Source info:
# add_mesh_local_qrcode.py => __init__.py
# python-qrcode(5.0.1) => modules/qrcode (see modules/qrcode/LICENSE)
# six(1.7.2) => modules/six.py
#

# Tell python where to find the bundled dependencies
import os.path
import sys
modules_path = os.path.join(os.path.dirname(__file__), "modules")
if modules_path not in sys.path:
    sys.path.append(modules_path)
del modules_path

#
# END BUNDLE HEADER
#
