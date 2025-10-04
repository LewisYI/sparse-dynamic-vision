import os

# 设置文件所在目录
folder_path = 'D:/Projects/opticalflowdata_20250725'  # 替换为你的实际路径

# 遍历目录中的所有文件
for filename in os.listdir(folder_path):
    # 只处理以 diff_ 开头并以 .csv 结尾的文件
    if filename.startswith('[\'') and filename.endswith('.csv'):
        # new_name = filename.replace('diff_', '', 1)
        new_name = filename.replace(filename[:-4], filename[2:7],1)
        old_path = os.path.join(folder_path, filename)
        new_path = os.path.join(folder_path, new_name)
        os.rename(old_path, new_path)
        print(f'Renamed: {filename} -> {new_name}')
