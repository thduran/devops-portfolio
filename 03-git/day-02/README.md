[english below]

# **Pipeline de CI com Github Actions**

Aqui descrevo o pipeline de CI do arquivo `.github/workflows/first-workflow.yaml` (linhas 46 a 82), que automatiza o processo de teste, build e publicação de uma imagem Docker para uma aplicação Go.

## **Objetivo do workflow**

Garantir que, a cada alteração enviada ao repo, o código seja automaticamente:
1.  Obtido.
2.  Configurado no ambiente Go correto.
3.  Tenha suas dependências baixadas.
4.  Seja testado.
5.  Autenticado com o Docker Hub de forma segura.
6.  Empacotado em uma imagem Docker.
7.  Enviado (push) para o Docker Hub com versionamento automático.

## **Principais passos da pipeline**

1.  **`Obtaining code`**:
    * Utiliza action `actions/checkout@v5` para baixar o código do repo pro ambiente de execução do workflow.

2.  **`Setup Go environment`**:
    * Utiliza action `actions/setup-go@v5` pra configurar o ambiente com a versão correta (especificada como `1.22.x`).

3.  **`Install Go dependencies`**:
    * Navega até o diretório do projeto (`./git/day-02`).
    * Executa `go mod download` pra baixar as dependências do arquivo `go.mod`.

4.  **`Run tests`**:
    * No diretório do projeto, executa `go test ./... -v` pra rodar os testes de `main_test.go` e exibir os resultados.

5.  **`Logging in to Docker`**:
    * Utiliza action `docker/login-action@v3.1.0`.
    * **Segurança:** Credencias são **secrets**, configuradas em `Repo > Settings > Secrets and variables > Actions`.

6.  **`Build and push Docker image`**:
    * Utiliza action `docker/build-push-action@v6`.
    * **`context: ./git/day-02`**: diretório do `Dockerfile` e do código-fonte.
    * **`file: ./git/day-02/Dockerfile`**: caminho do `Dockerfile`.
    * **`push: true`**: push automático da imagem pro Docker Hub.
    * **`tags`**: Define tags:
        * `thiagoduran/github-actions-test:v${{ github.run_number }}`: cria tag única pra cada execução do workflow, usando o número da execução (`github.run_number`) como versão (ex: `v1`, `v2`, ...).
        * `thiagoduran/github-actions-test:latest`: Também aplica tag `latest`, prática comum pra indicar a versão mais recente.

## **Executando imagem localmente**

Após execução bem-sucedida, a imagem estará disponível no Docker Hub.

```bash
docker container run -d -p 8080:5000 thiagoduran/github-actions-test:latest
```
Isso iniciará um container com a aplicação, podendo acessar em `http://localhost:8080`.

---

[english]

# **CI pipeline with Github Actions**

Here, I describe the CI pipeline define at `.github/workflows/first-workflow.yaml` (lines 46 a 82), that automates process of testing, building and publishing of a Docker image for a Go app.

## **Workflow goals**

Ensure that, with every change pushed to the repo, the code is automatically:
1.  Obtained.
2.  Configured in the correct Go environment.
3.  Has its depedencies downloaded.
4.  Tested.
5.  Authenticated to Docker Hub securely.
6.  Packaged in a Docker image.
7.  Pushed to Docker Hub with automatic versioning.

## **Pipeline main steps**

1.  **`Obtaining code`**:
    * Uses action `actions/checkout@v5` to get the code from the repo to the workflow's runner environment.

2.  **`Setup Go environment`**:
    * Uses action `actions/setup-go@v5` to configure environment with the correct version (specified as `1.22.x`).

3.  **`Install Go dependencies`**:
    * Navigates to the project directory(`./git/day-02`).
    * Runs `go mod download` to download dependencies of `go.mod` file.

4.  **`Run tests`**:
    * In the project directory, runs `go test ./... -v` to run the tests defined in `main_test.go` and display the results.

5.  **`Logging in to Docker`**:
    * Uses action `docker/login-action@v3.1.0`.
    * **Security:** credentials are **secrets**, configured at `Repo > Settings > Secrets and variables > Actions`.

6.  **`Build and push Docker image`**:
    * Uses action `docker/build-push-action@v6`.
    * **`context: ./git/day-02`**: directory of `Dockerfile` and source code.
    * **`file: ./git/day-02/Dockerfile`**: `Dockerfile` path.
    * **`push: true`**: automatically pushes the image to Docker Hub.
    * **`tags`**: Defines tags:
        * `thiagoduran/github-actions-test:v${{ github.run_number }}`: creates a unique tag for each workflow execution, using run number (`github.run_number`) as version (ex: `v1`, `v2`, ...).
        * `thiagoduran/github-actions-test:latest`: also applies tag `latest`, common practice to indicate latest version.

## **Running image locally**

After successful execution, the image will be available in Docker Hub.

```bash
docker container run -d -p 8080:5000 thiagoduran/github-actions-test:latest
```
This will start a container with the app, accessible at `http://localhost:8080`.