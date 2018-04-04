FROM python:3

RUN apt-get update && apt-get install -y graphviz
RUN echo "alias ll='ls -alh'" >> ~/.bashrc
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

#COPY . .

CMD [ "python"]