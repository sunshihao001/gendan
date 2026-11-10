# 跟单领域｜俄语实战资料优先的 Solana Meme 专属方法论

> 2026-11-10 最新用户目标：优先俄语原始资料，建立具体的**跟单领域专属知识与思维方法**。过去提出的“先建通用 Meme 认知再研究跟单”不再是当前执行顺序。旧 Meme 知识仍保留，但只在解释某个跟单问题时按需调用。

## ✅ V0.2 可运行工具（优先入口）

**已在本地执行 22 项离线测试并生成实际 HTML/JSON 报告。** Windows 可直接运行仓库根目录 `start-windows.bat`；macOS/Linux 可运行 `sh start-macos-linux.sh`。两者只处理随附历史样本，并在完成后打开报告，不涉及签名或下单。 现在已恢复原有钱包关系引擎，并新增真实历史供应商快照核查与 Solana 原始交易检查器，不必再从研究报告开始。

~~~bash
python -m unittest discover -s tests -v
python -m tools.snapshot_case data/blix_archived_mint_vendor_summary.json --out output
python -m tools.inspect_signature --input-rpc /path/to/getTransaction.json --mint <Mint> --out output/tx_inspection.json
python -m gendan.cli data/demo_case.json --out output
~~~

- [实际工具说明与限制](docs/OPERATIONS-V0.2.md)｜[快照检查器](tools/snapshot_case.py)｜[原始交易检查器](tools/inspect_signature.py)｜[离线关系引擎](gendan/engine.py)。
- **真实结果：** 历史 Mint 的池相关 Holder Owner 被程序识别为不能直接作为独立可跟钱包；这源于以前已审计的供应商快照摘录，**不是**实时链上数据或真实跟单收益。
- **尚未完成：** 当前环境真实 RPC 访问、全钱包实时追踪、前向纸上跟单。README 中的研究文件属于支持材料，而非可运行产品本身。

## Blix × Gendan × ai-d：共同底层与跟单独有的判断（2026-11-10）

- **[跨项目能力与知识对照审计](project/BLIX-GENDAN-SHARED-CAPABILITY.md)**：逐项核对 Blix 已有源代码/知识、PR #16/#21 真实状态、Gendan 特有的跟单判断；不复制旧 Meme 全套体系。
- **[共享真实 Mint 案例 001](research/SHARED-CASE-001-BLIX-TO-GENDAN.md)**：复用 Blix 已审计的三次在线供应商快照，将“Pool 相关头部 Holder”从潜在跟单大户降级，展示同一市场事实产生的不同业务决策；非主网逐笔重放和盈利证明。

## 全项目建设入口（2026-11-10 新增）

**[全项目路线总图：研究＋市场实战＋策略验证＋产品工具＋数据风控](project/CONSTRUCTION-ROUTES.md)**：三条业务循环、六项支撑能力；九条工作路线的现实状态、成品复用、优先级、交付与防空转锚点。

**[第一轮真实只读调查启动卡](operations/FIRST-REAL-CASE.md)**：不需交易程序和真实资金，利用现成终端查公开钱包/Mint、保存签名证据、冻结观察时点；只交付证据充分的实际调查。

项目不再把“俄语研究报告数”当主要进度；研究继续服务于真实案例和未来纸上验证。未完成的真实数据验收仍明确标 NOT_RUN。

## 先看这里

- [俄语跟单知识入口](knowledge/copytrading-ru/README.md)：围绕真实筛钱包、逐笔评估、个性化过滤、观察与复盘，而不是泛化协议。
- **[研究 003：深度调查与反例](research/RU-003-deep-study.md)**：俄文原文逐段审读 × 多钱包/仓位双图 × 源码级重叠反例 × 真实公开地址/交易签名调查入口。
- [公开链上调查证据状态](research/RU-003-public-evidence.md) ｜ [可复算离线反例](research/labs/study003_overlap_repro.py)。
- [Mark × Froggy 长视频研究](knowledge/copytrading-ru/01-mark-video-study.md)：基于用户保存的俄中双语字幕，恢复作者实操及反面案例。
- [跟单专属钱包判断卡](knowledge/copytrading-ru/02-wallet-selection-specific.md)：具体问题、候选类型、钱包关联与纸上验证。
- [俄语原始资料和检索词](knowledge/copytrading-ru/SOURCES.md)：视频、Froggy 官方资料、俄语 Habr 案例、俄语 GitHub 文档，标明证据性质。
- [案例 RU-001](research/RU-CASE-001.md)：不是盈利秘诀，而是筛钱包后为何可能失效的具体研究。
- [AI 跟单工作指令](prompts/AI-跟单研究指令.md) / [当前台账](research/ACTIVE-LEDGER.md)。

## 你的问题就是项目的研究入口

- 一份 Froggy 导出里为什么有些高 PnL 钱包应该跳过？
- 同一钱包为什么不能复制它的全部交易？如何按买入金额、市值和持仓行为拆解？
- 多钱包属于同一组织、共享工具，还是独立交易者？资金、Token 和实际成交要如何区分？
- 新钱包接收 Token 后卖出时，原钱包是否仍值得跟踪？
- 该钱包能盈利，为什么跟随者可能因为执行延迟、费用和价格冲击而亏损？
- 初选的钱包十天之后还有效吗？没有交易的地址怎样处理？跟单盈亏与其他交易如何拆账？

## 来源与能力分工

**研究优先级**：俄语实操视频、原始文档、可检查的复盘与反例 → 项目特有的专业假说 → 成熟软件上的验证 → 后续修订。

**已成熟的软件**：Froggy 用于批量发现与筛选；GMGN/OKX/Blix 等用于交叉核查交易与资金；监控器用于观察买卖/转账。功能以其真实可见版本为准，不自己重复做一套交易终端。

**按需调用的市场知识**：[原通用 Meme 知识入口](knowledge/meme/README.md)、[原 Blix 专业知识](https://github.com/sunshihao001/grok/tree/blix/knowledge)、[ai-d 专业研究方法](https://github.com/sunshihao001/ai-d)。不复制十二域/专家制度作为默认过程。

## 事实边界

资料阅读≠实际运行。俄语作者操作演示≠稳定盈利。供应商 ROI、Win Rate 和 PnL≠自己的可复制收益。同槽/同源资金≠共同控制。仅进行只读调查与纸上跟单研究；不授权交易、签名、付款或提交私钥。

**当前状态**：已阅读已保存俄语字幕及部分公开俄语材料、完成方法与问题归纳；未登录 Froggy、未获取真实钱包导出、未核验作者真实盈利。接下来最有价值的是在真实导出或公开钱包上完成第一张可核验的研究卡，而不是继续扩展概念目录。
