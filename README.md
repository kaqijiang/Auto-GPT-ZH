# Auto-GPT：自主 GPT-4 实验

> 这里是Auto-GPT中文项目- 同步fork Auto-GPT   Auto-GPT修改了分支规则，Fork同步于Stable最新分支

![gzh](docs/imgs/gzh.png)

### 公众号<阿杰的人生路>回复"Auto-GPT"加入群聊，共同探讨更多玩法

### 中文版Demo :

![Demo video](docs/imgs/demo.gif)

Auto-GPT 是一个实验性开源应用程序，展示了 GPT-4 语言模型的功能。该程序由 GPT-4 驱动，将 LLM 的“思想”链接在一起，以自主实现您设定的任何目标。作为 GPT-4 完全自主运行的首批示例之一，Auto-GPT 突破了 AI 的可能性界限。

## 可以做什么？


**自主人工智能**：它所具备的能力主打的就是一个“自主”，**完全不用人类插手**的那种！

**例如：**我要求AutoGPT用Vue开发一个登录页面，结果不到3分钟，AI自己就“唰唰唰”地搞定了。

AI自己打开浏览器上网、自己使用第三方工具、自己思考、自己操作你的电脑。
它首先打开Vue官网，学习了下如何创建项目和模版，又去GitHub下载了一个类似的页面，下载下来自己改了一下。

**例如：**给它下达一个任务，让它去帮你做一些商业调查，或者历史故事。

AutoGPT在接到这项任务之后，便开始了他的展示：

- 思考中……
- 添加任务：调用浏览器或者GPTAPI去学习内容，再进行分析
- 添加任务：学习之后规划要做的事情
- 添加任务：逐步实现。
- 思考中……

然后AgentGPT先是输出执行的结果。
或者你给它下达命令：'请给我一下白宫的秘密资料'。
- 它会考虑如何去做
- 它可能会先从互联网上搜索和下载相关的文件。
- 如果觉得不够详细，它可能会学习一下黑客知识，黑进白宫获取资料。
- 这时候，请照顾好自己，因为你可能看着看着电脑，突然发现窗外一堆大汉，并佩戴者FBI徽章的人看着你，请不要慌张，请不要抵抗，也不要试图逃跑。
- 记得先拍照发个朋友圈。

开个玩笑，就是说它现在可以做你要它做的任何事情，它就是一个无敌超人的存在。
但是也请不要抱有太大希望，很可能运行半天什么也没有，它还是一个孩子，给它一点时间，思路很好，未来很美好。

## 📋 要求

- [Python 3.8 或者更高](https://www.tutorialspoint.com/how-to-install-python-in-windows)
- [OpenAI API key](https://platform.openai.com/account/api-keys)

可选的:

- [PINECONE API key](https://www.pinecone.io/)（如果你想要 Pinecone 支持存储日志，默认本地就行）
- [Milvus](https://milvus.io/)（如果你想要 Milvus 作为内存后端）

- [ElevenLabs Key](https://elevenlabs.io/) (如果你想让人工智能说话)

## 💾 安装方法

要安装 Auto-GPT，请按照下列步骤操作：

1. 确保满足上述所有**要求**，如果没有，请安装/获取它们。

以下命令需要在终端执行

2. 克隆存储库：对于此步骤，您需要安装 Git，但您可以通过单击此页面顶部的按钮来下载 zip 文件☝️

```
git clone git@github.com:kaqijiang/Auto-GPT-ZH.git
```

3. 终端中 cd到项目目录

```
cd Auto-GPT-ZH
```

4. 终端中安装所需的依赖项

```
pip install -r requirements.txt
```

5. 
- 重命名`.env.template`为`.env` 注意`.env.template`为隐藏文件，如果找不到就百度下你电脑window/mac如何显示隐藏文件。
- 填写您的`OPENAI_API_KEY`. 找到OPENAI_API_KEY=. 在'='之后，输入您唯一的 OpenAI API 密钥（不带任何引号或空格）。
- 如果您打算使用语音模式，请`ELEVEN_LABS_API_KEY`也填写您的。

  - 从以下网址获取您的 OpenAI API 密钥： https: [//platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys)。
  - 从[https://elevenlabs.io](https://elevenlabs.io/)获取您的 ElevenLabs API 密钥。您可以使用网站上的“个人资料”选项卡查看您的 xi-api-key。

## 终端代理方法

推荐工具：[【稳定，高速梯子推荐56一年，活动时5折，点击直达】](https://www.hjtnt.pro/auth/register?code=QRY5)

Mac 下载 [ClashX Pro](https://install.appcenter.ms/users/clashx/apps/clashx-pro/distribution_groups/public) 设置 系统代理 增强模式 然后复制终端代理命令 在终端中输入，重启即可

根据自己的工具修改对应的端口

```
export https_proxy=http://127.0.0.1:8484 http_proxy=http://127.0.0.1:8484 all_proxy=socks5://127.0.0.1:8484
```

Windows 下载 [Clash for Windows](https://wws.lanzoux.com/iCEgLj27fra)，设置 系统代理 ，在终端中输入，重启即可。

根据自己的工具修改对应的端口

```
# 使用 http 类型代理
set http_proxy=http://127.0.0.1:8484
set https_proxy=http://127.0.0.1:8484
# 使用 socks 类型代理
netsh winhttp set proxy proxy-server="socks=127.0.0.1:8484" bypass-list="localhost"
netsh winhttp show proxy
netsh winhttp reset proxy
# 使用 socks 类型代理
set http_proxy=socks5://127.0.0.1:8484
set https_proxy=socks5://127.0.0.1:8484
```

## 🔧 用法

1. 在终端中运行 `main.py` 

```
python -m autogpt
```

2. 在 AUTO-GPT 的每个操作之后，输入“y”来授权命令，“y -N”来运行 N 个连续命令，“n”来退出程序，或者为 AI 输入额外的反馈。

### 日志

您将在文件夹中找到活动和错误日志`./output/logs`

输出调试日志：

```
python -m autogpt --debug
```

### 命令行参数

以下是您在运行 Auto-GPT 时可以使用的一些常见参数：

> 将尖括号 (<>) 中的任何内容替换为您要指定的值

- `python scripts/main.py --help`查看所有可用命令行参数的列表。
- `python scripts/main.py --ai-settings <filename>`使用不同的 AI 设置文件运行 Auto-GPT。
- `python scripts/main.py --use-memory  <memory-backend>`指定 3 个内存后端之一：`local`、`redis`或`pinecone`'no_memory'。

> **注意**：其中一些标志有简写形式，`-m`例如`--use-memory`. 用于`python scripts/main.py --help`获取更多信息

## 🗣️ 语音模式

使用它来将 TTS 用于 Auto-GPT

```
python -m autogpt --speak
```
## OpenAI API 密钥配置
从以下网址获取您的 OpenAI API 密钥： https: //platform.openai.com/account/api-keys。

要将 OpenAI API 密钥用于 Auto-GPT，您需要设置账单（即付费账户）。

您可以在https://platform.openai.com/account/billing/overview设置付费账户。

要使 OpenAI API 密钥生效，请在 OpenAI API > 计费中设置付费帐户

![要使 OpenAI API 密钥生效，请在 OpenAI API > 计费中设置付费帐户](openai-api-key.png)

## 🔍 谷歌 API 密钥配置

此部分是可选的，如果您在运行谷歌搜索时遇到错误 429 问题，请使用官方谷歌 API。要使用该`google_official_search`命令，您需要在环境变量中设置 Google API 密钥。

1. 转到[谷歌云控制台](https://console.cloud.google.com/)。
2. 如果您还没有帐户，请创建一个并登录。
3. 通过单击页面顶部的“选择项目”下拉菜单并单击“新建项目”来创建一个新项目。给它起个名字，然后单击“创建”。
4. 转到[API 和服务仪表板](https://console.cloud.google.com/apis/dashboard)并单击“启用 API 和服务”。搜索“自定义搜索 API”并单击它，然后单击“启用”。
5. 转到[凭据](https://console.cloud.google.com/apis/credentials)页面并单击“创建凭据”。选择“API 密钥”。
6. 复制 API 密钥并将其设置为在您的计算机上命名的环境变量`GOOGLE_API_KEY`。请参阅下面的设置环境变量。
7. 转到[自定义搜索引擎](https://cse.google.com/cse/all)页面并单击“添加”。
8. 按照提示设置搜索引擎。您可以选择搜索整个网络或特定站点。
9. 创建搜索引擎后，单击“控制面板”，然后单击“基本”。复制“搜索引擎 ID”并将其设置为`CUSTOM_SEARCH_ENGINE_ID`在您的计算机上命名的环境变量。请参阅下面的设置环境变量。

*请记住，您的每日免费自定义搜索配额最多只允许 100 次搜索。要增加此限制，您需要为项目分配一个计费帐户，以从每天多达 10,000 次搜索中获利。*

### 设置环境变量

对于 Windows 用户：

```
setx GOOGLE_API_KEY "YOUR_GOOGLE_API_KEY"
setx CUSTOM_SEARCH_ENGINE_ID "YOUR_CUSTOM_SEARCH_ENGINE_ID"

```

对于 macOS 和 Linux 用户：

```
export GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY"
export CUSTOM_SEARCH_ENGINE_ID="YOUR_CUSTOM_SEARCH_ENGINE_ID"
```

## 设置缓存类型

默认情况下，Auto-GPT 将使用 LocalCache 而不是 redis 或 Pinecone。

要切换到任何一个，请将`MEMORY_BACKEND`env 变量更改为您想要的值：

- `local`（默认）使用本地 JSON 缓存文件
- `pinecone`使用您在 ENV 设置中配置的 Pinecone.io 帐户
- `redis`将使用您配置的 redis 缓存
- `milvus`将使用您配置的 milvus 缓存
- `weaviate`将使用您配置的 weaviate 缓存

### 设置

> 警告：本系统未经过安全保护，不应该公开访问。因此，请避免在互联网上使用Redis而不使用密码或根本不要使用Redis。

1. 安装 docker 桌面

```
docker run -d --name redis-stack-server -p 6379:6379 redis/redis-stack-server:latest
```

> 有关设置密码和其他配置的信息，请参阅[https://hub.docker.com/r/redis/redis-stack-server 。](https://hub.docker.com/r/redis/redis-stack-server)

1. 设置以下环境变量

> 替换尖括号 (<>) 中的**密码**

```
MEMORY_BACKEND=redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=<PASSWORD>
```

您可以选择设置

```
WIPE_REDIS_ON_START=False
```

持久化存储在 Redis 中的内存

您可以使用以下命令为 redis 指定内存索引：

```
MEMORY_INDEX=<WHATEVER>
```

### 🌲Pinecone API 密钥设置

Pinecone 支持存储大量基于向量的内存，允许在任何给定时间只为代理加载相关内存。

1. 如果您还没有帐户，请前往[pinecone并创建一个帐户。](https://app.pinecone.io/)
2. 选择`Starter`计划以避免被收费。
3. 在左侧边栏的默认项目下找到您的 API 密钥和区域。

在`.env`文件集中：

- `PINECONE_API_KEY`
- `PINECONE_ENV`（例如：*“us-east4-gcp”*）
- `MEMORY_BACKEND=pinecone`

或者，您可以从命令行设置它们（高级）：

对于 Windows 用户：

```
setx PINECONE_API_KEY "<YOUR_PINECONE_API_KEY>"
setx PINECONE_ENV "<YOUR_PINECONE_REGION>" # e.g: "us-east4-gcp"
setx MEMORY_BACKEND "pinecone"
```

对于 macOS 和 Linux 用户：

```
export PINECONE_API_KEY="<YOUR_PINECONE_API_KEY>"
export PINECONE_ENV="<YOUR_PINECONE_REGION>" # e.g: "us-east4-gcp"
export MEMORY_BACKEND="pinecone"
```

### Milvus 安装

[Milvus](https://milvus.io/)是一个开源的、高度可扩展的矢量数据库，可以存储大量基于矢量的内存并提供快速的相关搜索。

- 设置 milvus 数据库，保持你的 pymilvus 版本和 milvus 版本相同，以避免兼容问题。
  - 通过开源[安装 Milvus](https://milvus.io/docs/install_standalone-operator.md)
  - [或由Zilliz Cloud](https://zilliz.com/cloud)设置
- 设置`MILVUS_ADDR`为`.env`你的 milvus 地址`host:ip`。
- 设置`MEMORY_BACKEND`为`.env`启用`milvus`milvus 作为后端。
- 选修的
  - set `MILVUS_COLLECTION`in`.env`随意更改 milvus 集合名称，`autogpt`默认名称。

### Weaviate设置

[Weaviate](https://weaviate.io/)是一个开源矢量数据库。它允许存储来自 ML 模型的数据对象和向量嵌入，并无缝扩展到数十亿个数据对象。[Weaviate 实例可以在本地（使用 Docker）、Kubernetes 或使用 Weaviate 云服务创建](https://weaviate.io/developers/weaviate/quickstart)。虽然仍处于实验阶段，但支持[嵌入式 Weaviate ，它允许 Auto-GPT 进程本身启动 Weaviate 实例。](https://weaviate.io/developers/weaviate/installation/embedded)要启用它，请设置`USE_WEAVIATE_EMBEDDED`为`True`并确保您`pip install "weaviate-client>=3.15.4"`。

#### 设置环境变量

在您的`.env`文件中设置以下内容：

```
MEMORY_BACKEND=weaviate
WEAVIATE_HOST="127.0.0.1" # the IP or domain of the running Weaviate instance
WEAVIATE_PORT="8080" 
WEAVIATE_PROTOCOL="http"
WEAVIATE_USERNAME="your username"
WEAVIATE_PASSWORD="your password"
WEAVIATE_API_KEY="your weaviate API key if you have one"
WEAVIATE_EMBEDDED_PATH="/home/me/.local/share/weaviate" # this is optional and indicates where the data should be persisted when running an embedded instance
USE_WEAVIATE_EMBEDDED=False # set to True to run Embedded Weaviate
MEMORY_INDEX="Autogpt" # name of the index to create for the application
```

## 查看内存使用情况

1. 使用`--debug`标志查看内存使用情况:)

## 🧠内存预填充

#### python scripts/data_ingestion.py -h 

```

用法：data_ingestion.py [-h] (--file FILE | --dir DIR) [--init] [--overlap OVERLAP] [--max_length MAX_LENGTH]

将一个文件或包含多个文件的目录摄取到内存中。确保在运行此脚本之前设置您的 .env。

选项：-h, --help 显示此帮助消息并退出 --file FILE 要摄取的文件。--dir DIR 包含要摄取的文件的目录。--init 初始化内存并擦除其内容（默认值：False） --overlap OVERLAP 摄取文件时块之间的重叠大小（默认值：200） --max_length MAX_LENGTH 摄取文件时每个块的最大长度（默认值：4000）
```

#### python autogpt/data_ingestion.py --dir seed_data --init --overlap 200 --max_length 1000

- 该脚本位于 autogpt/data_ingestion.py，允许您将文件提取到内存中并在运行 Auto-GPT 之前预先填充。

  记忆预填充是一种技术，涉及将相关文档或数据摄取到 AI 的记忆中，以便它可以使用这些信息来生成更明智和准确的响应。

  为了预置到内存，每个文档的内容被分成指定最大长度的块，块之间有指定的重叠，然后每个块被添加到 .env 文件中的内存后端集。当提示 AI 回忆信息时，它可以访问那些预先植入的记忆以生成更明智和准确的响应。

  当处理大量数据或存在 AI 需要能够快速访问的特定信息时，此技术特别有用。通过预先植入内存，人工智能可以更有效地检索和使用这些信息，从而节省时间、API 调用并提高其响应的准确性。

  例如，您可以下载 API 文档、GitHub 存储库等，并在运行 Auto-GPT 之前将其提取到内存中。

  ⚠️如果您使用 Redis 作为您的内存，请确保运行 Auto-GPT 并在您的文件中`WIPE_REDIS_ON_START`设置为。`False``.env`

  ⚠️对于其他内存后端，我们目前在启动 Auto-GPT 时强制擦除内存。`data_ingestion.py`要使用这些内存后端摄取数据，您可以在 Auto-GPT 运行期间随时调用脚本。

  即使在 Auto-GPT 运行时摄取记忆，AI 也会立即使用记忆。

  在上面的示例中，脚本初始化内存，将目录中的所有文件摄取`/seed_data`到内存中，块之间的重叠为 200，每个块的最大长度为 4000。请注意，您也可以使用参数将`--file`单个文件摄取到内存中内存，并且脚本将只摄取`/auto_gpt_workspace`目录中的文件。

  您可以调整`max_length`和重叠参数以微调文档在“回忆”该内存时呈现给 AI 的方式：

  - 调整重叠值允许 AI 在调用信息时从每个块访问更多上下文信息，但会导致创建更多块，从而增加内存后端使用和 OpenAI API 请求。
  - 减小该`max_length`值将创建更多块，这可以通过在上下文中允许更多消息历史记录来节省提示令牌，但也会增加块的数量。
  - 增加该`max_length`值将为 AI 提供来自每个块的更多上下文信息，从而减少创建的块数量并节省 OpenAI API 请求。然而，这也可能会使用更多的提示标记并减少 AI 可用的整体上下文。

## 连续模式⚠️

**无需**用户授权即可 100% 自动化地运行 AI 。不推荐连续模式。它具有潜在危险，可能会导致您的 AI 永远运行或执行您通常不会授权的操作。使用风险自负。

1. `main.py`在终端中运行Python 脚本：

```
python -m autogpt --continuous
python -m autogpt --speak --continuous #带语音
```

2.要退出程序，请按 Ctrl + C

## GPT3.5 ONLY 模式 

如果您无权访问 GPT4 api，此模式将允许您使用 Auto-GPT！

```
python -m autogpt --gpt3only
python -m autogpt --speak --gpt3only #带语音
```

建议将虚拟机用于需要高度安全措施的任务，以防止对主计算机的系统和数据造成任何潜在危害。

## 🖼 图像生成

默认情况下，Auto-GPT 使用 DALL-e 进行图像生成。要使用 Stable Diffusion，需要一个[HuggingFace API 令牌。](https://huggingface.co/settings/tokens)

获得令牌后，将这些变量设置为`.env`：

```
IMAGE_PROVIDER=sd
HUGGINGFACE_API_TOKEN="YOUR_HUGGINGFACE_API_TOKEN"
```

## ⚠️ 限制

该实验旨在展示 GPT-4 的潜力，但存在一些局限性：

1. 不是完善的应用程序或产品，只是一个实验
2. 在复杂的真实业务场景中可能表现不佳。事实上，如果确实如此，请分享您的结果！
3. 运行成本非常高，因此请使用 OpenAI 设置和监控您的 API 密钥限制！

## 🛡 免责声明

免责声明 Auto-GPT 这个项目是一个实验性应用程序，按“原样”提供，没有任何明示或暗示的保证。使用本软件，即表示您同意承担与其使用相关的所有风险，包括但不限于数据丢失、系统故障或可能出现的任何其他问题。

本项目的开发者和贡献者对因使用本软件而可能发生的任何损失、损害或其他后果不承担任何责任或义务。您对基于 Auto-GPT 提供的信息做出的任何决定和行动承担全部责任。

**请注意，由于使用代币，使用 GPT-4 语言模型可能会很昂贵。**通过使用此项目，您承认您有责任监控和管理您自己的代币使用情况和相关费用。强烈建议定期检查您的 OpenAI API 使用情况并设置任何必要的限制或警报以防止意外收费。

作为一项自主实验，Auto-GPT 可能会生成不符合现实世界商业惯例或法律要求的内容或采取的行动。您有责任确保基于此软件的输出做出的任何行动或决定符合所有适用的法律、法规和道德标准。本项目的开发者和贡献者对因使用本软件而产生的任何后果不承担任何责任。

通过使用 Auto-GPT，您同意就任何和所有索赔、损害、损失、责任、成本和费用（包括合理的律师费）对开发人员、贡献者和任何关联方进行赔偿、辩护并使其免受损害因您使用本软件或您违反这些条款而引起的。