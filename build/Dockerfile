FROM python:3.8.2-slim-buster
RUN mkdir -p /opt/module/acs-manage
WORKDIR /opt/module/acs-manage
COPY . ./
RUN python -m pip install --upgrade pip
RUN pip install pymysql web.py==0.61 pyjwt casbin requests -i https://pypi.tuna.tsinghua.edu.cn/simple
EXPOSE 8080
CMD python run.py 8080