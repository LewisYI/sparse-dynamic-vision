image_folder = 'D:/Projects/event_camera/ramnet/RAM_Net/data/EventScape/Town05_val/sequence_228/rgb/data'  # 图片所在的文件夹路径
import cv2
import os

# 设置参数
# image_folder = 'images'         # 图片所在的文件夹
output_video = 'val_228.mp4'
frame_rate = 25                 # 每秒25帧

# 获取所有图片文件，按文件名升序排序
image_files = sorted([
    f for f in os.listdir(image_folder)
    if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))
])

# 检查是否有图片
if not image_files:
    raise ValueError("未找到任何图像文件。请确认文件夹路径和图片格式是否正确。")

# 读取第一帧以确定图像尺寸
first_frame_path = os.path.join(image_folder, image_files[0])
first_frame = cv2.imread(first_frame_path)
if first_frame is None:
    raise FileNotFoundError(f"无法读取图片文件: {first_frame_path}")
height, width, _ = first_frame.shape

# 设置视频编码器
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video_writer = cv2.VideoWriter(output_video, fourcc, frame_rate, (width, height))

# 遍历写入每一帧
for filename in image_files:
    img_path = os.path.join(image_folder, filename)
    frame = cv2.imread(img_path)
    if frame is None:
        print(f"警告：跳过无效图像 {img_path}")
        continue
    video_writer.write(frame)

video_writer.release()
print(f"视频已保存为：{output_video}")
