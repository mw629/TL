import bpy
import bpy_extras.io_utils
import os


# オペレータ 出現ポイントのシンボルを読み込む
class MYADDON_OT_spawn_import_symbol(
    bpy.types.Operator, bpy_extras.io_utils.ImportHelper
):
    bl_idname = "myaddon.spawn_import_symbol"
    bl_label = "出現ポイントシンボルImport"
    bl_description = "出現ポイントのシンボルをファイルダイアログから選択してImportします"

    # ファイル選択ダイアログの拡張子フィルター
    filename_ext = ".obj"

    filter_glob: bpy.props.StringProperty(
        default="*.obj",
        options={'HIDDEN'},
        maxlen=255,
    )

    prototype_object_name = "PrototypePlayerSpawn"
    object_name = "PlayerSpawn"

    def execute(self, context):
        print(f"出現ポイントのシンボルをImportします: {self.filepath}")

        # 重複ロード防止
        spawn_object = bpy.data.objects.get(
            MYADDON_OT_spawn_import_symbol.prototype_object_name
        )
        if spawn_object is not None:
            self.report({'INFO'}, "プロトタイプオブジェクトは既に読み込まれています")
            return {'CANCELLED'}

        # filepathが未設定（プログラムからの呼び出し時）の場合、デフォルトパスを使用
        if not self.filepath:
            addon_directory = os.path.dirname(__file__)
            self.filepath = os.path.join(addon_directory, "player", "player.obj")

        full_path = self.filepath

        if not os.path.exists(full_path):
            self.report({'ERROR'}, f"モデルファイルが見つかりません: {full_path}")
            return {'CANCELLED'}

        # オブジェクトをインポート
        bpy.ops.wm.obj_import(
            'EXEC_DEFAULT',
            filepath=full_path,
            display_type='THUMBNAIL',
            forward_axis='Z',
            up_axis='Y',
        )

        # 回転を適用
        bpy.ops.object.transform_apply(
            location=False,
            rotation=True,
            scale=False,
            properties=False,
            isolate_users=False,
        )

        # アクティブなオブジェクトを取得
        object = bpy.context.active_object

        # オブジェクト名を変更
        object.name = MYADDON_OT_spawn_import_symbol.prototype_object_name

        # オブジェクトの種類を設定
        object["type"] = MYADDON_OT_spawn_import_symbol.object_name

        # メモリ上にはおいておくがシーンから外す
        bpy.context.collection.objects.unlink(object)

        return {'FINISHED'}


# オペレータ 出現ポイントのシンボルを作成・配置する
class MYADDON_OT_spawn_create_symbol(bpy.types.Operator):
    bl_idname = "myaddon.spawn_create_symbol"
    bl_label = "出現ポイントシンボルの作成"
    bl_description = "出現ポイントのシンボルを作成します"
    bl_options = {'REGISTER', 'UNDO'}

    object_name = "PlayerSpawn"

    def execute(self, context):
        # 読み込み済みのコピー元オブジェクトを検索
        spawn_object = bpy.data.objects.get(
            MYADDON_OT_spawn_import_symbol.prototype_object_name
        )

        # まだ読み込んでいない場合
        if spawn_object is None:
            # 読み込みオペレータを実行する
            bpy.ops.myaddon.spawn_import_symbol('EXEC_DEFAULT')
            # 再検索。今度は見つかるはず
            spawn_object = bpy.data.objects.get(
                MYADDON_OT_spawn_import_symbol.prototype_object_name
            )

        if spawn_object is None:
            self.report({'ERROR'}, "モデルの読み込みに失敗しました")
            return {'CANCELLED'}

        print("出現ポイントのシンボルを作成します")

        # Blenderでの選択を解除する
        bpy.ops.object.select_all(action='DESELECT')

        # 複製元の非表示オブジェクトを複製する
        object = spawn_object.copy()

        # 複製したオブジェクトを現在のシーンにリンク（出現させる）
        bpy.context.collection.objects.link(object)

        # オブジェクト名を変更
        object.name = MYADDON_OT_spawn_create_symbol.object_name

        return {'FINISHED'}
