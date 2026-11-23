#!/usr/bin/env python3
"""
Webpage Share 工具 - 将 HTML 文件上传到网页分享服务，生成可分享的链接。

用法:
    python3 webpage_share.py upload /path/to/file.html
    python3 webpage_share.py list
    python3 webpage_share.py config
    python3 webpage_share.py download <filename> [output_path]
"""

import argparse
import json
import os
import sys
from pathlib import Path

import requests


def config_path(profile, env_file):
    if env_file:
        return Path(env_file).expanduser()
    if profile == "codex":
        return Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex") / "webpage-share.env"
    return Path(os.environ.get("HERMES_HOME") or Path.home() / ".hermes") / ".env"


def _read_env_file(path):
    """读取单个 .env 文件。"""
    env = {}
    if not path.exists():
        return env
    with open(path, "r", encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, val = line.partition("=")
                if key:
                    env[key] = val.strip().strip('"').strip("'")
    return env


def load_env(profile_env):
    """
    安全读取配置：
    - URL 、tenant_id 和 api_key 均从 profile 的 .env 或环境变量读取
    - 不允许硬编码默认值
    """
    profile_cfg = _read_env_file(profile_env)

    # 所有配置均从环境变量或 profile .env 读取，不允许默认值
    url = os.environ.get("WEBPAGE_SHARE_URL") or profile_cfg.get("WEBPAGE_SHARE_URL", "")
    tenant = os.environ.get("WEBPAGE_SHARE_TENANT_ID") or profile_cfg.get("WEBPAGE_SHARE_TENANT_ID", "")
    key = os.environ.get("WEBPAGE_SHARE_API_KEY") or profile_cfg.get("WEBPAGE_SHARE_API_KEY", "")

    return {"url": url.rstrip("/"), "tenant_id": tenant, "api_key": key}


def get_config(path):
    cfg = load_env(path)
    missing = [name for name, value in cfg.items() if not value]
    if missing:
        sys.exit(f"[ERR] {path} 或环境变量缺少配置: {', '.join(missing)}")
    return cfg


def cmd_upload(file_path, config):
    path = Path(file_path)
    if not path.exists():
        print(f"[ERR] 文件不存在: {file_path}")
        sys.exit(1)

    if not path.is_file() or path.suffix.lower() not in (".html", ".htm"):
        sys.exit("[ERR] 请选择 HTML 文件。")

    upload_url = f"{config['url']}/api/upload"
    headers = {"X-API-Key": config["api_key"]}

    try:
        with open(path, "rb") as f:
            files = {"file": (path.name, f, "text/html")}
            resp = requests.post(upload_url, headers=headers, files=files, timeout=30)
        resp.raise_for_status()
        data = resp.json()
    except requests.RequestException as e:
        print(f"[ERR] 上传失败: {e}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"[ERR] 服务器返回无效 JSON: {resp.text[:200]}")
        sys.exit(1)

    if data.get("success") and data.get("url"):
        print(f"[OK] 上传成功：{data.get('filename', path.name)}")
        url = data.get('url', '')
        if url:
            print(f"\n分享链接：{url}")
    else:
        err_msg = data.get('error', '未知错误')
        print(f"[ERR] 上传失败：{err_msg}")
        sys.exit(1)


def cmd_list(config):
    list_url = f"{config['url']}/api/list?tenant={config['tenant_id']}"
    headers = {"X-API-Key": config["api_key"]}

    try:
        resp = requests.get(list_url, headers=headers, timeout=30)
        resp.raise_for_status()
        data = resp.json()
    except requests.RequestException as e:
        print(f"[ERR] 获取失败：{e}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"[ERR] 服务器返回无效 JSON: {resp.text[:200]}")
        sys.exit(1)

    if not data.get("success"):
        err_msg = data.get('error', '未知错误')
        print(f"[ERR] 获取失败：{err_msg}")
        sys.exit(1)

    pages = data.get("pages", [])
    if not pages:
        print("暂无页面")
        return

    print("页面列表：\n")
    for p in pages:
        print(f"- {p.get('filename', '未知')}")
        print(f"  {p.get('url', '')}")


def cmd_config(config):
    masked_key = "***"
    print(f"配置信息：\n")
    print(f"- 公共服务：{config['url']}")
    print(f"- 租户 ID: {config['tenant_id']}")
    print(f"- API Key: {masked_key}")


def cmd_download(filename, output_path, config):
    download_url = f"{config['url']}/api/download"
    headers = {"X-API-Key": config["api_key"]}

    try:
        resp = requests.get(download_url, params={"filename": filename}, headers=headers, timeout=30)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"[ERR] 下载失败: {e}")
        sys.exit(1)

    save_path = Path(output_path) if output_path else Path(filename)
    try:
        save_path.write_bytes(resp.content)
    except OSError as e:
        print(f"[ERR] 保存文件失败: {e}")
        sys.exit(1)

    print(f"[OK] 已下载: {save_path}")
    print(f"     大小: {len(resp.content)} bytes")
    print(f"     保存至: {save_path.resolve()}")


def main():
    parser = argparse.ArgumentParser(
        description="Webpage Share - 上传 HTML 到网页分享服务"
    )
    parser.add_argument("--profile", choices=("hermes", "codex"), default="hermes", help="选择配置目录")
    parser.add_argument("--env-file", help="显式指定分享服务配置文件")
    sub = parser.add_subparsers(dest="command")

    p_upload = sub.add_parser("upload", help="上传 HTML 文件")
    p_upload.add_argument("file_path", help="HTML 文件路径")

    p_download = sub.add_parser("download", help="下载已分享的页面")
    p_download.add_argument("filename", help="要下载的文件名")
    p_download.add_argument("output_path", nargs="?", default=None, help="保存路径（默认当前目录同名文件）")

    sub.add_parser("list", help="列出已分享的页面")
    sub.add_parser("config", help="查看配置")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    config = get_config(config_path(args.profile, args.env_file))
    if args.command == "upload":
        cmd_upload(args.file_path, config)
    elif args.command == "download":
        cmd_download(args.filename, args.output_path, config)
    elif args.command == "list":
        cmd_list(config)
    elif args.command == "config":
        cmd_config(config)


if __name__ == "__main__":
    main()
