# short-url

### Executar o projeto

* Para executar o projeto é necessário que você já possua o Docker e Docker-Compose instalados em seu sistema operacional.

```bash
git clone https://github.com/MichaelDeMattos/short-url
cd short-url
sudo chmod +x run.sh
sudo chmod +x wait-for-it.sh
./run.sh
```

* Criando a estrutura de banco de dados [Migrations]
```bash
sudo docker exec -ti short-url-app-1 /bin/bash
flask db init # Somente se não foi executado nenhuma migration anteriormente
flask db migrate
flask db upgrade
```

### Executar testes

*  Para executar os testes é necessário que a aplicação esteja rodando.
```bash
pytest tests
```

### Docs

* A documentação com a collection dos endpoints esta disponível no diretório docs e pode ser aberta com o software Postman.
