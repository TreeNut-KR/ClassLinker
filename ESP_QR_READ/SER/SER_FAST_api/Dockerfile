FROM python:3.12-bullseye

EXPOSE 5100

RUN mkdir /src

COPY ./FASTapi.py /src/FASTapi.py

COPY ./FAST_index.html /src/FAST_index.html

RUN pip install fastapi

RUN pip install uvicorn

RUN pip install sqlalchemy

RUN pip install dataset

RUN pip install sqlite-utils

RUN pip install jinja2

RUN pip install python-multipart

ENTRYPOINT ["python", "/src/FASTapi.py"]
# 이미지 생성 명령어
# docker build -f Dockerfile -t python .
#

# 컨테이너 생성 명령어
#docker run -p 5100:5100 python