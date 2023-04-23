import builtins


hooked_open = False


cmd_tr: dict[str, str] = {
    'google': '谷歌搜索',
    'browse_website': '浏览网页',
    'start_agent': '启动代理人',
    'message_agent': '向代理人发送消息',
    'list_agents': '列出代理人',
    'delete_agent': '删除代理人',
    'clone_repository': '克隆仓库',
    'write_to_file': '写入内容到文件',
    'read_file': '读取文件',
    'append_to_file': '追加内容到文件',
    'delete_file': '删除文件',
    'search_files': '搜索文件',
    'analyze_code': '分析代码',
    'improve_code': '改进代码',
    'write_tests': '编写测试',
    'execute_python_file': '执行 Python 文件',
    'generate_image': '生成图像',
    'send_tweet': '发送推文',
    'execute_shell': '执行 Shell 命令',
    'execute_shell_popen': '使用 Popen 执行 Shell 命令',
    'download_file': '下载文件',
    'do_nothing': '什么都不做',
    'task_complete': '任务完成',
    'human_feedback': '人类反馈'
}

cmd_arg_tr: dict[str, str] = {
    'code': '代码',
    'file': '文件',
    'command_line': '命令行参数',
    'filename': '文件名',
    'text': '文本',
    'directory': '目录',
    'url': '网址',
    'repo_url': '仓库网址',
    'clone_path': '本地目标路径',
    'prompt': '提示词',
    'suggestions': '建议',
    'question': '问题',
    'focus': '关注点',
    'task': '任务',
    'key': '键',
    'message': '消息内容',
    'input': '输入',
    'name': '名称',
    'agent_type': '代理人类型',
    'repository_url': '仓库网址',
    'query': '搜索词'
}

mem_type_tr: dict[str, str] = {
    'PineconeMemory': 'Pinecone 存储',
    'RedisMemory': 'Redis 数据库',
    'WeaviateMemory': 'Weaviate 存储',
    'MilvusMemory': 'Milvus 存储',
    'NoMemory': '无记忆',
    'LocalCache': '本地缓存'
}


def translate_command_args(args: dict[str, str]) -> dict[str, str]:
    if not args or not isinstance(args, dict):
        return args
    ret = args.copy()
    for k in args.keys():
        if (tr_k := cmd_arg_tr.get(k, None)) is None:
            print(f'警告: 参数名 \'{k}\' 未汉化')
            continue
        ret[tr_k] = ret.pop(k)
    return ret


def translate_command(cmd: str) -> str:
    if not cmd or not isinstance(cmd, str):
        return cmd
    if (ret := cmd_tr.get(cmd, None)) is None:
        print(f'警告: 指令 \'{cmd}\' 未汉化')
        return cmd
    return ret


def translate_memory_type(mem_type: str) -> str:
    if not mem_type or not isinstance(mem_type, str):
        return mem_type
    if (ret := mem_type_tr.get(mem_type, None)) is None:
        print(f'警告: 记忆类型 \'{mem_type}\' 未汉化')
        return mem_type
    return ret


def fix_json_by_removing_preface(ai_resp: str) -> str:
    """GPT 3.5 doesn't work well with some locales so we need this hack for now"""
    if not ai_resp or not isinstance(ai_resp, str):
        return ai_resp
    count = 0
    escaped = False
    start = -1
    end = -1
    for i, c in enumerate(ai_resp):
        if c == '{' and not escaped:
            if start == -1:
                start = i
            count += 1
        elif c == '}' and not escaped:
            count -= 1
            if count == 0:
                end = i
                break
        escaped = c == '\\'
    if start == -1 or end == -1:
        return ai_resp
    return ai_resp[start:end + 1]


def fix_json_by_removing_newline_in_values(ai_resp: str) -> str:
    """JSON doesn't allow this"""
    if not ai_resp or not isinstance(ai_resp, str):
        return ai_resp
    buff = ''
    in_str = False
    escaped = False
    for c in ai_resp:
        if c == '"' and not escaped:
            in_str = not in_str
        elif c == '\n' and in_str:
            c = '\\n'
        buff += c
        escaped = c == '\\'
    return buff


def my_open(orig_open, *args, **kwargs):
    """encoding is not utf-8 by default with some locales"""
    argc = len(args)
    if (argc > 1 and 'b' in args[1]) or 'encoding' in kwargs:
        return orig_open(*args, **kwargs)
    else:
        return orig_open(*args, encoding='utf-8', **kwargs)

def hook_open():
    global hooked_open

    if not hooked_open:
        orig_open = open
        builtins.open = lambda *args, **kwargs: my_open(orig_open, *args, **kwargs)
        hooked_open = True
