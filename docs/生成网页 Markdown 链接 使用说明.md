# 🚀 CopyQ 自动化：网页 Markdown 链接抓取指南

通过此功能，你只需复制一个 URL，按下快捷键，CopyQ 会自动在后台抓取网页标题，并在你的光标处直接粘贴出 `[标题](链接)`。

## 第一步：部署后端抓取项目 (`fetcher`)

我们使用 `uv` 来管理 Python 环境，确保抓取速度和依赖隔离。

1. **克隆项目**
   在你的工作目录（例如 `D:/MyData/01_Projects/Code/`）打开终端：
   ```bash
   git clone https://github.com/tabortao/fetcher.git
   cd fetcher
   ```

2. **安装虚拟环境**
   使用 `uv` 快速创建环境并安装依赖：
   ```bash
   # 创建虚拟环境
    uv venv

    # 安装依赖（方式一：使用 requirements.txt）
    uv pip install -r requirements.txt

    # 安装依赖（方式二：使用 uv sync，推荐）
    uv sync

    # 安装Playwright浏览器（推荐，用于备用方案）
    uv run playwright install chromium
   ```

3. **测试脚本**
   确保手动执行可以成功获取标题：
   ```bash
   # 使用虚拟环境中的 python 执行
   .venv\Scripts\python.exe fetcher.py https://mp.weixin.qq.com/s/cwJqbFlThxzkHf0wtI8pBg --title-only
   ```

---

## 第二步：配置 CopyQ 命令

1. 在 CopyQ 主窗口按下 `F6` 进入 **“命令/全局快捷键”** 设置。
2. 点击右下角 **“粘贴命令 (Paste Commands)”**，导入以下配置：

```ini
[Commands]
1\Name=生成网页 Markdown 链接 🔗
1\Command="
    copyq:
    var url = str(clipboard()).trim();
    if (!/^https?:\\/\\//i.test(url)) {
        popup('❌ 错误', '剪贴板内容不是链接！\\n' + url, 3000);
        abort();
    }

    popup('正在抓取标题...', '请求发送中 ⏳', 1500);

    var scriptPath = 'D:/MyData/01_Projects/Code/fetcher/fetcher.py';
    
    // 执行 Python 脚本
    var res = execute('cmd', '/c', 'python', '-X', 'utf8', scriptPath, url, '--title-only');
    
    // 获取输出内容（如果 stdout 为空，则去 stderr 里找，以防脚本把日志打错地方）
    var rawOutput = str(res.stdout).trim();
    if (!rawOutput) {
        rawOutput = str(res.stderr).trim();
    }

    // 【核心逻辑】：无视 exitCode，只要有内容就当做成功！
    if (rawOutput.length > 0) {
        // 提取第一行作为标题
        var lines = rawOutput.split(/[\\r\\n]+/);
        var title = lines[0].trim();
        
        if (title) {
            var markdownLink = '[' + title + '](' + url + ')';
            
            // 1. 强行插入到 CopyQ 历史记录的最顶端（第 0 行）
            var clipTab = config('clipboard_tab');
            if (clipTab) tab(clipTab); 
            insert(0, markdownLink);
            select(0);
            
            // 2. 同步更新系统的物理剪贴板
            copy(markdownLink);
            copySelection(markdownLink);
            
            // 3. 模拟键盘直接粘贴到当前你正在编辑的文本框里
            paste();
            
            popup('✅ 成功', 'Markdown 链接已生成并粘贴！\\n' + title, 3000);
        } else {
            popup('⚠️ 警告', '获取成功，但标题为空', 3000);
        }
    } 
    else {
        popup('❌ 抓取失败', '脚本未返回任何内容', 5000);
    }"
1\InMenu=true
1\IsGlobalShortcut=true
1\Icon=🔗
1\GlobalShortcut=ctrl+shift+l
```

---

## 第三步：使用方法

1. **复制链接**：在浏览器中复制任何网页地址（如：`https://mp.weixin.qq.com/s/Y1gsX1Rucux0bxX-zxf54Q`）。
2. **触发快捷键**：在你的编辑器（Obsidian, VS Code, 微信等）中按下 `Ctrl + Shift + L`。
3. **自动完成**：
   * 右下角会弹出“正在抓取...”的提示。
   * 1~2 秒后，光标处会自动粘贴出完美的 Markdown 链接。
   * 该链接也会同步保存到 CopyQ 的历史记录首位。

---

## 💡 小贴士
* **路径问题**：如果你的 `fetcher` 项目路径不同，请务必修改代码中 `WORK_DIR` 的值。
* **网络环境**：如果抓取 GitHub 等国外网站失败，请确保你的系统终端可以访问外网或在脚本中配置了代理。

