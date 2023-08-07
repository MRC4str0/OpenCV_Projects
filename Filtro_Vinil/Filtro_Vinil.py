import cv2

class Filtro_Vinil():

    def __init__(self, img_path):
        self.img = cv2.imread(img_path)
        self.img_copy = self.img.copy()

        cv2.namedWindow('Filtro Vinil')
        cv2.setMouseCallback('Filtro Vinil', self.mouse_location)

    
    def mouse_location(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.draw_circles(self.img, (x, y))


    def draw_circles(self, img, center):
        a, l = img.shape[:2]
        self.img_copy = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        for r in range(0, (a + l), 4):
            cv2.circle(self.img_copy, center, r, (0,0,0), 1, cv2.LINE_AA)


    def show_image(self):
        while True:
            k = cv2.waitKey(1)

            if k == 27:
                break

            elif k == ord('s'):
                try:
                    path = str(input('Digite o caminho: '))
                    cv2.imwrite(path + '.jpg', self.img_copy)
                
                except:
                    print('Erro ao salvar imagem!')

                else:
                    print('Imagem salva com sucesso!')
                    break

            else:
                cv2.imshow('Filtro Vinil', self.img_copy)


fv = Filtro_Vinil(r'Filtro_Vinil\img_teste2.jpg')
fv.show_image()