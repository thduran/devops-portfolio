[english below]

## **1. Gitflow na prática**

### **Passos:**

1.  **Iniciando:**
    * Crie o repo.
    * Inicialize o git:
      ```bash
      git init
      ```

2.  **Branch de desenvolvimento (`developer`):**
    * Crie a branch de desenvolvimento:
      ```bash
      git checkout -b developer
      ```
    * Adicione o código (ex: `main.go`), faça o commit:
      ```bash
      git add .
      git commit -m "feat: código do projeto"
      ```

3.  **Branch de funcionalidade (`feature`):**
    * Crie uma branch para uma nova funcionalidade, partindo da `developer`:
      ```bash
      git checkout -b feature/feature-xpto
      ```
    * Altere o código (`main.go`), faça o commit:
      ```bash
      git add .
      git commit -m "feat: implementa a funcionalidade XPTO"
      ```
    * Use `git log` para ver o histórico de commits em todas as branches.

4.  **Merge da feature para developer:**
    * Volte para a branch `developer`:
      ```bash
      git checkout developer
      git branch # para confirmar a branch atual
      ```
    * Integre as alterações da `feature`:
      ```bash
      git merge feature/feature-xpto
      ```

5.  **Branch de release (`release`):**
    * Crie uma branch `release` a partir da `developer` para preparar uma nova versão (ambiente de homologação):
      ```bash
      git checkout -b release
      ```
    * *Nota: A branch `main` representa a produção.* Crie-a se ainda não existir:
      ```bash
      git checkout -b main
      ```

6.  **Merge da release para main:**
    * Após testes e aprovação na `release`, integre na `main`:
      ```bash
      git checkout main
      git merge release
      ```
    * Use `git log` para ver que todas as branches tem a mesma base de commits após os merges.

7.  **Branch de correção (`hotfix`):**
    * Se surgir um bug em produção (`main`), crie branch `hotfix` partindo da `main`:
      ```bash
      git checkout -b hotfix/correcao-xpto
      ```
    * Faça a correção, adicione e commit:
      ```bash
      git add .
      git commit -m "fix: corrige bug XPTO"
      ```

8.  **Merge do hotfix:**
    * Integre na `main`:
      ```bash
      git checkout main
      git merge hotfix/correcao-xpto
      ```
    * **Importante:** Integre também na `developer` pra evitar que o bug retorne:
      ```bash
      git checkout developer
      git merge hotfix/correcao-xpto
      ```
    * *Curiosidade:* se você olhar o código na `developer` antes desse merge, ele ainda será a versão antiga, sem a correção.

---

## **2. GitHub Flow**

### **Passos:**

1.  Crie a branch `main`, adicione o código e dê push:
    ```bash
    # ... git add ., git commit ...
    git push origin main
    ```

2.  **Branch de funcionalidade (`feature`):**
    * Crie-a e mude para uma nova branch a cada funcionalidade ou correção:
      ```bash
      git checkout -b feature/xpto
      ```
    * Altere o código, faça o commit e dê push:
      ```bash
      # ... git add ., git commit ...
      git push origin feature/xpto
      ```

3.  **Abrir um Pull Request (PR):**
    * No GitHub, vai ter uma mensagem sugerindo a criação de um PR.
    * Também dá pra ver em **Pull requests > New pull request**.
    * Selecione a branch de origem (`feature/xpto`) e de destino (`main`).
    * Clique em **Create pull request**.
    * *Outra forma:* use o botão **Compare & pull request** que aparece após o push.

4.  **Revisão e merge:**
    * Por padrão, é esperado que outra pessoa revise o código do PR.
    * O revisor vai em **Pull requests**, seleciona o PR, revisa (commits, arquivos) e, estando tudo certo, clica em **Merge pull request**.

5.  **Atualizar o repo local:**
    * Volte para a branch `main` e dê um pull:
      ```bash
      git checkout main
      git pull origin main
      ```
    * Agora o código local na `main` será atualizado com o que foi feito via PR.

---

## **3. Pull Request template**

* **Criação:**
    * No repo, pressione a tecla `.` para abrir o editor online.
    * Crie pasta `.github`.
    * Dentro dela, crie arquivo chamado `pull_request_template.md`.
    * Faça o commit pelo ícone de "Controle do Código-Fonte" no editor.
    * Para voltar ao repo, clique no ícone de 3 linhas (menu).

* **Resultado:** toda vez que alguém criar PR, o campo de descrição já virá preenchido.

---

## **4. GitHub Actions: exemplo**

* **Exemplo:** O arquivo da raiz `.github/workflows/first-workflow.yaml` é um workflow que vai sendo incrementado ao longo dos estudos, mostrando o que tenho aprendido. Linhas 1 a 44 se referem ao day-01.

---

[english]

## **1. Gitflow in practice**

### **Steps:**

1.  **Starting:**
    * Create the repo.
    * Initialize git:
      ```bash
      git init
      ```

2.  **Development branch (`developer`):**
    * Create the development branch:
      ```bash
      git checkout -b developer
      ```
    * Add the code (ex: `main.go`), make the commit:
      ```bash
      git add .
      git commit -m "feat: project code"
      ```

3.  **Feature branch (`feature`):**
    * Create a branch for a new feature, starting from `developer`:
      ```bash
      git checkout -b feature/feature-xpto
      ```
    * Change the code (`main.go`), make the commit:
      ```bash
      git add .
      git commit -m "feat: implements XPTO feature"
      ```
    * Use `git log` to see the commit history across all branches..

4.  **Merge feature to developer:**
    * Go back to the `developer` branch:
      ```bash
      git checkout developer
      git branch # to confirm the current branch
      ```
    * Integrate the changes from `feature`:
      ```bash
      git merge feature/feature-xpto
      ```

5.  **Release branch (`release`):**
    * Create a `release` branch from `developer` to prepare a new version (staging environment):
      ```bash
      git checkout -b release
      ```
    * *Note: The `main` branch represents production. Create it if it doesn't exist yet:
      ```bash
      git checkout -b main
      ```

6.  **Merge release to main:**
    * After testing and approval on `release`, integrate into `main`:
      ```bash
      git checkout main
      git merge release
      ```
    * Use `git log` to see that all branches have the same commit base after the merges.

7.  **Hotfix branch (`hotfix`):**
    * If a bug appears in production (`main`), create a `hotfix` branch starting from `main`:
      ```bash
      git checkout -b hotfix/fix-xpto
      ```
    * Make the correction, add and commit:
      ```bash
      git add .
      git commit -m "fix: corrects XPTO bug"
      ```

8.  **Merge hotfix:**
    * Integrate into `main`:
      ```bash
      git checkout main
      git merge hotfix/fix-xpto
      ```
    * **Important:** Integrate also into `developer` to prevent the bug from returning:
      ```bash
      git checkout developer
      git merge hotfix/fix-xpto
      ```
    * *Note:* if you look at the code in `developer` before this merge, it will still be the old version, without the fix.

---

## **2. GitHub Flow**

### **Steps:**

1.  Create the `main` branch, add the code and push:
    ```bash
    # ... git add ., git commit ...
    git push origin main
    ```

2.  **Feature branch (`feature`):**
    * Create and switch to a new branch for each feature or fix:
      ```bash
      git checkout -b feature/xpto
      ```
    * Change the code, make the commit and push:
      ```bash
      # ... git add ., git commit ...
      git push origin feature/xpto
      ```

3.  **Open a Pull Request (PR):**
    * On GitHub, there will be a message suggesting the creation of a PR.
    * You can also go to **Pull requests > New pull request**.
    * Select the source branch (`feature/xpto`) and destination (`main`).
    * Click **Create pull request**.
    * *Another way:* use the **Compare & pull request** button that appears after the push.

4.  **Review and merge:**
    * By default, it is expected that someone else reviews the PR code..
    * The reviewer goes to **Pull requests**, selects the PR, reviews (commits, files) and, if everything is okay, clicks **Merge pull request**.

5.  **Update the local repo:**
    * Go back to the `main` branch and pull:
      ```bash
      git checkout main
      git pull origin main
      ```
    * Now the local code in `main` will be updated with what was done via PR.

---

## **3. Pull Request template**

* **Creation:**
    * In the repo, press the `.` key to open the online editor.
    * Create a `.github` folder.
    * Inside it, create a file named `pull_request_template.md`.
    * Make the commit through the "Source Control" icon in the editor.
    * To return to the repo, click the 3-line icon (menu).

* **Result:** every time someone creates a PR, the description field will already be filled.

---

## **4. GitHub Actions: example**

* **Exemplo:** The root file `.github/workflows/first-workflow.yaml` is a workflow that is being incremented throughout my studies, showing what I've been learning. Lines 1 to 44 refer to day-01.
