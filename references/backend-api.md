# webpage-share 后端服务 API 参考

## 服务信息

- **代码路径**：`/path/to/webpage-share-service/services/auth-server.js`
- **配置路径**：`/path/to/webpage-share-service/data/tenants.json`
- **存储路径**：`/path/to/webpage-share-service/storage/tenant-{openId}/`
- **pm2 管理**：`pm2 describe webpage-share`
- **端口**：`9080`（默认）

## API 端点

### POST /api/upload

**认证**：`X-API-Key: {api_key}` 头

**请求体**：multipart/form-data
- `file`: HTML 文件

**响应**：
```json
{
  "success": true,
  "filename": "xxx.html",
  "url": "https://your-domain.com/ou_xxx/pages/xxx.html"
}
```

**错误响应**：
- `401`：缺少 API_KEY
- `403`：无效的 API_KEY
- `400`：非 multipart 格式或 boundary 错误

### GET /api/list

**认证**：`X-API-Key: {api_key}` 头

**响应**：
```json
{
  "success": true,
  "pages": [
    {
      "filename": "xxx.html",
      "url": "https://your-domain.com/ou_xxx/pages/xxx.html",
      "size": 12345
    }
  ]
}
```

### GET /api/download

**认证**：`X-API-Key: {api_key}` 头

**Query 参数**：
- `filename`: 要下载的文件名（例如 `report.html`）

**响应**：直接返回 HTML 文件内容（`text/html`）

## 服务管理

```bash
# 查看状态
pm2 describe webpage-share

# 查看日志
pm2 logs webpage-share --lines 100

# 重启
pm2 restart webpage-share

# 健康检查
/path/to/webpage-share-service/scripts/healthcheck.sh
```

