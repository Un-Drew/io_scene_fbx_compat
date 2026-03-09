# What's this?

This project aims to edit Blender's official FBX IO addon to make it backwards-compatible with multiple versions of Blender.

More specifically, this addon has 2 goals:
1. Use the appropriate API functions depending on the version of Blender that it's installed on.
2. Keep any bug-fixes/features that have been added throughout the years, to make them available to older versions.

Currently, this project supports Blender versions from **2.81 to 5.0**.

# Context

Many of Blender's major & minor updates have introduced a bunch of API changes. For some of these, the FBX python addon had to be updated to support/leverage that new API. Since that addon was normally bundled with Blender, there was (presumably) no incentive for the Blender developers to make it backwards-compatible with APIs in older versions.
