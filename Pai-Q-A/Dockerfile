# First stage, build the frontend
FROM node:14.17.5

RUN npm config set registry https://registry.npm.taobao.org

ENV FRONTEND=/opt/vue
WORKDIR $FRONTEND

COPY vue/ $FRONTEND
RUN npm install
RUN npm run build

# Second stage for the backend
FROM python:3.7.4

ENV HOME=/opt/paid_q_a
WORKDIR $HOME

COPY . $HOME
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt




# Copy frontend from the first stage
COPY --from=0 /opt/vue/dist vue/dist

EXPOSE 80

ENV PYTHONUNBUFFERED=true
CMD ["/bin/sh", "config/run.sh"]
