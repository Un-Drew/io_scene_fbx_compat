"""This module does various tasks related to checking/using the available API features of the current ver of Blender.

Many of Blender's major & minor updates have introduced a bunch of API changes. For some of these, the FBX python addon
had to be updated to support/leverage that new API.

Since that addon was normally bundled with Blender, there was (presumably) no incentive for the Blender developers to
make it backwards-compatible with APIs in older versions. However, because this project aims to be backwards-compatible,
some API calls need to be done conditionally.

As such, this module does the following:

* Keeps track of which API features are available.
* Sometimes, provides functions that conditionally use the appropriate API.
"""

import bpy
import bpy_extras.node_shader_utils

__author__ = "UnDrew"

# Checks whether a bpy type (an RNA struct) has a property by name.
# Source: https://blender.stackexchange.com/a/300562
def bpy_type_has_prop(btype, propname):
    for prop in btype.bl_rna.properties:
        if prop.identifier == propname:
            return True
    return False

""" Added in 2.91.0 """

HAS_MESH_ATTRIBUTES = bpy_type_has_prop(bpy.types.Mesh, 'attributes')
HAS_SUBSURF_BOUNDARY_SMOOTH = bpy_type_has_prop(bpy.types.SubsurfModifier, 'boundary_smooth')
HAS_BSDF_EMISSION_STRENGTH = hasattr(bpy_extras.node_shader_utils.PrincipledBSDFWrapper, 'emission_strength')
