# 大模型接口调用
from openai import OpenAI

# 根据模型名称调用对应的接口（含文件上传）
def llm_call(name, apikey, prompt, file_content):
    if name == 'deepseek':
        return llm_deepseek(apikey, prompt, file_content)
    elif name == 'kimi':
        return llm_kimi(apikey, prompt, file_content)
    elif name == '千问':
        return llm_qwen(apikey, prompt, file_content)
    else:
        return False, '不支持的大模型'

# 根据模型名称调用对应的接口（不含文件上传）
def llm_chat_call(name, apikey, prompt):
    if name == 'deepseek':
        return llm_deepseek_chat(apikey, prompt)
    elif name == 'kimi':
        return llm_kimi_chat(apikey, prompt)
    elif name == '千问':
        return llm_qwen_chat(apikey, prompt)
    else:
        return False, '不支持的大模型'

# 模型：deepseek-v2.5
def llm_deepseek(apikey, prompt, file_content):
    client = OpenAI(
        api_key=apikey,
        base_url="https://api.deepseek.com/v1"
    )

    # 支持上下文对话
    messages = [
        {
            "role": "system",
            "content": "你是一个专业的智能数据分析助手，请你严格根据文档内容来回答问题，不要编造信息。"
        },
        {
            "role": "user",
            "content": f"以下是我提供的文档内容：\n\n{file_content}"
        }
    ]

    # 最新消息
    messages.append({"role": "user", "content": prompt})
    #print(messages)

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            response_format={"type": "json_object"},
            temperature=0.1,
            presence_penalty=0.0,
            stream=False
        )

        #print(response)
        return True, response.choices[0].message.content
    except Exception as e:
        print(f"llm_deepseek error: {e}")
        message = f"error: {e}"
        return False, message

# 模型：qwen3-max
def llm_qwen(apikey, prompt, file_content):
    client = OpenAI(
        api_key=apikey,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
    )

    # 支持上下文对话
    messages = [
        {
            "role": "system",
            "content": "你是一个专业的智能数据分析助手，请你严格根据文档内容来回答问题，不要编造信息。"
        },
        {
            "role": "user",
            "content": f"以下是我提供的文档内容：\n\n{file_content}"
        }
    ]

    # 最新消息
    messages.append({"role": "user", "content": prompt})
    #print(messages)
    
    try:
        response = client.chat.completions.create(
            model="qwen3-max",
            messages=messages,
            response_format={"type": "json_object"},
            temperature=0.1,
            presence_penalty=0.0,
            stream=False
        )

        print(response)
        return True, response.choices[0].message.content
    except Exception as e:
        print(f"llm_qwen error: {e}")
        message = f"error: {e}"
        return False, message

# 模型：kimi-k2-turbo-preview
def llm_kimi(apikey, prompt, file_content):
    client = OpenAI(
        api_key=apikey,
        base_url="https://api.moonshot.cn/v1",
    )
    
    # 支持上下文对话
    messages = [
        {
            "role": "system",
            "content": "你是一个专业的智能数据分析助手，请你严格根据文档内容来回答问题，不要编造信息。",
        },
        {
            "role": "user",
            "content": f"以下是我提供的文档内容：\n\n{file_content}",
        }
    ]

    # 最新消息
    messages.append({"role": "user", "content": prompt})
    #print(messages)
    
    try:
        response = client.chat.completions.create(
            model="kimi-k2-turbo-preview",
            messages=messages,
            response_format={"type": "json_object"},
            temperature=0.1,
            presence_penalty=0.0,
            stream=False
        )
    
        #print(response)
        return True, response.choices[0].message.content
    except Exception as e:
        print(f"llm_kimi error: {e}")
        message = f"error: {e}"
        return False, message

# 模型：deepseek-v2.5 不传文件
def llm_deepseek_chat(apikey, prompt):
    client = OpenAI(
        api_key=apikey,
        base_url="https://api.deepseek.com/v1"
    )

    messages = [
        {
            "role": "system",
            "content": "你是一个专业的智能数据分析助手。"
        },
        {
            "role": "user",
            "content": prompt
        }
    ]

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            response_format={"type": "json_object"},
            temperature=0.1,
            stream=False
        )

        #print(response)
        return True, response.choices[0].message.content
    except Exception as e:
        print(f"llm_deepseek_chat error: {e}")
        message = f"error: {e}"
        return False, message

# 模型：qwen3-max 不传文件
def llm_qwen_chat(apikey, prompt):
    client = OpenAI(
        api_key=apikey,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
    )

    messages = [
        {
            "role": "system",
            "content": "你是一个专业的智能数据分析助手。"
        },
        {
            "role": "user",
            "content": prompt
        }
    ]
    
    try:
        response = client.chat.completions.create(
            model="qwen3-max",
            messages=messages,
            response_format={"type": "json_object"},
            temperature=0.1,
            stream=False
        )

        #print(response)
        return True, response.choices[0].message.content
    except Exception as e:
        print(f"llm_qwen_chat error: {e}")
        message = f"error: {e}"
        return False, message

# 模型：kimi-k2-turbo-preview 不传文件
def llm_kimi_chat(apikey, prompt):
    client = OpenAI(
        api_key=apikey,
        base_url="https://api.moonshot.cn/v1",
    )
    
    # 把它放进请求中
    messages = [
        {
            "role": "system",
            "content": "你是一个专业的智能数据分析助手。"
        },
        {
            "role": "user",
            "content": prompt
        },
    ]
    
    try:
        response = client.chat.completions.create(
            model="kimi-k2-turbo-preview",
            messages=messages,
            response_format={"type": "json_object"},
            temperature=0.1,
            stream=False
        )
    
        #print(response)
        return True, response.choices[0].message.content
    except Exception as e:
        print(f"llm_kimi_chat error: {e}")
        message = f"error: {e}"
        return False, message
