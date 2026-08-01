#include "level_data.h"
#include "level_loader.h"
#include <iostream>
#include <map>
#include <vector>

// ダミーのモデル・オブジェクトクラスの定義 (スライド7ページのシーン配置ロジック再現用)
class Model {
public:
    std::string name;
};

class Object3d {
public:
    static Object3d* Create(Model* model) {
        Object3d* obj = new Object3d();
        obj->model = model;
        return obj;
    }

    void SetPosition(const TL::Vector3& pos) {
        translation = pos;
    }

    void SetRotation(const TL::Vector3& rot) {
        rotation = rot;
    }

    void SetScale(const TL::Vector3& scl) {
        scaling = scl;
    }

    Model* model = nullptr;
    TL::Vector3 translation;
    TL::Vector3 rotation;
    TL::Vector3 scaling;
};

// ダミーの登録済みモデルリスト
std::map<std::string, Model*> models;
// ゲーム内のアクティブな3Dオブジェクトリスト
std::vector<Object3d*> objects;

void SetupDummyModels() {
    models["player"] = new Model{"player"};
    models["enemy"] = new Model{"enemy"};
    models["stage"] = new Model{"stage"};
}

// レベルデータからオブジェクトを生成、配置するメイン関数 (スライド7ページ)
void PlaceObjectsFromLevel(TL::LevelData* levelData) {
    // レベルデータからオブジェクトを生成、配置
    for (auto& objectData : levelData->objects) {
        // ファイル名から登録済みモデルを検索
        Model* model = nullptr;
        decltype(models)::iterator it = models.find(objectData.fileName);
        if (it != models.end()) {
            model = it->second;
        }

        // モデルを指定して3Dオブジェクトを生成
        Object3d* newObject = Object3d::Create(model);

        // 座標
        newObject->SetPosition(objectData.translation);
        // 回転角
        newObject->SetRotation(objectData.rotation);
        // 座標 (※スライド内コメントで「座標」とあるが SetScale を呼び出す処理)
        newObject->SetScale(objectData.scaling);

        // 配列に登録
        objects.push_back(newObject);

        // デバッグ出力
        std::cout << "Placed Object: Name=" << objectData.name 
                  << ", File=" << objectData.fileName 
                  << ", Pos=(" << objectData.translation.x << ", " << objectData.translation.y << ", " << objectData.translation.z << ")"
                  << std::endl;
        
        if (objectData.collider.hasCollider) {
            std::cout << " -> Collider Attached: Type=" << objectData.collider.type
                      << ", Center=(" << objectData.collider.center.x << ", " << objectData.collider.center.y << ", " << objectData.collider.center.z << ")"
                      << ", Size=(" << objectData.collider.size.x << ", " << objectData.collider.size.y << ", " << objectData.collider.size.z << ")"
                      << std::endl;
        }
    }
}

int main() {
    SetupDummyModels();

    std::cout << "--- Loading Level Data ---" << std::endl;
    // レベルファイルの読み込みテスト (例: "stage1")
    // ※実際には "Resources/Levels/stage1.json" がロードされます
    TL::LevelData* levelData = TL::LevelLoader::Load("stage1");

    if (levelData != nullptr) {
        PlaceObjectsFromLevel(levelData);
        delete levelData;
    }

    // 後片付け
    for (auto* obj : objects) delete obj;
    for (auto& pair : models) delete pair.second;

    return 0;
}
