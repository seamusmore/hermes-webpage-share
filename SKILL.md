---
name: webpage-share
slug: webpage-share
version: 2.0.0
description: 网页分享技能 - 将 HTML 文件上传到网页分享服务，生成可分享的链接
trigger:
  - "分享这个 HTML"
  - "把这个网页分享"
  - "生成一个可分享的链接"
  - "上传 HTML 到网页服务"
  - "分享这个网页"
---

## 定位

**webpage-share 是 HTML 分享助手**，当用户想要分享 HTML 文件时，执行脚本上传文件并返回分享链接。

---

## 触发条件
当用户说以下关键词时触发：
- "分享这个 HTML"
- "把这个网页分享"
- "生成一个可分享的链接"
- "上传 HTML 到网页服务"
- "分享这个网页"

---

## 隐私检查（发布前必做）

技能代码和文档中容易意外泄露真实 ID、密钥或姓名。推送前执行以下检查：

```bash
cd E:/home/admin/hermes/skills/webpage-share

# 检查是否有真实飞书 open_id
grep -rn "ou_[a-f0-9]\{32\}" references/ scripts/ SKILL.md

# 检查是否有真实 API key
grep -rni "sk_ou_[a-f0-9]" references/ scripts/ SKILL.md

# 检查文档示例中是否用了真实值（应全部是 xxx 占位符）
grep -rni "ou_[a-f0-9]" references/ | grep -v "ou_xxx"
```

如果发现真实值，替换为占位符后再推送。

## 铁律

- **只做用户要求的事**：不擅自删除文件、修改无关引用、或"顺手清理"用户没提的内容。用户说删什么才删什么。
- **示例必须用占位符**：所有文档中的文件名、ID、路径、链接必须用 `xxx`、`example.html` 等占位符，禁止使用真实项目名称或用户真实数据。

---

## 配置

### 1. 获取租户配置

1. **访问公共服务**：https://your-domain.com/pages.html
2. **飞书登录**：点击登录按钮，完成飞书授权
3. **自动注册**：系统自动创建租户（租户 ID = 你的飞书 open_id）
4. **获取 API_KEY**：登录后在管理页面查看 API_KEY

### 2. 填写 .env

```bash
# 1. 复制示例到当前 profile 的 .env
cp ~/.hermes/skills/webpage-share/.env.example \
   ~/.hermes/.env   # 或 ~/.hermes/profiles/<profile>/.env

# 2. 编辑 profile 的 .env，填入自己的租户配置
WEBPAGE_SHARE_URL=https://your-domain.com
WEBPAGE_SHARE_TENANT_ID=ou_xxx        # 你的飞书 open_id
WEBPAGE_SHARE_API_KEY=sk_ou_xxx_xxx   # 登录后自动生成的 key
```

脚本读取优先级：环境变量 → profile 的 `.env`。URL、tenant_id、api_key 均不允许默认值，未配置时报错退出。

---

## 使用流程

### 场景 1：分享 HTML 文件

```
用户：分享这个 HTML 文件 /home/admin/report.html

AI 思考：
1. 检测到分享关键词
2. 执行 webpage_share.py upload
3. 返回分享链接

AI 行动：
python3 ~/.hermes/skills/webpage-share/scripts/webpage_share.py upload /home/admin/report.html

AI 回复：
[OK] 已上传：report.html
分享链接：https://your-domain.com/ou_xxx/pages/xxx-report.html

任何获得链接的飞书用户登录后都可以访问～
```

### 场景 2：分享当前生成的 HTML

```
用户：把刚才生成的原型分享出去

AI 行动：
python3 ~/.hermes/skills/webpage-share/scripts/webpage_share.py upload /path/to/generated.html

AI 回复：
[OK] 已生成分享链接：
https://your-domain.com/ou_xxx/pages/xxx-prototype.html
```

### 场景 3：查看已分享的页面列表

```
用户：我分享了哪些网页？

AI 行动：
python3 ~/.hermes/skills/webpage-share/scripts/webpage_share.py list

AI 回复：
页面列表：
1. 蛇蛇宇宙版
   https://your-domain.com/ou_xxx/pages/xxx.html
2. 四季流浪猫 珍藏版
   https://your-domain.com/ou_xxx/pages/xxx.html
...
```

### 场景 4：查看配置

```bash
用户：网页分享的配置是什么？

AI 行动：
python3 ~/.hermes/skills/webpage-share/scripts/webpage_share.py config
```

### 场景 5：下载已分享的页面

```
用户：把那个页面下回来 / 下载「xxx.html」

AI 行动：
python3 ~/.hermes/skills/webpage-share/scripts/webpage_share.py download example.html

# 指定保存路径
python3 ~/.hermes/skills/webpage-share/scripts/webpage_share.py download example.html /tmp/example.html
```

AI 回复：
[OK] 已下载: example.html
     大小: 9593 bytes
     保存至: C:\Users\xiehong\...
```

### upload

```bash
python3 scripts/webpage_share.py upload <file_path>
```

- 上传 HTML 文件到网页分享服务
- 返回：`[OK] 上传成功` + 分享链接

### list

```bash
python3 scripts/webpage_share.py list
```

- 列出已分享的页面
- 返回：`{success, pages: [{filename, url, size}]}`

### config

```bash
python3 scripts/webpage_share.py config
```

- 显示当前配置（API Key 脱敏）

### download

```bash
python3 scripts/webpage_share.py download <filename> [output_path]
```

- 下载已分享的页面
- 不传 `output_path` 则保存到当前目录，文件名与远程一致
- 返回：`[OK] 已下载` + 大小 + 保存路径

---

## 注意事项

### 1. 文件必须是 HTML

```
[OK] 正确：report.html
[ERR] 错误：report.pdf（不支持）
```

### 2. 分享链接需要飞书登录

- 任何获得链接的飞书用户都可以访问
- 需要飞书授权登录（公司内网安全）

### 3. 删除操作限制

- **AI 无法删除文件**
- 删除操作必须由用户亲自到管理页面手动执行
- 管理页面地址：https://your-domain.com/pages.html
---

## 系统架构

```
Hermes 技能脚本（客户端）
    ↓ HTTP POST/GET
/path/to/webpage-share-service/services/auth-server.js （后端服务，pm2 管理）
    ↓ 读写
/path/to/webpage-share-service/storage/tenant-{openId}/ （文件存储）
```

- **后端服务端口**：`9080`
- **pm2 进程名**：`webpage-share`
- **后端配置**：`/path/to/webpage-share-service/data/tenants.json`

### 后端 HTTP API（兜底 curl）

**上传文件**：
```bash
curl -X POST "${PUBLIC_SERVICE_URL}/api/upload" \
  -H "X-API-Key: ${API_KEY}" \
  -F "file=@/path/to/file.html"
```

**列出文件**：
```bash
curl -X GET "${PUBLIC_SERVICE_URL}/api/list" \
  -H "X-API-Key: ${API_KEY}"
```

**下载文件**：
```bash
curl -X GET "${PUBLIC_SERVICE_URL}/api/download?filename=report.html" \
  -H "X-API-Key: ${API_KEY}" \
  -o report.html
```

---

## 参考资料

- 后端 API 详情见 `references/backend-api.md`

---

**版本**: 2.1.0
**创建日期**: 2026-04-08
**维护者**: 蛇蛇
