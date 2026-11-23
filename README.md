# Webpage Share

适用于 Codex 和 Hermes 的独立 skill — 将 HTML 文件上传到网页分享服务，生成可分享的链接。

## 前置依赖

本技能需要配合 **webpage-share-service** 后端服务一起使用：

- **后端服务仓库**：https://github.com/seamusmore/webpage-share-service
- 请先部署并启动后端服务，获取服务地址后再配置本技能。
- 如果已经部署过后端服务，请直接阅读对应的技能安装与配置步骤。

## 在 Codex 中安装

将本仓库克隆到个人技能目录。仓库根目录包含 `SKILL.md`，Codex 会从这里发现技能。客户端需要 Python 3 和 requests。

**Windows PowerShell**

```powershell
git clone https://github.com/seamusmore/hermes-webpage-share.git "$HOME/.agents/skills/webpage-share"
python -m pip install requests
```

**macOS / Linux**

```sh
git clone https://github.com/seamusmore/hermes-webpage-share.git "$HOME/.agents/skills/webpage-share"
python3 -m pip install requests
```

按下方“配置”一节设置 `WEBPAGE_SHARE_URL`、`WEBPAGE_SHARE_TENANT_ID`、`WEBPAGE_SHARE_API_KEY` 三个环境变量，并确保启动 Codex 的进程可以读取它们。已有 Hermes 配置的机器也可直接复用 `HERMES_HOME/.env`（默认 `~/.hermes/.env`）。技能目录只存放代码和使用说明。

打开新的 Codex 会话，输入“用 webpage-share 分享这份 HTML”，并附上本地文件路径。要先验证配置，可在 PowerShell 中运行：

```powershell
python "$HOME/.agents/skills/webpage-share/scripts/webpage_share.py" config
```

## 在 Hermes 中安装

```bash
# 1. 克隆技能仓库
git clone https://github.com/seamusmore/hermes-webpage-share.git \
  ~/.hermes/skills/webpage-share

# 2. 参照 .env.example，在当前 profile 的 .env 中添加下方三个配置项
```

## 配置

### 1. 获取租户配置

1. **访问公共服务**：`https://your-domain.com/pages.html`
2. **飞书登录**：点击登录按钮，完成飞书授权
3. **自动注册**：系统自动创建租户（租户 ID = 你的飞书 open_id）
4. **获取 API_KEY**：登录后在管理页面查看 API_KEY

### 2. 填写 .env

```bash
WEBPAGE_SHARE_URL=https://your-domain.com
WEBPAGE_SHARE_TENANT_ID=ou_xxx
WEBPAGE_SHARE_API_KEY=sk_ou_xxx
```

脚本读取优先级：**环境变量 → profile 的 `.env`**。URL、tenant_id、api_key 均不允许默认值，未配置时报错退出。

## 使用

### 上传 HTML 文件

```bash
python3 ~/.hermes/skills/webpage-share/scripts/webpage_share.py upload /path/to/file.html
```

### 列出已分享的页面

```bash
python3 ~/.hermes/skills/webpage-share/scripts/webpage_share.py list
```

### 查看当前配置

```bash
python3 ~/.hermes/skills/webpage-share/scripts/webpage_share.py config
```

### 下载已分享的页面

```bash
# 保存到当前目录，文件名与远程一致
python3 ~/.hermes/skills/webpage-share/scripts/webpage_share.py download example.html

# 指定保存路径
python3 ~/.hermes/skills/webpage-share/scripts/webpage_share.py download example.html /tmp/example.html
```

## 文件结构

```
.
├── .env.example          # 配置示例
├── .gitignore            # Git 忽略规则
├── LICENSE               # 许可证
├── README.md             # 本文件
├── SKILL.md              # Codex 和 Hermes 共用的技能定义
├── references/
│   └── backend-api.md    # 后端 API 参考文档
└── scripts/
    └── webpage_share.py  # 主脚本（upload / list / config）
```

## 许可证

MIT
