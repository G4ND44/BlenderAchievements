from achievement_class import *
import datetime
class SleepNotFound(AchievementData):
    name = "404 Sleep Not Found"
    description= "Have Blender open at 4:04 am local time"
    internal_name = "sleep_not_found"
    current_progress = 0
    max_progress = 1
    _timer = None

    def trigger_at_time(self):
        self.current_progress = 1
        self.completed = True
        self.unregister_handles()

    def register_handles(self):
        if self.completed:
            return 
        now = datetime.datetime.now()
        target_time = now.replace(hour=4, minute=4, second=0, microsecond=0)
        if target_time < now:
            target_time += datetime.timedelta(days=1)
        time_difference = target_time - now
        bpy.app.timers.register(self.trigger_at_time,first_interval=time_difference.total_seconds(),persistent=True)

        
    def unregister_handles(self):
        if bpy.app.timers.is_registered(self.trigger_at_time):
            bpy.app.timers.unregister(self.trigger_at_time)

