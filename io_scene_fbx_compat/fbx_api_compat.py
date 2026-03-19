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

"""
Functions that check a class's props/funcs by name. This script uses these to find out which APIs are available.

Motivation:

A naive way to check whether an API is available would be to rely on the current Blender version. This works fine for
official Blender releases, but wouldn't always be correct on pre-release builds. It's not uncommon for a property to be
changed or replaced in the middle of a release cycle, so to support this, a more concrete check is needed.

Fortunately, both Python and Blender's RNA system allow you, from the class alone, to explicitly check for props/funcs.
Doing this is much safer than relying on the version alone.

Why stop here:

A safer (and technically more correct) approach would've been to check the instances at runtime, using exceptions.
However, doing this for every instance would risk slowing the addon down, which I didn't want to do.

In contrast, checking the class guarantees me that the result will be consistent throughout the process's lifetime,
which in turn allows me to cache the result here. Also, personally, I think it's more readable this way.
"""

# Checks whether a natively-defined class has the specified RNA property.
# Adapted from: https://blender.stackexchange.com/a/300562
def class_has_rna_prop(cla, propname):
    return propname in cla.bl_rna.properties

# Checks whether a class's RNA property is readonly.
# NOTE: For a full list of all of a propery's attributes, run: print(dir(cla.bl_rna.properties[propname]))
def class_rna_prop_is_readonly(cla, propname):
    return cla.bl_rna.properties[propname].is_readonly

# Checks whether a class has the specified python property (not to be confused with python attributes).
# NOTE: Sometimes, this is also applicable to natively-defined classes, because they're partially defined in Python.
#       See: https://projects.blender.org/blender/blender/src/tag/v5.0.0/scripts/modules/_bpy_types.py
def class_has_py_prop(cla, propname):
    return hasattr(cla, propname)

# Checks whether a class has a function (either natively-defined or python-defined).
def class_has_func(cla, funcname):
    return hasattr(cla, funcname)

"""
Added in 2.91.0
Sources:
    * https://developer.blender.org/docs/release_notes/2.91/python_api/#other-changes
    * https://developer.blender.org/docs/release_notes/2.91/modeling/#subdivision-surfaces
    * https://developer.blender.org/docs/release_notes/2.91/python_api/#compatibility
"""

HAS_MESH_ATTRIBUTES = class_has_rna_prop(bpy.types.Mesh, 'attributes')
HAS_VRTX_COLS_AS_ATTRS = HAS_MESH_ATTRIBUTES
HAS_SUBSURF_BOUNDARY_SMOOTH = class_has_rna_prop(bpy.types.SubsurfModifier, 'boundary_smooth')
HAS_BSDF_EMISSION_STRENGTH = class_has_py_prop(bpy_extras.node_shader_utils.PrincipledBSDFWrapper, 'emission_strength')

"""
Added in 3.0.0
Sources:
    * https://developer.blender.org/docs/release_notes/3.0/python_api/#idproperty-ui-data-api
    * https://docs.blender.org/api/2.93/bpy.types.Object.html#bpy.types.Object.cycles_visibility
    * https://docs.blender.org/api/3.0/bpy.types.Object.html#bpy.types.Object.visible_shadow
"""

HAS_REFACTORED_UI_DATA = class_has_func(bpy.types.bpy_struct, 'id_properties_ui')
HAS_REFACTORED_VISIBLE_FLAGS = class_has_rna_prop(bpy.types.Object, 'visible_shadow')

"""
Added in 3.1.0
Source: https://developer.blender.org/docs/release_notes/3.1/python_api/#other-additions
"""

HAS_VRTX_AND_PLGN_NORM_ARRAYS = class_has_rna_prop(bpy.types.Mesh, 'vertex_normals')

"""
Added in 3.2.0
Sources:
    * https://developer.blender.org/docs/release_notes/3.2/sculpt/#color-attributes
    * https://docs.blender.org/api/3.2/change_log.html#bpy-types-mesh
"""

HAS_MESH_COL_ATTRS_PROP = class_has_rna_prop(bpy.types.Mesh, 'color_attributes')  # Also when the UI for them changed

"""
Added in 3.4.0
Sources:
    * https://docs.blender.org/api/3.4/change_log.html#bpy-types-bytecolorattributevalue
    * https://docs.blender.org/api/3.4/change_log.html#bpy-types-floatcolorattributevalue
    * https://developer.blender.org/docs/release_notes/3.4/python_api/#internal-mesh-format
"""

HAS_COL_ATTR_SRGB_PROP = HAS_VRTX_COLS_AS_ATTRS and class_has_rna_prop(bpy.types.ByteColorAttributeValue, 'color_srgb')
HAS_MESH_ATTR_MATERIAL_INDEX = check_ver(3, 4, 0, 'beta')  # unsure how to check this more concretely...
# NOTE: - This added `Mesh.has_crease_edge` at same time.
HAS_REFACTORED_EDGE_CREASES = class_has_rna_prop(bpy.types.Mesh, 'edge_creases')

"""
Added in 3.5.0
Source: https://developer.blender.org/docs/release_notes/3.5/python_api/#internal-mesh-format
"""

HAS_MESH_ATTR_POSITION = check_ver(3, 5, 0, 'beta')  # unsure how to check this more concretely...
HAS_MESH_ATTR_SHARP_EDGE = check_ver(3, 5, 0, 'beta')  # unsure how to check this more concretely...
HAS_UV_LAYER_UV_PROP = class_has_rna_prop(bpy.types.MeshUVLoopLayer, 'uv')

"""
Added in 3.6.0
Source: https://developer.blender.org/docs/release_notes/3.6/python_api/#internal-mesh-format
"""

HAS_REFACTORED_POLYS_FOR_CONSISTENT_ORDER_WITH_LOOPS = class_rna_prop_is_readonly(bpy.types.MeshPolygon, 'loop_total')
HAS_MESH_ATTR_SHARP_FACE = check_ver(3, 6, 0, 'beta')  # unsure how to check this more concretely...
HAS_MESH_ATTRS_CORNER_VERT_AND_CORNER_EDGE = check_ver(3, 6, 0, 'beta')  # unsure how to check this more concretely...
HAS_MESH_ATTR_EDGE_VERTS = check_ver(3, 6, 0, 'beta')  # unsure how to check this more concretely...
