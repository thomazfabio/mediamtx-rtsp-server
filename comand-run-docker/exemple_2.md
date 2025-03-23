# Para rodar assumindo a rede do host
docker run --rm -it --network host   -v $(pwd)/mediamtx.yml:/mediamtx.yml   -v $(pwd)/videos:/videos   7247667a3ebc