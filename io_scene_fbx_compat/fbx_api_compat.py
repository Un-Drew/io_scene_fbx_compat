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
    # NOTE: Doing some_blender_type.bl_rna returns some sort of metadata bpy_struct for that type.
    #       The exact same metadata is also accessible from instances of that type.
    for prop in btype.bl_rna.properties:
        if prop.identifier == propname:
            return True
    return False

def bpy_type_has_func(btype, funcname):
    # NOTE: hasattr, when used on a bpy type, will detect functions.
    return hasattr(btype, funcname)

def py_class_has_prop(pyclass, propname):
    # NOTE: hasattr, when used on a python class, will detect properties (those tied to a getter and setter).
    return hasattr(pyclass, propname)

def py_class_has_func(pyclass, funcname):
    # NOTE: hasattr, when used on a python class, will ALSO detect functions.
    return hasattr(pyclass, funcname)

""" Added in 2.91.0 """

HAS_MESH_ATTRIBUTES = bpy_type_has_prop(bpy.types.Mesh, 'attributes')
HAS_SUBSURF_BOUNDARY_SMOOTH = bpy_type_has_prop(bpy.types.SubsurfModifier, 'boundary_smooth')
HAS_BSDF_EMISSION_STRENGTH = py_class_has_prop(bpy_extras.node_shader_utils.PrincipledBSDFWrapper, 'emission_strength')

""" Added in 3.0.0 """

HAS_REFACTORED_UI_DATA = bpy_type_has_func(bpy.types.bpy_struct, 'id_properties_ui')
HAS_REFACTORED_VISIBLE_FLAGS = bpy_type_has_prop(bpy.types.Object, 'visible_shadow')
