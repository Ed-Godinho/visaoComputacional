# Edneython Campos Godinho
# RU 3836801
import os
import cv2

class avaliar_imagem:
    # A função abaixo tenta remover o background da imagem com base no intervalo de cores especificado
    def remove_background(img):
        lower = (65, 65, 65)
        upper = (255, 255, 255)
        if img is not None:
            mask = cv2.inRange(img, lower, upper)
            mask = cv2.bitwise_not(mask)
            img_mask = cv2.bitwise_and(img, img, mask=mask)
        return img_mask


    def verificar_interseccao(contorno_1_parametro, contorno_2_parametro):
        # Converte as coordenadas dos contornos para o formato de polígonos convexos e verifica a intersecção entre eles
        contorno_1 = cv2.convexHull(contorno_1_parametro)
        contorno_2 = cv2.convexHull(contorno_2_parametro)
        result = cv2.intersectConvexConvex(contorno_1, contorno_2)
        return result[0]


    def extrair_info(img):
        # Converte a imagem para escala de cinza e aplica um limiar para obter uma imagem binária e encontra os contornos
        img_ = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, threshold = cv2.threshold(img_, 1, 255, cv2.THRESH_BINARY)
        contornos, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        areas_contornos = []
        contornos_selecionados = []
        
        for contorno in contornos:
            # Calcula a área de cada contorno e verifica se o contorno deve ser avaliado, evitando contornos com intersecção
            avaliar = True
            area = cv2.contourArea(contorno)
            if len(contornos_selecionados) > 0:
                for contour_selecionado in contornos_selecionados:
                    if avaliar_imagem.verificar_interseccao(contorno, contour_selecionado):
                        avaliar = False
            
            # Se o contorno deve ser avaliado, verifica se a área está dentro do intervalo especificado e desenha um retângulo
            if avaliar and 400 < area < 6000:
                contornos_selecionados.append(contorno)
                areas_contornos.append(area)
                x, y, w, h = cv2.boundingRect(contorno)
                cv2.rectangle(img_, (x, y), (x + w, y + h), (255, 255, 255), 2)
        
        return img_, areas_contornos


def main():
    # Define a pasta que armazena as imagens dos dados
    pasta_imagens = 'imagensDados'

    # Lista os arquivos na pasta imagensDados
    files = os.listdir(pasta_imagens)
    for file in files:
        file_path = os.path.join(pasta_imagens, file)
        #Chama os métodos da classe para processar a imagem retornando a cada iteração uma tela com os contornos desenhados e a quantidade de faces encontradas na imagem são exibidas no terminal
        img = cv2.imread(file_path)
        img = avaliar_imagem.remove_background(img)
        img_, faces = avaliar_imagem.extrair_info(img)

        # Exibe a imagem com os contornos desenhados
        cv2.imshow(f"Contornos do arquivo: {file}", img_)

        # Faz print da quantidade de faces encontradas na imagem
        print(f"Quantidade de face encontradas no arquivo {file} : {len(faces)}")
        cv2.waitKey(0) # Aguarda o usuário pressionar uma tecla para continuar o loop

    cv2.destroyAllWindows()  # Fecha todas as janelas ao fim do processo.


if __name__ == '__main__':
    main()