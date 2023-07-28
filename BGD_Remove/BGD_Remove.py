import numpy as np
import cv2

class bgd_remove:

    def __init__(self, img_path = None):
        
        if img_path == None:
            print('Imagem Vazia')
        else:
            self.img = cv2.imread(img_path)

        cv2.namedWindow('Background Remove')
        self.img_copy = self.img.copy()
        self.cdr_list = list()

    
    def draw_rect(self, event, x, y, flag, param):
        
        if event == cv2.EVENT_LBUTTONDOWN:
            if len(self.cdr_list) != 0:
                self.cdr_list.clear()
                self.reset_img()

            self.cdr_list.append((x, y))

        elif event == cv2.EVENT_LBUTTONUP:
            self.cdr_list.append((x, y))
            cv2.rectangle(self.img_copy, (self.cdr_list[0][0], self.cdr_list[0][1]), (x, y), (0, 0, 255), 2)


    def remove_background(self):
        mask = np.zeros(self.img.shape[:2], np.uint8)
        shape_roi = (self.cdr_list[0][0], self.cdr_list[0][1], (self.cdr_list[1][0] - self.cdr_list[0][0]), (self.cdr_list[1][1] - self.cdr_list[0][1]))
        bgdModel = np.zeros((1, 65), np.float64)
        imgModel = np.zeros((1, 65), np.float64)

        cv2.grabCut(self.img, mask, shape_roi, bgdModel, imgModel, 3, cv2.GC_INIT_WITH_RECT)
        res = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
        res = self.img * res[:, :, np.newaxis]

        return res


    def new_wind(self, roi_img = None):
        cv2.namedWindow('ROI')
        while cv2.waitKey(1) != 27:
            cv2.imshow('ROI', roi_img)

        cv2.destroyWindow('ROI')


    def reset_img(self):
        self.img_copy = self.img.copy()


    def show_img(self):
        cv2.setMouseCallback('Background Remove', self.draw_rect)

        while True:
            k = cv2.waitKey(1)

            if k == 27:
                break

            elif k == ord('r'):
                self.reset_img()

            elif k == ord('d'):
                res = self.remove_background()
                self.new_wind(res)

            else:
                cv2.imshow('Background Remove', self.img_copy)

        cv2.destroyAllWindows()