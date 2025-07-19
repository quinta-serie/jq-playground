#!/bin/bash

set -e

APP_NAME="jq-playground"
INSTALL_PATH="/usr/local/bin"
SCRIPT_NAME="jq-playground"
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$PROJECT_DIR/.venv"
WRAPPER_PATH="$PROJECT_DIR/$SCRIPT_NAME"
LINK_PATH="$INSTALL_PATH/$APP_NAME"

echo "🔧 Setting up environment..."

if [ ! -d "$VENV_DIR" ]; then
  echo "📦 Creating virtual environment at .venv..."
  python3 -m venv "$VENV_DIR"
else
  echo "✅ Virtual environment already exists."
fi

echo "📦 Installing Python dependencies..."
source "$VENV_DIR/bin/activate"
pip install --upgrade pip
pip install -r "$PROJECT_DIR/requirements.txt"
deactivate

echo "⚙️ Generating launcher script..."

cat << EOF > "$WRAPPER_PATH"
#!/bin/bash
cd "$PROJECT_DIR"
source "$VENV_DIR/bin/activate"
python jq_playground.py &
EOF

chmod +x "$WRAPPER_PATH"

echo "🔗 Creating symlink at $LINK_PATH..."
sudo ln -sf "$WRAPPER_PATH" "$LINK_PATH"

echo "✅ Installation complete!"
echo "🚀 You can now run the app from anywhere using: $APP_NAME"
