FROM python:3.12.1
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8

# 시간대 설정을 위한 환경 변수 추가
ENV TZ=Asia/Seoul

COPY . /app
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# tzdata 설치 및 시간대 설정
RUN apt-get update && \
    apt-get install -y tzdata && \
    ln -fs /usr/share/zoneinfo/Asia/Seoul /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata

# 소스 코드 복사
COPY . .

# 어플리케이션 실행
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]

# 이미지 생성 명령어c
# docker build -f Dockerfile -t python .
#

# 컨테이너 생성 명령어
#docker run -p 5100:5100 python