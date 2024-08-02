import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from matplotlib.animation import FuncAnimation

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 参数设置
x = np.linspace(-10, 10, 1000)
mean1, std1 = 0, 1  # 瘦高斯
mean2, std2 = 0, 2  # 胖高斯的标准差
amp1, amp2 = 2.5, 4  # 瘦高斯和胖高斯的幅度
step_size = 0.1  # 平移步长
start_pos = -7.5
end_pos = 7.5
frames = int((end_pos - start_pos) / step_size) + 1

# 计算归一化的瘦高斯分布
gaussian1 = norm.pdf(x, mean1, std1)
gaussian1 /= np.trapz(gaussian1, x)  # 归一化，使其面积为1


# 计算胖高斯分布
def gaussian2(height, x, mean, std):
    return height * norm.pdf(x, mean, std)


# 计算重叠面积函数（曲线乘积的积分）
def overlap_area(g1, g2):
    product = g1 * g2
    return np.trapz(np.abs(product), x)  # 取绝对值后积分


# 初始化重叠面积列表
overlap_areas1 = []
overlap_areas2 = []
products1 = []
products2 = []

# 准备图形
fig1, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 10))
ax1.set_xlim(-10, 10)
ax1.set_ylim(0, 1.5)
line1, = ax1.plot(x, gaussian1 * amp1, label='瘦高斯 (×2.5)')
line2, = ax1.plot(x, gaussian2(amp2, x, mean2, std2), label='胖高斯 (×4)')
product_plot1, = ax1.plot([], [], 'g-', label='曲线乘积 (胖高斯动)')
ax1.legend()
ax1.set_title('胖高斯运动中（瘦高斯不动）')
ax1.grid(True)

ax2.set_xlim(start_pos, end_pos)
overlap_plot1, = ax2.plot([], [], 'r-', label='重叠面积 (胖高斯动)')
ax2.set_xlabel('位置')
ax2.set_ylabel('重叠面积')
ax2.legend()
ax2.set_title('重叠面积 (胖高斯动)')
ax2.grid(True)

ax3.set_xlim(-10, 10)
ax3.set_ylim(0, 1.5)
line3, = ax3.plot(x, gaussian1 * amp1, label='瘦高斯 (×2.5)')
line4, = ax3.plot(x, gaussian2(amp2, x, mean2, std2), label='胖高斯 (×4)')
product_plot2, = ax3.plot([], [], 'g-', label='曲线乘积 (瘦高斯动)')
ax3.legend()
ax3.set_title('瘦高斯运动中（胖高斯不动）')
ax3.grid(True)

ax4.set_xlim(start_pos, end_pos)
overlap_plot2, = ax4.plot([], [], 'r-', label='重叠面积 (瘦高斯动)')
ax4.set_xlabel('位置')
ax4.set_ylabel('重叠面积')
ax4.legend()
ax4.set_title('重叠面积 (瘦高斯动)')
ax4.grid(True)


# 更新函数
def update(frame):
    shift = start_pos + frame * step_size

    # 胖高斯移动，瘦高斯不动
    gaussian2_moving = gaussian2(amp2, x, shift, std2)
    line2.set_ydata(gaussian2_moving)
    overlap1 = overlap_area(gaussian1 * amp1, gaussian2_moving)
    overlap_areas1.append(overlap1)

    # 自动调整y轴
    # ax2.set_ylim(0, 2)
    ax2.set_ylim(0, max(overlap_areas1, default=1.1) * 1.1)
    overlap_plot1.set_data(np.linspace(start_pos, start_pos + step_size * len(overlap_areas1), len(overlap_areas1)),
                           overlap_areas1)

    # 计算曲线乘积
    product1 = (gaussian1 * amp1) * gaussian2_moving
    products1.append(product1)
    product_plot1.set_data(x, product1)

    # 瘦高斯移动，胖高斯不动
    gaussian1_moving = gaussian2(amp1, x, shift, std1)
    line3.set_ydata(gaussian1_moving)
    gaussian2_static = gaussian2(amp2, x, mean2, std2)
    overlap2 = overlap_area(gaussian1_moving, gaussian2_static)
    overlap_areas2.append(overlap2)

    # 自动调整y轴
    # ax4.set_ylim(0, 2)
    ax4.set_ylim(0, max(overlap_areas2, default=1.1) * 1.1)
    overlap_plot2.set_data(np.linspace(start_pos, start_pos + step_size * len(overlap_areas2), len(overlap_areas2)),
                           overlap_areas2)

    # 计算曲线乘积
    product2 = gaussian1_moving * gaussian2_static
    products2.append(product2)
    product_plot2.set_data(x, product2)

    # 打印当前帧的重叠面积
    # print(f"Frame {frame}: 重叠面积 (胖高斯动) = {overlap1}, 重叠面积 (瘦高斯动) = {overlap2}")

    return line2, overlap_plot1, product_plot1, line3, overlap_plot2, product_plot2


# 动画
ani = FuncAnimation(fig1, update, frames=frames, blit=False, interval=50, repeat=False)

# 显示
plt.tight_layout()
plt.show()
