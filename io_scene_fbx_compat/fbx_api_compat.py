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

def cycle_to_num(cycle):
    if cycle == 'alpha':
        return 0
    elif cycle == 'beta':
        return 1
    elif cycle == 'rc':
        return 2
    else:
        # Even if this isn't 'release', assume it anyway, as there could be Extra Secret cylce vals I'm not aware of. :S
        return 3

BL_VER_MAJOR, BL_VER_MINOR, BL_VER_MICRO = bpy.app.version
BL_VER_CYCLE = cycle_to_num(bpy.app.version_cycle)

def check_ver(min_major, min_minor, min_micro, min_cycle):
    if BL_VER_MAJOR > min_major:
        return True
    if BL_VER_MAJOR < min_major:
        return False
    if BL_VER_MINOR > min_minor:
        return True
    if BL_VER_MINOR < min_minor:
        return False
    if BL_VER_MICRO > min_micro:
        return True
    if BL_VER_MICRO < min_micro:
        return False
    return BL_VER_CYCLE >= cycle_to_num(min_cycle)

# Checks whether a bpy type has a property by name.
# Adapted from: https://blender.stackexchange.com/a/300562
def bpy_type_has_prop(btype, propname):
    return propname in btype.bl_rna.properties

def bpy_type_has_func(btype, funcname):
    # NOTE: hasattr, when used on a bpy type, will detect functions.
    return hasattr(btype, funcname)

def py_class_has_prop(pyclass, propname):
    # NOTE: hasattr, when used on a python class, will detect properties (those tied to a getter and setter).
    return hasattr(pyclass, propname)

def py_class_has_func(pyclass, funcname):
    # NOTE: hasattr, when used on a python class, will ALSO detect functions.
    return hasattr(pyclass, funcname)

"""
Added in 2.91.0
Sources:
    * https://developer.blender.org/docs/release_notes/2.91/python_api/#other-changes
    * https://developer.blender.org/docs/release_notes/2.91/modeling/#subdivision-surfaces
    * https://developer.blender.org/docs/release_notes/2.91/python_api/#compatibility
"""

HAS_MESH_ATTRIBUTES = bpy_type_has_prop(bpy.types.Mesh, 'attributes')
HAS_VRTX_COLS_AS_ATTRS = HAS_MESH_ATTRIBUTES
HAS_SUBSURF_BOUNDARY_SMOOTH = bpy_type_has_prop(bpy.types.SubsurfModifier, 'boundary_smooth')
HAS_BSDF_EMISSION_STRENGTH = py_class_has_prop(bpy_extras.node_shader_utils.PrincipledBSDFWrapper, 'emission_strength')

"""
Added in 3.0.0
Sources:
    * https://developer.blender.org/docs/release_notes/3.0/python_api/#idproperty-ui-data-api
    * https://docs.blender.org/api/2.93/bpy.types.Object.html#bpy.types.Object.cycles_visibility
    * https://docs.blender.org/api/3.0/bpy.types.Object.html#bpy.types.Object.visible_shadow
"""

HAS_REFACTORED_UI_DATA = bpy_type_has_func(bpy.types.bpy_struct, 'id_properties_ui')
HAS_REFACTORED_VISIBLE_FLAGS = bpy_type_has_prop(bpy.types.Object, 'visible_shadow')

"""
Added in 3.1.0
Source: https://developer.blender.org/docs/release_notes/3.1/python_api/#other-additions
"""

HAS_VRTX_AND_PLGN_NORM_ARRAYS = bpy_type_has_prop(bpy.types.Mesh, 'vertex_normals')

"""
Added in 3.2.0
Sources:
    * https://developer.blender.org/docs/release_notes/3.2/sculpt/#color-attributes
    * https://docs.blender.org/api/3.2/change_log.html#bpy-types-mesh
"""

HAS_MESH_COL_ATTRS_PROP = bpy_type_has_prop(bpy.types.Mesh, 'color_attributes')  # Also when the UI for them changed

"""
Added in 3.4.0
Sources:
    * https://docs.blender.org/api/3.4/change_log.html#bpy-types-bytecolorattributevalue
    * https://docs.blender.org/api/3.4/change_log.html#bpy-types-floatcolorattributevalue
    * https://developer.blender.org/docs/release_notes/3.4/python_api/#internal-mesh-format
"""

HAS_COL_ATTR_SRGB_PROP = HAS_VRTX_COLS_AS_ATTRS and bpy_type_has_prop(bpy.types.ByteColorAttributeValue, 'color_srgb')
HAS_REFACTORED_EDGE_CREASES = bpy_type_has_prop(bpy.types.Mesh, 'edge_creases')  # added 'has_crease_edge' at same time
HAS_MESH_ATTR_MATERIAL_INDEX = check_ver(3, 4, 0, 'beta')  # unsure how to check this more concretely...

"""
Added in 3.5.0
Source: https://developer.blender.org/docs/release_notes/3.5/python_api/#internal-mesh-format
"""

HAS_MESH_ATTR_POSITION = check_ver(3, 5, 0, 'beta')  # unsure how to check this more concretely...
HAS_MESH_ATTR_SHARP_EDGE = check_ver(3, 5, 0, 'beta')  # unsure how to check this more concretely...
HAS_UV_LAYER_UV_PROP = bpy_type_has_prop(bpy.types.MeshUVLoopLayer, 'uv')
