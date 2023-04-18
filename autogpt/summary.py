from autogpt.llm_utils import create_chat_completion


def summarize_text(driver, text, question):
    if not text:
        return "Error: 没有可总结的文本"

    text_length = len(text)
    print(f"文字长度: {text_length} 字符")

    summaries = []
    chunks = list(split_text(text))

    scroll_ratio = 1 / len(chunks)
    for i, chunk in enumerate(chunks):
        scroll_to_percentage(driver, scroll_ratio * i)
        print(f"总结中 {i + 1} / {len(chunks)}")
        messages = [create_message(chunk, question)]

        summary = create_chat_completion(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=300,
        )
        summaries.append(summary)

    print(f"已总结 {len(chunks)}.")

    combined_summary = "\n".join(summaries)
    messages = [create_message(combined_summary, question)]

    return create_chat_completion(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=300,
    )


def split_text(text, max_length=8192):
    paragraphs = text.split("\n")
    current_length = 0
    current_chunk = []

    for paragraph in paragraphs:
        if current_length + len(paragraph) + 1 <= max_length:
            current_chunk.append(paragraph)
            current_length += len(paragraph) + 1
        else:
            yield "\n".join(current_chunk)
            current_chunk = [paragraph]
            current_length = len(paragraph) + 1

    if current_chunk:
        yield "\n".join(current_chunk)


def create_message(chunk, question):
    return {
        "role": "user",
        "content": f'"""{chunk}""" 使用以上文本，请以中文回答以下问题:'
        f' question: "{question}" -- if the question cannot be answered using the text,'
        " please summarize the text.",
    }


def scroll_to_percentage(driver, ratio):
    if ratio < 0 or ratio > 1:
        raise ValueError("百分比应该在 0 和 1 之间")
    driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight * {ratio});")
