import bpy
import sys
import os

# TLフォルダおよびlevel_editorフォルダの絶対パスを取得してsys.pathに登録
addon_dir = r"c:\Program Files\Blender Foundation\Blender 4.4\4.4\scripts\addons_core\TL"
if '__file__' in globals() and __file__:
    addon_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

level_editor_dir = os.path.join(addon_dir, "level_editor")
for p in [addon_dir, level_editor_dir]:
    if p not in sys.path:
        sys.path.insert(0, p)

# 各モジュールからクラスをインポート
try:
    from .stretch_vertex import MYADDON_OT_stretch_vertex
    from .create_ico_sphere import MYADDON_OT_create_ico_sphere
    from .import_scene import MYADDON_OT_import_scene
    from .export_scene import MYADDON_OT_export_scene
    from .my_menu import TOPBAR_MT_my_menu
    from .add_filename import MYADDON_OT_add_filename, OBJECT_PT_file_name
    from .add_collider import MYADDON_OT_add_collider, OBJECT_PT_collider
except ImportError:
    from stretch_vertex import MYADDON_OT_stretch_vertex
    from create_ico_sphere import MYADDON_OT_create_ico_sphere
    from import_scene import MYADDON_OT_import_scene
    from export_scene import MYADDON_OT_export_scene
    from my_menu import TOPBAR_MT_my_menu
    from add_filename import MYADDON_OT_add_filename, OBJECT_PT_file_name
    from add_collider import MYADDON_OT_add_collider, OBJECT_PT_collider

# アドオン情報
bl_info = {
    "name": "Level Editor",
    "author": "Taro Kamata",
    "version": (1, 0),
    "blender": (4, 4, 0),
    "location": "トップバー > MyMenu",
    "description": "レベルエディタ アドオン",
    "category": "Development",
}

# メニューをトップバーに描画する関数
def draw_menu(self, context):
    self.layout.menu("TOPBAR_MT_my_menu", text="MyMenu")

# Blenderに登録するクラスリスト
classes = (
    MYADDON_OT_stretch_vertex,
    MYADDON_OT_create_ico_sphere,
    MYADDON_OT_import_scene,
    MYADDON_OT_export_scene,
    TOPBAR_MT_my_menu,
    MYADDON_OT_add_filename,
    OBJECT_PT_file_name,
    MYADDON_OT_add_collider,
    OBJECT_PT_collider,
)

# アドオン有効化時の処理
def register():
    for cls in classes:
        try:
            bpy.utils.register_class(cls)
        except ValueError:
            pass
    bpy.types.TOPBAR_MT_editor_menus.append(draw_menu)
    print("Level Editorアドオンが有効化されました。")

# アドオン無効化時の処理
def unregister():
    bpy.types.TOPBAR_MT_editor_menus.remove(draw_menu)
    for cls in reversed(classes):
        try:
            bpy.utils.unregister_class(cls)
        except RuntimeError:
            pass
    print("Level Editorアドオンが無効化されました。")

if __name__ == "__main__":
    register()
