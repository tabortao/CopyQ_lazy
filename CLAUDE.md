# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a CopyQ clipboard manager configuration repository containing custom commands, themes, and scripts. CopyQ is an advanced clipboard manager that allows scripting and automation of clipboard operations.

## Repository Structure

- **/命令/** - Contains individual CopyQ command files in .ini format
- **/主题/** - Contains CopyQ theme files (.ini format)
- **/一键导入/** - Contains the complete configuration package for one-click import
- **/Script/** - Contains external scripts (e.g., weather.py)
- **/docs/** - Documentation files including changelog and usage instructions
- **/images/** - Screenshots and visual assets

## Key Files

### Configuration Files
- `一键导入/一键导入.cpq` - Complete CopyQ configuration package
- `命令/全部命令.ini` - All commands bundled together
- `skill.md` - Comprehensive CopyQ scripting guide and best practices

### Documentation
- `README.md` - Main repository documentation
- `docs/ChangeLog.md` - Development history and feature updates
- `docs/全文抓取到 Obsidian 使用说明.md` - Usage instructions for Obsidian integration
- `docs/生成网页 Markdown 链接 使用说明.md` - Usage instructions for web link generation

## Development Commands

### CopyQ Command Development

1. **Test individual commands:**
   - Open CopyQ (F6 to access commands)
   - Import individual .ini files from `/命令/` directory
   - Test functionality with sample data

2. **Import complete configuration:**
   ```bash
   # Use CopyQ GUI: File -> Import -> Select "一键导入.cpq"
   # This imports all commands, themes, and settings at once
   ```

3. **Export configuration:**
   ```bash
   # Use CopyQ GUI: File -> Export -> Save as .cpq file
   # This creates a backup or shareable configuration
   ```

### Script Testing

For Python scripts (e.g., weather functionality):
```bash
cd Script/
python weather.py
```

## Code Architecture

### CopyQ Command Structure

Each command follows this INI format:
```ini
[Commands]
1\Name=Command Name
1\Command="
    copyq:
    // JavaScript code here
    // Use single quotes or escape double quotes
"
1\InMenu=true
1\Icon=📝
1\Shortcut=ctrl+shift+key
```

### Key API Patterns

1. **Text Selection Pattern:**
   ```javascript
   var rows = selectedItems();
   var text = "";
   if (rows.length > 0) {
       text = str(read("text/plain", rows[0]));
   } else {
       text = str(clipboard());
   }
   ```

2. **Network Requests:**
   ```javascript
   // Use temporary files + curl for complex requests
   var tempFile = Dir().tempPath() + '/temp.json';
   var f = File(tempFile);
   f.open();
   f.write(JSON.stringify(data));
   f.close();

   var res = execute('curl', '-s', '-X', 'POST', '-d', '@' + tempFile, url);
   f.remove();
   ```

3. **Settings Management:**
   ```javascript
   var token = settings('api_token');
   if (!token) {
       token = dialog('.title', 'Configuration', 'Enter API Token:', '');
       settings('api_token', token);
   }
   ```

## Important Notes

### Common Issues

1. **Exit Code 41:** Usually caused by unescaped double quotes in INI files
   - Solution: Use single quotes in JavaScript or escape double quotes with `\\"`

2. **Text Encoding:** CopyQ returns Byte arrays - always use `str()` to convert
   ```javascript
   var text = str(read('text/plain', 0));
   ```

3. **File Operations:** Always use try-catch for external file operations
   ```javascript
   try {
       loadTheme("./path/to/theme.ini");
   } catch (e) {
       popup("Error", "Theme file not found");
   }
   ```

### Best Practices

1. **Robustness:** Always check for empty selections and clipboard content
2. **Feedback:** Use `popup()` to provide user feedback for operations
3. **Compatibility:** Handle both selected items and clipboard content
4. **Error Handling:** Use try-catch blocks for file operations and external calls

## Recent Features

Based on the changelog, recent additions include:
- 全文抓取到 Obsidian (Full-text capture to Obsidian)
- 生成网页 Markdown 链接 (Generate web Markdown links)
- 发送到Memos (Send to Memos)
- AI润色助手 (AI Polish Assistant)
- 浮窗看天气 (Weather popup)

## External Dependencies

- **CopyQ**: Required clipboard manager application
- **Python**: For weather script functionality
- **curl**: For HTTP requests in CopyQ scripts
- **API Keys**: Various services (DeepSeek, Memos, etc.) require configuration

## Testing Strategy

1. **Unit Testing**: Test individual commands with sample data
2. **Integration Testing**: Test complete workflows (e.g., web capture → Obsidian)
3. **Error Testing**: Test edge cases (empty clipboard, network failures)
4. **UI Testing**: Verify popup messages and user interactions

## Deployment

1. Install CopyQ application
2. Import configuration via `一键导入.cpq`
3. Configure API keys and paths in individual command files
4. Test all shortcuts and menu items
5. Verify theme loading and visual appearance
