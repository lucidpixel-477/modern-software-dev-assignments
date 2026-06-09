# Next.js JSON 笔记管理器

## 项目概览

本项目是一个使用 Next.js App Router 构建的完整笔记管理 Web 应用。用户可以在简洁的响应式界面中创建、查看、更新和删除笔记。笔记会持久化保存到本地 `data/notes.json` 文件中，因此刷新浏览器或重启开发服务器后仍然可用。

## 技术栈

- Next.js
- TypeScript
- App Router
- 服务端 API 路由
- 本地 JSON 文件存储
- Tailwind CSS

## 环境要求

- Node.js 20 或更高版本
- npm

## 安装

进入```anaconda prompt```，进入```cs146s```环境，并进入```nextjs-json-notes```所在路径

安装项目依赖：

```bash
npm install
```

## 本地运行

启动开发服务器：

```bash
npm run dev
```

在浏览器中打开 [http://localhost:3000](http://localhost:3000)。

## 笔记数据

应用将笔记保存在：

```text
data/notes.json
```

如果该文件不存在，应用会自动创建。

## 已知限制

- 笔记保存在本地 JSON 文件中，因此并发写入没有数据库级锁保护。
- 没有身份认证或用户级笔记归属。
- 本地 JSON 存储适合开发和学习，不适合部署到多个服务器实例的生产环境。
