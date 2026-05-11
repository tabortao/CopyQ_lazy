import sys
import subprocess
import os

# 配置路径
CAESIUM_EXE = r"D:\GreenSoftware\Image\Caesium Image Compressor\caesiumclt\caesiumclt.exe"
QUALITY = "88"

if len(sys.argv) < 2:
    print("❌ 错误: 未接收到路径")
    sys.exit(1)

input_path = sys.argv[1]

if not os.path.exists(input_path):
    print(f"❌ 错误: 找不到路径 -> {input_path}")
    sys.exit(1)

# 基础命令参数
cmd = [
    CAESIUM_EXE,
    "-q", QUALITY,
    "--format", "webp",
    "--same-folder-as-input",
    "-e",             # 保留 EXIF 元数据（修复旋转问题）
    "--keep-dates"    # 保留原文件时间戳
]

# 判断是文件还是文件夹
is_dir = os.path.isdir(input_path)
if is_dir:
    cmd.append("-R")  # 文件夹递归处理

cmd.append(input_path)

try:
    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')

    target_name = os.path.basename(input_path.rstrip('/\\'))
    if result.returncode == 0:
        if is_dir:
            print(f"✅ 成功: 文件夹 [{target_name}] 内的图片已批量处理！")
        else:
            print(f"✅ 成功: {target_name} -> webp")
    else:
        print(f"❌ 失败: {target_name}\n原因: {result.stderr.strip() or result.stdout.strip()}")
except Exception as e:
    print(f"⚠️ 执行异常: {str(e)}")
