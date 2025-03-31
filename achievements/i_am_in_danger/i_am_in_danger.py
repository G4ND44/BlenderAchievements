from achievement_class import *
import bpy

class IAmInDanger(AchievementData):
    name = "I am in danger"
    description= "Apply a Subdivision Surface modifier with level 6"
    internal_name = "i_am_in_danger"
    current_progress = 0
    max_progress = 1
    def check_if_cube_was_deleted(self,scene,deps_graph):
        if self.completed:
            return
        for obj in bpy.context.selected_objects:
            for mod in obj.modifiers:
                print(mod)
                if mod.type == 'SUBSURF':
                    if mod.levels >= 6:
                        self.current_progress = 1
                        self.completed = 1
                        self.save_data()
                        self.unregister_handles()
    def register_handles(self):
        if self.completed:
            return
        if self.check_if_cube_was_deleted not in bpy.app.handlers.depsgraph_update_post:
            bpy.app.handlers.depsgraph_update_post.append(self.check_if_cube_was_deleted)
    def unregister_handles(self):
        if self.check_if_cube_was_deleted in bpy.app.handlers.depsgraph_update_post:
            bpy.app.handlers.depsgraph_update_post.remove(self.check_if_cube_was_deleted)