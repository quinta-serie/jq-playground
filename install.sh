#!/bin/bash

APP_NAME="jq-playground"
TARGET_FILE="jq_playground.py"
INSTALL_PATH="/usr/local/bin"

# Obtém o caminho absoluto do diretório atual
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_PATH="$SCRIPT_DIR/$TARGET_FILE"
LINK_PATH="$INSTALL_PATH/$APP_NAME"

# Verifica se o arquivo alvo existe
if [ ! -f "$TARGET_PATH" ]; then
    echo "Error: $TARGET_FILE not found in $SCRIPT_DIR"
    exit 1
fi

# Cria o link simbólico
echo "Creating symlink: $LINK_PATH -> $TARGET_PATH"
sudo ln -sf "$TARGET_PATH" "$LINK_PATH"

# Torna o script executável
chmod +x "$TARGET_PATH"

echo "✅ Installed! You can now run the app using: $APP_NAME"
