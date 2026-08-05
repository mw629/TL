import bpy

# オペレータ ファイル名追加
class MYADDON_OT_add_filename(bpy.types.Operator):
    bl_idname = "myaddon.add_filename"
    bl_label = "ファイル名追加"
    bl_description = "オブジェクトにファイル名を追加するオペレータ"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        self.report({'INFO'}, "ファイル名を追加しました")
        return {'FINISHED'}

# パネル ファイル名設定
class OBJECT_PT_file_name(bpy.types.Panel):
    bl_label = "ファイル名設定"
    bl_idname = "OBJECT_PT_file_name"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    def draw(self, context):
        layout = self.layout
        layout.operator("myaddon.add_filename", text="ファイル名追加")
