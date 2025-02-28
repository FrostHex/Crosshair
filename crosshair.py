import tkinter as tk  # pip install tkinter
import pyautogui      # pip install pyautogui
from math import cos, sin

line_width = 3   # 线粗细（像素）
line_length = 30 # 线长度（像素）
gap = 5          # 留空大小（像素）
threshold = 2    # 鼠标点击的误差范围（像素）
color = 'light green'  # 十字颜色

cross_type_horizontal = True  # 初始绘制横十字
theta = 3.1416/4
diagonal_length = int(line_length / (2 ** 0.5))
diagonal_gap = int(gap / (2 ** 0.5))


def create_cross(canvas, center_x, center_y, line_length, line_width, cross_type_horizontal):
    # 横十字
    if cross_type_horizontal:
        canvas.create_line(center_x - line_length, center_y, center_x - gap, center_y, width=line_width, fill=color)  # 左
        canvas.create_line(center_x + gap, center_y, center_x + line_length, center_y, width=line_width, fill=color)  # 右
        canvas.create_line(center_x, center_y - line_length, center_x, center_y - gap, width=line_width, fill=color)  # 上
        canvas.create_line(center_x, center_y + gap, center_x, center_y + line_length, width=line_width, fill=color)  # 下
    # 斜十字
    else:
        canvas.create_line(center_x - diagonal_length, center_y - diagonal_length, center_x - diagonal_gap, center_y - diagonal_gap, width=line_width, fill=color)
        canvas.create_line(center_x + diagonal_gap, center_y + diagonal_gap, center_x + diagonal_length, center_y + diagonal_length, width=line_width, fill=color)
        canvas.create_line(center_x - diagonal_length, center_y + diagonal_length, center_x - diagonal_gap, center_y + diagonal_gap, width=line_width, fill=color)
        canvas.create_line(center_x + diagonal_gap, center_y - diagonal_gap, center_x + diagonal_length, center_y - diagonal_length, width=line_width, fill=color)


def main():
    global cross_type_horizontal
    screen_width, screen_height = pyautogui.size()
    window = tk.Tk()
    window.attributes("-transparentcolor", "white")
    window.attributes("-fullscreen", True)
    window.lift()
    window.attributes('-topmost', True)
    window.configure(bg='white')
    canvas = tk.Canvas(window, bg='white', highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=tk.YES)

    center_x = int(screen_width / 2)
    center_y = int(screen_height / 2)

    def rotate(x, y, theta):
        return cos(theta) * (x - center_x) - sin(theta) * (center_y - y) + center_x, sin(theta) * (x - center_x) + cos(theta) * (center_y - y) + center_y


    def update_cross():
        global cross_type_horizontal
        x, y = pyautogui.position()
        # 若当前是斜十字，则对鼠标位置进行旋转
        if not cross_type_horizontal:
            x, y = rotate(x, y, theta)

        if (x > center_x - line_length - threshold and x < center_x - gap + threshold and
            y > center_y - line_width//2 - threshold and y < center_y + line_width//2 + threshold):
                canvas.delete("all")
                cross_type_horizontal = not cross_type_horizontal  # 切换十字类型
                create_cross(canvas, center_x, center_y, line_length, line_width, cross_type_horizontal)
        elif (x > center_x + gap - threshold and x < center_x + line_length + threshold and
              y > center_y - line_width//2 - threshold and y < center_y + line_width//2 + threshold):
                canvas.delete("all")
                cross_type_horizontal = not cross_type_horizontal
                create_cross(canvas, center_x, center_y, line_length, line_width, cross_type_horizontal)
        elif (x > center_x - line_width//2 - threshold and x < center_x + line_width//2 + threshold and
              y > center_y - line_length - threshold and y < center_y - gap + threshold):
                canvas.delete("all")
                cross_type_horizontal = not cross_type_horizontal
                create_cross(canvas, center_x, center_y, line_length, line_width, cross_type_horizontal)
        elif (x > center_x - line_width//2 - threshold and x < center_x + line_width//2 + threshold and
              y > center_y + gap - threshold and y < center_y + line_length + threshold):
                canvas.delete("all")
                cross_type_horizontal = not cross_type_horizontal
                create_cross(canvas, center_x, center_y, line_length, line_width, cross_type_horizontal)

        canvas.after(1000 // 600, update_cross)  # 每帧调用一次update_cross，假设帧率为60


    # x_test = 0
    # y_test = 0
    # cross_type_horizontal = False
    # for x_raw in range(center_x - 100, center_x + 100):
    #     for y_raw in range(center_y - 100, center_y + 100):
    #         x_test, y_test = rotate(x_raw, y_raw, theta)
    #         if (x_test > center_x - line_length - threshold and x_test < center_x - gap + threshold and
    #             y_test > center_y - line_width//2 - threshold and y_test < center_y + line_width//2 + threshold):
    #             canvas.create_line(x_raw-1, y_raw-1, x_raw+1, y_raw+1, fill='light blue')
    #         elif (x_test > center_x + gap - threshold and x_test < center_x + line_length + threshold and
    #             y_test > center_y - line_width//2 - threshold and y_test < center_y + line_width//2 + threshold):
    #             canvas.create_line(x_raw-1, y_raw-1, x_raw+1, y_raw+1, fill='light blue')
    #         elif (x_test > center_x - line_width//2 - threshold and x_test < center_x + line_width//2 + threshold and
    #             y_test > center_y - line_length - threshold and y_test < center_y - gap + threshold):
    #             canvas.create_line(x_raw-1, y_raw-1, x_raw+1, y_raw+1, fill='light blue')
    #         elif (x_test > center_x - line_width//2 - threshold and x_test < center_x + line_width//2 + threshold and
    #             y_test > center_y + gap - threshold and y_test < center_y + line_length + threshold):
    #             canvas.create_line(x_raw-1, y_raw-1, x_raw+1, y_raw+1, fill='light blue')

    # 创建初始横十字
    create_cross(canvas, center_x, center_y, line_length, line_width, cross_type_horizontal)
    update_cross()
    window.mainloop()


if __name__ == '__main__':
    main()