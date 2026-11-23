---
name: webpage-share
description: 用户明确要求把本地 HTML 上传到 Webpage Share、生成分享链接，或列出、下载该服务中的网页时使用。
---

# Webpage Share

从本 SKILL.md 所在目录向上两级找到插件根目录，使用根目录下的 `scripts/webpage_share.py`。将脚本和本地文件的路径解析为绝对路径，以保留用户工作目录；路径包含空格时使用引号。Windows 使用 `python`，其他系统通常使用 `python3`。需要 Python 3 和 requests。

## 配置

为脚本传入全局参数 `--profile codex`。脚本读取进程环境变量以及 Codex 用户目录下的 `webpage-share.env`（优先使用 CODEX_HOME，默认 ~/.codex）。如已配置 Hermes 并要沿用同一分享服务，可显式传入 `--env-file` 指向该 profile 的 .env。配置项为 WEBPAGE_SHARE_URL、WEBPAGE_SHARE_TENANT_ID、WEBPAGE_SHARE_API_KEY。使用 config 检查配置，保持 API Key 私密。

## 命令

```text
python "<插件根目录>/scripts/webpage_share.py" --profile codex upload "<HTML 绝对路径>"
python "<插件根目录>/scripts/webpage_share.py" --profile codex list
python "<插件根目录>/scripts/webpage_share.py" --profile codex download "<远程文件名>" "<本地目标路径>"
python "<插件根目录>/scripts/webpage_share.py" --profile codex config
```

仅上传用户指定的 HTML。成功后将服务返回的实际 URL 作为可点击链接交付；访问权限由该服务管理。遇到上传超时，先用 list 核对服务端结果再决定是否重试。删除页面由用户在服务管理界面操作。
