#!/usr/bin/env bash
set -o errexit

echo "🚀 Kurulum başlıyor..."

pip install -r requirements.txt

echo "📦 Playwright browser indiriliyor..."
playwright install chromium

echo "✅ Kurulum tamamlandı!"
