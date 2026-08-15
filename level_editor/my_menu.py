import bpy


# サブメニューのクラス定義
class TOPBAR_MT_my_menu(bpy.types.Menu):
    bl_label = "MyMenu"
    bl_idname = "TOPBAR_MT_my_menu"

    def draw(self, context):
        layout = self.layout
        layout.operator("myaddon.stretch_vertex", text="頂点を伸ばす")
        layout.operator("myaddon.create_ico_sphere", text="ICO球生成")
        layout.operator("myaddon.export_scene", text="シーン出力")
        layout.operator("myaddon.import_scene", text="シーン入力")
        layout.operator(
            "myaddon.spawn_create_enemy_symbol", text="敵出現ポイントシンボルの作成"
        )
        layout.operator(
            "myaddon.spawn_create_player_symbol",
            text="プレイヤー出現ポイントシンボルの作成",
        )
        layout.separator()
        layout.operator(
            "wm.url_open", text="マニュアル", icon='HELP'
        ).url = "https://docs.blender.org/"
