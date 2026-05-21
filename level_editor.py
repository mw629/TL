import bpy

def safe_print(*args, sep=" ", end="\n"):
    import sys
    text = sep.join(str(arg) for arg in args) + end
    try:
        import ctypes
        cp = f"cp{ctypes.windll.kernel32.GetConsoleOutputCP()}"
        sys.stdout.buffer.write(text.encode(cp, errors='replace'))
        sys.stdout.flush()
    except Exception:
        sys.stdout.write(text)
        sys.stdout.flush()

bl_info = {
    "name": "MyMenu",
    "author": "Taro Kamata",
    "version": (1, 0),
    "blender": (4, 4, 0),
    "location": "トップバー > MyMenu",
    "description": "拡張メニュー by Taro Kamata.",
    "category": "Development",
}

# オペレータ 頂点を伸ばす
class MYADDON_OT_stretch_vertex(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_stretch_vertex"
    bl_label = "頂点を伸ばす"
    bl_description = "頂点座標を引っ張って伸ばします"
    # リドゥ、アンドゥ可能オプション
    bl_options = {'REGISTER', 'UNDO'}

    # メニューを実行したときに呼ばれるコールバック関数
    def execute(self, context):
        if "Cube" in bpy.data.objects:
            bpy.data.objects["Cube"].data.vertices[0].co.x += 1.0
            safe_print("頂点を伸ばしました。")
        else:
            self.report({'ERROR'}, "Cubeという名前のオブジェクトが見つかりません。")
        
        # オペレータの命令終了を通知
        return {'FINISHED'}

# オペレータ ICO球生成
class MYADDON_OT_create_ico_sphere(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_create_object"
    bl_label = "ICO球生成"
    bl_description = "ICO球を生成します"
    bl_options = {'REGISTER', 'UNDO'}

    # メニューを実行したときに呼ばれるコールバック関数
    def execute(self, context):
        bpy.ops.mesh.primitive_ico_sphere_add()
        safe_print("ICO球を生成しました。")
        
        return {'FINISHED'}

# オペレータ シーン出力
class MYADDON_OT_export_scene(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_export_scene"
    bl_label = "シーン出力"
    bl_description = "シーン情報をExportします"

    def execute(self, context):
        import math
        safe_print("シーン情報をExportします")
        for obj in context.scene.objects:
            safe_print(f"{obj.type} - {obj.name}")
            safe_print(f"Trans({obj.location.x:.6f}, {obj.location.y:.6f}, {obj.location.z:.6f})")
            
            # Convert rotation euler from radians to degrees
            rot_x = math.degrees(obj.rotation_euler.x)
            rot_y = math.degrees(obj.rotation_euler.y)
            rot_z = math.degrees(obj.rotation_euler.z)
            safe_print(f"Rot({rot_x:.6f}, {rot_y:.6f}, {rot_z:.6f})")
            
            safe_print(f"Scale({obj.scale.x:.6f}, {obj.scale.y:.6f}, {obj.scale.z:.6f})")
            if obj.parent:
                safe_print(f"Parent:{obj.parent.name}")
            safe_print()
            
        safe_print("シーン情報をExportしました")
        self.report({'INFO'}, "シーン情報をExportしました")
        return {'FINISHED'}

# サブメニューのクラス定義
class TOPBAR_MT_my_menu(bpy.types.Menu):
    bl_label = "MyMenu"
    bl_idname = "TOPBAR_MT_my_menu"

    def draw(self, context):
        layout = self.layout
        # オペレータをメニューに追加
        layout.operator(MYADDON_OT_stretch_vertex.bl_idname, text=MYADDON_OT_stretch_vertex.bl_label)
        layout.operator(MYADDON_OT_create_ico_sphere.bl_idname, text=MYADDON_OT_create_ico_sphere.bl_label)
        layout.operator(MYADDON_OT_export_scene.bl_idname, text=MYADDON_OT_export_scene.bl_label)
        
        layout.separator()
        layout.operator("wm.url_open", text="マニュアル", icon='HELP').url = "https://docs.blender.org/"

# メニューを描画する関数
def draw_menu_manual(self, context):
    # トップバーに「MyMenu」という名前でサブメニューを追加
    self.layout.menu("TOPBAR_MT_my_menu", text="MyMenu")

# 登録対象のクラス
classes = (
    MYADDON_OT_stretch_vertex,
    MYADDON_OT_create_ico_sphere,
    MYADDON_OT_export_scene,
    TOPBAR_MT_my_menu,
)

# アドオン有効化時の処理
def register():
    import sys
    if sys.platform == 'win32':
        try:
            import ctypes
            ctypes.windll.kernel32.SetConsoleOutputCP(65001)
        except Exception:
            pass
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.TOPBAR_MT_editor_menus.append(draw_menu_manual)
    safe_print("MyMenuアドオンが有効化されました。")

# アドオン無効化時の処理
def unregister():
    bpy.types.TOPBAR_MT_editor_menus.remove(draw_menu_manual)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    safe_print("MyMenuアドオンが無効化されました。")

# テスト実行用
if __name__ == "__main__":
    register()
