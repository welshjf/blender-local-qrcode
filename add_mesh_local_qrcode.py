# Copyright (c) 2014 Jacob Welsh <jwelsh+blender@welshcomputing.com>
#
# MIT/X11 license:
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

bl_info = {
    "name": "Local QR Code",
    "description": "Add a QR code mesh. Generates codes locally using \
python-qrcode, not a web service.",
    "author": "Jacob Welsh",
    "version": (1, 0),
    "blender": (2, 65, 0),
    "location": "View3D > Add > Mesh > Local QR Code",
    #"wiki_url": "http://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/Add_Mesh/Local_QR_Code_Generator",
    "category": "Add Mesh"
}

import bpy
import bmesh
from bpy_extras import object_utils
import qrcode

class AddQRCode(bpy.types.Operator):
    """Construct a QR code mesh"""
    bl_idname = "mesh.qrcode_add"
    bl_label = "QR Code"
    bl_options = {'REGISTER', 'UNDO'}

    data = bpy.props.StringProperty(
        name="Data",
        description="Data to store in the QR code",
        default="text")
    invert = bpy.props.BoolProperty(
        name="Invert",
        description="Create mesh in the dark areas instead of light")
    fixed = bpy.props.BoolProperty(
        name="Fixed size",
        description="Scale the QR code to a fixed size (otherwise use unit blocks)",
        default=True)
    join = bpy.props.BoolProperty(
        name="Join blocks",
        description="Join vertices of adjacent blocks",
        default=True)
    border = bpy.props.IntProperty(
        name="Border",
        description="Border width (default 4)",
        default=4, min=0, max=10)
    ec_mode = bpy.props.EnumProperty(
        items=[('ERROR_CORRECT_H', "H", "Correct up to 30% damage"),
               ('ERROR_CORRECT_Q', "Q", "Correct up to 25% damage"),
               ('ERROR_CORRECT_M', "M (default)", "Correct up to 15% damage"),
               ('ERROR_CORRECT_L', "L", "Correct up to 7% damage")],
        name="Error correction",
        default='ERROR_CORRECT_M')

    def create_qrcode_mesh(self):
        qr = qrcode.QRCode(
            error_correction=getattr(qrcode.constants, self.ec_mode),
            border=self.border)
        qr.add_data(self.data)
        qr.make()
        modules = qr.get_matrix()
        size = len(modules)

        mesh = bmesh.new()
        not_invert = not self.invert
        if self.fixed:
            x_scale = 2./size
            y_scale = -2./size
        else:
            x_scale = 1.
            y_scale = -1.
        for y in range(size):
            for x in range(size):
                if modules[y][x] ^ not_invert:
                    verts = [
                        mesh.verts.new((x_scale * x,     y_scale * y,     0.)),
                        mesh.verts.new((x_scale * x,     y_scale * (y+1), 0.)),
                        mesh.verts.new((x_scale * (x+1), y_scale * (y+1), 0.)),
                        mesh.verts.new((x_scale * (x+1), y_scale * y,     0.))
                    ]
                    mesh.faces.new(verts)
        if self.join:
            bmesh.ops.remove_doubles(mesh, verts=mesh.verts, dist=0.0001)
        return mesh

    def execute(self, context):
        mesh = bpy.data.meshes.new("qrcode")
        bm = self.create_qrcode_mesh()
        bm.to_mesh(mesh)
        bm.free()
        object_utils.object_data_add(context, mesh)
        return {'FINISHED'}

def menu_draw(self, context):
    self.layout.operator(AddQRCode.bl_idname, icon='PLUGIN')

def register():
    bpy.utils.register_class(AddQRCode)
    bpy.types.INFO_MT_mesh_add.append(menu_draw)

def unregister():
    bpy.utils.unregister_class(AddQRCode)
    bpy.types.INFO_MT_mesh_add.remove(menu_draw)

if __name__ == "__main__":
    register()
