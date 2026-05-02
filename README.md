# JAV New Release Tracker (JRT)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Ready-brightgreen)]()
[![GitHub stars](https://img.shields.io/github/stars/cheeemmms/Jav_New_Release_Tracker?style=flat)](https://github.com/cheeemmms/Jav_New_Release_Tracker/stargazers)

> 🇬🇧 [English version](README_EN.md) | 🇨🇳 中文版

自动化抓取指定女优的新发布作品，生成 Markdown 报告并分批在浏览器中预览。

---

## ⚠️ 免责声明

- **本项目仅供个人学习 Python 编程与 Web 自动化技术使用。**
- 使用者应自行遵守目标网站的 `robots.txt` 及使用条款。
- 请合理控制抓取频率，程序已内置 3-7 秒随机延迟，请勿修改为过短的间隔。
- 使用本项目产生的任何法律风险与责任，均由使用者自行承担。
- 作者不对任何滥用行为负责。

---

## 功能特性

- **增量抓取** — 基于上次运行时间或手动输入日期，只抓取新作品
- **精准定位** — 通过女优 UID 直接访问其主页，不做全站搜索
- **智能过滤** — 自动剔除 VR 类条目
- **聚合报告** — 按女优分类生成 Markdown 文件
- **分批预览** — 每批 20 个链接在浏览器中打开
- **状态记忆** — 运行成功后自动记录日期，下次增量衔接

---

## 运行流程概览

```
┌─────────────────────────────────────────────────────────┐
│  1. 程序启动 → 显示上次运行日期                            │
│  2. 选择：使用上次日期 / 手动输入新日期                     │
│  3. 自动打开浏览器 → 逐个抓取女优页面                       │
│  4. 生成 Markdown 报告 (outputs/Updates_YYYYMMDD.md)      │
│  5. 分批在浏览器中打开新作品链接                            │
│  6. 保存本次运行日期 → 完成                                │
└─────────────────────────────────────────────────────────┘
```

---

## 0 基础部署指南

如果你是第一次接触 Python 项目，请按以下步骤操作：

### 第一步：安装 Python

1. 打开浏览器，访问 https://www.python.org/downloads/
2. 点击黄色的 **Download Python** 按钮，下载最新版安装包
3. **重要**：运行安装包时，务必勾选底部的 **「Add Python to PATH」**（添加到环境变量），然后点击 Install Now

   ```
   ┌──────────────────────────────────┐
   │  ☑ Add Python to PATH   ← 必须勾选 │
   │  [Install Now]                   │
   └──────────────────────────────────┘
   ```

4. 安装完成后，验证是否成功：

   - 按 `Win + R`，输入 `cmd`，回车打开命令提示符
   - 输入以下命令，应该显示 Python 版本号（如 `Python 3.12.x`）：

   ```bash
   python --version
   ```

### 第二步：下载项目

**方式一（推荐）：使用 Git 克隆**

```bash
git clone https://github.com/cheeemmms/Jav_New_Release_Tracker.git
cd Jav_New_Release_Tracker
```

**方式二：直接下载 ZIP**

1. 打开 https://github.com/cheeemmms/Jav_New_Release_Tracker
2. 点击绿色的 **Code** 按钮 → **Download ZIP**
3. 解压到你想要的目录（如 `D:\Jav_New_Release_Tracker`）
4. 在解压后的文件夹地址栏输入 `cmd` 回车，打开命令提示符

### 第三步：安装依赖

在项目目录下（命令提示符中），依次执行：

```bash
pip install -r requirements.txt
```

如果看到 `pip` 不是内部命令的报错：

```bash
python -m pip install -r requirements.txt
```

### 第四步：安装浏览器

```bash
playwright install chromium
```

这一步会下载一个独立的 Chromium 浏览器（约 150MB），用于程序自动操作。只需执行一次。

### 第五步：环境验证

运行以下命令，确认一切就绪：

```bash
python -c "import yaml, arrow, rich, bs4, playwright; print('环境就绪!')"
```

看到 `环境就绪!` 即为成功。

---

## 配置指南

### 配置文件位置

所有配置在 `config/config.yaml` 中，用任意文本编辑器（记事本、VS Code 等）打开即可编辑。

### 如何获取女优 UID

1. 打开目标网站（如 `https://www.javbus.com`）
2. 在搜索框输入女优名字，点击搜索结果进入她的主页
3. 观察浏览器地址栏，URL 格式为：

   ```
   https://www.javbus.com/star/xxxx
                            ↑
                          这就是 UID
   ```

   | 示例 | 页面 URL | UID（填到配置中） |
   |------|----------|-------------------|
   | 三上悠亚 | `javbus.com/star/12xc` | `12xc` |
   | 深田咏美 | `javbus.com/star/ok12` | `ok12` |

   只需 URL 中 `/star/` 后面的那部分。

### 配置女优名单

编辑 `config/config.yaml`：

```yaml
settings:
  proxy: "http://127.0.0.1:7890"   # 代理地址，见下方说明
  batch_size: 20                   # 每批打开链接数
  headless: false                  # 是否隐藏浏览器（建议 false）

stars:
  - { name: "三上悠亚", id: "12xc" }
  - { name: "深田咏美", id: "ok12" }
  - { name: "你喜欢的女优", id: "她的UID" }
```

- `name`：任意名称，用于报告中的显示
- `id`：从网站 URL 中获取的 UID
- 每添加一位女优，复制一行 `{ name: "名字", id: "uid" }`

### 代理设置说明

如果你在国内访问目标网站，通常需要代理：

| 代理工具 | 默认地址 |
|----------|----------|
| Clash / Clash Verge | `http://127.0.0.1:7890` |
| V2Ray / v2rayN | `http://127.0.0.1:10809` |
| SSR | `http://127.0.0.1:1080` |

**不需要代理**：将 `proxy` 设为空字符串 `""`

```yaml
settings:
  proxy: ""
```

### 关于 headless 模式

- `headless: false` — **推荐**。浏览器窗口会显示出来，遇到验证码时可以手动操作
- `headless: true` — 浏览器在后台运行，不会弹出窗口。适合确认一切正常后的日常使用

---

## 运行

在项目目录下执行：

```bash
python src/main.py
```

### 首次运行

```
+--------------------------------------------------+
| JAV New Release Tracker                           |
+--------------------------------------------------+
[INFO] 加载配置...
[INFO] 首次运行，请输入起始日期
请输入起始日期 (YYYY-MM-DD): 2026-01-01

如果输入 2026-01-01，将抓取该日期之后发布的所有新作品。
之后的每次运行，程序会记住上次的日期。
```

### 后续运行

```
上次运行日期: 2026-05-01，请选择:
  1. 使用上次日期 (2026-05-01)
  2. 手动输入新日期
请输入序号: 
```

选择 `1` 即可增量抓取，只获取 5 月 1 日之后的新作品。

### 运行结果

程序会在 `outputs/` 目录下生成 Markdown 报告：

```
outputs/
└── Updates_20260502.md
```

报告示例：

```markdown
# JAV 更新报告 (2026-05-02)

## 三上悠亚
1. **作品标题一**
   - 日期: 2026-05-01
   - 链接: [https://www.javbus.com/...](...)

## 深田咏美
> 暂无更新
```

之后程序会分批在浏览器中打开新作品链接，每批 20 个，确认后继续。

---

## 常见问题

<details>
<summary><b>Q: 提示 "No module named 'xxx'"</b></summary>

依赖未完整安装，重新执行：
```bash
pip install -r requirements.txt
```
</details>

<details>
<summary><b>Q: 提示 "playwright 未安装浏览器"</b></summary>

执行：
```bash
playwright install chromium
```
</details>

<details>
<summary><b>Q: 浏览器闪退或页面加载失败</b></summary>

1. 检查代理是否正常：确认代理软件已开启且端口正确
2. 确认 `headless: false`，观察浏览器窗口中的具体情况
3. 如果出现 Cloudflare 验证，在可见的浏览器窗口中手动完成验证
</details>

<details>
<summary><b>Q: 某个女优抓取失败，程序会崩溃吗？</b></summary>

不会。单个女优页面的错误会被捕获，程序会跳过她并继续处理下一个。
</details>

<details>
<summary><b>Q: 如何修改每批打开的链接数？</b></summary>

在 `config/config.yaml` 中修改 `batch_size` 的值（默认 20）。
</details>

<details>
<summary><b>Q: 如何重置状态（重新抓取全部作品）？</b></summary>

编辑 `config/state.json`，将 `last_run_date` 改为一个很早的日期，或者直接删除该文件。
</details>

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
│   ├── config.yaml          # 女优名单、代理、分批大小
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
├── outputs/                 # 生成的报告
├── requirements.txt
└── .gitignore
```

---

## 个性化配置

### 添加自定义收藏站

你可以在项目根目录放置自己的 `favorites_*.html` 浏览器书签文件（例如从 Chrome 导出的书签），Git 已配置自动忽略这些文件，不会提交到仓库。

---

## 路线图

- [ ] 支持排除合集/预告片标识
- [ ] Markdown 中嵌入封面预览图
- [ ] 自动检测磁力链接是否存在

---

## License

MIT
