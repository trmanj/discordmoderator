#!/usr/bin/env bash
set -o errexit

echo "🚀 Chrome kurulumu başlıyor..."

apt-get update
apt-get install -y wget unzip jq

# Chrome versiyonunu bul
LATEST_VERSION=$(curl -s https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json | jq -r '.channels.Stable.version')
echo "Chrome versiyonu: $LATEST_VERSION"

# Chrome indir
wget "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/${LATEST_VERSION}/linux64/chrome-linux64.zip" -O chrome.zip
unzip -q chrome.zip
mv chrome-linux64 /opt/chrome
chmod +x /opt/chrome/chrome
ln -sf /opt/chrome/chrome /usr/bin/google-chrome

# ChromeDriver indir
wget "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/${LATEST_VERSION}/linux64/chromedriver-linux64.zip" -O chromedriver.zip
unzip -q chromedriver.zip
chmod +x chromedriver-linux64/chromedriver
mv chromedriver-linux64/chromedriver /usr/local/bin/chromedriver

echo "✅ Chrome kuruldu!"
echo "Chrome: $(/opt/chrome/chrome --version)"
echo "ChromeDriver: $(chromedriver --version)"

# Python deps
pip install -r requirements.txt
