import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("DEEPSEEK_API_KEY")
BASE_URL = "https://api.deepseek.com/v1/chat/completions"

memory = []

def read_file_tool(file_path: str) -> str:
    """读取本地代码文件，返回文件内容，捕获异常"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        return f"【文件{file_path}内容】:\n{content}"
    except FileNotFoundError:
        return f"工具错误：文件 {file_path} 找不到，请检查路径"
    except Exception as e:
        return f"工具读取异常：{str(e)}"


def llm_call(messages):
    """调用大模型API"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek-chat",
        "messages": messages,
        "temperature": 0.3
    }
    resp = requests.post(BASE_URL, json=payload, headers=headers, timeout=30)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]


def agent_loop():
    system_prompt = """
你是代码解释Agent。
如果用户要求解释某个本地代码文件，你必须输出标记：[[READ_FILE:文件名]]，例如 [[READ_FILE:test_code.py]]
只有输出这个标记，程序才会调用文件读取工具读取磁盘上的代码。
拿到文件内容后，你需要：解释代码逻辑，标注关键步骤，生成行内注释。
如果不需要读文件，直接回答用户问题。
不要编造文件内容，文件必须调用工具读取。
支持用户后续继续追问代码相关问题。
"""
    memory.append({"role": "system", "content": system_prompt})
    print("====代码解释Agent启动完成====")
    print("示例输入：帮我解释 test_code.py，输入exit退出\n")

    while True:
        user_input = input("用户> ")
        if user_input.strip().lower() == "exit":
            print("退出Agent")
            break
        memory.append({"role": "user", "content": user_input})
        try:
            answer = llm_call(memory)
        except Exception as err:
            print(f"大模型调用出错：{err}")
            continue

        if "[[READ_FILE:" in answer:
            start = answer.find("[[READ_FILE:") + len("[[READ_FILE:")
            end = answer.find("]]")
            filename = answer[start:end].strip()
            print(f">>> Agent调用工具读取文件：{filename}")
            tool_result = read_file_tool(filename)
            memory.append({"role": "tool", "content": tool_result})
            final_ans = llm_call(memory)
            print(f"Agent> {final_ans}\n")
            memory.append({"role": "assistant", "content": final_ans})
        else:
            print(f"Agent> {answer}\n")
            memory.append({"role": "assistant", "content": answer})


if __name__ == "__main__":
    agent_loop()
