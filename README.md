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

워크플로가 실행되려면, 버전 태그를 푸시해야 합니다. 예를 들어, `v1.0.0`이라는 태그를 푸시하여 새 릴리스를 생성할 수 있습니다:

```bash
git tag
git push origin <tag> # <tag>를 실제 태그로 수정하여 입력
```

### 7. GPG 사용 
```bash
git commit -m "Your commit message" -S

```

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
