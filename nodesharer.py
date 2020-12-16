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

bl_info = {
    "name": "Node Sharer",
    "author": "NodeSharer Devs",
    "version": (0, 1, 5),
    "blender": (2, 90, 0),
    "location": "Node Editor Toolbar",
    "description": "Share node setups as text strings.",
    "warning": "Blender can crash when pasting node groups. Save your work before pasting.",
    "category": "Node",
    "tracker_url": "https://github.com/wildiness/NodeSharer#supporthelp-and-bug-reports",
}  # outdated? remove?

import bpy
import pprint
import json
import inspect
import zlib
import base64
from . import compfixer


def dump(obj):
    """Dumps class variables and functions for debug"""
    print('\n')
    for attr in dir(obj):
        if hasattr(obj, attr):
            tmp = getattr(obj, attr)
            if inspect.isclass(obj):
                print("recursing")
                dump(attr)
            else:
                print("obj.%s = %s" % (attr, tmp))


class NS_node:
    """Stores a node, in preparation for JSONifying or before being added to a node tree"""

    _prop_common = ('name', 'bl_idname', 'inputs', 'outputs', 'location')  # always saved properties

    _prop_optional = {'hide': False, 'label': '', 'mute': False, 'parent': None, 'select': False, 'show_options': True,
                      'show_preview': False, 'show_texture': False,
                      'use_custom_color': False}  # Saved if they are not default valued

    _prop_common_ignored = ('bl_description', 'bl_icon', 'bl_label', 'type', 'bl_height_default', 'bl_height_max',
                            'bl_height_min', 'bl_rna', 'bl_static_type', 'bl_width_default',
                            'bl_width_max', 'bl_width_min', 'draw_buttons', 'draw_buttons_ext',
                            'input_template', 'texture_mapping', 'uv_map', 'color_mapping',
                            'internal_links', 'is_registered_node_type', 'output_template', 'poll', 'poll_instance',
                            'rna_type', 'socket_value_update', 'update', 'image_user', 'dimensions',
                            'width_hidden', 'interface', 'object', 'text', 'color', 'height', 'image',
                            'width', 'filepath')  # never saved cus they are useless or created with the node by blender

    def __init__(self, node, *args, **kwargs):
        self.properties = {}
        self.node = node

        self.pass_through = self.storenode()
        self.name = self.properties['name']

    def storenode(self):
        """Store a node's properties"""
        to_return = None
        tmp_prop = {}
        for attr in dir(self.node):
            if hasattr(self.node, attr):
                tmp_prop[attr] = getattr(self.node, attr)

        for k in tmp_prop:  # for key in node values
            if k in self._prop_common:
                if k == 'inputs':
                    tmp_inputs = {}
                    for idx, n_inputs in enumerate(self.node.inputs):
                        # key = '' + str(idx)
                        key = idx
                        try:
                            try:
                                tmp_inputs[key] = round(n_inputs.default_value, 5)
                            except:
                                tmp_inputs[key] = tuple(round(tmp_v, 5) for tmp_v in n_inputs.default_value)
                        except Exception as e:
                            print('input ' + str(idx) + ' not default value')
                            print(e)
                            # tmp_inputs[key] = ''
                    if tmp_inputs != {}:
                        self.properties[k] = tmp_inputs

                elif k == 'outputs':
                    tmp_outputs = {}
                    output_default_value = {}
                    for idx, n_outputs in enumerate(self.node.outputs):
                        # key = '' + str(idx)
                        key = idx
                        try:
                            try:
                                output_default_value[key] = round(n_outputs.default_value, 5)
                            except:
                                output_default_value[key] = tuple(round(tmp_v, 5) for tmp_v in n_outputs.default_value)
                        except AttributeError:
                            pass
                        try:
                            # print('Dumping ' + key)
                            if n_outputs.is_linked:
                                tmp_links = {}
                                for node_links in n_outputs.links:
                                    s = node_links.to_socket.path_from_id()
                                    s = int((s.split('inputs['))[1].split(']')[0])
                                    tmp_link_name = node_links.to_node.name
                                    if tmp_link_name in tmp_links:
                                        try:
                                            tmp_links[tmp_link_name] = tmp_links.get(tmp_link_name) + (s,)
                                        except:
                                            tmp_links[tmp_link_name] = (tmp_links.get(tmp_link_name),) + (s,)
                                    else:
                                        tmp_links[tmp_link_name] = s

                                tmp_outputs[key] = tmp_links
                        except:
                            tmp_outputs[n_outputs] = str(n_outputs.links)
                    if tmp_outputs != {}:
                        self.properties[k] = tmp_outputs
                    if output_default_value != {}:
                        self.properties['out_dv'] = output_default_value

                elif k == 'location':
                    try:
                        self.properties['loc'] = (round(tmp_prop[k][0]), round(tmp_prop[k][1]),)
                    except:
                        print("location/vector dump failed")

                else:
                    self.properties[k] = tmp_prop[k]

            elif k in self._prop_optional:
                value = tmp_prop[k]
                if value != self._prop_optional[k]:
                    if k == 'parent':
                        self.properties[k] = value.name
                        continue
                    self.properties[k] = value
                    if k == 'use_custom_color':
                        self.properties['color'] = tuple(round(tmp_v, 5) for tmp_v in tmp_prop['color'])

            elif k in self._prop_common_ignored:  # Sort out all unwanted properties
                continue

            elif k[:1] == '_':  # Sort out double underscore
                continue

            elif k == 'node_tree':
                try:
                    self.properties['node_tree'] = tmp_prop[k].name
                    to_return = {tmp_prop[k].name: NS_group(tmp_prop[k])}
                except Exception as e:
                    print('Group node tree failed')
                    print(e)
            elif k == 'color_ramp':
                tmp_cr = {}
                tmp_elements = {}

                tmp_cr['color_mode'] = tmp_prop[k].color_mode
                tmp_cr['hue_interpolation'] = tmp_prop[k].hue_interpolation
                tmp_cr['interpolation'] = tmp_prop[k].interpolation

                for element in tmp_prop[k].elements:
                    tmp_elements[round(element.position, 5)] = tuple(round(tmp_v, 5) for tmp_v in element.color)
                tmp_cr['elements'] = tmp_elements
                self.properties[k] = tmp_cr

            elif k == 'mapping':
                tmp_mapping = {}
                tmp_curves = {}

                tmp_mapping['clip_max_x'] = tmp_prop[k].clip_max_x
                tmp_mapping['clip_max_y'] = tmp_prop[k].clip_max_y
                tmp_mapping['clip_min_x'] = tmp_prop[k].clip_min_x
                tmp_mapping['clip_min_y'] = tmp_prop[k].clip_min_y

                tmp_mapping['extend'] = tmp_prop[k].extend
                tmp_mapping['tone'] = tmp_prop[k].tone
                tmp_mapping['use_clip'] = tmp_prop[k].use_clip

                for idc, curve in enumerate(tmp_prop[k].curves):
                    tmp_points = {}
                    for idp, point in enumerate(curve.points):
                        tmp_points[idp] = (round(point.location[0], 5), round(point.location[1], 5),)
                    tmp_curves[idc] = tmp_points
                tmp_mapping['curves'] = tmp_curves

                self.properties[k] = tmp_mapping

            else:  # Catch all. for the random named attributes
                if isinstance(tmp_prop[k], (int, str, bool, float)):
                    self.properties[k] = tmp_prop[k]
                else:
                    try:
                        self.properties[k] = tmp_prop[k].name
                    except:
                        pass
                        # self.properties[k] = 'object'

        return to_return  # Return to pass through

    def print_prop(self):
        pprint.pprint(self.properties)
        print('\n')

    def toJSON(self):
        return self.properties
        # return json.dumps(self.properties, sort_keys=True, indent=4)


class NS_nodetree:
    """stores NS_nodes's"""

    groups = {}

    def __init__(self):
        self._nodes = {}

    def add_node(self, node):
        """Add node to node tree"""
        n = NS_node(node)
        self._nodes[n.name] = n

        if n.pass_through is not None:
            k, v = n.pass_through.popitem()
            self.groups[k] = v

    def make_dict(self):
        tmp_dict = {}
        for nk, nv in self._nodes.items():
            tmp_dict[nk] = nv.properties
        return tmp_dict

    def print_tree(self):
        """Print tree"""
        for k in self._nodes:
            print('\n')
            self._nodes[k].print_prop()
        # pprint.pprint(self._nodes)
        # print('\n')

    def dumps_json(self, d):
        """Indented SON for viewing"""
        # for node in self._nodes:
        #     print(node.toJSON())
        print(json.dumps(d, default=lambda o: o.properties, indent=2))

    def dump_JSON(self, d):
        """Unindented json for compressing"""
        return json.dumps(d, separators=(',', ':'), default=lambda o: o.properties)
        # return json.dumps(d, separators=(',', ':'), default=lambda o: o.toJSON())

    def dumps_node_JSON(self):
        print('JSON dump of nodes')
        self.dumps_json(self._nodes)


class NS_material(NS_nodetree):
    """Stores a material and its nodes"""

    def __init__(self, mat):
        super().__init__()
        self._mat = mat
        self.name = self._mat.name
        self.groups.clear()
        self.get_nodes()
        self.ns_mat = {'name': self.name,
                       'type': 'material',
                       'nodes': self._nodes}
        if self.groups != {}:
            self.ns_mat['groups'] = self.groups

    def get_nodes(self):
        for node in self._mat.node_tree.nodes:
            self.add_node(node)

    def dumps_mat_JSON(self):
        print('JSON dump of material')
        self.dumps_json(self.ns_mat)

    def dump_mat_JSON(self):
        """Un indented JSON for compression"""
        return self.dump_JSON(self.ns_mat)

    def compress(self):
        prefix = self.prefix()
        try:
            # print('json string')
            json_str = self.dump_mat_JSON().encode("utf8")
            # print('compressed obj')
            compressed = zlib.compress(json_str, 9)
            encoded = base64.b64encode(compressed).decode()
            ns_string = prefix + encoded
            print('base64 encoded string(length = ' + str(len(ns_string)) + ') : \n')
            print(ns_string)
            print('\n')
            bpy.context.window_manager.clipboard = ns_string
            return ns_string, len(ns_string)
        except Exception as e:
            print("Failed in compress")
            print(e)

    def prefix(self):
        blender_version = bpy.app.version
        ns_version = str(0)
        prefix = 'NS' + ns_version + 'B' + str(blender_version[0]) + str(blender_version[1]) + str(
            blender_version[2]) + '!'
        return prefix


class NS_group(NS_nodetree):

    def __init__(self, nodetree):
        super().__init__()
        self._nt = nodetree
        self.properties = {}

        self.get_nodes()

    def get_nodes(self):
        for node in self._nt.nodes:
            self.add_node(node)

        self.properties = self.make_dict()

    def print_prop(self):
        pprint.pprint(self.properties)
        print('\n')

    def ret_nodes(self):
        d = self.make_dict()
        return d


class NS_mat_constructor(NS_nodetree):
    """Constructs a material nodetree"""

    def __init__(self, b64_string):
        """

        :param b64_string: node sharer compressed base 64 string
        """
        super().__init__()
        self.prefix = str(b64_string.split('!')[0])

        if str(self.prefix[:2]) != 'NS':
            return

        self.uncompressed = self.uncompress(b64_string.split('!')[1])
        # ns_ = Node Sharer
        self.ns_nodes = self.uncompressed['nodes']

        compfixer.fix(self.prefix, self.ns_nodes)  # Fix compatability

        self.ns_mat_name = self.uncompressed['name']
        self.ns_groups = self.uncompressed.pop('groups', None)

        # b_ = blender
        self.b_mat = bpy.data.materials.new(name=self.ns_mat_name)
        self.b_mat_name_actual = self.b_mat.name
        self.b_mat.use_nodes = True
        self.b_nodes = self.b_mat.node_tree.nodes

        self._created_nodes = []
        self._created_groups = {}

        # Construct groups first
        if self.ns_groups is not None:
            for ns_grp in self.ns_groups:
                print('Constructing group:' + ns_grp + '\n')
                group = bpy.data.node_groups.new(ns_grp, 'ShaderNodeTree')
                self._created_groups[ns_grp] = group.name
                # self._created_groups[grp] = group
            for b_grp in self._created_groups:
                try:
                    # self.construct(self.ns_groups[grp], group)
                    self.construct(self.ns_groups[b_grp], bpy.data.node_groups[self._created_groups[b_grp]],
                                   self._created_groups[b_grp], is_nodegroup=True)  # causes crash when linking
                except Exception as e:
                    print('Constructing node group node tree failed')
                    print(e)

        # Construct material node tree
        # self.construct(self.ns_nodes, self.b_mat.node_tree, is_material=True)  # Original

        self.construct(self.ns_nodes, bpy.data.materials[self.b_mat_name_actual].node_tree, self.b_mat_name_actual,
                       is_material=True)

    def uncompress(self, s):
        """
        Uncompresses the base64 node sharer text string
        :param s: base64 encoded node sharer text string
        :return: the uncompressed material dict
        """
        try:
            print('uncompressing \n')
            compressed = base64.b64decode(s)
            json_str = zlib.decompress(compressed).decode('utf8')
            # print('JSON \n' + json_str + '\n')
            material = json.loads(json_str)
            print('pprint JSON \n')
            pprint.pprint(material)
            return material
        except Exception as e:
            print(e)

    def construct(self, ns_nodes, nt, nt_parent_name, is_material=False, is_nodegroup=False):
        """
        Constructs a node tree
        :param nt_parent_name: name of node tree parent, either material or node group
        :param is_nodegroup: bool is node group
        :param ns_nodes: node sharer dict
        :param nt: Blender node tree
        :param is_material: bool is material
        """
        # b_nodes = nt.nodes  # original
        to_link = []
        to_parent = {}
        b_node_names = {}  # Node sharer name: blender actual name

        if is_material:
            b_nodes = bpy.data.materials[self.b_mat_name_actual].node_tree.nodes
        elif is_nodegroup:
            b_nodes = bpy.data.node_groups[nt_parent_name].nodes
        else:
            print('Did not specify material or node group')
            return

        # remove stock BSDF and output if creating a material
        if is_material is True:
            for n in b_nodes:
                b_nodes.remove(n)

        for k in ns_nodes:
            print('Constructing node:' + k + '\n')

            n = ns_nodes[k]

            bl_idname = n.pop('bl_idname')
            name = n.pop('name')

            # if is_material is True:
            # if True:
            node = b_nodes.new(bl_idname)
            node.name = name
            b_node_names[name] = node.name
            # else:
            #     try:
            #         node = b_nodes[name]
            #     except Exception as e:
            #         print('No existing node with that name, creating...')
            #         print(e)
            #         node = b_nodes.new(bl_idname)
            #         node.name = name

            # self._created_nodes.append(node)

            loc = n.pop('loc')
            node.location = (loc[0], loc[1])

            ns_node_tree = n.pop('node_tree', None)
            if ns_node_tree is not None:
                try:
                    node.node_tree = bpy.data.node_groups[self._created_groups[ns_node_tree]]
                except Exception as e:
                    print('Group node node tree assignment failed')
                    print(e)

            inputs = n.pop('inputs', None)
            if inputs is not None:
                for i in inputs:
                    v = inputs[i]
                    try:
                        node.inputs[int(i)].default_value = v
                    except Exception as e:
                        print('Failed to set input default value')
                        print(e)

            out_dv = n.pop('out_dv', None)
            if out_dv is not None:
                for i in out_dv:
                    v = out_dv[i]
                    try:
                        node.outputs[int(i)].default_value = v
                    except Exception as e:
                        print('Failed to set output default value')
                        print(e)

            outputs = n.pop('outputs', None)
            if outputs is not None:
                to_link.append({name: outputs})

            color_ramp = n.pop('color_ramp', None)
            if color_ramp is not None:
                elements = color_ramp['elements']
                node.color_ramp.color_mode = color_ramp['color_mode']
                node.color_ramp.hue_interpolation = color_ramp['hue_interpolation']
                node.color_ramp.interpolation = color_ramp['interpolation']
                i = 0
                for p, c in elements.items():
                    if i > 1:
                        new_cr_ele = node.color_ramp.elements.new(position=float(p))
                        new_cr_ele.color = c
                    else:
                        node.color_ramp.elements[i].position = float(p)
                        node.color_ramp.elements[i].color = c
                    i += 1

            mapping = n.pop('mapping', None)
            if mapping is not None:
                curves = mapping.pop('curves')
                for idc, curve in curves.items():
                    for idp, point in curve.items():
                        if int(idp) > 1:
                            node.mapping.curves[int(idc)].points.new(point[0], point[1])
                        else:
                            node.mapping.curves[int(idc)].points[int(idp)].location = point

                while len(mapping) > 0:
                    k, v = mapping.popitem()
                    try:
                        setattr(node.mapping, k, v)
                    except Exception as e:
                        print('failed to set mapping attribute: ' + str(k))
                        print(e)

            parent = n.pop('parent', None)
            if parent is not None:
                to_parent[name] = parent

            while len(n) > 0:
                k, v = n.popitem()
                try:
                    setattr(node, k, v)
                except Exception as e:
                    print('failed to set attribute: ' + str(k))
                    print(e)

        for l in to_link:
            k, v = l.popitem()

            for output, targets in v.items():
                for name, ids in targets.items():
                    input_ids = []
                    if isinstance(ids, int):  # ids can be int or list.
                        input_ids.append(ids)  # This is the very first backwards compatabilty compromise!
                    else:
                        input_ids.extend(ids)
                    for i in input_ids:
                        try:
                            # nt.links.new(b_nodes[k].outputs[int(output)], b_nodes[name].inputs[i])  # original
                            if is_material:
                                bpy.data.materials[self.b_mat_name_actual].node_tree.links.new(
                                    bpy.data.materials[self.b_mat_name_actual].node_tree.nodes[b_node_names[k]].outputs[
                                        int(output)],
                                    bpy.data.materials[self.b_mat_name_actual].node_tree.nodes[
                                        b_node_names[name]].inputs[i])  # test
                            elif is_nodegroup:
                                bpy.data.node_groups[nt_parent_name].links.new(
                                    bpy.data.node_groups[nt_parent_name].nodes[b_node_names[k]].outputs[int(output)],
                                    bpy.data.node_groups[nt_parent_name].nodes[b_node_names[name]].inputs[i])  # test
                        except Exception as e:
                            print('Failed to link')
                            print(e)

        for k, v in to_parent.items():
            try:
                if is_material:
                    bpy.data.materials[self.b_mat_name_actual].node_tree.nodes[b_node_names[k]].parent = \
                        bpy.data.materials[self.b_mat_name_actual].node_tree.nodes[b_node_names[v]]
                elif is_nodegroup:
                    bpy.data.node_groups[nt_parent_name].nodes[b_node_names[k]].parent = \
                        bpy.data.node_groups[nt_parent_name].nodes[b_node_names[v]]
                # Location of the frame, if shrink is active, depends on the location of the nodes parented to the frame
                # but the location of the nodes parented to the frame depends on the location of the frame
                # the end result is that the frame does not appear in correct position as when copied
                # tasking the location of a node and re-applying it after parenting to a frame does not solve the issue
            except Exception as e:
                print('Failed to parent node')
                print(e)


class OBJECT_MT_ns_copy_material(bpy.types.Operator):
    """Node Sharer: Copy complete material node setup as text string"""  # Use this as a tooltip for menu items and buttons.
    bl_idname = "node.ns_copy_material"  # Unique identifier for buttons and menu items to reference.
    bl_label = "Copy material as text string"  # Display name in the interface.
    bl_options = {'REGISTER'}  # 

    def execute(self, context):  # execute() is called when running the operator.

        my_mat = NS_material(context.material)
        my_mat.print_tree()
        ns_string, length = my_mat.compress()
        bpy.types.Scene.ns_string = ns_string
        text = 'Copied material as Node Sharer text string to clipboard. Text length: ' + str(length)
        self.report({'INFO'}, text)

        return {'FINISHED'}  # Lets Blender know the operator finished successfully.


class OBJECT_MT_ns_paste_material(bpy.types.Operator):
    """Node Sharer: Paste complete material node setup from text string"""  # Use this as a tooltip for menu items and buttons.
    bl_idname = "node.ns_paste_material"  # Unique identifier for buttons and menu items to reference.
    bl_label = "Paste material from text string in clipboard"  # Display name in the interface.
    bl_options = {'REGISTER'}  #

    def execute(self, context):  # execute() is called when running the operator.
        print('Paste material')

        new_mat = NS_mat_constructor(bpy.context.window_manager.clipboard)
        try:
            text = 'Pasted material from Node Sharer text string. Material name: ' + str(new_mat.b_mat.name)
            level = 'INFO'
        except AttributeError:
            text = "Failed to paste material, make sure it\'s an actual Node Sharer text string"
            level = 'ERROR'
        self.report({level}, text)

        return {'FINISHED'}  # Lets Blender know the operator finished successfully.


def menu_func(self, context):
    self.layout.operator(OBJECT_MT_ns_copy_material.bl_idname)
    self.layout.operator(OBJECT_MT_ns_paste_material.bl_idname)


def register():
    print("\n =============================================== \n")
    bpy.types.Scene.ns_string = bpy.props.StringProperty(name = "NodeString", default="")
    bpy.utils.register_class(OBJECT_MT_ns_copy_material)
    bpy.utils.register_class(OBJECT_MT_ns_paste_material)
    bpy.types.NODE_MT_node.append(menu_func)
    print("registered Add-on: Node Sharer")
    print("\n =============================================== \n")


def unregister():
    bpy.utils.unregister_class(OBJECT_MT_ns_copy_material)
    bpy.utils.unregister_class(OBJECT_MT_ns_paste_material)
    bpy.types.NODE_MT_node.remove(menu_func)
    print("unregistered Add-on: Node Sharer")


# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
if __name__ == "__main__":
    register()
