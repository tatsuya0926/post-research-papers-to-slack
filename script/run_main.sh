#!/bin/bash
# 作業ディレクトリに移動
cd /Users/***/post-research-papers-to-slack

# logファイルの作成
LOG_DIR="./logs"
LOG_FILE="$LOG_DIR/info.log"
if [ ! -d "$LOG_DIR" ]; then
    mkdir -p "$LOG_DIR"
fi

if [ ! -f "$LOG_FILE" ]; then
    touch "$LOG_FILE"
fi

# 仮想環境を起動
source /Users/***/post-research-papers-to-slack/.venv/bin/activate

python main.py >> "$LOG_FILE" 2>&1