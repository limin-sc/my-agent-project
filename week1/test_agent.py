# test_agent.py
# 放置于 D:\my-agent-project\week1\ 目录下

import os
import sys
import time
import pandas as pd
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain.tools import tool
from datetime import datetime
from pydantic import BaseModel, Field, field_validator

# 切换到项目根目录（确保 .env 能被找到）
project_root = "D:/my-agent-project"
os.chdir(project_root)
load_dotenv()  # 加载 .env 中的 DEEPSEEK_API_KEY

# ========== 工具定义（与 Day5 一致） ==========
@tool
def get_current_time(format: str = "YYYY-MM-DD HH:MM:SS") -> str:
    """获取当前的日期和时间。"""
    try:
        now = datetime.now()
        if format == "timestamp":
            return str(int(now.timestamp()))
        return now.strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        return f"获取时间失败：{str(e)}"

class DateDiffInput(BaseModel):
    start_date: str = Field(description="起始日期，格式 YYYY-MM-DD，例如 2025-05-01")
    end_date: str = Field(default=None, description="结束日期，格式 YYYY-MM-DD，默认当前日期")

    @field_validator('start_date', 'end_date', mode='before')
    @classmethod
    def validate_date(cls, v):
        if v is None:
            return v
        try:
            datetime.strptime(v, "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"日期 '{v}' 格式错误，请使用 YYYY-MM-DD")
        return v

@tool(args_schema=DateDiffInput)
def calculate_days_between(start_date: str, end_date: str = None) -> str:
    """计算两个日期之间的天数差。"""
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d") if end_date else datetime.now()
        delta = abs((end - start).days)
        return f"从 {start_date} 到 {end_date if end_date else '今天'} 相差 {delta} 天。"
    except Exception as e:
        return f"计算失败：{str(e)}"

# ========== 初始化 Agent ==========
llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1",
    temperature=0
)

tools = [get_current_time, calculate_days_between]
agent_executor = create_react_agent(llm, tools)

# ========== 测试用例集（10个） ==========
test_cases = [
    ("获取当前时间", "现在几点？"),
    ("日期差计算（正确格式）", "从2025-05-01到2025-05-21有多少天？"),
    ("日期差计算（默认结束日期）", "从2025-05-01到今天过了多少天？"),
    ("组合任务", "现在是几号？然后算一下从2025-05-01到今天多少天。"),
    ("同一天", "从2025-05-21到2025-05-21相差几天？"),
    ("未来日期", "从2025-06-01到2025-05-21相差几天？"),
    ("错误日期格式（斜杠）", "计算从2025/05/01到今天的相差天数"),
    ("无效日期（月份13）", "从2025-13-01到今天的相差天数"),
    ("缺少参数", "计算一下天数差"),
    ("无关问题", "你好，介绍一下你自己"),
]

results = []

print("开始评测，请稍候...\n")
for case_name, user_input in test_cases:
    print(f"=== 测试用例：{case_name} ===")
    print(f"用户输入：{user_input}")
    start_time = time.time()
    try:
        response = agent_executor.invoke({"messages": [("user", user_input)]})
        answer = response["messages"][-1].content
        # 检查是否调用了工具：判断消息列表中是否存在 ToolMessage
        tool_calls_made = any(
            msg.type == "tool" for msg in response["messages"]
        )
    except Exception as e:
        answer = f"Agent 执行异常：{str(e)}"
        tool_calls_made = False
    elapsed = round(time.time() - start_time, 2)

    results.append({
        "用例名称": case_name,
        "用户输入": user_input,
        "Agent回答": answer[:500],  # 限制长度，避免CSV过大
        "是否调用工具": tool_calls_made,
        "耗时(秒)": elapsed,
        "是否正确": "待人工判断",
        "失败类型": ""
    })
    print(f"Agent回答：{answer[:200]}...\n")

# 保存到 CSV
df = pd.DataFrame(results)
csv_path = os.path.join("week1", "test_results.csv")
os.makedirs("week1", exist_ok=True)
df.to_csv(csv_path, index=False, encoding="utf-8-sig")

print(f"✅ 评测完成！结果已保存至：{csv_path}")
print("请用 Excel 打开该文件，人工填写“是否正确”（True/False）和“失败类型”列。")