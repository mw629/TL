import bpy

# オペレータ 頂点を伸ばす
class MYADDON_OT_stretch_vertex(bpy.types.Operator):
    bl_idname = "myaddon.stretch_vertex"
    bl_label = "頂点を伸ばす"
    bl_description = "メッシュの頂点を伸ばすオペレータ"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # アクティブオブジェクトの頂点を伸び縮みさせる処理
        obj = context.active_object
        if obj and obj.type == 'MESH':
            mesh = obj.data
            for vertex in mesh.vertices:
                vertex.co.z *= 2.0
        return {'FINISHED'}
