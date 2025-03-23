import os
import ruamel.yaml

# Diretório base onde os vídeos estão armazenados
BASE_DIR = "./videos"

# Inicializa a configuração
config = {
    "paths": {},
    "authInternalUsers": [
        {"user": "fabio", "pass": "th0202", "ips": [], "permissions": [{"action": "publish"}]},
        {"user": "th", "pass": "th0202", "ips": [], "permissions": [{"action": "read"}]},
    ]
}

# Percorre as pastas dentro de /videos/
for category in os.listdir(BASE_DIR):
    category_path = os.path.join(BASE_DIR, category)
    
    if os.path.isdir(category_path):  # Confirma que é uma pasta
        for i, video in enumerate(sorted(os.listdir(category_path)), start=1):
            if video.endswith(".mp4"):
                stream_name = f"{category}_{i}"  # Ex: pedestres_1, pedestres_2...
                video_path = os.path.join(category_path, video)

                # Adiciona a configuração do stream RTSP
                config["paths"][stream_name] = {
                    "runOnInit": f"ffmpeg -re -stream_loop -1 -i {video_path} "
                                 "-c:v libx264 -preset veryfast -tune zerolatency "
                                 "-b:v 1000k -bufsize 500k "
                                 "-vf 'scale=1280:720,fps=30'"  
                                 f" -r 30 -an -f rtsp rtsp://fabio:th0202@localhost:8554/{category}_{i}",
                    "runOnInitRestart": True  # Corrigido: agora é um booleano
                }

# Salva o arquivo YAML corretamente
yaml = ruamel.yaml.YAML()
yaml.default_flow_style = False

with open("mediamtx.yml", "w") as f:
    yaml.dump(config, f)

print("✅ Arquivo 'mediamtx.yml' gerado com sucesso!")
print("🚀 Reinicie o MediaMTX para aplicar as mudanças.")
