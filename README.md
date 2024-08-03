![transparent](https://capsule-render.vercel.app/api?type=transparent&fontColor=A991E5&text=CLASS%20LINKER&height=150&fontSize=60&desc=By%20Joffice%20:%20Kim,%20Seo,%20Goe&descAlignY=75&descAlign=60)
# TreeNut 사용 설명서

TreeNut 프로그램은 Ubuntu 20.04 LTS 이상의 운영체제에서 사용하며, 시리얼 포트를 통해 데이터를 읽고 FastAPI 서버에 전송하는 Python 기반의 응용 프로그램입니다. 이 문서에서는 프로그램을 설정하고 실행하는 방법을 설명합니다.

## 사전 요구사항

- Ubuntu 20.04 LTS 이상의 운영체제
- Python 3.12.x
- JMEDUSERVER에서 구성된 FastAPI 서버

## 설치 및 실행

### 1. 시스템 패키지 및 Python 가상환경 설정

1. **`setup_venv.sh` 스크립트 다운로드 및 실행**

   먼저, `setup_venv.sh` 스크립트를 다운로드하여 실행합니다. 이 스크립트는 시스템 패키지와 Python 가상환경을 설정합니다.

   ```bash
   chmod +x setup_venv.sh
   source ./setup_venv.sh
   ```

   스크립트가 성공적으로 실행되면, Python 가상환경이 `.venv` 디렉토리에 생성됩니다.

### 2. 설정 파일 생성 및 수정

1. **`config.ini` 파일 생성**

   `TreeNut` 프로그램을 처음 실행하면 `config.ini` 파일이 자동으로 생성됩니다. 이 파일에는 FastAPI 서버의 IP 주소와 포트 번호가 포함되어 있습니다.

2. **`config.ini` 파일 수정**

   생성된 `config.ini` 파일을 열어 IP 주소와 포트 번호를 JMEDUSERVER의 FastAPI 서버에 맞게 변경합니다:

   ```ini
   [DEFAULT]
   IP = <FastAPI 서버의 IP 주소>
   PORT = <FastAPI 서버의 포트 번호>
   ```

### 3. 실행 파일 생성

1. **PyInstaller를 사용하여 실행 파일 생성**

   PyInstaller를 사용하여 `TreeNut`의 실행 파일을 생성합니다:

   ```bash
   pyinstaller --onefile --name TreeNut --icon ClassLinker_PyQT/treenut.ico ClassLinker_PyQT/TreeNut.py
   ```

   이 명령어는 `dist` 디렉토리에 `TreeNut`이라는 이름의 실행 파일을 생성합니다.

### 4. 시리얼 포트 권한 설정

시리얼 포트를 사용하기 위해 적절한 권한을 설정합니다:

```bash
sudo chmod a+rw /dev/ttyUSB*
```

### 5. 프로그램 실행

1. **생성된 실행 파일 실행**

   `dist` 디렉토리로 이동하여 생성된 `TreeNut` 실행 파일을 실행합니다:

   ```bash
   cd dist
   ./TreeNut
   ```

   이 명령어를 통해 `TreeNut` 프로그램이 시작되며, 시리얼 포트에서 데이터를 읽고 FastAPI 서버에 전송합니다.

### 6. 버전 태그 푸시

워크플로가 실행되려면, 버전 태그를 푸시해야 합니다. 예를 들어, `v1.0.0`이라는 태그를 푸시하여 새 릴리스를 생성할 수 있습니다.

```bash
git tag v1.0.0 # v1.0.0를 실제 태그로 수정, 생성됨
git push origin v1.0.0 # v1.0.0를 실제 태그로 수정하여 입력하면 푸시됨
```
### 6. 버전 태그 삭제
```bash
git tag -d v1.0.0 # v1.0.0를 로컬에서 태그 삭제
git push origin --delete v1.0.0 # v1.0.0를 원격 저장소에서 태그 삭제 
```

# GPG 키 생성 및 Git 연동 가이드

이 문서는 GPG 키를 생성하고 Git과 연동하는 과정을 단계별로 안내합니다.

## 1. GPG 설치

GPG(GNU Privacy Guard)가 설치되어 있지 않다면 [GPG 공식 사이트](https://gnupg.org/download/)에서 설치합니다.

## 2. GPG 키 생성

### 2.1. GPG 키 생성 명령어 실행

```sh
gpg --full-generate-key
```

### 2.2. 키 종류 선택

```plaintext
원하는 키 종류를 선택하십시오.
 (1) RSA 및 RSA
 (2) DSA와 엘가말
 (3) DSA(부호만)
 (4) RSA(부호만)
 (9) ECC(서명 및 암호화) *기본값*
 (10) ECC(부호만)
 (14) 카드의 기존 키
당신의 선택은? 1
```

### 2.3. 키 크기 설정

```plaintext
RSA 키의 길이는 1024비트에서 4096비트 사이일 수 있습니다.
어떤 키 크기를 원하십니까? (3072) 4096
```

### 2.4. 키 유효 기간 설정

```plaintext
키가 얼마나 오래 유효해야 하는지 지정하십시오.
 0 = 키가 만료되지 않음
 <n> = 키가 n일 후에 만료됨
 <N>W = 키가 n주 후에 만료됨
 <N>M = 키가 n개월 후에 만료됨
 <n>y = 키가 n년 후에 만료됨
키는 유효합니까? (0) 0
키가 전혀 만료되지 않음
맞습니까? (y/N) y
```

### 2.5. 사용자 ID 설정

```plaintext
실명: CutTheWire
메일 주소: sjmbee04@gmail.com
주석:
이 USER-ID를 선택했습니다.
 "CutTheWire <sjmbee04@gmail.com>"

(N)ame, (C)omment, (E)mail 또는 (O)kay/(Q)uit? o
```

## 3. GPG 키 확인

```sh
gpg --list-secret-keys --keyid-format LONG
```

출력 예시:
```plaintext
sec   rsa4096/77AAF6EF0DB97CB8 2024-08-03 [SC]
      690496BF5EC2D0F990D0F26977AAF6EF0DB97CB8
uid                 [ultimate] CutTheWire <sjmbee04@gmail.com>
ssb   rsa4096/6CDE688F2FE4DE82 2024-08-03 [E]
```

## 4. Git에 GPG 키 추가

### 4.1. GPG 키 설정

```sh
git config --global user.signingkey 77AAF6EF0DB97CB8
```

### 4.2. GPG 프로그램 경로 설정

```sh
git config --global gpg.program "C:\Program Files (x86)\GnuPG\bin\gpg.exe"
```

### 4.3. 커밋 서명 활성화

```sh
git config --global commit.gpgSign true
```

## 5. 커밋 서명 테스트

```sh
git commit -S -m "Your commit message"
```

## 6. 문제 해결

### 6.1. GPG 에이전트 재시작

```sh
gpgconf --kill gpg-agent
gpgconf --launch gpg-agent
```

### 6.2. 환경 변수 설정

```sh
$env:GPG_TTY=(Get-Host).UI.RawUI.WindowTitle
```

### 6.3. GPG 키 다시 가져오기

```sh
gpg --import "path/to/your/private/key"
```

### 6.4. 테스트 파일로 서명 확인

```sh
echo "test" > testfile.txt
gpg --clearsign testfile.txt
```

이 문서를 참고하여 GPG 키를 생성하고 Git에 연동하여 안전하게 커밋을 서명할 수 있습니다.

## 주요 기능

- **시리얼 포트 자동 검색 및 연결**: 프로그램이 실행되면 연결된 시리얼 포트를 자동으로 검색하고 연결을 시도합니다.
- **시리얼 포트에서 읽은 데이터를 FastAPI 서버로 전송**: 시리얼 포트에서 데이터를 읽고 FastAPI 서버에 전송합니다.
- **실시간 데이터 표시를 위한 GUI 제공**: Tkinter GUI를 사용하여 사용자에게 실시간으로 데이터를 표시합니다.
- **서버 연결 테스트**: 서버 연결 테스트를 수행하고 결과를 GUI에 표시합니다.

## Troubleshooting

- **IP 주소나 포트 번호 오류**: `config.ini` 파일의 IP 주소와 포트 번호가 정확한지 확인하십시오.
- **시리얼 포트 권한 문제**: `sudo chmod a+rw /dev/ttyUSB*` 명령어로 시리얼 포트 권한을 설정하십시오.
- **FastAPI 서버 연결 실패**: FastAPI 서버가 실행 중인지, IP 주소와 포트가 올바른지 확인하십시오.

이 설명서를 참고하여 TreeNut 프로그램을 성공적으로 설치하고 사용할 수 있습니다.
