
import bpy
import sys
import os
import importlib.util
from pathlib import Path
import inspect
import threading
import gpu
from gpu_extras.batch import batch_for_shader
from time import perf_counter
################# 
plugin_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(plugin_path)
_draw_handler = None
_texture = None
_shader = None
_timer = None
_last_achievement = None
_enabled = False
_time_stamp = 0.0
popup_max_time = 8.0
#######################
from achievement_class import *
bl_info = {
    "name": "Blender Achivements",
    "description": "Blender Achievements system for tracking your progress",
    "author": "Bartlomiej Gadzala",
    "version": (0, 5, 0),
    "blender": (4, 2, 3),
    "location": "View3D > Sidebar",
    "tracker_url": "https://github.com/G4ND44/BlenderAchievements",
    "category": "Object",
}
imported_achievements = []
achievements_popup_array = []
def register_all_achievements():
    achievements_dir = os.path.join(plugin_path, "achievements")
    folder_path = Path(achievements_dir)

    for subfolder in folder_path.iterdir():
        if subfolder.is_dir():
            achievements_files = [f for f in os.listdir(subfolder) if f.endswith(".py") and f != "__init__.py"]
            for achievements_file in achievements_files:
                file = achievements_file[:-3]  # Remove ".py"
                if os.path.basename(subfolder) == file: #accept only file that have same name as subfolder
                    module_path = os.path.join(subfolder, achievements_file)
                    spec  = importlib.util.spec_from_file_location(file, module_path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    for name, obj in inspect.getmembers(module, inspect.isclass):
                        #Check if it is a subclass of AchievementData but not AchievementData itself
                        if issubclass(obj, AchievementData) and obj is not AchievementData:
                            achievement = obj()  # Instantiate the achievement
                            achievement.register()
                            imported_achievements.append(achievement)

space_type = 'VIEW_3D'
region_type = 'UI'
category = "Achievements"
class VIEW3D_PT_AchievementsPanelCompleted(bpy.types.Panel):
    bl_label = "Completed"
    bl_idname = "VIEW3D_PT_AchievementsPanelCompleted"
    bl_space_type = space_type
    bl_region_type = region_type
    bl_category = category

    def draw(self, context):
        layout = self.layout
        for achievement in imported_achievements:
            if achievement.completed:
                achievement.draw_window_props(context,layout)
class VIEW3D_PT_AchievementsPanelNotCompleted(bpy.types.Panel):
    bl_label = "Pending"
    bl_idname = "VIEW3D_PT_AchievementsPanelNotCompleted"
    bl_space_type = space_type
    bl_region_type = region_type
    bl_category = category

    def draw(self, context):
        layout = self.layout
        for achievement in imported_achievements:
            if not achievement.completed:
                achievement.draw_window_props(context,layout)

def achievements_popup_draw():
    global _texture, _shader,_last_achievement, _time_stamp
    if _last_achievement is None:
        return 
    img = _last_achievement.load_popup_image()
    _texture = gpu.texture.from_image(img) if img else None
    if not img or _texture is None or _shader is None:
        return
    width, height = img.size
    time_elapsed = perf_counter() - _time_stamp
    normalized_time_elapsed = time_elapsed/popup_max_time
    x = 0  # Offset from bottom-left corner
    y = 0
    if normalized_time_elapsed <= 0.25:
        y = (1.0 - normalized_time_elapsed * 4.0) * width * (-1)
    elif normalized_time_elapsed >= 0.75:
        y = ((normalized_time_elapsed-0.75) * 4.0) * width * (-1)
    batch = batch_for_shader(_shader, 'TRI_FAN', {
        "pos": [(x, y), (x + width, y), (x + width, y + height), (x, y + height)],
        "texCoord": [(0, 0), (1, 0), (1, 1), (0, 1)]
    })
    gpu.state.blend_set("ALPHA")  # Enable transparency
    _shader.bind()

    if _texture:
        _shader.uniform_sampler("image", _texture)  # Properly bind the texture
    batch.draw(_shader)
def achievements_popup_show():
    global _draw_handler, _shader, _timer,_texture, _last_achievement, _time_stamp
    for achievement in imported_achievements:
        if achievement.completed and not achievement.popped:
            achievement.popped = True
            achievement.save_data()
            achievements_popup_array.append(achievement)
    if _draw_handler is not None or _last_achievement is not None or len(achievements_popup_array) == 0:
        return
    _last_achievement  = achievements_popup_array.pop()
    _shader = gpu.shader.from_builtin('IMAGE_COLOR')
    if not _shader:
        return
    img = _last_achievement.load_popup_image()
    if img is None:
        return (
    img.preview_ensure())
    _texture = gpu.texture.from_image(img) if img else None
    if img:
        _draw_handler = bpy.types.SpaceView3D.draw_handler_add(
            achievements_popup_draw, (), 'WINDOW', 'POST_PIXEL'
        )
        _timer = threading.Timer(popup_max_time, achievements_popup_hide) #Showup popup for 5 sec
        _time_stamp  = perf_counter()
        _timer.start()
def execute(): # constant loop
    achievements_popup_show()
    return 0.5 # 0.5 sec interval
def achievements_popup_hide():
    global _draw_handler, _texture, _shader, _timer,_last_achievement
    if _draw_handler is not None:
        bpy.types.SpaceView3D.draw_handler_remove(_draw_handler, 'WINDOW')
        _draw_handler = None
    if _texture:
        _texture = None 
    if _shader:
        _shader = None 
    if _timer:
        _timer.cancel()
        _timer = None
    if _last_achievement:
        _last_achievement = None
        
window_classes = [VIEW3D_PT_AchievementsPanelCompleted, VIEW3D_PT_AchievementsPanelNotCompleted]
def register():
    global _enabled
    for cls in window_classes:
        bpy.utils.register_class(cls)
    register_all_achievements()
    _enabled = True
    if not bpy.app.timers.is_registered(execute):
        bpy.app.timers.register(execute)

def unregister():
    global _timer,_enabled
    _timer = None
    _enabled = False
    for cls in window_classes:
        bpy.utils.unregister_class(cls)
    while imported_achievements:
        achievement = imported_achievements.pop(0)
        achievement.unregister()
    if bpy.app.timers.is_registered(execute):
        bpy.app.timers.unregister(execute)

if __name__ == "__main__":
    register()