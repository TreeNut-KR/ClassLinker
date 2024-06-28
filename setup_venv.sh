#!/bin/bash

# UTF-8 인코딩 설정
export LANG=C.UTF-8

# 시스템 패키지 업데이트 및 Python 빌드에 필요한 패키지 설치
echo "시스템 패키지 업데이트 중..."
sudo apt-get update

echo "필요한 패키지 설치 중..."
sudo apt-get install -y build-essential tk-dev libncurses5-dev libncursesw5-dev libreadline6-dev libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev wget

# Python 버전 설정
PYTHON_VERSION="3.12.1"
PYTHON_PATH="/usr/local/bin/python3.12"

# 가상 환경 디렉토리 이름 설정
ENV_DIR=".venv"

# 가상 환경 생성
echo "Python ${PYTHON_VERSION} 가상 환경 생성 중..."
$PYTHON_PATH -m venv $ENV_DIR

echo "가상 환경 활성화 중..."
source $ENV_DIR/bin/activate

# pip 최신 버전으로 업그레이드 (가상 환경 내부)
echo "pip 업그레이드 중..."
python -m pip install --upgrade pip

# requirements.txt 파일에 있는 모든 패키지 설치
echo "패키지 설치 중..."
pip install -r aligo/requirements.txt

echo "가상 환경이 성공적으로 설정되었습니다."
echo "가상 환경을 활성화하려면 다음 명령을 사용하세요:"
echo "source $ENV_DIR/bin/activate"