#!/usr/bin/env python3

import os
import replicate
import requests
import sys

def main():
    # 1. Cek token
    token = os.getenv("REPLICATE_API_TOKEN")
    if not token:
        print("[ERROR] REPLICATE_API_TOKEN belum di-set.")
        print("Silakan jalankan setup_replicate.sh terlebih dahulu.")
        sys.exit(1)

    print("[OK] Token ditemukan di environment.")

    # 2. Validasi token ke server Replicate
    print("[INFO] Mengecek validitas token...")

    resp = requests.get(
        "https://api.replicate.com/v1/models",
        headers={"Authorization": f"Token {token}"}
    )

    if resp.status_code != 200:
        print(f"[ERROR] Token tidak valid. HTTP {resp.status_code}")
        sys.exit(1)

    print("[OK] Token valid!")

    # 3. Tampilkan beberapa model
    data = resp.json()
    print("\n=== Beberapa Model Tersedia ===")
    for i, m in enumerate(data.get("results", [])[:5], start=1):
        print(f"{i}. {m['owner']}/{m['name']} (versi terbaru: {m['latest_version']['id'][:8]}...)")

    # 4. Jalankan model contoh BLIP tapi dengan versi spesifik
    print("\n[INFO] Menjalankan model contoh: salesforce/blip:2e1dddc8")

    try:
        output = replicate.run(
            "salesforce/blip:2e1dddc8",
            input={
                "image": "https://raw.githubusercontent.com/replicate/replicate-python/main/tests/fixtures/cat.jpeg"
            }
        )
        print("[HASIL] Caption untuk gambar kucing:")
        print(output)
    except Exception as e:
        print("[ERROR] Gagal menjalankan model:", str(e))

    print("\n[SELESAI] Script selesai dijalankan.")

if __name__ == "__main__":
    main()
