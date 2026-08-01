#pragma once

#include "level_data.h"
#include <string>

namespace TL {

class LevelLoader {
public:
    // JSONファイルを読み込み、LevelData構造体にデシリアライズする
    static LevelData* Load(const std::string& fileName);
};

} // namespace TL
