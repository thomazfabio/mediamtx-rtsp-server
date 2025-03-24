# usando ffmepg para converter resoluções
## HD (1280x720)
for file in *.mp4; do ffmpeg -i "$file" -vf scale=1280:720 -c:v libx264 -crf 23 -preset fast -c:a aac -b:a 128k "HD_$file"; done

## CIF NTSC (352x240)
for file in *.mp4; do ffmpeg -i "$file" -vf scale=352:240 -c:v libx264 -crf 23 -preset fast -c:a aac -b:a 128k "CIF_NTSC_$file"; done

## VGA (640x480)
for file in *.mp4; do 
    ffmpeg -i "$file" -vf "scale=640:480,setsar=1" -c:v libx264 -crf 23 -preset fast -c:a aac -b:a 128k "VGA_$file"; 
done
