import os
import sys

import requests
from tqdm import tqdm


def download_with_progress(url: str, out_filename: str):
    r = requests.get(url, stream=True)
    if r.status_code != 200:
        return False
    total_size = int(r.headers.get('content-length', 0))
    block_size = 1024  # 1 Kilobyte
    t = tqdm(total=total_size, unit='iB', unit_scale=True)
    with open(out_filename, 'wb') as f:
        for data in r.iter_content(block_size):
            t.update(len(data))
            f.write(data)
    t.close()
    if total_size != 0 and t.n != total_size:
        print('Erro no download!!!')
        return False
    return True


if not os.path.exists('yolo_weights/yolov3.weights'):
    print('Aguarde. Fazendo download dos pesos da yolo darknet...')
    success = download_with_progress('https://pjreddie.com/media/files/yolov3.weights',
                                     'yolo_weights/yolov3.weights')
    if not success:
        sys.exit('Não foi possível obter os pesos yolov3 da darknet!!!')

TRAIN_DIR = 'bases/yolo/'
if not os.path.exists(TRAIN_DIR):
    sys.exit('Não foi encontrado diretório bases/yolo. Use o arquivo '
             'extracoes/yolo.py para gerar a base de treinamento. Utilize labelImg '
             ' ou outro similar para revisar as marcações e treinar novamente.')

with open('yolo_weights/container_train.txt', 'w') as train:
    for filename in os.listdir(TRAIN_DIR):
        with open(os.path.join(TRAIN_DIR, filename, filename + '.txt')) as txt_in:
            labels = txt_in.readline()
        train.write(os.path.join(TRAIN_DIR, filename, filename + '.jpg') +
                    ' ' + labels + '0')

print('Foi baixado arquivo yolo_weights/yolov.weights '
      'e montado arquivo de treinamento yolo_weights/train_container.txt a partir do '
      ' diretório yolo(gerado por extracoes/yolo.py e refinado com labelImg). \n'
      'Siga as intrucoes no arquivo README-yolo.md para baixar e treinar a rede yolo.')