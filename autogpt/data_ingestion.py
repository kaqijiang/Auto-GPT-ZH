import argparse
import logging

from autogpt.config import Config
from autogpt.commands.file_operations import ingest_file, search_files
from autogpt.memory import get_memory

cfg = Config()


def configure_logging():
    logging.basicConfig(
        filename="log-ingestion.txt",
        filemode="a",
        format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
        datefmt="%H:%M:%S",
        level=logging.DEBUG,
    )
    return logging.getLogger("AutoGPT-Ingestion")


def ingest_directory(directory, memory, args):
    """
     通过为每个文件调用 ingest_file 函数来摄取目录中的所有文件。

     :param directory: 包含要摄取的文件的目录
     :param memory: 具有 add() 方法的对象，用于将块存储在内存中
     """
    try:
        files = search_files(directory)
        for file in files:
            ingest_file(file, memory, args.max_length, args.overlap)
    except Exception as e:
        print(f"获取目录 '{directory}' 时出错：{str(e)}")


def main() -> None:
    logger = configure_logging()

    parser = argparse.ArgumentParser(
        description="Ingest a file or a directory with multiple files into memory. "
        "Make sure to set your .env before running this script."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--file", type=str, help="The file to ingest.")
    group.add_argument(
        "--dir", type=str, help="The directory containing the files to ingest."
    )
    parser.add_argument(
        "--init",
        action="store_true",
        help="Init the memory and wipe its content (default: False)",
        default=False,
    )
    parser.add_argument(
        "--overlap",
        type=int,
        help="The overlap size between chunks when ingesting files (default: 200)",
        default=200,
    )
    parser.add_argument(
        "--max_length",
        type=int,
        help="The max_length of each chunk when ingesting files (default: 4000)",
        default=4000,
    )

    args = parser.parse_args()

    # Initialize memory
    memory = get_memory(cfg, init=args.init)
    print("使用内存类型：" + memory.__class__.__name__)

    if args.file:
        try:
            ingest_file(args.file, memory, args.max_length, args.overlap)
            print(f"文件 '{args.file}' 已成功获取。")
        except Exception as e:
            logger.error(f"获取文件 '{args.file}' 时出错：{str(e)}")
            print(f"获取文件 '{args.file}' 时出错：{str(e)}")
    elif args.dir:
        try:
            ingest_directory(args.dir, memory, args)
            print(f"目录 '{args.dir}' 成功获取。")
        except Exception as e:
            logger.error(f"获取目录 '{args.dir}' 时出错：{str(e)}")
            print(f"获取目录 '{args.dir}' 时出错：{str(e)}")
    else:
        print(
           "请提供 auto_gpt_workspace 目录中的文件路径 (--file) 或目录名称 (--dir) 作为输入。"
        )


if __name__ == "__main__":
    main()
