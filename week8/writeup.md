# Week 8 Write-up

## Instructions

本文件已根据 week8 三个版本的项目内容填写完成。

## Submission Details

Name: **TODO** \
SUNet ID: **TODO** \
Citations: **TODO**

This assignment took me about **TODO** hours to do.


## App Concept
三个版本实现的是同一个 Notes Manager 笔记管理应用。用户可以创建、查看、编辑和删除笔记；每条笔记包含标题、可选正文、创建时间和更新时间。应用都包含标题必填校验、删除确认、空状态提示和基础错误处理，并分别使用浏览器 localStorage、SQLite 数据库和本地 JSON 文件来演示不同技术栈下的持久化方案。


## Version #1 Description
```
APP DETAILS:
===============
Folder name: bolt_react_notes
AI app generation platform: bolt.new
Tech Stack: React 18 + TypeScript + Vite + Tailwind CSS
Persistence: 浏览器 localStorage，存储键为 notes-manager-notes
Frameworks/Libraries Used: React、TypeScript、Vite、Tailwind CSS、Lucide React、ESLint
(Optional but recommended) Screenshots of core flows: 未提交截图；核心流程可通过本地运行后创建、编辑、删除笔记进行验证。

REFLECTIONS:
===============
a. Issues encountered per stack and how you resolved them:
Bolt 生成的 Web App 功能正常，但是 Export 下载按钮不可用。
将项目下载到本地后，第一次运行 npm run dev 时提示 vite 不是内部或外部命令。
后来通过 npm install 安装依赖后解决。

b. Prompting (e.g. what required additional guidance; what worked poorly/wel):
初始提示词比较有效，因为我明确说明了 Notes Manager、CRUD、note 字段、localStorage、标题校验等内容。最重要的是明确说不要 Supabase、Firebase、登录和外部后端，这样 Bolt 才没有把项目做复杂。额外需要指导的是持久化、校验和 README。效果不好的地方主要不是生成质量，而是 Bolt 的导出功能不可用，不过后来这个到处功能又可以用了。同时项目预览的打开速度很慢，总的来说这个工具在web app的创建和修改方面很强大，而且很方便，但是运行的速度很慢，给出提示词后有较大概率发生超时现象，同时 app 的预览加载很慢。

c. Approximate time-to-first-run and time-to-feature metrics: 
首次运行大约花费 20 分钟。完成完整 CRUD 功能大约花费 35 分钟，包括创建、编辑、删除、数据持久化、标题校验和本地运行检查。
```

## Version #2 Description
```
APP DETAILS:
===============
Folder name: flask-sqlite-notes
AI app generation platform: AI 编程助手辅助生成，手动检查和整理
Tech Stack: Python + Flask + SQLite + Jinja HTML templates + CSS
Persistence: 本地 SQLite 数据库 notes.db，应用启动时自动创建 notes 表
Frameworks/Libraries Used: Flask 3.1.3、sqlite3、pathlib、Jinja templates、原生 CSS
(Optional but recommended) Screenshots of core flows: 未提交截图；核心流程可通过 http://127.0.0.1:5000 创建、编辑、删除笔记进行验证。

REFLECTIONS:
===============
a. Issues encountered per stack and how you resolved them:
The main Flask issue was keeping the project small while still making it fully persistent. I used one SQLite database file and initialized the notes table at startup so the app can run without a separate database setup step. Another issue was making update and delete flows feel complete in a server-rendered app, so I used normal form submissions, redirects after successful writes, a delete confirmation in the UI, and simple 404/error handling for missing notes.

b. Prompting (e.g. what required additional guidance; what worked poorly/wel):
Flask 版本的提示词最有效的地方是直接指定了项目结构，比如 app.py、templates、static、requirements.txt、README.md。明确要求 SQLite、标题校验、note not found、删除确认也很有帮助。因为 Flask 结构比较简单，所以不需要太多轮提示。额外指导主要是让 requirements.txt 保持干净，只保留 Flask。

c. Approximate time-to-first-run and time-to-feature metrics: 
首次运行大约花费 10 分钟。完成完整 CRUD 功能大约花费 20 分钟，包括创建、编辑、删除、数据持久化、标题校验和本地运行检查。
```

## Version #3 Description
```
APP DETAILS:
===============
Folder name: nextjs-json-notes
AI app generation platform: AI 编程助手辅助生成，手动检查和整理
Tech Stack: Next.js App Router + React 19 + TypeScript + Tailwind CSS + Node.js API routes
Persistence: 本地 data/notes.json 文件；如果文件不存在，lib/notes.ts 会自动创建
Frameworks/Libraries Used: Next.js 16、React、TypeScript、Tailwind CSS、Next.js API routes、Node fs/promises、ESLint
(Optional but recommended) Screenshots of core flows: 未提交截图；核心流程可通过 http://localhost:3000 创建、编辑、删除笔记进行验证。

REFLECTIONS:
===============
a. Issues encountered per stack and how you resolved them:
The main Next.js issue was separating client UI state from server-side persistence. The page component talks to API routes, while the file-based persistence logic stays in lib/notes.ts and uses Node fs/promises only on the server side. I also needed to make sure the data directory and notes.json file are created when missing, so a fresh checkout can still run without manual data-file setup. Finally, because the repository root ignores lib/ folders, I updated the root .gitignore so this version's lib/notes.ts is included in submissions.

b. Prompting (e.g. what required additional guidance; what worked poorly/wel):
Next.js 版本比 Flask 需要更具体的提示。必须明确要求 App Router API routes，比如 GET/POST /api/notes，PUT/DELETE /api/notes/[id]。还要说明笔记保存到本地 JSON 文件，并且文件不存在时自动创建。最有用的是给出建议文件结构，比如 page.tsx、API route、lib/notes.ts、types/note.ts、data/notes.json。

c. Approximate time-to-first-run and time-to-feature metrics:
首次运行大约花费 20 分钟。完成完整 CRUD 功能大约花费 30 分钟，包括创建、编辑、删除、数据持久化、标题校验和本地运行检查。
```
