import bpy
import sys
import os
import importlib.util

# TLフォルダの絶対パスを取得
addon_dir = r"c:\Program Files\Blender Foundation\Blender 4.4\4.4\scripts\addons_core\TL"
level_editor_dir = os.path.join(addon_dir, "level_editor")

for p in [addon_dir, level_editor_dir]:
    if p not in sys.path:
        sys.path.insert(0, p)

# level_editor/__init__.py から直接登録処理を実行
init_path = os.path.join(level_editor_dir, "__init__.py")

spec = importlib.util.spec_from_file_location("level_editor", init_path)
level_editor_module = importlib.util.module_from_spec(spec)
sys.modules["level_editor"] = level_editor_module
spec.loader.exec_module(level_editor_module)

def register():
    level_editor_module.register()

def unregister():
    level_editor_module.unregister()

if __name__ == "__main__":
    register()
