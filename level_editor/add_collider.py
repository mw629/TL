import bpy

# オペレータ コライダー追加
class MYADDON_OT_add_collider(bpy.types.Operator):
    bl_idname = "myaddon.add_collider"
    bl_label = "コライダー追加"
    bl_description = "オブジェクトにコライダーを追加するオペレータ"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        self.report({'INFO'}, "コライダーを追加しました")
        return {'FINISHED'}

# パネル コライダー設定
class OBJECT_PT_collider(bpy.types.Panel):
    bl_label = "コライダー設定"
    bl_idname = "OBJECT_PT_collider"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    def draw(self, context):
        layout = self.layout
        layout.operator("myaddon.add_collider", text="コライダー追加")
