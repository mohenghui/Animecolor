import cv2
# 测试颜色选择框
# gui
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter.colorchooser import *
import numpy as np
import threading
# from PIL import Image
from tkinter import filedialog
from PIL import ImageTk,Image




class DrawStart():
    def __init__(self):
        self.select_color = 0
        self.b=0
        self.g=0
        self.r=0
        self.file_name=[]
        self.eraser_flag=False
        self.color_pen_flag=False
        self.color_pen_radius=0
        self.mask_picture_flag=False
        self.filenames= []
        self.img_finish=None
        self.mask_picture=None
        self.mask_width=0
        self.mask_height=0
        self.org_img=None
        self.pre_img=[]
        self.pre_num=0
        self.eraser_circle_mask=None
        self.pen_circle_mask=None
        self.circle_mask_name="./mask/mask.png"
        self.destory_flag=False
        self.t1=None
        self.eraser_size=10
        self.pen_size=10
        self.pen_use=False
        self.eraser_use=False
        self.pen_index=0
        self.eraser_index=0
        self.move_fin_pohoto=None
        self.new_windows=None
        self.save_filename=""
        self.row1=None
        # self.select_move_object=-1 #0为pen,1为eraser
    def start(self):
        def mouse_draw( event, x, y, flags, parm):
            if self.eraser_flag:  # 是否触发橡皮擦功能
                if event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:
                    self.pop_move_fin_photo(1)
                    self.org_img=self.img_finish.copy()
                    self.pre_img.append(self.img_finish.copy())
                    cv2.circle(self.img_finish, center=(x, y), radius=self.eraser_size,
                               color=(255,255,255), thickness=-1)
                elif event == cv2.EVENT_MOUSEMOVE:
                    self.eraser_circle_mask=Image.open(self.circle_mask_name)
                    self.eraser_circle_mask = self.eraser_circle_mask.resize((int(self.eraser_size * 2.5), int(self.eraser_size * 2.5)))
                    self.img_finish = self.org_img
                    self.move_picture(self.eraser_circle_mask, int(x*0.97), int(y*0.97))
                    self.eraser_index=0
            elif self.color_pen_flag:
                if event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:
                    self.pop_move_fin_photo(0)
                    self.org_img = self.img_finish.copy()
                    self.pre_img.append(self.img_finish.copy())
                    cv2.circle(self.img_finish, center=(x, y), radius = self.pen_size,
                                                  color = (self.b,self.g,self.r), thickness = -1)
                elif event == cv2.EVENT_MOUSEMOVE:
                    self.pen_circle_mask = Image.open(self.circle_mask_name)
                    self.pen_circle_mask = self.pen_circle_mask.resize((int(self.pen_size*2.5), int(self.pen_size*2.5)))
                    self.img_finish = self.org_img
                    self.move_picture(self.pen_circle_mask, int(x*0.97), int(y*0.97))
                    # self.move_picture(self.pen_circle_mask, int(x), int(y))
                    self.pen_index = 0
            if self.mask_picture_flag:
                if event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:
                    self.pre_img.append(self.img_finish.copy())
                    self.img_finish=self.org_img
                    self.move_picture(self.mask_picture,int(x/2),int(y/2))

            elif event == cv2.EVENT_RBUTTONDOWN:
                self.check_state(0)
                self.check_state(1)
                self.pre_img.append(self.img_finish.copy())
                # mask = np.zeros((self.img_finish.shape[1] + 2, self.img_finish.shape[0] + 2), np.uint8)
                mask = np.zeros((self.img_finish.shape[0] + 2, self.img_finish.shape[1] + 2), np.uint8)
                cv2.floodFill(self.img_finish, mask, (x, y), [self.b,self.g,self.r])

        # img = cv2.imread(self.file_name[0])
        img = Image.open(self.file_name[0])
        img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
        img = cv2.resize(img, (int(img.shape[1] * 1.5), int(img.shape[0] * 1.5)))


        # 灰度处理
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # 平滑操作，去除噪声
        img_blur = cv2.medianBlur(img_gray, 3)
        # 通过阈值提取轮廓
        img_edge = cv2.adaptiveThreshold(img_blur,
                                         255,
                                         cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY,
                                         blockSize=25,
                                         C=3)
        # 将灰度图片变成 3 通道，用于后续合并
        img_edge = cv2.cvtColor(img_edge, cv2.COLOR_GRAY2BGR)
        # cv2.imshow("thr",img_edge)
        # 去除一些小的白点
        kernelX = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        kernelY = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

        # 膨胀，腐蚀
        ero_image = cv2.erode(img_edge, kernelX)
        ero_image = cv2.erode(ero_image, kernelX)
        dil_image = cv2.dilate(ero_image, kernelX)
        dil_image = cv2.dilate(dil_image, kernelX)
        # print(img)
        # # 腐蚀，膨胀

        dil_image = cv2.dilate(dil_image, kernelY)
        ero_image = cv2.erode(dil_image, kernelY)
        # cv2.imshow("ero",ero_image)
        # 平滑操作，去除噪声
        img_blur = cv2.medianBlur(ero_image, 3)
        cv2.namedWindow("finish")
        cv2.setMouseCallback("finish", mouse_draw)
        self.img_finish = img_blur
        self.pre_img.append(self.img_finish.copy())
        # print(self.i)
        # img_finish = np.ascontiguousarray(img_finish)
        # cv2.imshow("finish",img_finish)
        # cv2.line(img,(0,0),(300,300),(0,255,0),3)
        # self.pre_img=self.img_finish
        # print(self.img_finish)
        while self.destory_flag==False:
            cv2.imshow("ori", img)
            cv2.imshow('finish', self.img_finish)
            # 按 q 键退出
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        # cv2.destroyWindow("ori")
        # cv2.destroyWindow("finish")
        # self.img_finish=None
        self.__init__()#初始化
        cv2.destroyAllWindows()
        self.destory_flag = False
    def move_picture(self,mark,width,height):
        self.img_finish = self.org_img.copy()
        self.move_fin_pohoto = self.org_img.copy()
        im = Image.fromarray(cv2.cvtColor(self.img_finish, cv2.COLOR_BGR2RGB))
        layer = Image.new('RGBA', im.size, (0, 0, 0, 0))
        layer.paste(mark, (width, height))
        out = Image.composite(layer, im, layer)
        self.img_finish = cv2.cvtColor(np.asarray(out), cv2.COLOR_RGB2BGR)

        # self.pre_img.append(self.img_finish.copy())
    def pop_move_fin_photo(self,select_move_object):
        if(select_move_object==0):
            if (self.pen_index == 0):
                self.pen_use = True
                self.pen_index += 1
            elif (self.pen_use):
                self.img_finish=self.move_fin_pohoto
                self.pen_use = False
        else:
            if (self.eraser_index == 0):
                self.eraser_use = True
                self.eraser_index += 1
            elif (self.eraser_use):
                self.img_finish = self.move_fin_pohoto
                self.eraser_use = False
    def check_state(self,object):
        if(object==0):
            if (self.color_pen_flag):
                self.color_pen_flag = False
                self.img_finish = self.move_fin_pohoto
        else:
            if (self.eraser_flag):
                self.eraser_flag = False
                self.img_finish = self.move_fin_pohoto

    # def rotate_bound(self,image, angle):
    #     # grab the dimensions of the image and then determine the
    #     # center
    #     print(angle)
    #     image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    #     (h, w) = image.shape[:2]
    #     (cX, cY) = (w // 2, h // 2)
    #
    #     # grab the rotation matrix (applying the negative of the
    #     # angle to rotate clockwise), then grab the sine and cosine
    #     # (i.e., the rotation components of the matrix)
    #     M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
    #     cos = np.abs(M[0, 0])
    #     sin = np.abs(M[0, 1])
    #
    #     # compute the new bounding dimensions of the image
    #     nW = int((h * sin) + (w * cos))
    #     nH = int((h * cos) + (w * sin))
    #
    #     # adjust the rotation matrix to take into account translation
    #     M[0, 2] += (nW / 2) - cX
    #     M[1, 2] += (nH / 2) - cY
    #
    #     # perform the actual rotation and return the image
    #     return cv2.warpAffine(image, M, (nW, nH))

    def work(self):

        # while(1):
            def Hex_to_RGB(hex):
                r = int(hex[1:3], 16)
                g = int(hex[3:5], 16)
                b = int(hex[5:7], 16)
                self.r = r
                self.g = g
                self.b = b
                bgr = str(b) + ',' + str(g) + ',' + str(r)
                # print(bgr)
                return bgr
            root = Tk()
            # root.geometry("400x200")

            def test01():
                self.file_name.clear()
                self.file_name += filedialog.askopenfilenames()
                # print(self.file_name)
                if(self.file_name):
                    self.t1 = threading.Thread(target=Draw.start)
                    # if (not self.t1.is_alive()):
                    self.t1.start()
                # self.t1.is_alive()
                # self.t1.join()
            def test02():
                a1 = askcolor(color='black', title='请选择你要涂鸦的颜色')
                if(a1!=None):
                    self.select_color=Hex_to_RGB(a1[1])
                # print(select_color)
            def test03():
                if (self.color_pen_flag == False):
                    self.color_pen_flag = True
                    self.check_state(1)
                else:
                    self.color_pen_flag = False

                self.org_img = self.img_finish.copy()
            def test04():
                if(self.eraser_flag==False):
                    self.eraser_flag=True
                    self.check_state(0)
                else:
                    self.eraser_flag = False

                self.org_img = self.img_finish.copy()
            # a1的值为元组
            # root.config(bg=a1[1])

            def test05():
                self.pre_img.append(self.img_finish.copy())
                self.org_img=self.img_finish.copy()
                self.mask_picture_flag=True
                self.filenames.clear()
                self.filenames += filedialog.askopenfilenames()
                print(self.filenames)
                if(len(self.filenames)):
                    mark = Image.open(self.filenames[0])
                    mark = mark.resize((int(mark.width*0.5), int(mark.height*0.5)))
                    self.mask_picture=mark
                    self.move_picture(mark,50,50)
                else:
                    self.mask_picture_flag = False
            def test06():
                if(self.pre_img):
                    self.img_finish=self.pre_img.pop()

            def test07():
                self.destory_flag=True
                self.t1.join()

            # def test08(change_object,change_movement):
            #     #change_object,0为涂鸦笔改变size，1为橡皮擦改变size
            #     #change_movement,0为变小，1为变大
            #     if(change_object==0):
            #         if(change_movement==0):
            #             self.pen_size-=1
            #
            #         else:
            #             self.pen_size+=1
            #     else:
            #         if (change_movement == 0):
            #             self.eraser_size -= 1
            #         else:
            #             self.eraser_size += 1
                # print("pen_size",self.pen_size)
                # print("eraser_size",self.eraser_size)

            def test08(ev=None):
                self.pen_size=pen_size_scale.get()
            def test09(ev=None):
                self.eraser_size=earse_scale.get()
            def test10():
                self.mask_picture_flag=False
            def test11(ev=None):
                self.mask_picture = self.mask_picture.resize((mask_wsize_scale.get(), self.mask_picture.height))
            def test12(ev=None):
                self.mask_picture = self.mask_picture.resize((self.mask_picture.width, mask_hsize_scale.get()))

            def test13():
                self.new_windows = Tk(className="系统提示")
                self.new_windows.wm_attributes('-topmost', 1)
                screenwidth, screenheight = self.new_windows.maxsize()
                width = 200
                height = 100
                size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
                self.new_windows.geometry(size)
                self.new_windows.resizable(0, 0)
                lable = Label(self.new_windows, height=2)
                lable['text'] = '请输入文件名!(无后缀)'
                lable.pack()
                entry = Entry(self.new_windows)
                self.save_filename_tool = StringVar()
                entry.pack()
                entry.focus_set()
                Button(self.new_windows, text="确定", command=lambda :test14(entry.get())).pack(side=tk.RIGHT)
                self.new_windows.mainloop()

            def test14(Sfilename):
                self.save_filename = Sfilename
                if len(self.save_filename) == 0:
                    # print("用户名必须输入!")
                    root.wm_attributes('-topmost',1)
                    messagebox.showwarning(title='系统提示', message='请输入文件名!')
                    # self.new_windows('-topmost', 1)
                    self.new_windows.destroy()
                    # self.new_windows.mainloop()
                    return False
                # print("用户名：%s" % (self.save_filename))
                if(self.img_finish.all()==None):
                    self.new_windows.destroy()
                    messagebox.showwarning(title='系统提示', message='保存失败!')
                else:
                    cv2.imwrite("./" + self.save_filename + ".png", self.img_finish)
                    self.new_windows.destroy()
                    messagebox.showwarning(title='系统提示', message='保存成功!')

            root.title("")
            screenWidth = root.winfo_screenwidth()  # 获取显示区域的宽度
            screenHeight = root.winfo_screenheight()  # 获取显示区域的高度
            tk_width = 500  # 设定窗口宽度
            tk_height = 400  # 设定窗口高度
            tk_left = int((screenWidth - tk_width) / 2)
            tk_top = int((screenHeight - tk_width) / 2)
            root.geometry('%dx%d+%d+%d' % (tk_width, tk_height, tk_left, tk_top))
            root.minsize(tk_width, tk_height)  # 最小尺寸
            root.maxsize(tk_width, tk_height)  # 最大尺寸
            root.resizable(width=False, height=False)
            root.iconbitmap('image/icon.ico')
            # 背景图片
            bg_image = Image.open(r'./image/bg.jpg')
            bg_image=bg_image.resize((tk_width,tk_height))
            background_image = ImageTk.PhotoImage(bg_image)
            background_label = Label(root, image=background_image)
            background_label.place(x=0, y=0, relwidth=1, relheight=1)
            btn_1=Button(root, text='请选择你要涂鸦的图片', command=test01,
                   height=0)
            btn_1.place(x=169,y=90,anchor='w')
            # btn.pack()
            btn_2=Button(root, text='请选择你要涂鸦的颜色', command=test02,
                   height=0)
            btn_2.place(x=169, y=130, anchor='w')
            btn_3=Button(root, text='涂鸦笔', command=test03,
                   height=0)
            btn_3.place(x=208, y=170, anchor='w')

            # Text(root, width=10, height=1).grid(row=0, column=1)
            btn_4=Button(root, text='橡皮擦', command=test04,
                   height=0)
            btn_4.place(x=208, y=210, anchor='w')

            pen_size_scale = Scale(root, from_=1, to=50, orient=tk.HORIZONTAL, command=test08)
            pen_size_scale.set(10)  # 设置初始值
            pen_size_scale.place(x=60, y=170, anchor='w')

            earse_scale = Scale(root, from_=1, to=50, orient=tk.HORIZONTAL, command=test09)
            earse_scale.set(10)  # 设置初始值
            earse_scale.place(x=60, y=210, anchor='w')

            btn_5=Button(root, text='添加帖纸', command=test05,
                   height=0)
            btn_5.place(x=201, y=250, anchor='w')


            # if(self.mask_picture!=None):
            mask_wsize_scale = Scale(root, from_=50, to=700, orient=tk.HORIZONTAL, command=test11)
            # mask_wsize_scale.set(int(self.mask_picture.width * 0.5))  # 设置初始值
            # mask_wsize_scale.set(100)  # 设置初始值
            mask_wsize_scale.place(x=60, y=250, anchor='w')
            mask_hsize_scale = Scale(root, from_=50, to=700, orient=tk.HORIZONTAL, command=test12)
            # mask_hsize_scale.set(100)  # 设置初始值
            # mask_hsize_scale.set(int(self.mask_picture.height * 0.5))  # 设置初始值
            mask_hsize_scale.place(x=310, y=250, anchor='w')
            # mask_route = Scale(root, from_=0, to=360, orient=tk.HORIZONTAL, command=test13)
            # mask_route.set(0)  # 设置初始值
            # mask_route.place(x=230, y=250, anchor='w')
                # mask_hsize_scale.update()
                # mask_wsize_scale.update()
            btn_8 = Button(root, text='确定', command=test10,
                           height=0)
            btn_8.place(x=270, y=250, anchor='w')
            btn_6=Button(root, text='返回上一步', command=test06,
                   height=0)
            btn_6.place(x=196, y=290, anchor='w')
            btn_9 = Button(root, text='保存图片', command=test13,
                           height=0)
            btn_9.place(x=168, y=330, anchor='w')
            btn_7=Button(root, text='取消图片', command=test07,
                   height=0)
            btn_7.place(x=238, y=330, anchor='w')
            #涂鸦笔调整大小
            # btn_8 = Button(root, text='小一点', command=lambda :test08(0, 0),
            #                height=0)
            # btn_8.place(x=119, y=130, anchor='w')
            # btn_9 = Button(root, text='大一点', command=lambda :test08(0, 1),
            #                height=0)
            # btn_9.place(x=219, y=130, anchor='w')
            # # 橡皮擦调整大小
            # btn_10 = Button(root, text='小一点', command=lambda :test08(1, 0),
            #                height=0)
            # btn_10.place(x=119, y=160, anchor='w')
            # btn_11 = Button(root, text='大一点', command=lambda :test08(1, 1),
            #                height=0)
            # btn_11.place(x=219, y=160, anchor='w')

            root.mainloop()

if __name__ == '__main__':
    Draw=DrawStart()
    # t1 = threading.Thread(target=Draw.start)
    t2 = threading.Thread(target=Draw.work)
    # t1.start()
    t2.start()


