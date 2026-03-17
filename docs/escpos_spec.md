# BIXOLON Thermal POS Printer — ESC/POS Command Protocol Specification

> **Source:** Command Manual Ver. 1.00 — BIXOLON Corporation  
> **Supported Models:** SRP-380/382 series, SRP-330/332 series, SRP-350/352 series, SRP-F310II/F312II, SRP-E300/E302, SRP-B300, SRP-Q200/Q300/Q302/QE300/QE302, SRP-S200/S300/S320/S3000

---

## 1. Motion Units Reference

| Resolution | Horizontal Unit | Vertical Unit | Max Feed |
|---|---|---|---|
| 180 dpi | 0.141 mm (1/180 inch) | 0.0705 mm (1/360 inch) | 17.98 mm |
| 203 dpi | 0.125 mm (1/203 inch) | 0.0625 mm (1/406 inch) | 15.937 mm |

---

## 2. Command List (Overview)

| No | Command | Hex | Function |
|---|---|---|---|
| 1 | HT | 09 | Horizontal tab |
| 2 | LF | 0A | Print and line feed |
| 3 | FF | 0C | Form feed (page mode) |
| 4 | CR | 0D | Print and carriage return |
| 5 | CAN | 18 | Cancel print data in page mode |
| 6 | DLE EOT | 10 04 n | Transmit real-time status |
| 7 | DLE DC4 | 10 14 n m t | Generate pulse at real-time |
| 8 | ESC SP | 1B 20 n | Set character right space |
| 9 | ESC ! | 1B 21 n | Set print mode |
| 10 | ESC $ | 1B 24 nL nH | Set absolute print position |
| 11 | ESC % | 1B 25 n | Select/cancel user-defined character set |
| 12 | ESC & | 1B 26 ... | Define user-defined character set |
| 13 | ESC * | 1B 2A m nL nH d1..dk | Specify bit image mode |
| 14 | ESC - | 1B 2D n | Turn underline mode on/off |
| 15 | ESC 2 | 1B 32 | Select default line spacing |
| 16 | ESC 3 | 1B 33 n | Set line spacing |
| 17 | ESC = | 1B 3D n | Select peripheral device |
| 18 | ESC ? | 1B 3F n | Cancel user-defined characters |
| 19 | ESC @ | 1B 40 | Initialize printer |
| 20 | ESC D | 1B 44 n1..nk NUL | Set horizontal tab positions |
| 21 | ESC E | 1B 45 n | Turn emphasized mode on/off |
| 22 | ESC G | 1B 47 n | Turn double-strike mode on/off |
| 23 | ESC J | 1B 4A n | Print and feed paper |
| 24 | ESC L | 1B 4C | Select page mode |
| 25 | ESC M | 1B 4D n | Select character font |
| 26 | ESC R | 1B 52 n | Specify international character set |
| 27 | ESC S | 1B 53 | Select standard mode |
| 28 | ESC T | 1B 54 n | Select print direction in page mode |
| 29 | ESC V | 1B 56 n | Turn 90° clockwise rotation on/off |
| 30 | ESC W | 1B 57 xL xH yL yH dxL dxH dyL dyH | Set print area in page mode |
| 31 | ESC \ | 1B 5C nL nH | Set relative print position |
| 32 | ESC a | 1B 61 n | Set position alignment |
| 33 | ESC d | 1B 64 n | Print and feed n lines |
| 34 | ESC i | 1B 69 | Partial cut |
| 35 | ESC m | 1B 6D | Partial cut |
| 36 | ESC p | 1B 70 m t1 t2 | Generate pulse |
| 37 | ESC t | 1B 74 n | Select character code table |
| 38 | ESC v | 1B 76 | Transmit paper sensor status |
| 39 | ESC { | 1B 7B n | Turn upside-down print mode on/off |
| 40 | FS p | 1C 70 n m | Print NV bit image |
| 41 | FS q | 1C 71 n [...] | Define NV bit image |
| 42 | GS ! | 1D 21 n | Select character size |
| 43 | GS $ | 1D 24 nL nH | Set absolute vertical print position (page mode) |
| 44 | GS ( A | 1D 28 41 pL pH n m | Execute test print |
| 45 | GS ( L / GS 8 L | 1D 28 4C ... | Select graphics data |
| 46 | GS ( k | 1D 28 6B ... | Specify and print symbol (QR/barcode) |
| 47 | GS * | 1D 2A x y d1..dk | Define downloaded bit image |
| 48 | GS / | 1D 2F m | Print downloaded bit image |
| 49 | GS : | 1D 3A | Start/end macro definition |
| 50 | GS B | 1D 42 n | Turn white/black reverse print mode on/off |
| 51 | GS H | 1D 48 n | Select print position of HRI characters |
| 52 | GS I | 1D 49 n | Transmit printer ID |
| 53 | GS L | 1D 4C nL nH | Set left margin |
| 54 | GS V | 1D 56 n | Select cut mode and execute partial cut |
| 55 | GS W | 1D 57 nL nH | Set print area width |
| 56 | GS ^ | 1D 5E r t m | Execute macro |
| 57 | GS a | 1D 61 n | Enable/Disable ASB |
| 58 | GS f | 1D 66 n | Select font for HRI characters |
| 59 | GS h | 1D 68 n | Set bar code height |
| 60 | GS k | 1D 6B m d1..dk NUL | Print bar code |
| 61 | GS r | 1D 72 n | Transmit status |
| 62 | GS v 0 | 1D 76 30 m xL xH yL yH d1..dk | Print raster bit image |
| 63 | GS w | 1D 77 n | Set bar code width |
| 64 | BS M | — | Select device font type |
| 65 | BS V | — | Select cut mode (partial/full cut) |
| 66 | BS ^ P | — | Set power saving mode |

---

## 3. Command Details

### HT — Horizontal Tab
- **Hex:** `09`
- **Range:** None
- **Description:** Moves print position to next horizontal tab position. Tab positions are set with `ESC D`. Underline is not applied to the tab space.

---

### LF — Print and Line Feed
- **Hex:** `0A`
- **Description:** Prints data in buffer and feeds one line (based on current line spacing). In page mode, only moves print position.

---

### FF — Form Feed
- **Hex:** `0C`
- **Description:** In page mode, prints all buffered data and returns to standard mode. Ignored if paper is at print start position.

---

### CR — Print and Carriage Return
- **Hex:** `0D`
- **Description:** Prints data. If auto line feed is enabled, also performs one line feed (same as LF).

---

### CAN — Cancel Print Data (Page Mode)
- **Hex:** `18`
- **Description:** Clears receive buffer and print buffers. **Effective only in page mode** (set by `ESC L`).

---

### DLE EOT — Transmit Real-Time Status
- **Hex:** `10 04 n`
- **Range:** `1 ≤ n ≤ 4`
- **Description:** Transmits printer status in real-time (higher priority than other commands).

| n | Function |
|---|---|
| 1 | Printer status |
| 2 | Off-line status |
| 3 | Error status |
| 4 | Paper roll sensor status |

**n=1 Printer Status Byte:**

| Bit | Off(0) | On(1) |
|---|---|---|
| 2 | Drawer pin 3 LOW | Drawer pin 3 HIGH |
| 3 | Online | Offline |

**n=2 Off-line Status Byte:**

| Bit | Off(0) | On(1) |
|---|---|---|
| 2 | Cover closed | Cover open |
| 3 | No feed button | FEED button pressed |
| 5 | No paper-end stop | Printing stopped |
| 6 | No error | Error occurred |

**n=3 Error Status Byte:**

| Bit | Off(0) | On(1) |
|---|---|---|
| 3 | No autocutter error | Autocutter error |

**n=4 Paper Sensor Status Byte:**

| Bit | Off(0) | On(1) |
|---|---|---|
| 2,3 | Paper adequate | Paper near end (0x0C) |
| 5,6 | Paper present | Paper not present (0x60) |

---

### DLE DC4 — Generate Pulse (Real-Time)
- **Hex:** `10 14 n m t`
- **Range:** `n=1`, `m=0,1`, `1 ≤ t ≤ 8`
- **Description:** Outputs drive pulse to drawer kick-out connector.

| m | Connector Pin |
|---|---|
| 0 | Pin 2 |
| 1 | Pin 5 |

- Pulse ON time = `t × 100 ms`, OFF time = `t × 100 ms`

---

### ESC SP — Set Character Right Space
- **Hex:** `1B 20 n`
- **Range:** `0 ≤ n ≤ 255`, Default: `n=0`
- **Description:** Right space = `n × horizontal motion unit`. Doubled in double-width mode.

---

### ESC ! — Set Print Mode
- **Hex:** `1B 21 n`
- **Range:** `0 ≤ n ≤ 255`, Default: `n=0`

| Bit | Off | On |
|---|---|---|
| 0 | Font A | Font B |
| 3 | Normal | Emphasized |
| 4 | Normal height | Double-height |
| 5 | Normal width | Double-width |
| 7 | No underline | Underline |

---

### ESC $ — Set Absolute Print Position
- **Hex:** `1B 24 nL nH`
- **Range:** `0 ≤ (nL + nH×256) ≤ 65535`
- **Description:** Position = `(nL + nH×256) × horizontal motion unit` from left edge of print area.

---

### ESC % — Select/Cancel User-Defined Character Set
- **Hex:** `1B 25 n`
- **Range:** `0 ≤ n ≤ 255`, Default: `n=0`
- `n=0`: Deselect user-defined set; `n=1`: Select user-defined set.

---

### ESC & — Define User-Defined Character Set
- **Hex:** `1B 26 y c1 c2 [x1 d1...d(y×x1)]...[xk d1...d(y×xk)]`
- **Range:** `y=3`, `32 ≤ c1 ≤ c2 ≤ 126`, x ≤ 12 (Font A) / ≤ 9 (Font B)
- **Description:** Defines user-defined characters from code c1 to c2.

---

### ESC * — Specify Bit Image Mode
- **Hex:** `1B 2A m nL nH d1..dk`
- **Range:** `m = 0,1,32,33`

| m | Mode | Vertical dots | k |
|---|---|---|---|
| 0 | 8-dot single-density | 8 | nL + nH×256 |
| 1 | 8-dot double-density | 8 | nL + nH×256 |
| 32 | 24-dot single-density | 24 | (nL + nH×256) × 3 |
| 33 | 24-dot double-density | 24 | (nL + nH×256) × 3 |

---

### ESC - — Turn Underline Mode On/Off
- **Hex:** `1B 2D n`
- **Range:** `0 ≤ n ≤ 2` or `48 ≤ n ≤ 50`, Default: `n=0`

| n | Function |
|---|---|
| 0, 48 | Off |
| 1, 49 | On (1-dot thick) |
| 2, 50 | On (2-dot thick) |

---

### ESC 2 — Select Default Line Spacing
- **Hex:** `1B 32`
- **Description:** Resets line spacing to default (~30 dots). 180dpi: 4.23 mm / 203dpi: 3.75 mm.

---

### ESC 3 — Set Line Spacing
- **Hex:** `1B 33 n`
- **Range:** `0 ≤ n ≤ 255`
- **Description:** Line spacing = `n × vertical motion unit` (standard mode), or horizontal motion unit in certain page mode directions.

---

### ESC = — Select Peripheral Device
- **Hex:** `1B 3D n`
- **Range:** `1 ≤ n ≤ 3`

| n | Function |
|---|---|
| 1, 3 | Enable printer |
| 2 | Disable printer (ignores all commands except ESC= and real-time) |

---

### ESC ? — Cancel User-Defined Characters
- **Hex:** `1B 3F n`
- **Range:** `32 ≤ n ≤ 126`
- **Description:** Removes user-defined character at code n. Resident character is used instead.

---

### ESC @ — Initialize Printer
- **Hex:** `1B 40`
- **Description:** Resets printer to power-on state. Clears print buffer. Does **not** clear receive buffer or NV memory.

---

### ESC D — Set Horizontal Tab Positions
- **Hex:** `1B 44 n1..nk 00`
- **Range:** `1 ≤ n ≤ 255`, `0 ≤ k ≤ 32`
- Default positions: columns 8, 16, 24, ..., 248.
- `ESC D NUL` cancels all tab positions. Max 32 tabs.

---

### ESC E — Turn Emphasized Mode On/Off
- **Hex:** `1B 45 n`
- **Range:** `0 ≤ n ≤ 255`, Default: `n=0`
- LSB=0: Off; LSB=1: On.

---

### ESC G — Turn Double-Strike Mode On/Off
- **Hex:** `1B 47 n`
- **Range:** `0 ≤ n ≤ 255`, Default: `n=0`
- LSB=0: Off; LSB=1: On.

---

### ESC J — Print and Feed Paper
- **Hex:** `1B 4A n`
- **Range:** `0 ≤ n ≤ 255`
- **Description:** Prints buffer, feeds `n × vertical motion unit`. In page mode, only moves print position.

---

### ESC L — Select Page Mode
- **Hex:** `1B 4C`
- **Description:** Switches to page mode. Return to standard mode via `ESC S`, `FF`, or `ESC @`.
- Commands **not active** in page mode: `ESC L`, `FS q`, `GS ( A`
- Commands **not effective** in page mode (applied on return to standard): `ESC V`, `ESC a`, `ESC {`, `GS L`, `GS W`

---

### ESC M — Select Character Font
- **Hex:** `1B 4D n`
- **Range:** `n = 0, 1, 48, 49`, Default: `n=0`

| n | Font |
|---|---|
| 0, 48 | Font A |
| 1, 49 | Font B |

---

### ESC R — Specify International Character Set
- **Hex:** `1B 52 n`
- **Range:** `0 ≤ n ≤ 13`, Default: `n=0`

| n | Character Set | n | Character Set |
|---|---|---|---|
| 0 | U.S.A | 7 | Spain I |
| 1 | France | 8 | Japan |
| 2 | Germany | 9 | Norway |
| 3 | U.K | 10 | Denmark II |
| 4 | Denmark I | 11 | Spain II |
| 5 | Sweden | 12 | Latin America |
| 6 | Italy | 13 | Korea |

---

### ESC S — Select Standard Mode
- **Hex:** `1B 53`
- **Description:** Switches back to standard mode. Clears print buffer. `CAN` and `GS $` are ignored in standard mode.

---

### ESC T — Select Print Direction in Page Mode
- **Hex:** `1B 54 n`
- **Range:** `0 ≤ n ≤ 3` or `48 ≤ n ≤ 51`, Default: `n=0`

| n | Print Direction | Starting Position |
|---|---|---|
| 0, 48 | Left → Right | Upper left |
| 1, 49 | Bottom → Top | Lower left |
| 2, 50 | Right → Left | Lower right |
| 3, 51 | Top → Bottom | Upper right |

---

### ESC V — Turn 90° Clockwise Rotation On/Off
- **Hex:** `1B 56 n`
- **Range:** `0 ≤ n ≤ 2` or `48 ≤ n ≤ 50`, Default: `n=0`
- `n=0,48`: Off; `n=1,2,49,50`: On. Not effective in page mode.

---

### ESC W — Set Print Area in Page Mode
- **Hex:** `1B 57 xL xH yL yH dxL dxH dyL dyH`
- **Description:**
  - Horizontal start = `(xL + xH×256) × horizontal motion unit`
  - Vertical start = `(yL + yH×256) × vertical motion unit`
  - Horizontal width = `(dxL + dxH×256) × horizontal motion unit`
  - Vertical width = `(dyL + dyH×256) × vertical motion unit`
- Max printable area: 180dpi → 72.2 mm × 234.3 mm; 203dpi → 72 mm × 207.75 mm

---

### ESC \ — Set Relative Print Position
- **Hex:** `1B 5C nL nH`
- **Description:** Moves print position `(nL + nH×256) × motion unit` to the right from current position.

---

### ESC a — Set Position Alignment
- **Hex:** `1B 61 n`
- **Range:** `0 ≤ n ≤ 2` or `48 ≤ n ≤ 50`, Default: `n=0`

| n | Alignment |
|---|---|
| 0, 48 | Left |
| 1, 49 | Center |
| 2, 50 | Right |

Not effective in page mode.

---

### ESC d — Print and Feed n Lines
- **Hex:** `1B 64 n`
- **Range:** `0 ≤ n ≤ 255`
- **Description:** Prints buffer, feeds n lines based on `ESC 2`/`ESC 3` settings.

---

### ESC i — Partial Cut
- **Hex:** `1B 69`
- **Description:** Executes a partial cut (1 point left uncut). Requires autocutter hardware.

---

### ESC m — Partial Cut
- **Hex:** `1B 6D`
- **Description:** Same as `ESC i`. Executes partial cut (1 point left uncut).

---

### ESC p — Generate Pulse
- **Hex:** `1B 70 m t1 t2`
- **Range:** `m = 0,1,48,49`; `0 ≤ t1,t2 ≤ 255`
- ON time = `t1 × 2 ms`; OFF time = `t2 × 2 ms` (if t2 < t1, OFF = `t1 × 2 ms`)

| m | Connector Pin |
|---|---|
| 0, 48 | Pin 2 |
| 1, 49 | Pin 5 |

---

### ESC t — Select Character Code Table
- **Hex:** `1B 74 n`
- **Range:** `0–5, 16–19, 21–31, 33–42, 47, 49–52, 255`, Default: `n=0`

| n | Code Page |
|---|---|
| 0 | CP437 (USA) |
| 1 | Katakana |
| 2 | CP850 (Multilingual) |
| 3 | CP860 (Portuguese) |
| 4 | CP863 (Canadian-French) |
| 5 | CP865 (Nordic) |
| 16 | CP1252 (Latin I) |
| 17 | CP866 (Cyrillic #2) |
| 18 | CP852 (Latin 2) |
| 19 | CP858 (Euro) |
| 21 | CP862 (Hebrew) |
| 22 | CP864 (Arabic) |
| 23 | Thai42 |
| 24 | CP1253 (Greek) |
| 25 | CP1254 (Turkish) |
| 26 | CP1257 (Baltic) |
| 27 | Farsi |
| 28 | CP1251 (Cyrillic) |
| 29 | CP737 (Greek) |
| 30 | CP775 (Baltic) |
| 31 | Thai14 |
| 33 | CP1255 (Hebrew) |
| 34–35, 39 | Thai variants |
| 36 | CP855 (Cyrillic) |
| 37 | CP857 (Turkish) |
| 38 | CP928 (Greek) |
| 40 | CP1256 (Arabic) |
| 41 | CP1258 (Vietnam) |
| 42 | Khmer |
| 47 | CP1250 (Czech) |
| 49–51 | TCVN / VISCII (Vietnamese) |
| 52 | CP912 (Albania) |
| 255 | User Code Page |

---

### ESC v — Transmit Paper Sensor Status
- **Hex:** `1B 76`
- **Description:** Transmits 1 byte. `0x03` = near end; `0x0C` = paper end.

---

### ESC { — Turn Upside-Down Print Mode On/Off
- **Hex:** `1B 7B n`
- **Range:** `0 ≤ n ≤ 255`, Default: `n=0`
- LSB=0: Off; LSB=1: On. Valid only at beginning of line. Not effective in page mode.

---

### FS p — Print NV Bit Image
- **Hex:** `1C 70 n m`
- **Range:** `1 ≤ n ≤ 255`; `0 ≤ m ≤ 3` or `48 ≤ m ≤ 51`

| m | Mode |
|---|---|
| 0, 48 | Normal |
| 1, 49 | Double-width |
| 2, 50 | Double-height |
| 3, 51 | Quadruple |

---

### FS q — Define NV Bit Image
- **Hex:** `1C 71 n [xL xH yL yH d1..dk]1..[xL xH yL yH d1..dk]n`
- **Range:** `1 ≤ n ≤ 255`; max `(xL+xH×256) ≤ 1023`; max `(yL+yH×256) ≤ 288`; NV capacity = 256 KB
- Horizontal dots = `(xL+xH×256)×8`; Vertical dots = `(yL+yH×256)×8`
- All previously defined NV images are deleted when this command is executed.

---

### GS ! — Select Character Size
- **Hex:** `1D 21 n`
- **Range:** `0 ≤ n ≤ 255`, Default: `n=0`
- Bits 0–3: vertical enlargement (1–8x); Bits 4–7: horizontal enlargement (1–8x)

| Bits 4–7 (Hex) | Horizontal | Bits 0–3 (Hex) | Vertical |
|---|---|---|---|
| 00 | ×1 | 00 | ×1 |
| 10 | ×2 | 01 | ×2 |
| 20 | ×3 | 02 | ×3 |
| 30 | ×4 | 03 | ×4 |
| ... | ... | ... | ... |
| 70 | ×8 | 07 | ×8 |

---

### GS $ — Set Absolute Vertical Print Position (Page Mode)
- **Hex:** `1D 24 nL nH`
- **Description:** Sets vertical print start position in page mode. Ignored in standard mode.

---

### GS ( A — Execute Test Print
- **Hex:** `1D 28 41 02 00 n m`
- **Range:** `n=0–2 or 48–50`; `m=1,2 or 49,50`

| m | Test Pattern |
|---|---|
| 1, 49 | Hexadecimal dump mode |
| 2, 50 | Self-test (configuration + default code page) |

---

### GS ( L / GS 8 L — Select Graphics Data
- **Hex (GS ( L):** `1D 28 4C pL pH m fn [parameters]`
- **Hex (GS 8 L):** `1D 38 4C p1 p2 p3 p4 m fn [parameters]`
- pL/pH specifies byte count after pH.

| fn | Function |
|---|---|
| 0, 48 | Transmit NV graphics memory capacity |
| 2, 50 | Print graphics data from print buffer |
| 3, 51 | Transmit remaining NV graphics memory capacity |
| 64 | Transmit NV graphics key code list |
| 65 | Delete all NV graphics data |
| 66 | Delete specified NV graphics data (by kc1, kc2) |
| 67 | Define NV graphics data |
| 69 | Print specified NV graphics data (by kc1, kc2) |
| 112 | Store graphics data in print buffer |

---

### GS ( k — Specify and Print Symbol (QR Code etc.)
- **Hex:** `1D 28 6B pL pH cn fn [parameters]`
- Used for QR Code encoding and printing. Supports numeric, alphanumeric, Kanji, and 8-bit data compression modes.

---

### GS * — Define Downloaded Bit Image
- **Hex:** `1D 2A x y d1..d(x×y×8)`
- **Range:** `1 ≤ x ≤ 255`; `1 ≤ y ≤ 48`; `x×y ≤ 1536`
- User-defined characters are cleared when this command is executed.

---

### GS / — Print Downloaded Bit Image
- **Hex:** `1D 2F m`
- **Range:** `0 ≤ m ≤ 3` or `48 ≤ m ≤ 51`
- Modes: Normal / Double-width / Double-height / Quadruple. Must be at line start with empty buffer.

---

### GS : — Start/End Macro Definition
- **Hex:** `1D 3A`
- **Description:** Toggles macro definition on/off. Macro is executed with `GS ^`.

---

### GS B — Turn White/Black Reverse Print Mode On/Off
- **Hex:** `1D 42 n`
- **Range:** `0 ≤ n ≤ 255`, Default: `n=0`
- LSB=0: Off; LSB=1: On. Does not affect multi-byte characters (CJK).

---

### GS H — Select Print Position of HRI Characters
- **Hex:** `1D 48 n`
- Specifies where HRI characters are printed relative to barcode.

---

### GS I — Transmit Printer ID
- **Hex:** `1D 49 n`
- Transmits printer identification information.

---

### GS L — Set Left Margin
- **Hex:** `1D 4C nL nH`
- **Description:** Left margin = `(nL + nH×256) × horizontal motion unit`. Not effective in page mode.

---

### GS V — Select Cut Mode and Execute Cut
- **Hex:** `1D 56 n`
- **Description:** Executes partial cut. Requires autocutter hardware.

---

### GS W — Set Print Area Width
- **Hex:** `1D 57 nL nH`
- **Description:** Print area width = `(nL + nH×256) × horizontal motion unit`. Not effective in page mode.

---

### GS ^ — Execute Macro
- **Hex:** `1D 5E r t m`
- **Description:** Executes macro defined by `GS :`. `r` = repetitions; `t` = wait time; `m` = mode.

---

### GS a — Enable/Disable ASB (Automatic Status Back)
- **Hex:** `1D 61 n`
- **Range:** `0 ≤ n ≤ 255`, Default: `n=0`
- `n=0`: Disable; `n>0`: Enable. Printer continuously transmits 4-byte status.

**ASB Status Format (4 bytes):**

| Byte | Bit | Off | On |
|---|---|---|---|
| 1st | 2 | Drawer pin 3 LOW | Drawer pin 3 HIGH |
| 1st | 3 | Online | Offline |
| 1st | 5 | Cover closed | Cover open |
| 1st | 6 | FEED button not pressed | FEED button pressed |
| 2nd | 2 | No mechanical error | Mechanical error |
| 2nd | 3 | No autocutter error | Autocutter error |
| 2nd | 5 | No unrecoverable error | Unrecoverable error |
| 2nd | 6 | No auto-recoverable error | Auto-recoverable error |
| 3rd | 0,1 | Paper adequate | Paper near end (0x03) |
| 3rd | 2,3 | Paper present | No paper (0x0C) |

---

### GS f — Select Font for HRI Characters
- **Hex:** `1D 66 n`
- **Range:** `n = 0,1,48,49`, Default: `n=0`

| n | Font |
|---|---|
| 0, 48 | Font A |
| 1, 49 | Font B |

---

### GS h — Set Bar Code Height
- **Hex:** `1D 68 n`
- **Range:** `1 ≤ n ≤ 255`, Default: `n=162`
- Height = `n dots`. Unit: 180dpi = 0.141 mm/dot; 203dpi = 0.125 mm/dot.

---

### GS k — Print Bar Code
- **Hex (format ①):** `1D 6B m d1..dk NUL` — `0 ≤ m ≤ 6`
- **Hex (format ②):** `1D 6B m n d1..dn` — `65 ≤ m ≤ 73`

| m (①) | m (②) | Barcode |
|---|---|---|
| 0 | 65 | UPC-A |
| 1 | 66 | UPC-E |
| 2 | 67 | JAN13 (EAN13) |
| 3 | 68 | JAN8 (EAN8) |
| 4 | 69 | CODE39 |
| 5 | 70 | ITF |
| 6 | 71 | CODABAR |
| — | 72 | CODE93 |
| — | 73 | CODE128 |

---

### GS r — Transmit Status
- **Hex:** `1D 72 n`
- **Range:** `n = 1,2,49,50`

| n | Function |
|---|---|
| 1, 49 | Paper sensor status |
| 2, 50 | Drawer kick-out connector status |

**Paper sensor (n=1,49):**

| Bit | Off | On |
|---|---|---|
| 0,1 | Paper adequate | Paper near end (0x03) |
| 2,3 | Paper present | No paper (0x0C) |

---

### GS v 0 — Print Raster Bit Image
- **Hex:** `1D 76 30 m xL xH yL yH d1..dk`
- **Range:** `0 ≤ m ≤ 3` or `48 ≤ m ≤ 51`; `1 ≤ (xL+xH×256) ≤ 128`; `1 ≤ (yL+yH×256) ≤ 4095`
- k = `(xL+xH×256) × (yL+yH×256)`

| m | Mode |
|---|---|
| 0, 48 | Normal |
| 1, 49 | Double-width |
| 2, 50 | Double-height |
| 3, 51 | Quadruple |

---

### GS w — Set Bar Code Width
- **Hex:** `1D 77 n`
- **Range:** `2 ≤ n ≤ 6`, Default: `n=3`

| n | Module Width (mm) | Thin (mm) | Thick (mm) |
|---|---|---|---|
| 2 | 0.282 | 0.282 | 0.706 |
| 3 | 0.423 | 0.423 | 1.129 |
| 4 | 0.564 | 0.564 | 1.411 |
| 5 | 0.706 | 0.706 | 1.834 |
| 6 | 0.847 | 0.847 | 2.258 |

---

## 4. Notes

- Settings for `ESC !`, `ESC @`, printer reset, or power cycling **reset** most formatting commands.
- `NV graphics` and `NV user memory` are **not** cleared by `ESC @`.
- **Page mode** vs **Standard mode**: Many commands behave differently between the two modes. Always check the mode before sending position/print commands.
- **Real-time commands** (`DLE EOT`, `DLE DC4`) are executed with higher priority and can be processed regardless of buffer state.
