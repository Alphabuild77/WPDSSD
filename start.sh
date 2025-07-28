#!/data/data/com.termux/files/usr/bin/bash

echo ""
echo "⚙️  WPDSSD - Instalador automático para Termux"
echo "============================================="
echo ""
echo "🔧 Actualizando paquetes..."
pkg update -y && pkg upgrade -y

echo ""
echo "📦 Instalando Python y dependencias básicas..."
pkg install -y python git curl

echo ""
echo "🐍 Instalando paquetes de Python..."
pip install --upgrade pip
pip install fastapi uvicorn ebooklib beautifulsoup4 playwright

echo ""
echo "🌐 Instalando navegador para Playwright (Chromium headless)..."

echo ""
echo "🚀 Iniciando servidor en http://127.0.0.1:8000"
echo "Puedes acceder a la documentación en: http://127.0.0.1:8000/docs"
echo ""
uvicorn main:app --host 0.0.0.0 --port 8000
