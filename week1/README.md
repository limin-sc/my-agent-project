# Week 1: AI Agent 基础与工具链

## 📌 概述
本周完成了 AI Agent 开发环境的搭建，掌握了 LangChain + LangGraph 的基本使用，构建了具备工具调用、长期记忆和异常处理能力的 ReAct Agent，并编写了系统性的评测脚本。

## 📂 内容列表

| 文件 | 描述 |
|------|------|
| `02_env_and_first_llm.ipynb` | Day 2：环境配置、DeepSeek API 调用、Jupyter 内核设置 |
| `03_react_agent_add_tool.ipynb` | Day 3：使用 `create_react_agent` 构建加法工具 Agent |
| `04_memory_sqlite.ipynb` | Day 4：通过 `SqliteSaver` 实现跨会话长期记忆 |
| `05_multi_tools_pydantic.ipynb` | Day 5：设计时间工具和日期差工具，引入 Pydantic 强校验和异常处理 |
| `test_agent.py` | Day 6：自动化评测脚本，测试 10 个用例并生成 CSV 结果 |
| `test_results.csv` | 评测原始数据（需人工标注正确性） |
| `summary_report.md` | 第一周学习总结与失败分析 |
| `requirements.txt` | 项目依赖列表 |
| `README.md` | 本文件 |

## 🚀 环境准备

### 1. 创建环境（使用 Anaconda）
```bash
conda create -n my_agent python=3.10 -y
conda activate my_agent

# （可选）设置国内镜像源加速
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
conda config --set show_channel_urls yes
2. 安装项目依赖
方法一：使用 requirements.txt（推荐）
将以下内容保存为 week1/requirements.txt：

text
langchain>=0.3.0
langchain-openai>=0.2.0
langgraph>=0.1.0
langgraph-checkpoint-sqlite>=0.1.0
pydantic>=2.0.0
python-dotenv>=1.0.0
jupyter>=1.0.0
ipykernel>=6.29.0
pandas>=2.0.0
requests>=2.31.0
在虚拟环境激活状态下执行：

bash
cd D:\my-agent-project
pip install --upgrade pip
pip install -r week1/requirements.txt
方法二：手动安装
bash
pip install langchain langchain-openai langgraph langgraph-checkpoint-sqlite pydantic python-dotenv jupyter ipykernel pandas requests
3. 配置 API 密钥（DeepSeek）
在项目根目录 D:\my-agent-project 下创建 .env 文件，内容如下：

text
DEEPSEEK_API_KEY=sk-你的实际密钥
重要：确保 .env 已加入 .gitignore，防止泄露。

如何获取 DeepSeek API Key？
访问 platform.deepseek.com 注册登录 → API Keys → 创建新密钥。

4. 注册 Jupyter 内核（可选）
bash
python -m ipykernel install --user --name=my_agent --display-name="Python (my-agent)"
启动 Jupyter：

bash
jupyter notebook
在 Notebook 中右上角选择内核 Python (my-agent)。

5. 验证环境
创建一个临时 Python 文件或 Jupyter cell，运行：

python
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()
llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1"
)
response = llm.invoke("Hello")
print(response.content)
若成功输出内容（非报错），说明环境已就绪。

🧪 测试脚本运行说明
在终端中依次执行：

bash
conda activate my_agent
D:
cd D:\my-agent-project\week1
python test_agent.py
运行后将生成 test_results.csv，请人工标注正确性并填写 summary_report.md。