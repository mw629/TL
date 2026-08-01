#include "level_loader.h"
#include <fstream>
#include <cassert>
#include <iostream>

// json.hppが同じディレクトリやインクルードパスにあることを想定
// もしくはシングルヘッダー版のnlohmann/jsonを使用
#include "json.hpp"

namespace TL {

// デフォルトのベースディレクトリと拡張子定義 (スライド1ページ)
const std::string kDefaultBaseDirectory = "Resources/Levels/";
const std::string kExtension = ".json";

// オブジェクトの再帰走査関数 (スライド6ページ)
static void ParseObjectRecursive(const nlohmann::json& objectJson, LevelData* levelData) {
    // すべてのオブジェクトで "type" を含むかチェック (スライド3, 6ページ)
    assert(objectJson.contains("type"));
    
    // 種別を取得
    std::string type = objectJson["type"].get<std::string>();

    // MESHである場合の処理 (スライド4ページ)
    // ※スライド注記: 「本当はMESHを含めた全オブジェクトを追加するべき」に従い、MESH以外（EMPTYやCAMERA等）もオブジェクトとして追加します。
    levelData->objects.emplace_back(LevelData::ObjectData{});
    LevelData::ObjectData& objectData = levelData->objects.back();
    
    objectData.type = type;
    if (objectJson.contains("name")) {
        objectData.name = objectJson["name"].get<std::string>();
    }

    if (type == "MESH") {
        if (objectJson.contains("file_name")) {
            objectData.fileName = objectJson["file_name"].get<std::string>();
        }
    }

    // トランスフォームのパラメータ読み込み (スライド5ページ)
    if (objectJson.contains("transform")) {
        const nlohmann::json& transform = objectJson["transform"];
        
        // 平行移動 (BlenderのZ-upからゲーム座標系(Y/Z入れ替え)への変換)
        objectData.translation.x = (float)transform["translation"][0];
        objectData.translation.y = (float)transform["translation"][2];
        objectData.translation.z = (float)transform["translation"][1];

        // 回転角 (BlenderのZ-upからゲーム座標系への変換 + 符号反転)
        objectData.rotation.x = -(float)transform["rotation"][0];
        objectData.rotation.y = -(float)transform["rotation"][2];
        objectData.rotation.z = -(float)transform["rotation"][1];

        // スケーリング
        objectData.scaling.x = (float)transform["scaling"][0];
        objectData.scaling.y = (float)transform["scaling"][2];
        objectData.scaling.z = (float)transform["scaling"][1];
    }

    // コライダーのパラメータ読み込み (スライド4ページ TODO, スライド10ページ)
    if (objectJson.contains("collider")) {
        const nlohmann::json& colliderJson = objectJson["collider"];
        objectData.collider.hasCollider = true;
        objectData.collider.type = colliderJson["type"].get<std::string>();
        
        objectData.collider.center.x = (float)colliderJson["center"][0];
        objectData.collider.center.y = (float)colliderJson["center"][1];
        objectData.collider.center.z = (float)colliderJson["center"][2];

        objectData.collider.size.x = (float)colliderJson["size"][0];
        objectData.collider.size.y = (float)colliderJson["size"][1];
        objectData.collider.size.z = (float)colliderJson["size"][2];
    }

    // TODO: オブジェクト走査を再帰関数にまとめ、再帰呼出で枝を走査する (スライド6ページ)
    if (objectJson.contains("children")) {
        for (const auto& childJson : objectJson["children"]) {
            ParseObjectRecursive(childJson, levelData);
        }
    }
}

LevelData* LevelLoader::Load(const std::string& fileName) {
    // 連結してフルパスを得る (スライド1ページ)
    const std::string fullpath = kDefaultBaseDirectory + fileName + kExtension;

    // ファイルストリーム (スライド1ページ)
    std::ifstream file;

    // ファイルを開く
    file.open(fullpath);
    // ファイルオープン失敗をチェック
    if (file.fail()) {
        assert(0);
        return nullptr;
    }

    // JSON文字列から解凍したデータ (スライド2ページ)
    nlohmann::json deserialized;

    // 解凍
    file >> deserialized;

    // 正しいレベルデータファイルかチェック
    assert(deserialized.is_object());
    assert(deserialized.contains("name"));
    assert(deserialized["name"].is_string());

    // "name"を文字列として取得
    std::string name = deserialized["name"].get<std::string>();
    // 正しいレベルデータファイルかチェック
    assert(name.compare("scene") == 0);

    // レベルデータ格納用インスタンスを生成 (スライド3ページ)
    LevelData* levelData = new LevelData();

    // ※vectorの引っ越し（メモリ再確保とコピー）が発生するのを防ぐため、事前にreserveする (スライド6ページ)
    if (deserialized.contains("objects")) {
        size_t estimatedSize = deserialized["objects"].size();
        levelData->objects.reserve(estimatedSize);
    }

    // "objects"の全オブジェクトを走査 (スライド3, 6ページ)
    if (deserialized.contains("objects")) {
        for (const auto& object : deserialized["objects"]) {
            ParseObjectRecursive(object, levelData);
        }
    }

    return levelData;
}

} // namespace TL
