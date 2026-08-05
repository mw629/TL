import bpy

# サブメニューのクラス定義
class TOPBAR_MT_my_menu(bpy.types.Menu):
    bl_label = "MyMenu"
    bl_idname = "TOPBAR_MT_my_menu"

    def draw(self, context):
        layout = self.layout
        layout.operator("myaddon.stretch_vertex", text="頂点を伸ばす")
        layout.operator("myaddon.create_ico_sphere", text="ICO球作成")
        layout.operator("myaddon.import_scene", text="シーンインポート")
        layout.operator("myaddon.export_scene", text="シーンエクスポート")
        layout.separator()
        layout.operator("wm.url_open", text="マニュアル", icon='HELP').url = "https://docs.blender.org/"
