import bpy

bl_info = {
    "name": "MyMenu",
    "author": "Taro Kamata",
    "version": (1, 0),
    "blender": (4, 4, 0),
    "location": "トップバー > MyMenu",
    "description": "拡張メニュー by Taro Kamata.",
    "category": "Development",
}

# サブメニューのクラス定義
class TOPBAR_MT_my_menu(bpy.types.Menu):
    bl_label = "MyMenu"
    bl_idname = "TOPBAR_MT_my_menu"

    def draw(self, context):
        layout = self.layout
        # 画像の通り「マニュアル」のみを表示
        layout.operator("wm.url_open", text="マニュアル", icon='HELP').url = "https://docs.blender.org/"

# メニューを描画する関数
def draw_menu_manual(self, context):
    # トップバーに「MyMenu」という名前でサブメニューを追加
    self.layout.menu("TOPBAR_MT_my_menu", text="MyMenu")

# アドオン有効化時の処理
def register():
    bpy.utils.register_class(TOPBAR_MT_my_menu)
    bpy.types.TOPBAR_MT_editor_menus.append(draw_menu_manual)
    print("MyMenuアドオンが有効化されました。")

# アドオン無効化時の処理
def unregister():
    bpy.types.TOPBAR_MT_editor_menus.remove(draw_menu_manual)
    bpy.utils.unregister_class(TOPBAR_MT_my_menu)
    print("MyMenuアドオンが無効化されました。")

# テスト実行用
if __name__ == "__main__":
    register()
