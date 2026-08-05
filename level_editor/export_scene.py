import bpy
import bpy_extras.io_utils
import json
import math

# オペレータ シーンエクスポート (JSON形式出力)
class MYADDON_OT_export_scene(bpy.types.Operator, bpy_extras.io_utils.ExportHelper):
    bl_idname = "myaddon.export_scene"
    bl_label = "シーンエクスポート"
    bl_description = "シーンのノードツリーや属性情報をJSONファイルとしてエクスポートします"
    bl_options = {'REGISTER', 'UNDO'}

    # 出力するファイルの拡張子
    filename_ext = ".json"

    filter_glob: bpy.props.StringProperty(
        default="*.json",
        options={'HIDDEN'},
        maxlen=255,
    )

    def parse_object_recursive(self, obj):
        """オブジェクトとその子要素を再帰的にJSON辞書構造へ変換"""
        object_data = {
            "name": obj.name,
            "type": obj.type
        }

        # カスタムプロパティ 'file_name' があれば出力データに追加
        if "file_name" in obj:
            object_data["file_name"] = obj["file_name"]

        # トランスフォーム情報 (位置, 回転, スケール)
        trans = obj.location
        rot = [
            math.degrees(obj.rotation_euler.x),
            math.degrees(obj.rotation_euler.y),
            math.degrees(obj.rotation_euler.z)
        ]
        scale = obj.scale

        object_data["transform"] = {
            "translation": [trans.x, trans.y, trans.z],
            "rotation": rot,
            "scaling": [scale.x, scale.y, scale.z]
        }

        # コライダー情報がある場合は追加
        if "collider" in obj or "collider_type" in obj:
            collider_type = obj.get("collider_type", "BOX")
            center = list(obj.get("collider_center", [0.0, 0.0, 0.0]))
            size = list(obj.get("collider_size", [1.0, 1.0, 1.0]))
            object_data["collider"] = {
                "type": collider_type,
                "center": center,
                "size": size
            }

        # 子オブジェクトを再帰的に処理
        if len(obj.children) > 0:
            object_data["children"] = [
                self.parse_object_recursive(child) for child in obj.children
            ]

        return object_data

    def export(self, context):
        """JSONデータを作成してファイルに出力"""
        scene_data = {
            "name": "scene",
            "objects": []
        }

        # 親を持たないルートオブジェクトを取得
        root_objects = [obj for obj in context.scene.objects if obj.parent is None]

        # ルートオブジェクトごとに再帰処理
        for obj in root_objects:
            scene_data["objects"].append(self.parse_object_recursive(obj))

        # 指定されたファイルパスへJSON保存
        with open(self.filepath, "w", encoding="utf-8") as file:
            json.dump(scene_data, file, indent=4, ensure_ascii=False)

        print("シーン情報をJSON形式で出力しました: %r" % self.filepath)

    def execute(self, context):
        self.export(context)
        self.report({'INFO'}, "JSON形式でシーンをエクスポートしました")
        return {'FINISHED'}
