Jav_New_Release_Tracker/
├── config/
│   ├── config.yaml             # 静态配置：女优名单 (stars)、代理设置 (proxy)、分批大小
│   └── state.json              # 运行状态：last_run_date（由程序自动维护）
├── src/
│   ├── main.py                 # 入口文件：负责流程调度与用户交互
│   ├── scraper/
│   │   ├── engine.py           # 爬虫引擎：Playwright 启动、Stealth 注入、页面加载
│   │   └── parser.py           # 解析逻辑：BeautifulSoup 提取标题、日期、过滤 VR/合集
│   ├── output/
│   │   ├── md_generator.py     # 报告生成：将字典数据转换为 Markdown 文本
│   │   └── browser_opener.py   # 浏览器操作：分批唤起 webbrowser.open()
│   └── utils/
│       ├── logger.py           # 日志模块：Rich 样式的终端输出
│       └── config_loader.py    # 配置解析：读取 YAML/JSON 并处理异常
├── outputs/                    # 报告存放目录
│   └── Updates_20231027.md     # 自动生成的 MD 文件
├── requirements.txt            # 项目依赖列表
└── .gitignore                  # 忽略 state.json (可选) 与 __pycache__