# Webpage Share

Hermes 技能 — 将 HTML 文件上传到网页分享服务，生成可分享的链接。

## 前置依赖

本技能需要配合 **webpage-share-service** 后端服务一起使用：

- **后端服务仓库**：https://github.com/seamusmore/webpage-share-service
- 请先部署并启动后端服务，获取服务地址后再配置本技能。

## 安装

```bash
# 1. 克隆技能仓库
git clone https://github.com/seamusmore/hermes-webpage-share.git \
  ~/.hermes/skills/webpage-share

# 2. 复制配置示例到当前 profile 的 .env
cp ~/.hermes/skills/webpage-share/.env.example \
   ~/.hermes/.env
# 或 ~/.hermes/profiles/<profile>/.env

# 3. 编辑 .env 填入你自己的配置
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
WEBPAGE_SHARE_TENANT_ID=ou_xxx        # 你的飞书 open_id
WEBPAGE_SHARE_API_KEY=sk_ou_xxx       # 登录后自动生成的 key
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
├── SKILL.md              # Hermes 技能定义
├── references/
│   └── backend-api.md    # 后端 API 参考文档
└── scripts/
    └── webpage_share.py  # 主脚本（upload / list / config）
```

## 许可证

MIT
