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
    "version": (2, 1, 0),
    "blender": (2, 82, 0),
    "location": "Properties > Window > Render",
    "warning": "",
    "description": "Render Selected Frames",
    "category": "Render",
}


import bpy
from bpy.types import (Operator,
                        Panel,
                        PropertyGroup)


def getFrames(frames_string):
    frames = []
    splitted = frames_string.split(',')
    for s in splitted:
        if s.find('-') > -1:
            range_ends = s.split('-')
            start = int(range_ends[0])
            end = int(range_ends[1])

            for num in range(start,end):
                frames.append(num)

            frames.append(end)
        else:
            if s.isdigit():
                frames.append(int(s))

    return frames


class RenderSelectedFrames(PropertyGroup):
    selected_frames: bpy.props.StringProperty(
        name="Frames",
        default="",
        description="Frames to render, for example: 1,3-5,8",
        )


class RENDER_SELECTED_FRAMES_OT_operator(Operator):
    """Render Selected Frames"""
    bl_idname = "rsf_ot.render_frames"
    bl_label = "Render Frames"

    _timer = None
    frames_list = []
    current_index = 0
    path = ""

    def cancel(self, context):                
        context.window_manager.event_timer_remove(self._timer)
        context.scene.render.filepath = self.path

    def execute(self, context):
        self.current_index = 0

        scene = context.scene
        scene.render.image_settings.file_format = 'PNG'
        self.path = scene.render.filepath

        rsf = scene.render_selected_frames
        selected_frames = rsf.selected_frames

        if selected_frames == '':
            self.report({'WARNING'}, "Choose frames to render first")
            return {'CANCELLED'}
        else:
            self.frames_list = getFrames(selected_frames)

            wm = context.window_manager
            self._timer = wm.event_timer_add(time_step=0.01, window=context.window)
            wm.modal_handler_add(self)

            return {'RUNNING_MODAL'}

    def modal(self, context, event):
        if event.type == 'ESC':
            self.cancel(context)

            last_rendered = self.frames_list[self.current_index - 1]
            print(f"cancelled after frame: {last_rendered}")
            self.report({'WARNING'}, f"Rendering stopped. The last renderred frame: {last_rendered}")

            return {'CANCELLED'}

        elif event.type == 'TIMER':
            if self.current_index < len(self.frames_list):
                scene = context.scene
                frame = self.frames_list[self.current_index]

                scene.frame_set(frame)
                scene.render.filepath = f"{self.path}{frame}"
                bpy.ops.render.render(write_still=True)

                self.current_index += 1

            else:
                self.cancel(context)
                print("finished")
                self.report({'WARNING'}, "Finished")

                return {'FINISHED'}

        return {"PASS_THROUGH"}


class RENDER_SELECTED_FRAMES_PT_panel(Panel):
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
        col.scale_y = 1.5
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
    for c in reversed(classes):
        bpy.utils.unregister_class(c)

    del bpy.types.Scene.render_selected_frames


if __name__ == "__main__":
    register()
