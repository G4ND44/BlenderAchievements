from achievement_class import *
import bpy

class NobodyGotTimeForThat(AchievementData):
    name = "Ain't nobody got time for that"
    description= "Use Smart UV for unwrapping"
    internal_name = "nobody_got_time_for_that"
    current_progress = 0
    max_progress = 1
    def check_if_smart_uv_was_used(self,scene,deps_graph):
        if self.completed:
            return
        if bpy.context.active_operator:
            op = bpy.context.active_operator
            if op.bl_idname == 'UV_OT_smart_project':
                self.current_progress = 1
                self.completed = True
                self.unregister_handles()

    def register_handles(self):
        if self.completed:
            return
        if self.check_if_smart_uv_was_used not in bpy.app.handlers.depsgraph_update_post:
            bpy.app.handlers.depsgraph_update_post.append(self.check_if_smart_uv_was_used)
    def unregister_handles(self):
        if self.check_if_smart_uv_was_used in bpy.app.handlers.depsgraph_update_post:
            bpy.app.handlers.depsgraph_update_post.remove(self.check_if_smart_uv_was_used)