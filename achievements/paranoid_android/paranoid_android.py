import time
from achievement_class import *
class ParanoidAndroid(AchievementData):
    name = "Paranoid Android"
    description= "Save at least 3 times in a minute"
    internal_name = "paranoid_android"
    current_progress = 0
    max_progress = 1
    save_timestamps = []
    def check_last_saves_time_stamps(self,path,blend_file):
        if self.completed:
            return
        if len(self.save_timestamps)  >= 3:
            del self.save_timestamps.remove[0]
        else:
            self.save_timestamps.append(time.time())

        if len(self.save_timestamps) < 3:
            return
        
        last_three_are_in_minute = True
        current_time = time.time()
        for timestamp in self.save_timestamps:
            print(current_time -timestamp)
            if current_time -60 > timestamp:
                last_three_are_in_minute = False
        
        if last_three_are_in_minute:
            self.current_progress = 1
            self.completed = True
            self.save_data()
            self.unregister_handles()
        
    def register_handles(self):
        if self.completed:
            return
        if self.check_last_saves_time_stamps not in bpy.app.handlers.save_post:
            bpy.app.handlers.save_post.append(self.check_last_saves_time_stamps)
    def unregister_handles(self):
        if self.check_last_saves_time_stamps in bpy.app.handlers.save_post:
            bpy.app.handlers.save_post.remove(self.check_last_saves_time_stamps)