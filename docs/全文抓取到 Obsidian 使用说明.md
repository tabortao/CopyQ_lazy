# 📥 CopyQ 全文抓取到 Obsidian 配置手册

## 第一步：后端项目环境搭建 (`fetcher`)

我们使用 `uv` 快速部署项目，确保其运行在独立的虚拟环境中。

1. **克隆项目**
   在你的代码存放目录（例如 `D:/MyData/01_Projects/Code/`）打开终端：
   ```bash
   git clone https://github.com/tabortao/fetcher.git
   cd fetcher
   ```

2. **使用 `uv` 创建并配置环境**
   ```bash
    uv venv

    # 安装依赖（方式一：使用 requirements.txt）
    uv pip install -r requirements.txt

    # 安装依赖（方式二：使用 uv sync，推荐）
    uv sync

    # 安装Playwright浏览器（推荐，用于备用方案）
    uv run playwright install chromium
   ```

3. **手动验证**
   测试一次全文抓取，确保路径和权限正常（以 example.com 为例）：
   ```bash
   .venv\Scripts\python.exe fetcher.py https://example.com -o ./test_out -i ./test_images
   ```

---

## 第二步：配置 CopyQ 命令

1. 在 CopyQ 界面按下 `F6`。
2. 点击右下角 **“粘贴命令 (Paste Commands)”**，导入以下代码：

```ini
[Commands]
1\Name=全文抓取到 Obsidian 📥
1\Command="
    copyq:
    // ==================== ⚙️ 配置区 ====================
    var WORK_DIR = 'D:/MyData/01_Projects/Code/fetcher';
    var MD_DIR = 'D:/MyData/03_Resources/MyObsidian/IPARA/03-Resources/Fetcher';
    
    // 自动生成的路径
    var PYTHON_EXE = WORK_DIR + '/.venv/Scripts/python.exe';
    var SCRIPT_PATH = WORK_DIR + '/fetcher.py';
    var IMG_DIR = MD_DIR + '/images';
    // ===================================================

    var url = str(clipboard()).trim();
    if (!/^https?:\\/\\//i.test(url)) {
        popup('❌ 错误', '剪贴板内不是有效的链接');
        abort();
    }

    popup('🚀 开始深度抓取', '正在下载全文并处理图片...\\n' + url, 3000);

    // 调用 Python 执行全文下载
    var res = execute(
        'cmd', '/c', 
        PYTHON_EXE, '-X', 'utf8', SCRIPT_PATH, 
        url, '-o', MD_DIR, '-i', IMG_DIR
    );

    var rawOutput = str(res.stdout).trim() || str(res.stderr).trim();

    if (rawOutput.length > 0) {
        var title = rawOutput.split(/[\\r\\n]+/)[0].trim();
        popup('✅ 抓取保存成功', '已存入 Obsidian：\\n' + title, 5000);
    } else {
        popup('❌ 抓取失败', '请检查 fetcher 配置或网络状态', 6000);
    }"
1\InMenu=true
1\IsGlobalShortcut=true
1\Icon=📥
1\GlobalShortcut=ctrl+shift+d
```

---

## 第三步：使用说明

### 1. 执行抓取
*   **复制链接**：在浏览器中找到你想收藏的文章，`Ctrl + C` 复制链接。
*   **快捷键触发**：按下 `Ctrl + Shift + D`。
*   **等待反馈**：
    *   **气泡 1**：提示“开始深度抓取”。
    *   **气泡 2**：几秒后（取决于图片数量），提示“抓取保存成功”。

### 2. 在 Obsidian 中查看
*   进入你的 Obsidian，定位到 `03-Resources/Fetcher` 文件夹。
*   你会看到刚才抓取的网页已转为 `.md` 文件。
*   所有的网页图片已自动保存到该文件夹下的 `images` 子目录中，并已在 Markdown 中正确引用。

---

## 💡 维护与自定义
*   **修改存储位置**：如果你想更换 Obsidian 的存放目录，只需按 `F6` 修改代码中 `MD_DIR` 的路径即可。
*   **更新项目**：如果 `fetcher` 有更新，进入文件夹执行 `git pull`，然后 `uv pip install -r requirements.txt` 即可完成升级。
*   **路径注意**：代码中建议始终使用正斜杠 `/`，以避免 Windows 环境下繁琐的转义字符问题。