import requests
import os
import multiprocessing
import cv2
from PIL import Image

# abre o arquiv onde esta os links
arquivo = open("links.txt", "r")
link = []
linhas = arquivo.readlines()

# coloca os links em uma lista
i = 0
for linha in linhas:
    i = i + 1
    link.append(linha)

arquivo.close()

s = 0
ar = 0
e = 0

for url in link:
    try:
        # baixa o link que esta no vetor se o link esta com erro manda a mensagem de link errado
        r = requests.get(url)
        r.raise_for_status()
    except Exception as err:
        # print(f'Error: {err}')
        e = e + 1
        print(f'!!! Link com erro !!!')
    else:
        s = s + 1
        img = s.__str__() + '.jpg'

        with open(img, 'wb') as f:
            f.write(r.content)

        try:
            # check para ver se a imagem é valida ou não
            imagem = cv2.imread(img)
            cv2.imshow("check image", imagem)
        except Exception as err:
            er = 1
        else:
            er = 0

        if (er == 1):
            # se o arquivo não for valido deleta ele
            os.remove(img)
            s = s - 1
            ar = ar + 1
            print(f"Arquivo com erro")
        else:
            print(f'Success!')

            # read image
            imag = cv2.imread(img, cv2.IMREAD_UNCHANGED)

            # height, width, number of channels in image
            height = imag.shape[0]
            width = imag.shape[1]

            # verifica o rize da imagem, se não for 1208 x 720 converte ela
            if (height != 720) or (width != 1280):
                imag = Image.open(img)  # image extension *.png,*.jpg
                new_width = 1280
                new_height = 720
                imag = imag.resize((new_width, new_height), Image.ANTIALIAS)
                imag.save(img)  # format may what u want ,*.png,*jpg,*.gif


ok = s + ar

arquivo = open("_relatorio_.txt", "w")
arquivo.write(f"Total de links .....................: {i}")
arquivo.write(f"\nTotal de links com erro ............: {e}\n")
arquivo.write(f"\nTotal de imagens baixadas ..........: {ok}")
arquivo.write(f"\nTotal de imagens baixadas com erro .: {ar}")
arquivo.write(f"\nTotal de imagens OK ................: {s}\n")
arquivo.write(f"\nTamanho de cada imagem: {new_width} x {new_height}")
arquivo.close()

arquivo = open("0.txt", "w")
arquivo.write(f"{s}")
arquivo.close()
