#!/usr/bin/env bash
set -e

echo "🚀 Kurulum başlıyor..."

pip install -r requirements.txt

echo "📦 Playwright browser indiriliyor..."
# Chromium'u system deps ile birlikte indir
playwright install chromium
playwright install-deps chromium

echo "✅ Kurulum tamamlandı!"
