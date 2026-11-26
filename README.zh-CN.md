# 多助手协作模板

[English](README.md)

用项目文件在不同 AI 助手之间交接。日常沿主线推进，遇到重要问题时，指定参与者从同一节点独立完成。你决定何时开放互评，以及哪些成果回到主线。

## 快速开始

1. **安装协作文件。** 新仓库可使用 GitHub 模板。已有或本地项目可用 Windows 或 macOS 安装工具、预览式命令行安装，或手动复制四项。已有规则和记录保留在原项目里。[安装与导入流程](collaboration/ONBOARDING.md)
2. **初始化或导入。** 新项目说「初始化协作」，旧项目说「导入旧项目」。进展、决定、待续讨论和下一步都写进 `PROJECT.md`。
3. **按节点分岔。** 指定来源节点、任务和助手名单。每位参与者开新会话，只使用固定的共同材料和自己的分支。
4. **开放互评并拍板。** 交齐后由你开放互评。决定采用哪些成果后，指定一位助手合并并验收。其他助手从更新后的主线继续。

## 安装

- **Windows**。双击 [Windows 安装器](https://github.com/Tau-57C/agent-collaboration-template/releases/latest/download/Agent-Collaboration-Setup.exe)，选择项目根目录。需要 Python 3.11 或更新版本，并能通过 `py -3` 或 `python` 启动。
- **macOS**。解压 [macOS 安装包](https://github.com/Tau-57C/agent-collaboration-template/releases/latest/download/Agent-Collaboration-Setup-macOS.zip)，打开 `Install on macOS.command`，选择项目根目录。需要能用 `python3` 启动 Python 3.11 或更新版本。
[手动复制和命令行备用方式](collaboration/ONBOARDING.md#install-the-collaboration-files)

助手负责整理历史和保存本地版本。没有 Git 的旧项目，可核实的旧节点逐个留档，最后单独保存导入时的项目现状。想只用文件交接时，在 `PROJECT.md` 中把 “Checkpoint Git” 设为 “Files only”。[节点和本地 Git 规则](collaboration/GUIDE.md#local-git-at-checkpoints)

## 常用短提示词

把 N03 换成实际节点号，把【】里的内容换成你的任务或材料。

### 接入项目

| 什么时候 | 发给谁         | 直接说       |
| -------- | -------------- | ------------ |
| 新项目   | 新项目的助手   | 初始化协作。 |
| 已有项目 | 负责导入的助手 | 导入旧项目。 |

### 日常主线与换手

| 什么时候                 | 发给谁             | 直接说                           |
| ------------------------ | ------------------ | -------------------------------- |
| 推进任务                 | 当前助手           | 继续主线，做【任务】。           |
| 补充材料                 | 当前助手           | 把【文件】作为当前任务的材料。   |
| 查看进度                 | 当前助手           | 现在到哪个节点了？下一步是什么？ |
| 手动留节点               | 当前助手           | 把这里记为主线节点。             |
| 换走前留讨论             | 原助手             | 记下这段讨论，我要换助手。       |
| 让新助手接手或合并后继续 | 新助手或原分支助手 | 从主线继续。                     |
| 让新助手接着聊           | 新助手             | 从主线继续，接着上次讨论。       |
| 原助手没额度             | 新助手             | 从主线继续，结合我贴的旧问答。   |

### 分岔、互评与合并

| 什么时候       | 发给谁             | 直接说                                      |
| -------------- | ------------------ | ------------------------------------------- |
| 从指定节点分岔 | 当前主线助手       | 从 N03 分岔，请【助手名单】独立做【任务】。 |
| 开始独立工作   | 每位助手的新会话   | 按 N03 独立作答，做完就交付。               |
| 检查交付       | 协调助手           | N03 谁还没交付？                            |
| 互评前追加     | 需要补做的分支助手 | 保持独立，补做【事项】。                    |
| 开放互评       | 协调助手           | 开放 N03 互评。                             |
| 请各方评审     | 各分支助手         | 按 N03 的标准，评审其他分支的成果和对话。   |
| 拍板合并       | 唯一指定的合并助手 | N03 采用【方案】，由你合并并验收。          |

### 按需使用

| 什么时候         | 发给谁           | 直接说                                |
| ---------------- | ---------------- | ------------------------------------- |
| 保留具体原话     | 能看到原文的助手 | 把这段对话原文归档。                  |
| 看版本历史       | 能访问项目的助手 | 看最近 5 次本地 Git 提交。            |
| 关闭节点自动提交 | 当前助手         | 这个项目只记节点，关闭自动 Git 提交。 |

## 到哪里查

| 文件 | 用途 |
|---|---|
| [AGENTS.md](AGENTS.md) | 助手共用的协作规则 |
| [PROJECT.md](PROJECT.md) | 主线进展、决定、待续讨论和节点 |
| [协作指南](collaboration/GUIDE.md) | 流程细节和中英提示词 |
| [参与名单](collaboration/PARTICIPANTS.md) | 不同客户端和会话的名单示例 |
| [对话归档](collaboration/ARCHIVE.md) | 通过索引查看原文、评审和决定 |
| [完整虚构示例](examples/) | 六位助手交付、互评并合回主线的示例 |
| [节点检查器](tools/check_node.py) | 可选工具，核对名单、交付、互评和合并记录 |

客户端获取原文的能力各有差异。必要时导出或复制可见对话。需要严格隔离独立分支时，用工作区访问权限限制共享范围。[客户端兼容性](collaboration/COMPATIBILITY.md)

## 测试和构建

```sh
python tools/check_node.py examples/report-layout/N03
python -m unittest discover -s tests -v
```

Windows 上可从仓库构建安装器，需要 Python 3.11 或更新版本以及 .NET Framework 的 C# 编译器。

```powershell
python tools/build_windows_installer.py Agent-Collaboration-Setup.exe
```

[MIT 许可证](LICENSE)。
