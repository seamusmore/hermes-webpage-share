#!/usr/bin/env python3
"""
Webpage Share 工具 - 将 HTML 文件上传到网页分享服务，生成可分享的链接。

用法:
    python3 webpage_share.py upload /path/to/file.html
    python3 webpage_share.py list
    python3 webpage_share.py config
"""

import argparse
import json
import os
import sys
from pathlib import Path

import requests


DEFAULT_URL = ""


def _read_env_file(path):
    """读取单个 .env 文件。"""
    env = {}
    if not path.exists():
        return env
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, val = line.partition("=")
                if key:
                    env[key] = val.strip().strip('"').strip("'")
    return env


def load_env():
    """
    安全读取配置：
    - URL 、tenant_id 和 api_key 均从 profile 的 .env 或环境变量读取
    - 不允许硬编码默认值
    """
    profile_env = Path(os.environ.get("HERMES_HOME", Path.home() / ".hermes")) / ".env"
    profile_cfg = _read_env_file(profile_env)

    # 所有配置均从环境变量或 profile .env 读取，不允许默认值
    url = os.environ.get("WEBPAGE_SHARE_URL") or profile_cfg.get("WEBPAGE_SHARE_URL", "")
    tenant = os.environ.get("WEBPAGE_SHARE_TENANT_ID") or profile_cfg.get("WEBPAGE_SHARE_TENANT_ID", "")
    key = os.environ.get("WEBPAGE_SHARE_API_KEY") or profile_cfg.get("WEBPAGE_SHARE_API_KEY", "")

    return {"url": url.rstrip("/"), "tenant_id": tenant, "api_key": key}


def get_config():
    """获取配置，未配置时报错退出。"""
    cfg = load_env()
    url = cfg["url"]
    tenant = cfg["tenant_id"]
    key = cfg["api_key"]

    if not url:
        print("[ERR] 服务地址未配置。")
        print("\n请在当前 profile 的 .env 文件中添加以下配置：")
        print(f"  文件路径: {os.environ.get('HERMES_HOME', '~/.hermes')}/.env")
        print()
        print("  WEBPAGE_SHARE_URL=https://your-domain.com")
        sys.exit(1)

    if not tenant or not key:
        print("[ERR] 配置不完整。")
        print("\n请在当前 profile 的 .env 文件中添加以下配置：")
        print(f"  文件路径: {os.environ.get('HERMES_HOME', '~/.hermes')}/.env")
        print()
        print("  WEBPAGE_SHARE_TENANT_ID=ou_xxx")
        print("  WEBPAGE_SHARE_API_KEY=sk_ou_xxx")
        print()
        print("获取方法: 访问管理页面飞书登录后自动获取")
        sys.exit(1)

    return {"url": url, "tenant_id": tenant, "api_key": key}


def cmd_upload(file_path):
    config = get_config()
    path = Path(file_path)
    if not path.exists():
        print(f"[ERR] 文件不存在: {file_path}")
        sys.exit(1)

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

    if data.get("success"):
        print(f"[OK] 上传成功：{data.get('filename', path.name)}")
        url = data.get('url', '')
        if url:
            print(f"\n分享链接：{url}")
    else:
        err_msg = data.get('error', '未知错误')
        print(f"[ERR] 上传失败：{err_msg}")
        sys.exit(1)


def cmd_list():
    config = get_config()
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


def cmd_config():
    config = get_config()
    masked_key = config["api_key"][:8] + "***" if len(config["api_key"]) > 8 else "***"
    print(f"配置信息：\n")
    print(f"- 公共服务：{config['url']}")
    print(f"- 租户 ID: {config['tenant_id']}")
    print(f"- API Key: {masked_key}")


def main():
    parser = argparse.ArgumentParser(
        description="Webpage Share - 上传 HTML 到网页分享服务"
    )
    sub = parser.add_subparsers(dest="command")

    p_upload = sub.add_parser("upload", help="上传 HTML 文件")
    p_upload.add_argument("file_path", help="HTML 文件路径")

    sub.add_parser("list", help="列出已分享的页面")
    sub.add_parser("config", help="查看配置")

    args = parser.parse_args()

    if args.command == "upload":
        cmd_upload(args.file_path)
    elif args.command == "list":
        cmd_list()
    elif args.command == "config":
        cmd_config()
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
