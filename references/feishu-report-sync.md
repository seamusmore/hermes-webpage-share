# 从飞书文档+Base 同步更新 HTML 报告

## 场景

用户有一个飞书工作汇报文档（docx），内嵌两个多维表格（bitable）：
- 当前进度表（版本/状态/业务模块/开发/测试/产品 人日）
- 任务详情表（工作内容/端口/状态/版本）

需要从文档+Base 同步数据，生成/更新一个可分享的 HTML 报告页面。

## 流程

### 1. 读取文档正文

```bash
lark-cli docs +fetch --api-version v2 --doc <doc_token> --doc-format markdown --as user
```

提取：
- 已完成工作量
- 投入人数
- 当前问题（含子说明）
- 本周工作内容
- 日期/版本号

### 2. 读取 Base 表格数据

```bash
# 先获取表列表
lark-cli base +table-list --base-token <bitable_token> --as user

# 读取各表记录（limit 200，确认 has_more=false）
lark-cli base +record-list --base-token <bitable_token> --table-id <table_id> --as user --limit 200
```

### 3. 计算汇总

- 人日合计 = SUM(开发) + SUM(测试) + SUM(产品)
- 文档中"已完成工作量"字段值可能与 Base 全表合计不一致，以 Base 全表合计为准

### 4. 生成 HTML

- 日期：用文档最新 revision 的日期
- 人力：从文档"投入人数"字段提取
- 完成量：用 Base 全表计算值（不是文档中的"已完成工作量"）
- 进度表：按 Base 记录渲染，含状态筛选按钮
- 任务详情：按 Base 记录渲染，含版本筛选按钮
- 当前问题：保持原文格式（含 `<br>` 换行和子说明的 `→` 前缀），**不要合并多段子说明为一段**
- Tab 默认：默认选中本周主推版本（通常是开发中且人数最多的版本）

### 5. 上传分享

```bash
E:/home/admin/hermes/hermes-agent/venv/Scripts/python \
  E:/home/admin/hermes/skills/webpage-share/scripts/webpage_share.py \
  upload <html_file_path>
```

## Pitfalls

1. **bitable token ≠ spreadsheet_token**：文档内嵌 bitable 的 `token` 属性不能传给 `lark-cli sheets`，必须走 `lark-cli base`
2. **文档"已完成工作量"≠ Base 全表合计**：文档中的数字可能是某个时间点的快照，计算时应以 Base 全表合计为准
3. **子说明格式**：当前问题中的 `→` 子说明在原文档中是多段，HTML 中要保持 `<br><span>→ ...</span>` 的独立段落形式，不要合并成一句
4. **身份选择**：读用户文档和 Base 统一用 `--as user`，不要用 bot
5. **版本号一致性**：文档中的"本周工作内容"提到的版本号要和 Base 表格中的版本字段保持一致
