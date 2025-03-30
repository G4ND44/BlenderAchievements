from achievement_class import *
class CubeSlayer(AchievementData):
    name = "Cube Slayer"
    description= "Delete 1000 cubes"
    internal_name = "cube_slayer"
    current_progress = 0
    max_progress = 1000
    previous_cube_count = 0
    def reset_on_load(self,scene,deps_graph):
        self.previous_cube_count = 0
    def track_cubes_count(self,scene,deps_graph):
        if self.completed:
            return
        current_cube_count = sum(1 for obj in bpy.context.scene.objects if obj.type == 'MESH' and obj.name.startswith("Cube"))
        if current_cube_count < self.previous_cube_count:
            self.current_progress += (self.previous_cube_count - current_cube_count)
            print(self.current_progress)
        if self.current_progress >= self.max_progress:
            self.current_progress = self.max_progress
            self.completed = True
            self.unregister_handles()
        self.previous_cube_count = current_cube_count
    ##########################
    def register_handles(self):
        if self.completed:
            return
        if self.reset_on_load not in bpy.app.handlers.load_post:
            bpy.app.handlers.load_post.append(self.reset_on_load)
        if self.track_cubes_count not in bpy.app.handlers.depsgraph_update_post:
            bpy.app.handlers.depsgraph_update_post.append(self.track_cubes_count)
    def unregister_handles(self):
        if self.reset_on_load in bpy.app.handlers.load_post:
            bpy.app.handlers.load_post.remove(self.reset_on_load)
        if self.track_cubes_count in bpy.app.handlers.depsgraph_update_post:
            bpy.app.handlers.depsgraph_update_post.remove(self.track_cubes_count)