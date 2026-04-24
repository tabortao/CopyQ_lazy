# 🛠️ CopyQ 脚本编写指南与技能栈 (CopyQ Skill)

## 1. 核心设计哲学 (Core Principles)
编写高质量 CopyQ 脚本应遵循以下三个原则：
* **鲁棒性优先 (Robustness)**：永远假设用户可能在没有选中任何条目、或者剪贴板为空的情况下触发快捷键。必须做好判空和拦截。
* **及时反馈 (Feedback)**：脚本在后台静默运行容易让人困惑，关键节点（成功、失败、网络请求中）应使用 `popup()` 给予视觉反馈。
* **兼容与平滑 (Smoothness)**：优先获取当前用户选中的条目，如果没有选中，再退而求其次读取剪贴板最顶部内容。

## 2. INI 文件格式规范 (INI Structure)
一键导入的 CopyQ 命令遵循特定的 INI 格式，编写时需严格注意转义规则：

```ini
[Commands]
1\Name=命令名称
1\InMenu=true                 # 是否在右键菜单显示
1\IsGlobalShortcut=true       # 是否为全局快捷键
1\Icon=📝                     # FontAwesome 图标或 Emoji
1\Shortcut=ctrl+shift+m       # 快捷键绑定
1\Command="
    copyq:
    // 注意：在 INI 格式中，内部代码的所有的双引号必须转义为 \\\"
    // 或者干脆在代码中全部使用单引号 ''
    var text = 'Hello World'; 
    popup('提示', text);
"
```
> ⚠️ **避坑**：如果通过 INI 导入时总是报 `退出代码: 41`，90% 是因为代码内存在未转义的双引号 `"`，导致 INI 解析被提前截断。

## 3. 高频核心 API 速查 (Essential APIs)

### ✂️ 剪贴板与条目操作
* `selectedItems()`: 获取当前选中的行号数组（如 `[0, 1, 2]`）。
* `clipboard()`: 获取系统当前剪贴板的纯文本。
* `read(mime, row)`: 读取指定行号和格式的数据，如 `read('text/plain', 0)`。
* `write(mime, data...)`: 将数据写入 CopyQ 顶部。
* `copy(text)`: 将内容写入系统主剪贴板。
* `paste()`: 模拟 `Ctrl+V` 将剪贴板内容输出到当前活动窗口。

### 💬 交互与界面
* `popup(title, message, timeMs)`: 弹出屏幕右下角气泡提示（非阻塞）。
* `dialog('.title', '标题', '输入提示:', '')`: 弹出带输入框的对话框，用于获取用户输入。
* `abort()`: 立即终止脚本运行。

### ⚙️ 系统与环境
* `settings(key, [value])`: 读写永久性配置数据（非常适合存储 API Token 或个人偏好）。
* `config(key, [value])`: 修改 CopyQ 自身的设置（如隐藏工具栏 `config('hide_toolbar', true)`）。
* `open(url)`: 使用系统默认浏览器打开网页。
* `execute(cmd, arg1, arg2...)`: 在后台执行系统命令（如运行 curl 或 python 脚本）。

### 📁 文件操作
* `Dir().homePath()` / `Dir().tempPath()`: 获取用户主目录或系统临时目录。
* `File(path)`: 实例化文件对象，支持 `open()`, `write()`, `readAll()`, `remove()`。

---

## 4. 高阶实战技巧模板 (Advanced Patterns)

### 🌟 模板 1：万能文本获取 (优先选中项，次选剪贴板)
这套逻辑适用于 90% 的文本处理命令：
```javascript
copyq:
var rows = selectedItems();
var text = "";

if (rows.length > 0) {
    text = str(read("text/plain", rows[0])); // 读取 CopyQ 中选中的第一项
} else {
    text = str(clipboard()); // 读取系统剪贴板当前内容
}

if (!text) {
    popup("错误", "未检测到任何文本内容");
    abort();
}
// 后续对 text 进行处理...
```

### 🌟 模板 2：安全的网络请求 (使用系统 `curl`)
由于 CopyQ 原生的网络请求处理复杂 Header（如 Auth）不够方便，处理 JSON POST 请求的最优解是**借助临时文件 + `curl`**：
```javascript
copyq:
var payload = JSON.stringify({ content: "Hello" });
var tempFile = Dir().tempPath() + '/temp_payload.json';

// 1. 将数据写入临时文件，防止在命令行中传递 JSON 遇到恶心的转义问题
var f = File(tempFile);
f.open();
f.write(payload);
f.close();

// 2. 调用系统 curl 发送请求
var res = execute(
    'curl', '-s', '-w', '%{http_code}', '-o', '-',
    '-X', 'POST',
    '-H', 'Authorization: Bearer YOUR_TOKEN',
    '-H', 'Content-Type: application/json',
    '-d', '@' + tempFile, 
    'https://api.example.com/data'
);

f.remove(); // 3. 清理临时文件

// 4. 解析结果
var output = str(res.stdout);
var httpCode = output.slice(-3); // 获取后缀的状态码
```

### 🌟 模板 3：带记忆功能的首次配置弹窗
编写需要密钥的插件时，让脚本自动记住用户的输入：
```javascript
copyq:
var token = settings('my_api_token');

// 如果没有 token，说明是第一次运行
if (!token) {
    token = dialog('.title', '初始化配置', '请输入你的 API Token:', '');
    if (!token) abort(); // 用户点击了取消
    settings('my_api_token', token); // 永久保存
}

// 如果请求报 401 权限错误，清空 token，下次自动重新弹窗
// settings('my_api_token', ''); 
```

### 🌟 模板 4：危险操作的防崩溃容错 (`try...catch`)
当调用外部文件（如切换主题、执行本地特殊程序）时，必须防止文件缺失导致 CopyQ 崩溃：
```javascript
copyq:
try {
    loadTheme("./config/copyq/themes/pure.ini");
} catch (e) {
    // 即使找不到主题文件，也不影响后续代码执行
    popup("提示", "找不到主题文件，保持默认外观。");
}
```

---

## 5. 常见故障排查 (Troubleshooting)

1. **退出代码: 41**：
   * 检查是否在 `Command=" "` 的 INI 结构内部使用了未转义的双引号 `"`。
   * 检查 JavaScript 语法错误（缺少括号、变量未定义）。
   * 检查是否调用了不存在的本地文件且没有加 `try...catch`。
2. **文本乱码或无法处理**：
   * CopyQ 读取出来的数据通常是 Byte 数组，记得使用 `str()` 转换为字符串。例如：`str(read('text/plain', 0))`。
3. **快捷键失效 / 没反应**：
   * 可能是旧命令残留导致快捷键冲突。去 `F6` 命令列表里搜索并删除重复的旧命令。

