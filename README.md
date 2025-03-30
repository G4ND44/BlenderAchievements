# BlenderAchievements
Blender Achievements system for tracking your progress


## Installation

Download zip file from official release page or by downloading the whole repository. To install add-on in Blender, click the Install from Disk menu item and select the .zip file.

    
## Contributing

Contributions are always welcome!
The achievements are easy to add, but there are are some simple rules to remember:

> ### Guidelines:
> - All achievements need to be in the `achievements` folder.
> - Subfolders and .py files are need to be named with lowercase with no space
> - The .py file needs to be name the same as folder, same with `internal_name` variable
> - n achievement folder there are 3 img files that needs to be present: `unlocked_icon.png` , `popup_icon.png`, `not_unlocked_icon.png`
This is how folder structure should look assuming you adding achievement named `Example Achievement`:

    BlenderAchievements/
    ├──__init__.py
    ├── achievement_class.py 
    ├── achievements/
    │   ├── example_achievement
    │   │   ├── example_achievement.py
    │   │   ├── unlocked_icon.png
    │   │   ├── not_unlocked_icon.png
    │   │   ├── popup_icon.png
    │   ├── ...

Base `example_achievement.py` structure:

    from achievement_class import *
    class ExampleAchievement(AchievementData):
        name = "Example Achievement"
        description= ""
        internal_name = "example_achievement"
        current_progress = 0 # internal current progress of achievement
        max_progress = 1 # max progress of achievement

        def custom_behaviour(self,scene,deps_graph): #can be bind for example to bpy.app.handlers.depsgraph_update_post
            if self.completed:
                return

        def register_handles(self):
            if self.completed:
                return
            # register behaviour using bpy.app.handlers
        def unregister_handles(self):
            # unregister behaviour using bpy.app.handlers

`self.completed` and `self.current_progress` are automatically saved and loaded by `achievement_class`

If you want to bind any custom function you should use Blender bpy.app.handlers
https://docs.blender.org/api/current/bpy.app.handlers.html


### Adding graphics:
For popup images use `popup_image_template.psd`. Here you need to add custom icon, achievement name and achievement description. This template is used for `replacing popup_icon.png`.  `unlocked_icon.png` and `not_unlocked_icon.png` needs to be replaced as well


## Special Thanks

- Isiart Studio for providing the achievements icons [@isiart](https://isiart.pl/)

