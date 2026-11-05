import sys, os
# Add local libs folder to Python path for EasyOCR and dependencies
libs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'libs'))
if libs_path not in sys.path:
    sys.path.insert(0, libs_path)

"""
Quick screen OCR using EasyOCR + mss (fast screen capture).
Tuned for: RTX 3050 6GB Laptop GPU, i5-13450HX, 24GB RAM, Windows.

Install once:
    pip install easyocr mss opencv-python numpy
    # Make sure torch has CUDA support (check with: python -c "import torch; print(torch.cuda.is_available())")
    # If it prints False, reinstall torch with CUDA 12.1 wheel:
    #   pip uninstall torch
    #   pip install torch --index-url https://download.pytorch.org/whl/cu121

Usage:
    python screen_ocr.py            # scan full screen once
    python screen_ocr.py --region   # scan a specific region (x,y,w,h prompted)
    python screen_ocr.py --watch    # keep scanning every N seconds (Ctrl+C to stop)
"""

import argparse
import time
import sys

import mss
import numpy as np
import cv2
import easyocr

_reader = None


def get_reader(langs=("en",)):
    global _reader
    if _reader is None:
        print("[*] Loading EasyOCR model onto GPU (first run downloads weights)...", file=sys.stderr)
        # Disable verbose progress bar to avoid Unicode encoding issues on Windows console
        _reader = easyocr.Reader(list(langs), gpu=True, verbose=False)
    return _reader


def grab_screen(region=None):
    """Capture the screen (full or region) using pyautogui as fallback."""
    try:
        with mss.mss() as sct:
            monitor = sct.monitors[1]
            if region:
                x, y, w, h = region
                monitor = {"left": x, "top": y, "width": w, "height": h}
            raw = sct.grab(monitor)
            img = np.array(raw)  # BGRA
            return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    except Exception:
        # Fallback to pyautogui screenshot (works on Windows)
        import pyautogui
        if region:
            x, y, w, h = region
            img = pyautogui.screenshot(region=(x, y, w, h))
        else:
            img = pyautogui.screenshot()
        img = np.array(img)  # RGB
        return cv2.cvtColor(img, cv2.COLOR_RGB2BGR)


def run_ocr(img, langs=("en",), min_conf=0.4):
    reader = get_reader(langs)
    results = reader.readtext(img)
    return [(text, conf, bbox) for bbox, text, conf in results if conf >= min_conf]


def draw_annotations(img, results):
    out = img.copy()
    for text, conf, bbox in results:
        pts = np.array(bbox, dtype=np.int32)
        cv2.polylines(out, [pts], isClosed=True, color=(0, 255, 0), thickness=2)
        x, y = pts[0]
        cv2.putText(out, text[:30], (x, max(y - 5, 0)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    return out


def scan_once(region=None, save_annotated=False, langs=("en",)):
    t0 = time.time()
    img = grab_screen(region)
    results = run_ocr(img, langs=langs)
    dt = time.time() - t0
    print(f"\n[+] Found {len(results)} text blocks in {dt:.2f}s")
    for text, conf, _ in results:
        print(f"  ({conf:.2f}) {text}")
    if save_annotated:
        annotated = draw_annotations(img, results)
        out_path = f"ocr_scan_{int(time.time())}.png"
        cv2.imwrite(out_path, annotated)
        print(f"[*] Saved annotated screenshot -> {out_path}")
    return results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--region", action="store_true", help="prompt for a custom region")
    ap.add_argument("--watch", type=float, default=0, help="rescan every N seconds")
    ap.add_argument("--save", action="store_true", help="save an annotated screenshot")
    ap.add_argument("--lang", nargs="+", default=["en"], help="EasyOCR language codes, e.g. en hi")
    args = ap.parse_args()
    region = None
    if args.region:
        x = int(input("x: "))
        y = int(input("y: "))
        w = int(input("width: "))
        h = int(input("height: "))
        region = (x, y, w, h)
    get_reader(args.lang)
    if args.watch > 0:
        try:
            while True:
                scan_once(region, save_annotated=args.save, langs=args.lang)
                time.sleep(args.watch)
        except KeyboardInterrupt:
            print("\n[!] Stopped.")
    else:
        scan_once(region, save_annotated=args.save, langs=args.lang)

if __name__ == "__main__":
    main()
