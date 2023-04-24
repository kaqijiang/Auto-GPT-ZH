# Auto-GPT：自主 GPT-4 实验

> 这里是Auto-GPT中文项目- 同步fork Auto-GPT   Auto-GPT修改了分支规则，Fork同步于Stable最新分支

![gzh](docs/imgs/gzh.png)

### 公众号<阿杰的人生路>回复"Auto-GPT"加入群聊，共同探讨更多玩法

推荐工具：[【稳定，高速梯子推荐56一年，活动时5折，点击直达】](https://www.hjtnt.pro/auth/register?code=hwWF)

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

> 环境（选择一个）

- Python 3.10或更高版本（说明：[适用于Windows](https://www.tutorialspoint.com/how-to-install-python-in-windows)）
- Docker [Docker Hub](https://hub.docker.com/r/significantgravitas/auto-gpt)
- [VSCode + 开发容器](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

## 快速入门

1. 设置您的OpenAI [API密钥](https://platform.openai.com/account/api-keys)
2. 下载[最新版本](https://github.com/kaqijiang/Auto-GPT-ZH/releases/latest)
3. 安装[依赖项](https://github.com/Significant-Gravitas/Auto-GPT/blob/master/docs/installation.md)并设置[环境变量](https://github.com/Significant-Gravitas/Auto-GPT/blob/master/docs/installation.md)
4. [运行](https://github.com/Significant-Gravitas/Auto-GPT/blob/master/docs/usage.md)应用程序
5. 如果报错包含http 和 443 字样请查看[终端代理设置](./docs/终端代理.md)。

有关完整的设置说明和配置选项，请参阅以下链接的[文档](https://github.com/Significant-Gravitas/Auto-GPT/blob/master/docs)。

## 💾 使用文档

[安装方法](./docs/安装方法.md)

[使用方法](./docs/使用方法.md)

[声音](./docs/声音.md)

[搜索](./docs/搜索.md)

[缓存](./docs/缓存.md)

[图像生成](./docs/图像生成.md)

## ⚠️ 局限性

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
