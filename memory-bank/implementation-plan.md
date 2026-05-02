# JRT - 实施计划 (Implementation Plan)

## 开发阶段总览

| 阶段 | 名称 | 涉及文件 | 预估依赖 |
|------|------|----------|----------|
| P1 | 项目脚手架 | 目录结构、requirements.txt、.gitignore、config | 无 |
| P2 | 工具模块 | config_loader.py、logger.py | P1 |
| P3 | 爬虫核心 | engine.py、parser.py | P2 |
| P4 | 输出模块 | md_generator.py、browser_opener.py | P2 |
| P5 | 主入口 | main.py | P3、P4 |
| P6 | 集成验证 | 端到端测试、异常处理加固 | P5 |

---

## P1：项目脚手架

### 目标
搭建项目骨架，使后续模块可独立开发与测试。

### 任务清单
- [ ] **1.1** 创建目录结构
  - `config/`、`src/scraper/`、`src/output/`、`src/utils/`、`outputs/`
- [ ] **1.2** 创建 `requirements.txt`
  - playwright、beautifulsoup4、rich、pyyaml、arrow、playwright-stealth
- [ ] **1.3** 创建 `.gitignore`
  - 忽略 `__pycache__/`、`state.json`、`outputs/*.md`、`.venv/`
- [ ] **1.4** 创建 `config/config.yaml`（模板）
  - settings: proxy、batch_size、headless
  - stars: 女优列表
- [ ] **1.5** 创建 `config/state.json`（初始状态）
  - last_run_date 默认值

---

## P2：工具模块

### 目标
提供配置加载与日志输出能力，是所有模块的基础依赖。

### 任务清单
- [ ] **2.1** `src/utils/__init__.py` — 空文件，标记包
- [ ] **2.2** `src/utils/config_loader.py`
  - `load_yaml(path)` → 返回 dict，含异常处理
  - `load_json(path)` → 返回 dict，文件不存在时返回默认值
  - `save_json(path, data)` → 写入 JSON
  - 路径均基于项目根目录自动解析
- [ ] **2.3** `src/utils/logger.py`
  - 使用 Rich Console 封装
  - `log_info(msg)`、`log_success(msg)`、`log_warning(msg)`、`log_error(msg)`
  - `log_title(msg)` — 醒目标题
  - `ask_choice(question, choices)` — 交互式选择

---

## P3：爬虫核心

### 目标
实现浏览器自动化与页面解析，是项目的核心逻辑。

### 任务清单
- [ ] **3.1** `src/scraper/__init__.py` — 空文件
- [ ] **3.2** `src/scraper/engine.py`
  - `BrowserEngine` 类：
    - `__init__(config)` — 初始化配置（代理、headless）
    - `start()` — 启动 Playwright + Stealth 注入
    - `navigate(url, timeout)` — 导航到页面并返回 BeautifulSoup 对象
    - `close()` — 关闭浏览器
    - 上下文管理器支持 (`__enter__` / `__exit__`)
  - 随机延时函数 (3-7 秒)
- [ ] **3.3** `src/scraper/parser.py`
  - `parse_star_page(html, star_name, cutoff_date)` → 返回作品列表
    - 提取：标题、详情页 URL、发布日期
    - 日期比较过滤（早于 cutoff_date 则停止）
    - VR 标签过滤
    - 容错：无作品时返回空列表
  - 数据结构：`{"title": str, "url": str, "date": str, "is_vr": bool}`

---

## P4：输出模块

### 目标
生成 Markdown 报告并分批打开浏览器。

### 任务清单
- [ ] **4.1** `src/output/__init__.py` — 空文件
- [ ] **4.2** `src/output/md_generator.py`
  - `generate_report(results, output_dir)` → 返回报告文件路径
    - results 结构：`{star_name: [MovieData, ...]}`
    - 无更新女优显示"暂无更新"
    - 文件命名：`Updates_YYYYMMDD.md`
    - 按女优分类输出，含序号、日期、标题、链接
- [ ] **4.3** `src/output/browser_opener.py`
  - `open_batch(urls, batch_size)` → 交互式分批打开
    - 每批等待用户确认后继续
    - 显示进度：已打开 X / Y
    - 用户可随时退出

---

## P5：主入口

### 目标
串联全部流程，实现设计文档中定义的完整工作流。

### 任务清单
- [ ] **5.1** `src/__init__.py` — 空文件
- [ ] **5.2** `src/main.py`
  - 三个阶段完整实现：
    1. **初始化与环境检查**
       - 加载 config.yaml 和 state.json
       - 展示 last_run_date，询问用户选择日期
       - 可选：检查代理可用性
    2. **执行抓取**
       - 启动浏览器引擎
       - 循环女优列表，逐个抓取并解析
       - 异常处理：单个女优失败不影响全局
    3. **结果输出与交互**
       - 生成 Markdown 报告
       - 分批打开链接
       - 成功结束后更新 state.json

---

## P6：集成验证

### 目标
保障代码质量与异常覆盖。

### 任务清单
- [ ] **6.1** 端到端验证（手动运行）
- [ ] **6.2** 常见异常场景覆盖
  - 代理不可用
  - 女优页面 404 / 超时
  - 无新作品
  - state.json 不存在（首次运行）
- [ ] **6.3** Rich 控制台输出美化验收
- [ ] **6.4** 检查所有 import 是否正确，依赖是否完整

---

## 开发顺序

```
P1 → P2 → P3 + P4 (可并行) → P5 → P6
```

P3 与 P4 均可独立于对方开发（它们只依赖 P2），但 P5 需要两者都完成。
