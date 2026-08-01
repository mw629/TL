import bpy
import bpy_extras

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
class MYADDON_OT_export_scene(bpy.types.Operator, bpy_extras.io_utils.ExportHelper):
    bl_idname = "myaddon.myaddon_ot_export_scene"
    bl_label = "シーン出力"
    bl_description = "シーン情報をExportします"

    # 出力するファイルの拡張子
    filename_ext = ".scene"

    def write_and_print(self, file, text):
        file.write(text + "\n")
        safe_print(text)

    def parse_scene_recursive(self, file, object, level):
        indent = " " * (level * 4)
        
        self.write_and_print(file, indent + object.type)
        
        trans = object.location
        
        import math
        import mathutils
        rot = mathutils.Vector((math.degrees(object.rotation_euler.x), math.degrees(object.rotation_euler.y), math.degrees(object.rotation_euler.z)))
        
        scale = object.scale
        
        # トランスフォーム情報を表示
        self.write_and_print(file, indent + "T %f %f %f" % (trans.x, trans.y, trans.z))
        self.write_and_print(file, indent + "R %f %f %f" % (rot.x, rot.y, rot.z))
        self.write_and_print(file, indent + "S %f %f %f" % (scale.x, scale.y, scale.z))
        # カスタムプロパティ'file_name'
        if "file_name" in object:
            self.write_and_print(file, indent + "N %s" % object["file_name"])
        self.write_and_print(file, indent + 'END')
        self.write_and_print(file, '')

        # 子ノードへ進む（深さが1上がる）
        for child in object.children:
            self.parse_scene_recursive(file, child, level + 1)

    def export(self, context):
        """ファイルに出力"""
        safe_print("シーン情報出力開始... %r" % self.filepath)
        
        with open(self.filepath, "wt", encoding="utf-8") as file:
            self.write_and_print(file, "SCENE")
            self.write_and_print(file, "")
            
            # ルートオブジェクト（親がないオブジェクト）を抽出
            root_objects = [obj for obj in context.scene.objects if obj.parent is None]
            
            # すべてのルートオブジェクトから再帰出力を開始
            for obj in root_objects:
                self.parse_scene_recursive(file, obj, 0)

    def execute(self, context):
        safe_print("シーン情報をExportします")
        
        self.export(context)
        
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

# オペレータ カスタムプロパティ['file_name']追加
class MYADDON_OT_add_filename(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_add_filename"
    bl_label = "FileName 追加"
    bl_description = "['file_name']カスタムプロパティを追加します"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # ['file_name']カスタムプロパティを追加
        context.object["file_name"] = ""
        return {'FINISHED'}


# パネル ファイル名
class OBJECT_PT_file_name(bpy.types.Panel):
    """オブジェクトのファイルネームパネル"""
    bl_idname = "OBJECT_PT_file_name"
    bl_label = "FileName"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"

    # サブメニューの描画
    def draw(self, context):
        # パネルに項目を追加
        if "file_name" in context.object:
            # 既にプロパティがあれば、プロパティを表示
            self.layout.prop(context.object, '["file_name"]', text=self.bl_label)
        else:
            # プロパティがなければ、プロパティ追加ボタンを表示
            self.layout.operator(MYADDON_OT_add_filename.bl_idname)


# Blenderに登録するクラスリスト
classes = (
    MYADDON_OT_stretch_vertex,
    MYADDON_OT_create_ico_sphere,
    MYADDON_OT_export_scene,
    TOPBAR_MT_my_menu,
    MYADDON_OT_add_filename,
    OBJECT_PT_file_name,
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
