import bpy

# オペレータ 無効オプション追加
class MYADDON_OT_add_disabled(bpy.types.Operator):
    bl_idname = "myaddon.add_disabled"
    bl_label = "無効オプション追加"
    bl_description = "オブジェクトに無効フラグを追加するオペレータ"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.active_object:
            context.active_object["disabled"] = True
            self.report({'INFO'}, "無効フラグを追加しました")
        return {'FINISHED'}

# パネル 無効オプション
class OBJECT_PT_disabled(bpy.types.Panel):
    bl_label = "Disabled"
    bl_idname = "OBJECT_PT_disabled"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    def draw(self, context):
        layout = self.layout
        obj = context.active_object
        if obj is None:
            return

        if "disabled" in obj:
            layout.prop(obj, '["disabled"]', text="disabled")
        else:
            layout.operator("myaddon.add_disabled", text="Add Disabled")
