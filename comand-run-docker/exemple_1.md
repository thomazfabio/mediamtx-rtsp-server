# Para rodar mapeando as portas
docker run --rm -it -p 8554:8554   -v $(pwd)/mediamtx.yml:/mediamtx.yml   -v $(pwd)/videos:/videos   7247667a3ebc