#!/usr/bin/env python3
"""
BIXOLON SRP-350III ESC/POS 테스트 영수증 출력
======================================================
출력 방식: ESC/POS 텍스트 커맨드를 bytes로 직접 조립 →
          win32print.WritePrinter 로 USB 포트(USB002)에 RAW 전송

사전 조건 (최초 1회):
  PowerShell (관리자) 에서 아래 명령으로 스풀러 큐 등록
  Add-Printer -Name "BIXOLON SRP-350III RAW" `
              -DriverName "Generic / Text Only" `
              -PortName "USB002"

사용법:
  python main.py                       # 자동 탐색 후 출력
  python main.py --printer "이름"      # 프린터 이름 직접 지정
  python main.py --list                # 등록된 프린터 목록만 출력
"""

import argparse
import datetime
import sys

import win32print  # pywin32

# ──────────────────────────────────────────────────────────────
# ESC/POS 커맨드 상수  (BIXOLON 매뉴얼 기반)
# ──────────────────────────────────────────────────────────────
ESC = b"\x1b"
GS  = b"\x1d"
LF  = b"\x0a"

INIT          = ESC + b"\x40"           # ESC @      프린터 초기화
ALIGN_LEFT    = ESC + b"\x61\x00"       # ESC a 0    좌측 정렬
ALIGN_CENTER  = ESC + b"\x61\x01"       # ESC a 1    가운데 정렬
ALIGN_RIGHT   = ESC + b"\x61\x02"       # ESC a 2    우측 정렬
BOLD_ON       = ESC + b"\x45\x01"       # ESC E 1    굵게 켜기
BOLD_OFF      = ESC + b"\x45\x00"       # ESC E 0    굵게 끄기
UNDERLINE_ON  = ESC + b"\x2d\x01"       # ESC - 1    밑줄 켜기
UNDERLINE_OFF = ESC + b"\x2d\x00"       # ESC - 0    밑줄 끄기
DOUBLE_BOTH   = GS  + b"\x21\x11"       # GS  ! 0x11 가로+세로 2배
DOUBLE_HEIGHT = GS  + b"\x21\x01"       # GS  ! 0x01 세로 2배
NORMAL_SIZE   = GS  + b"\x21\x00"       # GS  ! 0x00 기본 크기
FEED_5        = ESC + b"\x64\x05"       # ESC d 5    5줄 피드
PARTIAL_CUT   = GS  + b"\x56\x42\x00"  # GS  V B 0  부분 컷

# 80mm 용지 기준 48컬럼
COLS = 48


# ──────────────────────────────────────────────────────────────
# 텍스트 유틸
# ──────────────────────────────────────────────────────────────

def line(text: str = "", width: int = 0, align: str = "left") -> bytes:
    """텍스트를 cp437 인코딩 후 LF 추가. width 지정 시 정렬 패딩."""
    if width:
        if align == "center":
            text = text.center(width)
        elif align == "right":
            text = text.rjust(width)
        else:
            text = text.ljust(width)
    return text.encode("cp437", errors="replace") + LF


def sep(char: str = "-") -> bytes:
    """구분선 한 줄."""
    return (char * COLS).encode("cp437") + LF


def two_col(left: str, right: str) -> bytes:
    """좌/우 정렬 두 컬럼 한 줄. 합산 COLS 맞춤."""
    space = COLS - len(left) - len(right)
    return (left + " " * max(space, 1) + right).encode("cp437", errors="replace") + LF


# ──────────────────────────────────────────────────────────────
# QR 코드 커맨드  GS ( k  (Function 165–181)
# ──────────────────────────────────────────────────────────────

def build_qr(data: str, module_size: int = 5) -> bytes:
    raw = data.encode("utf-8")
    store_len = len(raw) + 3
    pL = store_len & 0xFF
    pH = (store_len >> 8) & 0xFF
    buf = bytearray()
    buf += bytes([0x1D, 0x28, 0x6B, 0x04, 0x00, 0x31, 0x41, 0x32, 0x00])  # Model 2
    buf += bytes([0x1D, 0x28, 0x6B, 0x03, 0x00, 0x31, 0x43, module_size]) # 모듈 크기
    buf += bytes([0x1D, 0x28, 0x6B, 0x03, 0x00, 0x31, 0x45, 0x31])        # 오류정정 M
    buf += bytes([0x1D, 0x28, 0x6B, pL,   pH,   0x31, 0x50, 0x30])        # 데이터 저장
    buf += raw
    buf += bytes([0x1D, 0x28, 0x6B, 0x03, 0x00, 0x31, 0x51, 0x30])        # 출력
    return bytes(buf)


# ──────────────────────────────────────────────────────────────
# CODE128 바코드 커맨드  GS k  (type = 0x49)
# ──────────────────────────────────────────────────────────────

def build_barcode(data: str) -> bytes:
    raw = data.encode("ascii")
    buf = bytearray()
    buf += bytes([0x1D, 0x48, 0x02])              # HRI 텍스트 아래 출력
    buf += bytes([0x1D, 0x68, 0x60])              # 바코드 높이 96 도트
    buf += bytes([0x1D, 0x77, 0x02])              # 모듈 폭 2
    buf += bytes([0x1D, 0x6B, 0x49, len(raw)])    # GS k CODE128 + 길이
    buf += raw
    return bytes(buf)


# ──────────────────────────────────────────────────────────────
# 영수증 ESC/POS 스트림 조립
# ──────────────────────────────────────────────────────────────

def build_receipt() -> bytes:
    now = datetime.datetime.now()
    receipt_no = now.strftime("%Y%m%d%H%M%S")

    items = [
        ("Americano",        1, 3_000),
        ("Cafe Latte",       2, 4_000),
        ("Cappuccino",       1, 4_500),
        ("Blueberry Muffin", 1, 2_500),
        ("Cheesecake Slice", 2, 4_500),
    ]
    subtotal = sum(qty * price for _, qty, price in items)
    tax      = int(subtotal * 0.1)
    total    = subtotal + tax
    cash     = ((total // 1_000) + 1) * 1_000  # 올림 천 단위
    change   = cash - total
    qr_url   = f"https://bixolon.com/receipt/{receipt_no}"

    buf = bytearray()

    # ── 초기화 ──────────────────────────────────────────────────
    buf += INIT

    # ── 헤더 ────────────────────────────────────────────────────
    buf += ALIGN_CENTER
    buf += BOLD_ON + DOUBLE_BOTH
    buf += b"BIXOLON CAFE" + LF
    buf += NORMAL_SIZE + BOLD_OFF
    buf += line("SRP-350III  TEST RECEIPT", COLS, "center")
    buf += sep("=")

    # ── 거래 정보 ────────────────────────────────────────────────
    buf += ALIGN_LEFT
    buf += line(f"Date     : {now.strftime('%Y-%m-%d')}")
    buf += line(f"Time     : {now.strftime('%H:%M:%S')}")
    buf += line(f"Rcpt No  : {receipt_no}")
    buf += line(f"Cashier  : POS #1")
    buf += sep()

    # ── 상품 목록 ────────────────────────────────────────────────
    buf += BOLD_ON
    buf += line(f"{'Item':<26}{'Qty':>4}{'Amount':>12}  ")
    buf += BOLD_OFF
    buf += sep()

    for name, qty, unit_price in items:
        amount = qty * unit_price
        buf += line(f"{name:<26}{qty:>4}{amount:>10,}  ")

    buf += sep()

    # ── 합계 ─────────────────────────────────────────────────────
    buf += two_col("SUBTOTAL", f"{subtotal:>10,} KRW")
    buf += two_col("VAT (10%)", f"{tax:>10,} KRW")
    buf += sep("=")

    buf += BOLD_ON + DOUBLE_HEIGHT
    buf += two_col("TOTAL", f"{total:>10,} KRW")
    buf += NORMAL_SIZE + BOLD_OFF

    buf += sep("=")
    buf += two_col("CASH", f"{cash:>10,} KRW")
    buf += two_col("CHANGE", f"{change:>10,} KRW")
    buf += sep()

    # ── QR 코드 ──────────────────────────────────────────────────
    buf += ALIGN_CENTER + LF
    buf += build_qr(qr_url, module_size=5)
    buf += LF
    buf += UNDERLINE_ON
    buf += line(qr_url, COLS, "center")
    buf += UNDERLINE_OFF + LF

    # ── CODE128 바코드 ───────────────────────────────────────────
    buf += ALIGN_CENTER
    buf += build_barcode(receipt_no)
    buf += LF

    # ── 푸터 ─────────────────────────────────────────────────────
    buf += ALIGN_CENTER + LF
    buf += BOLD_ON
    buf += line("Thank you for visiting!", COLS, "center")
    buf += BOLD_OFF
    buf += line("www.bixolon-cafe.example.com", COLS, "center")
    buf += line("TEL: 02-000-0000", COLS, "center")
    buf += LF

    # ── 피드 & 컷 ────────────────────────────────────────────────
    buf += FEED_5
    buf += PARTIAL_CUT

    return bytes(buf)


# ──────────────────────────────────────────────────────────────
# win32print 헬퍼
# ──────────────────────────────────────────────────────────────

def get_printers() -> list[str]:
    printers = win32print.EnumPrinters(
        win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS
    )
    return [name for _flags, _desc, name, _comment in printers]


def get_port(printer_name: str) -> str:
    try:
        h = win32print.OpenPrinter(printer_name)
        try:
            return win32print.GetPrinter(h, 2).get("pPortName", "?")
        finally:
            win32print.ClosePrinter(h)
    except Exception:
        return "?"


def find_bixolon(printers: list[str]) -> str | None:
    for name in printers:
        if any(k in name.lower() for k in ("bixolon", "srp", "350")):
            return name
    return None


def send_raw(printer_name: str, data: bytes) -> bool:
    """win32print.WritePrinter 로 RAW ESC/POS 데이터 전송."""
    h = win32print.OpenPrinter(printer_name)
    try:
        win32print.StartDocPrinter(h, 1, ("ESC/POS Receipt", None, "RAW"))
        try:
            win32print.StartPagePrinter(h)
            win32print.WritePrinter(h, data)
            win32print.EndPagePrinter(h)
        finally:
            win32print.EndDocPrinter(h)
    finally:
        win32print.ClosePrinter(h)
    return True


# ──────────────────────────────────────────────────────────────
# 진입점
# ──────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="BIXOLON SRP-350III ESC/POS 테스트 영수증 출력"
    )
    parser.add_argument(
        "--printer", metavar="NAME", default=None,
        help="사용할 프린터 이름 (생략 시 자동 탐색)"
    )
    parser.add_argument(
        "--list", action="store_true",
        help="등록된 프린터 목록만 출력하고 종료"
    )
    args = parser.parse_args()

    # ── 프린터 목록 ──────────────────────────────────────────
    printers = get_printers()

    if args.list:
        print("등록된 프린터:")
        for p in printers:
            print(f"  {p}  (포트: {get_port(p)})")
        return

    # ── 대상 프린터 결정 ─────────────────────────────────────
    target = args.printer or find_bixolon(printers)

    if not target:
        print("[ERROR] BIXOLON SRP-350 프린터를 찾을 수 없습니다.", file=sys.stderr)
        print(
            "\n  PowerShell (관리자) 에서 아래 명령으로 스풀러 큐를 등록하세요:\n"
            "    Add-Printer -Name \"BIXOLON SRP-350III RAW\"\n"
            "                -DriverName \"Generic / Text Only\"\n"
            "                -PortName \"USB002\"",
            file=sys.stderr,
        )
        sys.exit(1)

    if args.printer and target not in printers:
        print(f"[WARN] '{target}' 가 목록에 없습니다. 그대로 진행합니다.")

    port = get_port(target)
    print(f"프린터 : {target}  (포트: {port})")

    # ── 영수증 생성 & 전송 ───────────────────────────────────
    data = build_receipt()
    print(f"전송   : {len(data):,} bytes  →  ", end="", flush=True)

    try:
        send_raw(target, data)
        print("완료")
    except Exception as e:
        print(f"실패\n[ERROR] {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()