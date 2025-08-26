import os
import requests
from tqdm import tqdm

urls = [
    'https://globbiomass.org/wp-content/uploads/GB_Maps/N00E020_agb.zip',
    'https://globbiomass.org/wp-content/uploads/GB_Maps/N00E060_agb.zip'
]

outdir = './downloads'
os.makedirs(outdir, exist_ok=True)

for url in urls:
    filename = os.path.join(outdir, os.path.basename(url))
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))

    with open(filename, 'wb') as file, tqdm(
        desc=f"Descargando {filename}",
        total=total_size,
        unit='B',
        unit_scale=True,
        unit_divisor=1024
    ) as bar:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
            bar.update(len(chunk))
            
print("Descargas completadas.")
