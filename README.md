\# Homework1：代码解释Agent

\## 项目简介

本项目实现一个简易代码解释Agent，具备Agent基础循环，集成本地文件读取工具。用户输入本地代码文件名，Agent调用工具读取磁盘代码，调用大模型完成代码逻辑解读、生成注释，支持多轮对话上下文记忆。



\## 技术栈

\- Python3

\- DeepSeek LLM API

\- 手写简易Agent循环，未使用LangChain/AutoGen框架，便于理解Agent底层逻辑



\## 项目结构

├── .env                # API 密钥配置

├── main.py             # Agent 主程序

├── test\_code.py        # 测试样例代码

├── README.md

└── .gitignore





\## 环境安装

1\. 创建虚拟环境

```bash

python -m venv venv

\\# 激活虚拟环境

\\# windows: venv\\\\Scripts\\\\activate

pip install requests python-dotenv




