#!/usr/bin/env python3
"""
Script fallback untuk mencoba berbagai versi model BLIP di Replicate.
"""

import replicate
import os
import sys

# Daftar versi yang mau dicoba
VERSIONS = [
    # versi lengkap (disarankan)
    "salesforce/blip:2e1dddc8621f72155f24cf2e0adbde548458d3cab9f00c0139eea840d0ac4746",
    # versi pendek
    "salesforce/blip:2e1dddc8",
    # latest (kadang bermasalah, tapi dicoba juga)
    "salesforce/blip:latest",
]

def main():
    token = os.getenv("REPLICATE_API_TOKEN")
    if not token:
        print("[ERROR] REPLICATE_API_TOKEN belum di-set. Jalankan setup_replicate.sh dulu.")
        sys.exit(1)

    test_image = "https://raw.githubusercontent.com/replicate/replicate-python/main/tests/fixtures/cat.jpeg"

    for version in VERSIONS:
        print(f"\n[INFO] Mencoba versi: {version}")
        try:
            output = replicate.run(
                version,
                input={"image": test_image}
            )
            print("[OK] Berhasil!")
            print("[HASIL OUTPUT]:", output)
            return  # berhenti kalau sudah berhasil
        except Exception as e:
            print(f"[GAGAL] {version} → {e}")

    print("\n[SELESAI] Semua versi gagal. Coba cek:")
    print("- Apakah token sudah benar & aktif?")
    print("- Apakah akun punya izin/billing untuk model ini?")
    print("- Apakah library `replicate` sudah terbaru (pip install --upgrade replicate)?")

if __name__ == "__main__":
    main()
