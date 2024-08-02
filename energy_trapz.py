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
mean2, std2 = 0, 2  # 胖高斯的初始标准差
step_size = 0.1  # 平移步长
start_pos = -7.5
end_pos = 7.5
frames = int((end_pos - start_pos) / step_size) + 1

# 计算高斯分布
factor = 2
gaussian1 = norm.pdf(x, mean1, std1)
gaussian2 = factor * norm.pdf(x, mean2, std2)


# 计算重叠面积函数
def overlap_area(g1, g2):
    return np.trapz(np.minimum(g1, g2), x)


# 初始化重叠面积列表
overlap_areas1 = []
overlap_areas2 = []
overlap_diff = []

# 准备图形
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 10))
ax1.set_xlim(-10, 10)
ax1.set_ylim(0, max(np.max(gaussian1), np.max(gaussian2)) * 1.1)
line1, = ax1.plot(x, gaussian1, label='瘦高斯')
line2, = ax1.plot(x, gaussian2, label='胖高斯')
ax1.legend()
ax1.set_title('胖高斯运动中（瘦高斯不动）')
ax1.grid(True)

ax3.set_xlim(-10, 10)
ax3.set_ylim(0, max(np.max(gaussian1), np.max(gaussian2)) * 1.1)
line3, = ax3.plot(x, gaussian1, label='瘦高斯')
line4, = ax3.plot(x, gaussian2, label='胖高斯')
ax3.legend()
ax3.set_title('瘦高斯运动中（胖高斯不动）')
ax3.grid(True)

overlap_plot1, = ax2.plot([], [], 'r-', label='重叠面积 (胖高斯动)')
ax2.set_xlim(start_pos, end_pos)
ax2.set_xlabel('位置')
ax2.set_ylabel('重叠面积')
ax2.legend()
ax2.set_title('重叠面积 (胖高斯动)')
ax2.grid(True)

overlap_plot2, = ax4.plot([], [], 'r-', label='重叠面积 (瘦高斯动)')
ax4.set_xlim(start_pos, end_pos)
ax4.set_xlabel('位置')
ax4.set_ylabel('重叠面积')
ax4.legend()
ax4.set_title('重叠面积 (瘦高斯动)')
ax4.grid(True)

# 新增一个子图显示差值
fig2, ax5 = plt.subplots(figsize=(8, 5))
diff_plot, = ax5.plot([], [], 'b-', label='重叠面积差值')
ax5.set_xlim(start_pos, end_pos)
ax5.set_xlabel('位置')
ax5.set_ylabel('差值')
ax5.legend()
ax5.set_title('重叠面积差值')
ax5.grid(True)


# 更新函数
def update(frame):
    global gaussian2, gaussian1, factor
    shift = start_pos + frame * step_size

    # 胖高斯移动，瘦高斯不动
    gaussian2_moving = factor * norm.pdf(x, shift, std2)
    line2.set_ydata(gaussian2_moving)
    overlap1 = overlap_area(gaussian1, gaussian2_moving)
    overlap_areas1.append(overlap1)

    # 自动调整y轴
    ax2.set_ylim(0, max(overlap_areas1, default=1.1) * 1.1)
    overlap_plot1.set_data(np.linspace(start_pos, start_pos + step_size * len(overlap_areas1), len(overlap_areas1)),
                           overlap_areas1)

    # 瘦高斯移动，胖高斯不动
    gaussian1_moving = norm.pdf(x, shift, std1)
    line3.set_ydata(gaussian1_moving)
    overlap2 = overlap_area(gaussian1_moving, gaussian2)
    overlap_areas2.append(overlap2)

    # 自动调整y轴
    ax4.set_ylim(0, max(overlap_areas2, default=1.1) * 1.1)
    overlap_plot2.set_data(np.linspace(start_pos, start_pos + step_size * len(overlap_areas2), len(overlap_areas2)),
                           overlap_areas2)

    # 计算重叠面积差值
    diff = np.abs(overlap1 - overlap2)
    overlap_diff.append(diff)

    # 自动调整y轴
    ax5.set_ylim(0, max(overlap_diff, default=1.1) * 1.1)
    diff_plot.set_data(np.linspace(start_pos, start_pos + step_size * len(overlap_diff), len(overlap_diff)),
                       overlap_diff)

    # 打印当前帧的重叠面积
    print(f"Frame {frame}: 重叠面积 (胖高斯动) = {overlap1}, 重叠面积 (瘦高斯动) = {overlap2}, 差值 = {diff}")

    return line2, overlap_plot1, line3, overlap_plot2, diff_plot


# 动画
ani = FuncAnimation(fig, update, frames=frames, blit=True, interval=50, repeat=False)

# 显示
plt.tight_layout()
plt.show()
