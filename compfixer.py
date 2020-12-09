"""
MIT License

Copyright (c) 2020 Node Sharer Devs

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import pprint
import bpy


def upgrade_to_blender2910(nodes):
    """
    Blender 2.91 adds a new input to the BSDF node, emit strength in slot 18, moving the previous slot 18 up etc.
    Anything that connect to slot 18 or above from before 2.91 will have it's slot number increased by one.
    The input default values will also be updated to match
    :param nodes: node tree as dict, nodes or groups
    """
    _BSDF_node_names = []
    print('Upgrading nodes to Blender 2.91...')
    for n in nodes:
        node = nodes[n]

        if node['bl_idname'] == 'ShaderNodeBsdfPrincipled':
            # Save the node name for so connections can be updated
            _BSDF_node_names.append(node['name'])

            # Shift the input default values slots up
            for i in reversed(range(18, 22 + 1)):
                nodes[n]['inputs'][str(i)] = node['inputs'][str(i-1)]
            del nodes[n]['inputs']['18']

    for n in nodes:
        node = nodes[n]
        try:
            for output, targets in node['outputs'].items():
                for name, ids in targets.items():
                    if name in _BSDF_node_names:
                        # increment if the slot is 18 or higher
                        if isinstance(ids, int) and ids >= 18:
                            nodes[n]['outputs'][output][name] = ids + 1
                        elif isinstance(ids, list):
                            tmp_ids = ids.copy()
                            for pos, i in enumerate(ids):
                                if i >= 18:
                                    tmp_ids[pos] = i + 1
                            nodes[n]['outputs'][output][name] = tmp_ids

        except KeyError:
            print('No outputs in node: {}'.format(node['name']))

    print('Upgrade to Blender 2.91 Complete!')
    # print('Made it past the second loop. Changed dict:')
    # pprint.pprint(nodes)


def version_difference(prefix):
    """
    Not used atm
    :param prefix:
    :return:
    """
    bv = bpy.app.version
    blender_version = int(str(bv[0]) + str(bv[1]) + str(bv[2]))

    ns_bv = int(prefix.split('B')[1])
    if ns_bv != blender_version:
        return True
    else:
        return False


def fix(prefix, nodes):
    """
    Fix compatibility
    :param prefix: Node Sharer prefix
    :param nodes: Node Sharer node dict
    """
    bv = bpy.app.version
    if bv >= (2, 91, 0):
        if int(prefix.split('B')[1]) < 2910:
            upgrade_to_blender2910(nodes)
