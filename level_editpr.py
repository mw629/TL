import bpy

bl_info = {
    "name": "レベルエディタ",
    "author": "Sybren A. Stüvel",
    "version": (4, 4),
    "blender": (4, 4, 0),
    "location": "N-panel in the 3D Viewport",
    "description": "レベルエディタ",
    "category": "Animation",
    "support": 'OFFICIAL',
    "doc_url": "{BLENDER_MANUAL_URL}/addons/animation/copy_global_transform.html",
}


def register():
    print("レベルエディタが有効化されました")

def unregister():
    print("レベルエディタが無効化されました。")

#テスト実行用コード
if __name__ == "__main__":
    register()