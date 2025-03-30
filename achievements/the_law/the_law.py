from achievement_class import *
import bpy
class TheLaw(AchievementData):
    name = "It is a law!"
    description= "Add new cube immediately after deleting the default one"
    internal_name = "the_law"
    current_progress = 0
    max_progress = 1
    default_cube_unique_id = -1
    def reset_unique_id_on_load(self,scene,deps_graph):
        default_cube_unique_id = -1
    def check_if_cube_was_deleted(self,scene,deps_graph):
        if self.completed:
            return
        if  self.default_cube_unique_id == -1:
            for obj in bpy.context.scene.objects:
                if obj.type == 'MESH' and obj.name == 'Cube' and obj.name_full=='Cube' and self.default_cube_unique_id == -1:
                    self.default_cube_unique_id = obj.as_pointer()
        else:
            cube_has_been_deleted = True
            for obj in bpy.context.scene.objects:
                if  self.default_cube_unique_id == obj.as_pointer():
                    cube_has_been_deleted = False
            if cube_has_been_deleted:
                if bpy.context.active_operator:
                    op = bpy.context.active_operator
                    if op.bl_idname == 'MESH_OT_primitive_cube_add':
                        self.current_progress = 1
                        self.completed = True
                        self.unregister_handles()
    def register_handles(self):
        if self.completed:
            return
        if self.reset_unique_id_on_load not in bpy.app.handlers.load_post:
            bpy.app.handlers.load_post.append(self.reset_unique_id_on_load)
        if self.check_if_cube_was_deleted not in bpy.app.handlers.depsgraph_update_post:
            bpy.app.handlers.depsgraph_update_post.append(self.check_if_cube_was_deleted)
    def unregister_handles(self):
        if self.reset_unique_id_on_load in bpy.app.handlers.load_post:
            bpy.app.handlers.load_post.remove(self.reset_unique_id_on_load)
        if self.check_if_cube_was_deleted in bpy.app.handlers.depsgraph_update_post:
            bpy.app.handlers.depsgraph_update_post.remove(self.check_if_cube_was_deleted)