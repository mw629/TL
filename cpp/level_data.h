#pragma once

#include <string>
#include <vector>

namespace TL {

// 3次元ベクトル構造体
struct Vector3 {
    float x = 0.0f;
    float y = 0.0f;
    float z = 0.0f;
};

// 自キャラの生成データ (スライド3ページ)
struct PlayerSpawnData {
    // 平行移動
    Vector3 translation;
    // 回転角
    Vector3 rotation;
};

// 敵キャラの生成データ (スライド "オブジェクトの走査" 要件)
struct EnemySpawnData {
    // 平行移動
    Vector3 translation;
    // 回転角
    Vector3 rotation;
    // リソースファイル名
    std::string fileName = "";
};

// コライダーデータ構造体 (スライド4, 10ページの要件を統合)
struct ColliderData {
    std::string type = "";
    Vector3 center;
    Vector3 size;
    bool hasCollider = false;
};

// レベルデータ内の個々のオブジェクト配置データ
struct LevelData {
    struct ObjectData {
        std::string name = "";
        std::string type = "";
        std::string fileName = ""; // MESHタイプのファイル名 (スライド4ページ)
        
        // トランスフォーム情報 (スライド5ページ)
        Vector3 translation;
        Vector3 rotation;
        Vector3 scaling;

        // コライダー情報 (スライド4ページのTODO)
        ColliderData collider;
    };

    // シーン全体のオブジェクトリスト
    std::vector<ObjectData> objects;

    // 自キャラ配列 (スライド3ページ)
    std::vector<PlayerSpawnData> players;

    // 敵キャラ配列 (スライド "オブジェクトの走査" 要件)
    std::vector<EnemySpawnData> enemies;
};

} // namespace TL
