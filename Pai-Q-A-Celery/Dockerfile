FROM python:3.7.4

ENV HOME=/opt/paid_q_a
WORKDIR $HOME

COPY . $HOME
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

EXPOSE 80

ENV PYTHONUNBUFFERED=true
CMD ["/bin/sh", "run.sh"]
