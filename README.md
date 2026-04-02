# What's this?

This is an edit of Blender's [FBX IO addon](https://projects.blender.org/blender/blender/src/branch/main/scripts/addons_core/io_scene_fbx) that makes it backwards-compatible with older Blender versions. It tries, where possible, to keep any bug-fixes/improvements/features that the addon has received over the years.

> [!IMPORTANT]
> This isn't a patch; it tries to keep the addon's behaviour unchanged. It, however, can be used as a base for other patches.

# Supported versions

Currently, this project supports Blender versions from <ins>**2.81 to 5.1**</ins>.

> Older versions like 2.79 and 2.80 are considered out-of-scope, due to the huge number of differences they have.

# Downloading and installing

You can download the latest *.zip file from the [Releases](https://github.com/Un-Drew/io_scene_fbx_compat/releases) tab, which can be installed like any addon/extension.

# Context and motivation

Almost every Blender release (except patch versions) brings a number of API changes with it. The FBX addon is normally part of Blender, so when it's eventually updated to use that new API, there's no incentive to keep it compatible with older versions. This means that any fixes or new features that the addon receives are also locked behind newer Blender releases, even when that might not be necessary.

This project attempts to solve this problem by providing an addon that behaves mostly the same in older versions. In addition, it can also act as a good base for anyone that wants to modify/patch the addon for any specific use-cases.

# License

This uses the same license as the original addon, which is [GPL-2.0-or-later](https://spdx.org/licenses/GPL-2.0-or-later.html).
