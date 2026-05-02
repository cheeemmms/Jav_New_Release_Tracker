# JAV New Release Tracker (JRT)

针对特定 Jav 网站，自动化抓取指定女优的新发布作品，生成 Markdown 报告并分批在浏览器中预览。

---

## 功能特性

-   **增量抓取** — 基于上次运行时间或手动输入日期，只抓取新作品
-   **精准定位** — 通过女优 UID 直接访问其主页，不做全站搜索
-   **智能过滤** — 自动剔除 VR 类条目，可扩展过滤规则
-   **聚合报告** — 按女优分类生成 Markdown 预览文件
-   **分批预览** — 每批 20 个链接在浏览器中打开，避免标签页过多
-   **状态记忆** — 运行成功后自动记录当前日期，下次增量衔接

---

## 技术栈

| 层级 | 技术 |
|------|------|
| 语言 | Python 3.10+ |
| 浏览器自动化 | Playwright + playwright-stealth |
| HTML 解析 | BeautifulSoup4 |
| 终端交互 | Rich |
| 配置 | YAML |
| 状态 | JSON |

---

## 项目结构

```
Jav_New_Release_Tracker/
├── config/
│   ├── config.yaml          # 静态配置：女优名单、代理、分批大小
│   └── state.json           # 运行状态（自动维护）
├── src/
│   ├── main.py              # 入口，流程调度与用户交互
│   ├── scraper/
│   │   ├── engine.py        # 浏览器引擎（Playwright + Stealth）
│   │   └── parser.py        # 页面解析（BeautifulSoup）
│   ├── output/
│   │   ├── md_generator.py  # Markdown 报告生成
│   │   └── browser_opener.py# 分批浏览器唤起
│   └── utils/
│       ├── logger.py        # Rich 终端日志
│       └── config_loader.py # YAML/JSON 读写
├── outputs/                 # 生成的报告存放目录
│   └── Updates_YYYYMMDD.md
├── requirements.txt
└── .gitignore
```

---

## 快速开始

### 1. 环境准备

```bash
# 克隆项目
git clone <repo-url>
cd Jav_New_Release_Tracker

# 安装依赖
pip install -r requirements.txt

# 安装 Playwright 浏览器（首次运行需要）
playwright install chromium
```

### 2. 配置

编辑 `config/config.yaml`，填入你的女优名单和代理设置：

```yaml
settings:
  proxy: "http://127.0.0.1:7890"
  batch_size: 20
  headless: false

stars:
  - { name: "示例女优", id: "xxxx" }
```

### 3. 运行

```bash
python src/main.py
```

首次运行会提示输入起始日期，之后每次运行会记住上次的日期，只抓取增量内容。

---

## 配置文件说明

### config.yaml

| 字段 | 类型 | 说明 |
|------|------|------|
| `settings.proxy` | string | HTTP 代理地址 |
| `settings.batch_size` | int | 每批打开的浏览器标签数 |
| `settings.headless` | bool | 是否无头模式（建议 false，方便手动过验证） |
| `stars` | list | 女优列表，需提供 name 和 id（站内 UID） |

### state.json

由程序自动维护，记录上次成功运行的日期。

---

## 注意事项

-   本项目仅供个人学习与技术研究使用
-   请合理控制抓取频率，内置 3-7 秒随机延迟
-   首次运行时建议 `headless: false`，以便手动完成 Cloudflare 验证
-   如果代理不可用，程序会在启动时给出提示

---

## 个性化配置

### 添加自定义收藏站

你可以在项目根目录放置自己的 `favorites_*.html` 浏览器书签文件（例如从 Chrome 导出的书签），Git 已配置自动忽略这些文件，不会提交到仓库。文件和 `.gitignore` 中的 `favorites_*.html` 规则匹配即可。

---

## 路线图

-   [ ] 支持排除合集/预告片标识
-   [ ] Markdown 中嵌入封面预览图
-   [ ] 自动检测磁力链接是否存在

---

## License

MIT
