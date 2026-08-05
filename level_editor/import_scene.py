import bpy

# オペレータ シーンインポート
class MYADDON_OT_import_scene(bpy.types.Operator):
    bl_idname = "myaddon.import_scene"
    bl_label = "シーンインポート"
    bl_description = "シーンデータをインポートするオペレータ"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        self.report({'INFO'}, "シーンをインポートしました")
        return {'FINISHED'}
