# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####


bl_info = {
    "name": "Render Selected Frames",
    "author": "Agnieszka Pas",
    "version": (2, 0, 0),
    "blender": (2, 81, 0),
    "location": "Properties > Window > Render",
    "warning": "",
    "description": "Render Selected Frames",
    "category": "Render",
}


import bpy


class RenderSelectedFrames(bpy.types.PropertyGroup):
    selected_frames: bpy.props.StringProperty(
        name="Frames",
        default="",
        description="Frames to render, for example: 1,3-5,8")


class RENDER_SELECTED_FRAMES_OT_operator(bpy.types.Operator):
    """Render Selected Frames"""
    bl_idname = "rsf_ot.render_frames"
    bl_label = "Render Frames"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        path = scene.render.filepath
        scene.render.image_settings.file_format = 'PNG'

        rsf = scene.render_selected_frames
        selected_frames = rsf.selected_frames
        frames_list = []

        if selected_frames == '':
            self.report({'WARNING'}, "Choose frames to render first")
            return {'CANCELLED'}
        else:
            splitted = selected_frames.split(',')
            for s in splitted:
                if s.find('-') > -1:
                    range_ends = s.split('-')
                    start = int(range_ends[0])
                    end = int(range_ends[1])

                    for num in range(start,end):
                        frames_list.append(num)

                    frames_list.append(end)
                else:
                    if s.isdigit():
                        frames_list.append(int(s))

            for frame in frames_list:
                scene.frame_set(frame)
                scene.render.filepath = path + str(frame)
                bpy.ops.render.render(write_still=True)

            scene.render.filepath = path
            return {'FINISHED'}


class RENDER_SELECTED_FRAMES_PT_panel(bpy.types.Panel):
    bl_idname = "RENDER_SELECTED_FRAMES_PT_panel"
    bl_label = "Render Selected Frames"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"
    bl_order = 101
    bl_options = {'DEFAULT_CLOSED'}
    COMPAT_ENGINES = {'CYCLES'}


    @classmethod
    def poll(cls, context):
        return context.scene

    
    def draw(self, context):
        scene = context.scene
        rsf = scene.render_selected_frames

        layout = self.layout
        col = layout.column()

        row = col.row()
        row.label(text="Frames:")
        col.prop(rsf, "selected_frames", text="")
        col.operator("rsf_ot.render_frames", text="Render Frames")


classes = (
    RenderSelectedFrames,
    RENDER_SELECTED_FRAMES_OT_operator,
    RENDER_SELECTED_FRAMES_PT_panel,
    )


def register():
    for c in classes:
        bpy.utils.register_class(c)
    
    bpy.types.Scene.render_selected_frames = bpy.props.PointerProperty(type=RenderSelectedFrames)


def unregister():
    del bpy.types.Scene.render_selected_frames
    for c in classes:
        bpy.utils.unregister_class(c)
