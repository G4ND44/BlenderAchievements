import json
import os
from dataclasses import dataclass, asdict, fields
import bpy
from bpy.app.handlers import persistent
from abc import ABC, abstractmethod
import atexit
import bpy.utils.previews

@dataclass
class AchivementProgress:
    current_progress: int
    completed: bool
    popped:bool

class AchievementData(ABC):
    name: str
    internal_name: str
    description: str
    currentProgress: int
    maxProgress: int
    completed: bool
    current_progress:int
    max_progress:int
    completed = False
    popped = False
    icons_previews : None
    def return_script_folder(self):
        script_path = os.path.abspath(__file__)
        script_folder = os.path.dirname(script_path)
        return script_folder + "\\Achievements\\" + self.internal_name + "\\"
    def return_json_path(self):
        return self.return_script_folder()+ "achievement_data.json"
    def return_popup_image_path(self):
        return self.return_script_folder()+"popup_icon.png"
    def return_not_unlocked_image_path(self):
        return self.return_script_folder()+"not_unlocked_icon.png"
    def return_unlocked_image_path(self):
        return self.return_script_folder()+"unlocked_icon.png"
    def load_popup_image(self):
        image_path = self.return_popup_image_path()
        img = bpy.data.images.get(image_path)
        if not img:
            img = bpy.data.images.load(image_path)
            img.name = image_path
        img.preview_ensure()
        return img
    def load_image(self,filepath):
        if self.icons_previews is None:
            return
        if filepath not in self.icons_previews:
            try:
                icon = self.icons_previews.load(filepath, filepath, 'IMAGE')
                return icon 
            except Exception as e:
                print(f"Failed to load image preview: {e}")
                return None
        else:
            return self.icons_previews[filepath]
    
    def save_data(self):
        data = AchivementProgress(
            current_progress=self.current_progress,
            completed=self.completed,
            popped=self.popped
        )
        with open(self.return_json_path(), "w") as f:
            json.dump(asdict(data), f, indent=6)  
    # Load data from JSON
    def load_data(self):
        path = self.return_json_path()
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as file:
                    data_dict = json.load(file)
                    self.current_progress = data_dict["current_progress"]
                    self.completed = data_dict["completed"]
                    self.popped= data_dict["popped"]
            except json.JSONDecodeError:
                self.save_data()
        else:
            self.save_data()


    def register_window_props(self,window_manager):
        expand_property = bpy.props.BoolProperty(self.internal_name+"_expand", default=False)
        setattr(window_manager, self.internal_name+"_expand", expand_property)


    def unregister_window_props(self,window_manager):
        delattr(window_manager, self.internal_name+"_expand")
    def draw_window_props(self,context,layout):
        col = layout.column()
        row = layout.row()
        row.label(text=self.name)
        row.label(text=str(self.current_progress) + "/" + str(self.max_progress))
        row.prop(context.window_manager, self.internal_name + "_expand", text="", icon='TRIA_DOWN')
        expand = getattr(context.window_manager, self.internal_name + "_expand")
        if not expand:
            return
        box = layout.box()
        if self.completed:
            unlocked_icon = self.load_image(self.return_unlocked_image_path())
            #if unlocked_icon and unlocked_icon.preview:
            if unlocked_icon:
                box.template_icon(icon_value=unlocked_icon.icon_id, scale=4)

        else:
            not_unlocked_icon = self.load_image(self.return_not_unlocked_image_path())
            if not_unlocked_icon:
                box.template_icon(icon_value=not_unlocked_icon.icon_id, scale=4)

        box = box.box()
        row = box.row()
        row.alignment = 'CENTER'
        row.label(text=self.description)

    @abstractmethod
    def register_handles(self):
        """Register Handlers Per Class"""
        pass
    @abstractmethod
    def unregister_handles(self):
        """Unregister Handlers Per Class"""
        pass

    def on_exit(self,path,blend_file):
        self.save_data()


    def register(self):
        if self.on_exit not in bpy.app.handlers.save_post:
            bpy.app.handlers.save_post.append(self.on_exit)
        atexit.register(self.on_exit)
        self.load_data()
        self.icons_previews = bpy.utils.previews.new()
        self.register_window_props(bpy.types.WindowManager)
        if not self.completed:
            self.register_handles()

    def unregister(self):
        self.unregister_handles()
        if self.on_exit in bpy.app.handlers.save_post:
            bpy.app.handlers.save_post.remove(self.on_exit)
       
        self.unregister_window_props(bpy.types.WindowManager)
        self.icons_previews.clear()
        self.icons_previews = None
        self.save_data()

            

  


