# BIXOLON SRP-350III ESC/POS Test Print

BIXOLON SRP-350III 영수증 프린터에 ESC/POS 커맨드를 USB로 직접 전송하는 테스트 출력 도구.

## 출력 방식

이미지 렌더링 없이 **ESC/POS 텍스트 커맨드를 bytes로 직접 조립**해서
`win32print.WritePrinter` 로 USB 포트(USB002)에 RAW 전송하는 방식.

- 텍스트 라인: cp437 인코딩 + 정렬/굵기/크기 ESC/POS 커맨드 조합
- QR 코드: `GS ( k` (Function 165–181)
- CODE128 바코드: `GS k` (type 0x49)
- 용지 컷: `GS V B 0` (부분 컷)

## 환경

- Windows
- Python 3.14+
- BIXOLON SRP-350III (USB 연결)

## 사전 조건 (최초 1회)

프린터 드라이버 없이 USB로 연결된 경우, Windows 스풀러에 RAW 큐를 수동 등록해야 한다.

PowerShell (관리자) 에서 실행:

```powershell
Add-Printer -Name "BIXOLON SRP-350III RAW" `
            -DriverName "Generic / Text Only" `
            -PortName "USB002"
```

> USB 포트 번호는 장치마다 다를 수 있다. 아래 명령으로 확인:
> ```powershell
> Get-PrinterPort | Where-Object { $_.Description -like "*BIXOLON*" }
> ```

## 설치

```sh
uv sync
```

## 사용법

```sh
# 자동 탐색 후 테스트 영수증 출력
python main.py

# 프린터 이름 직접 지정
python main.py --printer "BIXOLON SRP-350III RAW"

# 등록된 프린터 목록 확인
python main.py --list
```

## 출력 내용

테스트 영수증에 포함되는 항목:

- 가게 헤더 (2배 크기 굵게)
- 날짜 / 시간 / 영수증 번호 / 담당자
- 상품 목록 (품목 / 수량 / 금액)
- 소계 / 부가세 / 합계 / 현금 / 잔돈
- QR 코드
- CODE128 바코드
- 푸터 + 5줄 피드 + 부분 컷