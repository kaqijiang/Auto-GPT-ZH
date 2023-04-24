import builtins
import unittest
import json


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
    escaped = in_str = False
    start = end = -1
    for i, c in enumerate(ai_resp):
        if escaped:  # ignore the escaped char
            escaped = False
        elif c == '\\':  # ignore next char
            escaped = True
        elif c == '"':  # ignore quotes in the preface
            in_str = not in_str  # toggle in_str
        elif not in_str:  # ignore brackets inside strings
            if c == '{':
                if start == -1:
                    start = i  # found the first left bracket
                count += 1  # count left brackets
            elif c == '}':
                count -= 1  # count right brackets
                if count == 0:  # a complete json object is found
                    end = i  # take down the pos of the corresponding right bracket
                    break
    if start == -1 or end == -1:  # no valid json object found
        return ai_resp
    else:
        return ai_resp[start:end + 1]


def fix_json_by_removing_newline_in_values(ai_resp: str) -> str:
    """JSON doesn't allow this"""
    if not ai_resp or not isinstance(ai_resp, str):
        return ai_resp
    buff = ''
    escaped = in_str = False
    for c in ai_resp:
        if c == '"':
            if not escaped:  # ignore escaped quotes
                in_str = not in_str  # toggle in_str
        elif c == '\n':
            if in_str:  # if found a newline in a string
                c = '\\n'  # replace it with an escaped newline
        buff += c
        escaped = c == '\\' and not escaped  # check if the next char should be escaped
    return buff


class JSONFixTest(unittest.TestCase):
    def test_remove_preface(self):
        # Test that the preface is removed correctly
        good_resp = '''\
I want to use `google` command to search more information about `XXX`.

{
    "command": {
        "name": "google",
        "args": {
            "query": "XXX"
        }
    },
    "thoughts": {}
}
'''
        good_obj = {
            "command": {
                "name": "google",
                "args": {
                    "query": "XXX"
                }
            },
            "thoughts": {}
        }

        no_json = '''\
I want to use `google` command to search more information about `XXX`.
'''
        no_preface = '''\
{
    "command": {
        "name": "google",
        "args": {
            "query": "XXX"
        }
    },
    "thoughts": {}
}
'''

        truncated_resp = '''\
I want to use `google` command to search more information about `XXX`.

{
    "command": {
    }
'''

        multiple_json_resp = '''\
{
    "command": {
        "name": "XXX",
        "args": {}
    },
    "thoughts": {}
}

{
    "command": {
        "name": "blah",
        "args": {}
    },
    "thoughts": {}
}
'''
        first_obj = {
            "command": {
                "name": "XXX",
                "args": {}
            },
            "thoughts": {}
        }

        bad_syntax_resp = '''\
Some text.

{
    command: {},
    thoughts: {}
}
'''

        bad_syntax_resp_1 = '''\
{
    "command": {
        "name": "XXX"",
        "args": {}
    },
    "thoughts": {}
}
'''

        self.assertEqual(json.loads(fix_json_by_removing_preface(good_resp)), good_obj)
        self.assertEqual(fix_json_by_removing_preface(no_json), no_json)  # no change
        self.assertEqual(json.loads(fix_json_by_removing_preface(no_preface)), good_obj)
        self.assertEqual(fix_json_by_removing_preface(truncated_resp), truncated_resp)  # no change
        self.assertEqual(json.loads(fix_json_by_removing_preface(multiple_json_resp)), first_obj)
        with self.assertRaises(json.decoder.JSONDecodeError):
            json.loads(fix_json_by_removing_preface(bad_syntax_resp))
        with self.assertRaises(json.decoder.JSONDecodeError):
            json.loads(fix_json_by_removing_preface(bad_syntax_resp_1))

    def test_ignore_quotes_in_preface(self):
        # Test that quotes in the preface are ignored
        ai_resp = '''\
I see, "{1, 2, 3}" is a set instead of a list.

{
    "command": {
        "name": "write_to_file",
        "args": {
            "file_path": "test.txt",
            "text": "XXX"
        }
    },
    "thoughts": {}
}
'''
        good_obj = {
            "command": {
                "name": "write_to_file",
                "args": {
                    "file_path": "test.txt",
                    "text": "XXX"
                }
            },
            "thoughts": {}
        }

        self.assertEqual(json.loads(fix_json_by_removing_preface(ai_resp)), good_obj)

    def test_extracting_json_from_preface(self):
        good_resp = '''\
My reply would be { "sth": "blabla" }, what about yours?
'''
        good_obj = {
            "sth": "blabla"
        }

        self.assertEqual(json.loads(fix_json_by_removing_preface(good_resp)), good_obj)

    def test_escaping_in_string(self):
        escaping_string = '''\
This is a preface.

{
    "command": {
        "name": "XXX",
        "args": {
            "blabla": "if you count brackets in a string like this: \\"}}}\\", you are doing it wrong"
        }
    },
    "thoughts": {}
}
'''
        escaping_string_obj = {
            "command": {
                "name": "XXX",
                "args": {
                    "blabla": "if you count brackets in a string like this: \"}}}\", you are doing it wrong"
                }
            },
            "thoughts": {}
        }

        escaping_slashes = '''\
This is a preface.

{
    "command": {
        "name": "XXX",
        "args": {
            "blabla": "aaa\\\\bbb\\\\nccc\\nddd"
        }
    },
    "thoughts": {}
}
'''

        escaping_slashes_obj = {
            "command": {
                "name": "XXX",
                "args": {
                    "blabla": "aaa\\bbb\\nccc\nddd"
                }
            },
            "thoughts": {}
        }

        self.assertEqual(json.loads(fix_json_by_removing_preface(escaping_string)), escaping_string_obj)
        self.assertEqual(json.loads(fix_json_by_removing_preface(escaping_slashes)), escaping_slashes_obj)

    def test_escaping_newline_in_string(self):
        already_a_good_json = '''\
{
    "command": {
        "name": "XXX",
        "args": {
            "blabla": "blah"
        }
    }
}
'''
        good_obj = {
            "command": {
                "name": "XXX",
                "args": {
                    "blabla": "blah"
                }
            }
        }

        newline_in_value = '''\
{
    "command": {
        "name": "XXX",
        "args": {
            "blabla": "blah\nblah"
        }
    }
}
'''
        correct_obj = {
            "command": {
                "name": "XXX",
                "args": {
                    "blabla": "blah\nblah"
                }
            }
        }

        embedded_escaped_string_in_value_with_newline = '''\
{
    "command": {
        "name": "XXX",
        "args": {
            "blabla": "aaa\\"sth\nbla\\nbla\nelse\\"bbb"
        }
    }
}
'''

        embedded_escaped_string_in_value_with_newline_correct_obj = {
            "command": {
                "name": "XXX",
                "args": {
                    "blabla": "aaa\"sth\nbla\nbla\nelse\"bbb"
                }
            }
        }

        escaping_backslash = '''\
{
    "command": {
        "name": "XXX",
        "args": {
            "blabla": "aaa\\\\nsth\\\\bbb\\"\\\\ccc\\\\nddd\\"eee"
        }
    }
}
'''
        escaping_backslash_correct_obj = {
            "command": {
                "name": "XXX",
                "args": {
                    "blabla": "aaa\\nsth\\bbb\"\\ccc\\nddd\"eee"
                }
            }
        }

        self.assertEqual(json.loads(fix_json_by_removing_newline_in_values(already_a_good_json)), good_obj)

        # normally would crash without the fix
        self.assertEqual(json.loads(fix_json_by_removing_newline_in_values(newline_in_value)), correct_obj)

        self.assertEqual(json.loads(fix_json_by_removing_newline_in_values(
            embedded_escaped_string_in_value_with_newline)), embedded_escaped_string_in_value_with_newline_correct_obj)
        self.assertEqual(json.loads(fix_json_by_removing_newline_in_values(
                            escaping_backslash)), escaping_backslash_correct_obj)


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


if __name__ == '__main__':
    unittest.main()
