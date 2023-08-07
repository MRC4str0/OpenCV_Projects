import cv2

img = cv2.imread('img_teste1.jpg')
img_copy = img.copy()

def mouse_location(event, x, y, flag, param):
    global img_copy

    if event == cv2.EVENT_LBUTTONDOWN:
        img_copy = apl_efeito((x, y), img)


def apl_efeito(center, img):
    a, l = img.shape[:2]
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    for r in range(0, (l + a), 4):
        cv2.circle(img_gray, center, r, (0, 0, 0), 1, lineType = cv2.LINE_AA)

    return img_gray


cv2.namedWindow('Efeito')
cv2.setMouseCallback('Efeito', mouse_location)

while True:
    k = cv2.waitKey(1)

    if k == 27:
        break

    elif k == ord('s'):
        name_img = str(input('Nome do Arquivo: '))
        try:
            cv2.imwrite(name_img + '.jpg', img_copy)
        except:
            print('Erro ao salvar imagem!')
        else:
            print('Imagem salva com sucesso!')
            break

    else:
        cv2.imshow('Efeito', img_copy)
