FROM python:3.7 AS build

RUN apt-get update
RUN apt-get install -y cmake

WORKDIR /tmp
ADD https://github.com/graphql/libgraphqlparser/archive/v0.7.0.tar.gz .
RUN tar -xzf v0.7.0.tar.gz \
    && cmake -S libgraphqlparser-0.7.0 \
    && make \
    && rm v0.7.0.tar.gz

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY trello_to_graphql trello_to_graphql
COPY run.py .


FROM python:3.7-slim

COPY --from=build /usr/local/lib/python3.7 /usr/local/lib/python3.7
COPY --from=build /tmp/libgraphqlparser.so /usr/lib/

USER nobody

WORKDIR /app
COPY --from=build /app .
CMD ["python", "-u", "run.py"]
