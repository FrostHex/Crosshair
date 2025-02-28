import tkinter as tk  # pip install tkinter
import pyautogui      # pip install pyautogui
from math import cos, sin

line_wid = 3   # 线粗细（像素）
line_len = 30  # 线长度（像素）
line_gap = 5   # 中央留空长度（像素）
threshold = 2  # 鼠标点击的误差范围（像素）
line_color = 'light green'  # 十字颜色

cross_type_horizontal = False  # 绘制横十字或斜十字
theta = 3.1416/4 # 旋转45度
line_len_diag = int(line_len / (2 ** 0.5)) # 斜十字线段长度，除以根号2
line_gap_diag = int(line_gap / (2 ** 0.5)) # 斜十字中央留空长度，除以根号2
screen_width, screen_height = pyautogui.size()
center_x = int(screen_width / 2) # 屏幕中心x坐标
center_y = int(screen_height / 2) # 屏幕中心y坐标


# @brief: 将鼠标坐标(x, y)绕屏幕中心旋转theta角
# @param: x, y: 鼠标坐标
# @param: theta: 旋转角度
# @return: 旋转后的坐标(x', y')
def Rotate(x, y, theta):
    return cos(theta) * (x - center_x) - sin(theta) * (center_y - y) + center_x, sin(theta) * (x - center_x) + cos(theta) * (center_y - y) + center_y


# @brief: 更新十字准星
# @param: canvas: 画布
# @param: center_x, center_y: 十字准星中心坐标
# @param: line_len: 十字准星线段长度
# @param: line_wid: 十字准星线粗细
# @return: None
def Cross_Update(canvas, center_x, center_y, line_len, line_wid):
    global cross_type_horizontal 
    canvas.delete("all") # 清空画布
    cross_type_horizontal = not cross_type_horizontal  # 切换十字类型
    if cross_type_horizontal: # 横十字
        canvas.create_line(center_x - line_len, center_y, center_x - line_gap, center_y, width=line_wid, fill=line_color)  # 准星左侧线段
        canvas.create_line(center_x + line_gap, center_y, center_x + line_len, center_y, width=line_wid, fill=line_color)  # 准星右侧线段
        canvas.create_line(center_x, center_y - line_len, center_x, center_y - line_gap, width=line_wid, fill=line_color)  # 准星上侧线段
        canvas.create_line(center_x, center_y + line_gap, center_x, center_y + line_len, width=line_wid, fill=line_color)  # 准星下侧线段
    else: # 斜十字
        canvas.create_line(center_x - line_len_diag, center_y - line_len_diag, center_x - line_gap_diag, center_y - line_gap_diag, width=line_wid, fill=line_color) # 准星左上线段
        canvas.create_line(center_x + line_gap_diag, center_y + line_gap_diag, center_x + line_len_diag, center_y + line_len_diag, width=line_wid, fill=line_color) # 准星右下线段
        canvas.create_line(center_x - line_len_diag, center_y + line_len_diag, center_x - line_gap_diag, center_y + line_gap_diag, width=line_wid, fill=line_color) # 准星左下线段
        canvas.create_line(center_x + line_gap_diag, center_y - line_gap_diag, center_x + line_len_diag, center_y - line_len_diag, width=line_wid, fill=line_color) # 准星右上线段



# @brief: 检测鼠标是否在准星范围内
# @param: canvas: 画布
# @return: None
def Cross_Detect(canvas):
    x, y = pyautogui.position()
    global cross_type_horizontal

    # 若当前是斜十字，则将鼠标坐标旋转45度
    if not cross_type_horizontal: 
        x, y = Rotate(x, y, theta)

    # 判断鼠标是否在准星范围内
    if (x > center_x - line_len - threshold and x < center_x - line_gap + threshold and y > center_y - line_wid//2 - threshold and y < center_y + line_wid//2 + threshold):
        Cross_Update(canvas, center_x, center_y, line_len, line_wid)
    elif (x > center_x + line_gap - threshold and x < center_x + line_len + threshold and y > center_y - line_wid//2 - threshold and y < center_y + line_wid//2 + threshold):
        Cross_Update(canvas, center_x, center_y, line_len, line_wid)
    elif (x > center_x - line_wid//2 - threshold and x < center_x + line_wid//2 + threshold and y > center_y - line_len - threshold and y < center_y - line_gap + threshold):
        Cross_Update(canvas, center_x, center_y, line_len, line_wid)
    elif (x > center_x - line_wid//2 - threshold and x < center_x + line_wid//2 + threshold and y > center_y + line_gap - threshold and y < center_y + line_len + threshold):
        Cross_Update(canvas, center_x, center_y, line_len, line_wid)

    # 每帧调用一次Cross_Detect，假设帧率为60
    canvas.after(1000 // 60, lambda: Cross_Detect(canvas)) 


# @brief: 主函数
def main():
    window = tk.Tk()
    window.attributes("-transparentcolor", "white")
    window.attributes("-fullscreen", True)
    window.lift()
    window.attributes('-topmost', True)
    window.configure(bg='white')
    canvas = tk.Canvas(window, bg='white', highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=tk.YES)
    Cross_Update(canvas, center_x, center_y, line_len, line_wid) # 创建准星
    Cross_Detect(canvas)
    window.mainloop()


if __name__ == '__main__':
    main()