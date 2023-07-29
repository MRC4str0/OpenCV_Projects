import numpy as np
import cv2

class bgd_remove:

    def __init__(self, img_path = None):
        
        if img_path == None:
            print('Imagem Vazia')
        else:
            self.img = cv2.imread(img_path)

        cv2.namedWindow('Background Remove')
        cv2.createTrackbar('0 - Apagar\n1 - Adicionar', 'Background Remove', 0, 1, self.nada)
        self.img_copy = self.img.copy()
        self.mask = np.zeros(self.img.shape[:2], np.uint8)
        self.cdr_list = list()
        self.mode = self.press_mouse = False

    
    def draw(self, event, x, y, flag, param):
        
        if self.mode:
            pos_track = cv2.getTrackbarPos('0 - Apagar\n1 - Adicionar', 'Background Remove')
            color = (0, 0, 0) if pos_track == 0 else (255, 255, 255)

            if event == cv2.EVENT_LBUTTONDOWN:
                self.press_mouse = True

            elif event == cv2.EVENT_LBUTTONUP:
                self.press_mouse = False

            elif event == cv2.EVENT_MOUSEMOVE and self.press_mouse:
                cv2.circle(self.img_copy, (x, y), 2, color, -1)
                cv2.circle(self.mask, (x, y), 2, color, -1)

        else:
            if event == cv2.EVENT_LBUTTONDOWN:
                if len(self.cdr_list) != 0:
                    self.cdr_list.clear()
                    self.reset_img()

                self.cdr_list.append((x, y))

            elif event == cv2.EVENT_LBUTTONUP:
                self.cdr_list.append((x, y))
                cv2.rectangle(self.img_copy, (self.cdr_list[0][0], self.cdr_list[0][1]), (x, y), (0, 0, 255), 2)


    def remove_background(self, img):
        shape_roi = (self.cdr_list[0][0], self.cdr_list[0][1], (self.cdr_list[1][0] - self.cdr_list[0][0]), (self.cdr_list[1][1] - self.cdr_list[0][1]))
        self.bgdModel = np.zeros((1, 65), np.float64)
        self.imgModel = np.zeros((1, 65), np.float64)

        cv2.grabCut(img, self.mask, shape_roi, self.bgdModel, self.imgModel, 3, cv2.GC_INIT_WITH_RECT)
        res = np.where((self.mask == 2) | (self.mask == 0), 0, 1).astype('uint8')
        res = img * res[:, :, np.newaxis]

        self.mode = True
        return res


    def fine_tuning(self, img_bgd, mask_tuning):
        self.mask[mask_tuning == 0] = 0
        self.mask[mask_tuning == 255] = 1

        self.mask, self.bgdModel, self.imgModel = cv2.grabCut(img_bgd, self.mask, None, self.bgdModel, self.imgModel, 3, cv2.GC_INIT_WITH_MASK)
        res = np.where((self.mask == 2) | (self.mask == 0), 0, 1).astype('uint8')
        res = img_bgd * res[:, :, np.newaxis]

        return res


    def unite_mask(self, img, img_bgd):
        mask = np.zeros(img.shape, np.uint8)
        img_aux = cv2.addWeighted(img, 0.5, mask, 0.9, 1)
        img_aux = cv2.addWeighted(img_bgd, 0.8, img_aux, 0.3, 1)

        return img_aux

# Apenas para criar a trackbar...
    def nada(self, x):
        pass


    def reset_img(self):
        self.img_copy = self.img.copy()
        self.mode = False


    def show_img(self):
        cv2.setMouseCallback('Background Remove', self.draw)

        while True:
            k = cv2.waitKey(1)

            if k == 27:
                break

            elif k == ord('r'):
                self.reset_img()

            elif k == ord('d'):
                if self.mode:
                    res = self.fine_tuning(self.img, self.mask)
                else:
                    res = self.remove_background(self.img)
                
                self.img_copy = self.unite_mask(self.img, res)
                    

            else:
                cv2.imshow('Background Remove', self.img_copy)

        cv2.destroyAllWindows()