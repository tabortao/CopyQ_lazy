# 🖼️ CopyQ 自动化图片压缩与转码指南

借助 **CopyQ** 的快捷键生态与 [**Caesium CLT** ](https://saerasoft.com/caesiumclt/)强大的图像处理引擎，我们可以实现：选中图片或文件夹 -> 盲按快捷键 -> 自动完成图片压缩、转码并保存在原处。

## ✨ 核心特性
- **格式自由**：支持批量转为 WebP、JPEG 或 PNG。
- **智能排雷**：保留 EXIF 数据（防止手机竖排照片变横排），保留原文件修改时间。
- **智能识别**：支持复制单图、多图、整个文件夹，甚至支持直接复制带引号的路径文本。

---

## 🛠️ 第一步：部署 Python 驱动脚本

由于 Windows 路径的复杂性，我们使用 Python 作为“中间人”来安全调用 Caesium。

1. 在你的电脑中创建一个 Python 文件，例如：`D:\MyData\01_Projects\Code\CopyQ_lazy\Script\convert_image.py`。
2. 将以下代码复制并保存到该文件中：

```python
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

```

---

## 🚀 第二步：导入 CopyQ 命令

1. 打开 CopyQ，按下 `F6` 打开命令窗口。
2. 点击右下角 **“粘贴命令”**，导入以下配置：

```ini
[Commands]
1\Name=智能图片压缩 (Caesium) 🖼️
1\Command="
    copyq:
    // ==================== ⚙️ 配置区 ====================
    // 指向你刚刚保存的 Python 脚本路径 (请使用正斜杠 /)
    var PY_SCRIPT = 'D:/MyData/01_Projects/Code/CopyQ_lazy/Script/convert_image.py';
    // ===================================================

    var uriData = '';
    var rows = selectedItems();
    
    if (rows.length > 0) {
        uriData = str(read('text/uri-list', rows[0])) || str(read('text/plain', rows[0]));
    } 
    if (!uriData) {
        uriData = str(data('text/uri-list')) || str(data('text/plain'));
    }

    if (!uriData || (!uriData.match(/^[\"']?file:/i) && !uriData.match(/^[\"']?[a-zA-Z]:/))) {
        popup('❌ 操作错误', '请先复制或选中【图片/文件夹】', 4000);
        abort();
    }

    var lines = uriData.trim().split(/[\\r\\n]+/);
    var results = [];

    popup('🚀 开始处理', '正在呼叫引擎处理 ' + lines.length + ' 个目标...', 2000);

    for (var i in lines) {
        var rawUri = lines[i].trim();
        if (!rawUri) continue;

        rawUri = rawUri.replace(/^[\"']|[\"']$/g, '');
        var filePath = rawUri.replace(/^file:\\/\\/\\//i, '').replace(/^file:\\/\\//i, '');
        filePath = decodeURIComponent(filePath).replace(/\\\\/g, '/');

        var res = execute('cmd', '/c', 'python', '-X', 'utf8', PY_SCRIPT, filePath);
        
        var output = str(res.stdout).trim() || str(res.stderr).trim();
        results.push(output);
    }

    popup('处理报告', results.join('\\n'), 8000);
"
1\InMenu=true
1\IsGlobalShortcut=true
1\Icon=󰄄
1\GlobalShortcut=alt+w
```

---

## 🖱️ 如何使用

1. 打开 Windows 资源管理器。
2. 选中一张图片、多张图片，或者一个包含图片的**文件夹**，按下 `Ctrl + C` 复制。
3. （无需打开 CopyQ 界面）直接按下全局快捷键 **`Alt + W`**。
4. 屏幕右下角会弹出进度提示，完成后，原图旁边会自动生成压缩转码后的新图片。

---

## 🔧 高阶玩法：自定义压缩格式与画质

所有的核心处理逻辑都在 **Python 脚本** (`convert_image.py`) 中。如果你想改变输出效果，只需用记事本或代码编辑器打开该 Python 文件，修改顶部的 **⚙️ 核心配置区** 即可：

### 1. 调整压缩质量
找到 `QUALITY = "88"` 这一行：
* 想要体积更小，可调低：`QUALITY = "75"`
* 想要画质更好，可调高：`QUALITY = "95"`

### 2. 更改转换格式
找到 `TARGET_FORMAT = "webp"` 这一行：
* 转为最通用的格式：修改为 `TARGET_FORMAT = "jpeg"`
* 仅压缩原图体积但不改变格式：修改为 `TARGET_FORMAT = "original"`

### 3. 极致的无损压缩 (Lossless)
如果你不想损失任何画质，只希望剔除冗余数据来缩小体积（适合保存原图素材）：
修改 Python 代码中的 `cmd` 列表，**删掉** `-q` 和 `QUALITY` 这两行，**加上** `--lossless`：
```python
cmd = [
    CAESIUM_EXE,
    "--lossless",             # 开启无损压缩模式
    "--format", TARGET_FORMAT,
    "--same-folder-as-input",
    "-e",
    "--keep-dates"
]
```

### 4. 智能覆写（仅保留体积变小的图片）
有时候压缩完的 WebP 反而比原先的 JPG 大。如果你只想保留“确实被成功变小了”的压缩图片，可以在 Python 脚本的 `cmd` 列表中增加 `-O bigger` 参数：
```python
cmd = [
    # ... 前面的参数 ...
    "--same-folder-as-input",
    "-O", "bigger",           # 覆写策略：只有新文件比老文件小的时候才生成
    "-e",
    "--keep-dates"
]
```