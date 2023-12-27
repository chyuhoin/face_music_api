FROM python:3.9
WORKDIR /srv/face_music_api
COPY . /srv/face_music_api
# docker run的时候执行
RUN apt-get update \
&& apt-get install libglib2.0-dev \
&& apt-get install libsm6 \
&& apt-get install libxrender1 \
&& apt-get install libxext-dev \
&& pip install -r ./requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple \
&& pip install uwsgi \
&& echo 'dockerfile build success ...'
# 仅仅只是声明
EXPOSE 5000
# docker exec的时候执行
CMD ["uwsgi", "--ini uswgi.ini"]