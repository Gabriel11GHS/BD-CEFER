# db_project
Ambiente de desenvolvimento: WSL Ubuntu. 
## Como rodar

### 1. Instalar o Docker
Baixe e instale o Docker no seu sistema:

- [Docker Desktop para Windows/macOS](https://www.docker.com/products/docker-desktop)
- [Docker Engine para Linux](https://docs.docker.com/engine/install/)

Verifique a instalação:
```bash
docker --version
docker compose version
```

### 2. Baixar imagem do Postgres 17
```bash
docker pull postgres:17
```

### 3. Subir DB
Na pasta do repositório clonado 
``` bash
docker compose up -d
``` 

### (Opcional) Acessar psql
```bash 
docker exec -it postgres17 bash
su postgres
psql
```

### 4. Instalar dependências do Python

```
sudo apt install python3.12-venv
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

### 5. Rodar testes

```
pytest -s
```