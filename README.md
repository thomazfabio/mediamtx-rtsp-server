# 📡 **MediaMTX RTSP Server**  
🎥 **Servidor dinâmico de RTSP para simulação de múltiplas câmeras de segurança**  

## 🚀 **Sobre o Projeto**  
Este projeto permite criar um **servidor RTSP dinâmico** utilizando **MediaMTX** e **FFmpeg** dentro de um **container Docker**. Cada vídeo armazenado no diretório definido será automaticamente transformado em um **stream RTSP**, facilitando a simulação de diversas câmeras de segurança.  

## 🔧 **Requisitos**  
Antes de começar, certifique-se de ter os seguintes itens instalados:  
✅ **Docker** e **Docker Compose**  
✅ **Imagem do MediaMTX com FFmpeg**  
✅ **Python 3** e bibliotecas necessárias  

## 📂 **Estrutura de Diretórios**  
Os vídeos devem ser organizados em pastas dentro de um diretório chamado **videos/**. Cada pasta representa uma categoria de vídeos (ex: "birds", "transit").  

📁 **videos/**  
 ├── 📁 **birds/** (Categoria "Pássaros")  
 │ ├── 🖥️ `video1.mp4`  
 │ ├── 🖥️ `video2.mp4`  
 ├── 📁 **transit/** (Categoria "Trânsito")  
 │ ├── 🖥️ `video1.mp4`  
 │ ├── 🖥️ `video2.mp4`  

Cada **vídeo** dentro de uma categoria será exposto como um **stream RTSP** com um link único.  

---

## 🔑 **Configuração de Autenticação RTSP**  

O MediaMTX permite configurar autenticação para os **streams RTSP**, garantindo que apenas usuários autorizados possam acessar ou publicar vídeos. Essa configuração é definida no arquivo **`mediamtx.yml`**, gerado pelo script `set_config.py`.  

### 📌 **Como Funciona a Autenticação?**  

No arquivo `mediamtx.yml`, os streams RTSP são definidos individualmente, incluindo o caminho do vídeo e os parâmetros de transmissão. Cada stream possui uma URL RTSP específica, e as credenciais de acesso são configuradas na seção `authInternalUsers`.  

#### ✅ **Exemplo de Estrutura de um Stream RTSP no `mediamtx.yml`**  
```yaml
transit_5:
    runOnDemand: ffmpeg -re -stream_loop -1 -i ./videos/transit/village-of-tilton-traffic-camera.mp4
      -c:v libx264 -preset veryfast -tune zerolatency -b:v 1000k -bufsize 500k -vf
      'scale=1280:720,fps=30' -r 30 -an -f rtsp rtsp://fabio:th0202@localhost:8554/transit_5
    runOnInitRestart: true
```
➡️ Aqui, o stream **`transit_5`** é gerado a partir do arquivo de vídeo localizado em `./videos/transit/village-of-tilton-traffic-camera.mp4`.  
➡️ Esse stream pode ser acessado através do **link RTSP:**  
```
rtsp://fabio:th0202@localhost:8554/transit_5
```
✅ **A estrutura da URL RTSP segue este formato:**  
```
rtsp://usuario:senha@endereco_servidor:porta/nome_do_stream
```
No exemplo acima:  
- **Usuário:** `fabio`  
- **Senha:** `th0202`  
- **Endereço do Servidor:** `localhost`  
- **Porta:** `8554`  
- **Nome do Stream:** `transit_5`  

### 🔒 **Configuração de Usuários e Permissões**  

A autenticação RTSP é definida na seção `authInternalUsers` do `mediamtx.yml`.  

#### ✅ **Exemplo da Configuração de Usuários e Permissões**  
```yaml
authInternalUsers:
- user: fabio
  pass: th0202
  ips: []
  permissions:
  - action: publish
- user: th
  pass: th0202
  ips: []
  permissions:
  - action: read
```
📌 **Explicação:**  
- O usuário **`fabio`** tem a permissão `"publish"`, ou seja, pode publicar (transmitir) vídeos no servidor.  
- O usuário **`th`** tem a permissão `"read"`, ou seja, pode apenas visualizar os streams RTSP, mas **não pode transmitir** novos vídeos.  
- O campo `"ips": []` permite restringir o acesso a determinados IPs. Se estiver vazio, qualquer IP pode acessar.  

⚠️ **IMPORTANTE:**  
Antes de rodar o script `set_config.py`, edite as credenciais no próprio script para que os usuários e senhas reflitam a configuração desejada no `mediamtx.yml`. Isso garantirá que os links RTSP gerados funcionem corretamente.  

--- 

## ⚙️ **Passo a Passo para Configuração**  

### 1️⃣ **Clone o Repositório**  
```bash
git clone https://github.com/seu-usuario/mediamtx-rtsp-server.git
cd mediamtx-rtsp-server
```

### 2️⃣ **Crie a pasta de vídeos e adicione arquivos**  
```bash
mkdir -p videos/birds
mkdir -p videos/transit
mv meus_videos/*.mp4 videos/birds/
```

### 3️⃣ **Instale dependências Python**  
```bash
pip install -r requirements.txt
```

### 4️⃣ **Gere a Configuração do Servidor**  
```bash
python set_config.py
```
🔹 Isso irá gerar:  
✔️ O arquivo `mediamtx.yml` com a configuração RTSP  
✔️ Um arquivo `rtsp_streams.txt` com os links RTSP  

### 5️⃣ **Inicie o Servidor RTSP com Docker**  
```bash
docker run --rm -it --network host \
  -v $(pwd)/mediamtx.yml:/mediamtx.yml \
  -v $(pwd)/videos:/videos \
  mediamtx-image
```

### 6️⃣ **Acesse os Streams RTSP**  
Os links RTSP serão gerados no arquivo **`rtsp_streams.txt`**.  
📡 Exemplo de link RTSP:  
```
rtsp://fabio:th0202@localhost:8554/birds_1
```

### 7️⃣ **Testando o Stream**  
📺 **Usando VLC:**  
Abra o VLC → `Mídia` → `Abrir fluxo de rede` → Cole o link RTSP.  

🎬 **Usando FFplay:**  
```bash
ffplay rtsp://fabio:th0202@localhost:8554/birds_1
```

---

## 🛠 **Personalização**  
- **Altere as credenciais no `set_config.py` antes de rodar o script.**  
- **Adapte as configurações de qualidade no `mediamtx.yml` conforme necessário.**  

## 📌 **Contribuição**  
Sugestões e melhorias são bem-vindas! Abra uma **issue** ou envie um **pull request**.  

🚀 **Divirta-se simulando câmeras de segurança com RTSP!**
