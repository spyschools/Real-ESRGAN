#!/bin/bash
# Script setup API Token Replicate di Kali Linux + validasi token

# Minta token dari user
read -p "Masukkan REPLICATE_API_TOKEN: " TOKEN

# Simpan sementara untuk sesi saat ini
export REPLICATE_API_TOKEN="$TOKEN"

# Cek apakah paket curl terpasang
if ! command -v curl &> /dev/null; then
    echo "[INFO] curl belum terinstall. Menginstall dulu..."
    sudo apt update && sudo apt install -y curl
fi

echo "[INFO] Mengecek validitas token ke server Replicate..."

# Cek validasi token dengan memanggil endpoint Replicate
RESP=$(curl -s -o /tmp/replicate_check.json -w "%{http_code}" \
  -H "Authorization: Token $TOKEN" \
  https://api.replicate.com/v1/models)

if [ "$RESP" = "200" ]; then
    echo "[OK] Token valid!"

    # Tambahkan ke ~/.bashrc supaya permanen
    if ! grep -q "REPLICATE_API_TOKEN" ~/.bashrc; then
        echo "export REPLICATE_API_TOKEN=\"$TOKEN\"" >> ~/.bashrc
        echo "[OK] Token ditambahkan ke ~/.bashrc"
    else
        sed -i "s|^export REPLICATE_API_TOKEN=.*|export REPLICATE_API_TOKEN=\"$TOKEN\"|" ~/.bashrc
        echo "[OK] Token diupdate di ~/.bashrc"
    fi

    # Aktifkan tanpa restart
    source ~/.bashrc
    echo "[SELESAI] REPLICATE_API_TOKEN sudah diset permanen."
else
    echo "[ERROR] Token tidak valid (HTTP $RESP)."
    echo "Silakan cek kembali API token kamu di https://replicate.com/account"
fi
