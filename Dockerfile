FROM python:3.10-alpine
RUN apk update && apk add g++ jpeg-dev zlib-dev libjpeg make ffmpeg py3-matplotlib
WORKDIR /app
COPY . .
RUN --mount=type=cache,target=/root/.cache/pip \
pip install --upgrade pip && pip install -r req-prod.txt
CMD ["python", "/app/main.py"]
