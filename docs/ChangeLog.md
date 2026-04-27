# ChangeLog

## 备注

- 修改都使用的AI Studio，后续修改直接使用“CopyQ 命令编写助手”对话。
- 命令编写助手的地址：<https://aistudio.google.com/prompts/12a92O0PVAGjv9sbMUZ2YBlV8oWY4vmoE>

## 2026-04-27

- feat: 添加`生成网页 Markdown 链接.ini`命令和文档
  添加新的 CopyQ 命令脚本，用于自动抓取网页标题并生成 Markdown 格式链接
  同时添加详细的使用说明文档，包含部署指南和配置说明
- feat: 添加`全文抓取到 Obsidian.ini`命令和文档
  添加新的 CopyQ 命令配置文件和详细使用说明文档，实现通过快捷键将网页内容抓取并保存到 Obsidian 的功能

## 2026-04-24

- 在 README.md 中添加了感谢 [GFDGIT/CopyQ\_lazy](https://github.com/GFDGIT/CopyQ_lazy) 仓库的信息
- 创建了“粘贴纯文本（去除多余空行）”命令
- 创建了“AI-同时打开豆包和DeepSeek”命令
- feat: 添加`发送到Memos.ini`命令和文档
  ⚙️ 使用说明：
  需要在`发送到Memos.ini`中配置`memos_url`和`tag`
  在 CopyQ 里选中你想发送的任意一条文本，按下快捷键 Ctrl + Shift + M（你也可以在命令列表里自己修改快捷键）。
  第一次运行时，屏幕中心会弹出一个小窗口，让你输入 Access Token。
  (你需要在浏览器打开 Memos -> 左侧导航栏点 设置 -> 个人凭证 -> 创建一个新凭证并复制过来)
  输入并确定后，这条内容就会飞向你的 Memos，右下角会弹出 “保存成功 🎉”。
  以后再发送，只需按下快捷键，无需再次输入 Token，纯后台秒发！
- feat: 添加`AI润色助手.ini`命令和文档
  ⚙️ 使用说明：
  选中文本（或复制一段文字）。
  按下全局快捷键 Ctrl + Shift + P（P 代表 Polish / 润色，你可以自己改）。
  第一次运行时，会弹出一个配置框，你可以按自己的需求填入：
  Base URL: 例如填写 DeepSeek 的地址 <https://api.deepseek.com/v1/chat/completions> (注意：URL 必须包含到 /chat/completions 这级)。
  模型名称: 例如 deepseek-chat。
  API Key: 填入你的密钥。
  润色提示词: 默认是基础润色，你可以改成比如：“你是一个翻译官，请将以下文本翻译为地道、专业的英文，只需输出结果。”
  配置填好点确定，2\~3秒后，右下角弹出“润色完成”，你直接在当前编辑器里按 Ctrl+V，魔法就完成了！
- feat: 添加`浮窗看天气.ini`命令和文档
  ⚙️ 使用说明：
  需要在`浮窗看天气.ini`中配置`scriptPath`为你的天气Python脚本路径，python脚本中输入高德天气API Key
  按下全局快捷键 Shift+F5
  会弹出“正在查询天气...”的提示，然后显示龙岗区的天气信息
  天气信息会以浮动窗口形式显示，持续10秒
  显示内容包括：当前温度、天气状况、风力、湿度等信息

