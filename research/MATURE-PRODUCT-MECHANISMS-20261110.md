# 跟单成熟产品的内部机制与跨能力组合｜源码级对照与下一轮选择（2026-11-10）

> **用户批准的本轮任务**：在上一轮“跟单能发展哪些能力”基础上，深入对照成熟产品内部的工作方式、专业依据、相互配合和失败模式，再决定下一步。此文是源级研究成果，不是另建一套跟单系统、不是自动启用真实交易、也不意味着把任何 AI 新认识固化成永久流程。
>
> **证据状态**：本轮逐文件读取 GitHub 默认分支的源码和项目原始说明，额外核对 Jito/GMGN 官方文档；对 Million 的归属阈值进行了一个简化的离线逻辑反例计算，**并未运行第三方项目全部服务、CI、真实链上数据或交易**。作者声称的历史成绩、故障和运行情况仅按作者陈述记录。链接均保留可追溯路径。

## 1｜四套产品不是四个功能清单：它们把“跟单问题”放在不同地方

| 产品/类型 | 具体组合方式与源级依据 | 有价值的专业判断 | 重要边界 |
| --- | --- | --- | --- |
| [Million](https://github.com/Kelows/million)（钱包与机会发现） | [owner关系](https://github.com/Kelows/million/blob/main/apps/api/src/analysis/owners.service.ts) → [copy/consensus/ladder机会生成](https://github.com/Kelows/million/blob/main/apps/api/src/opportunities/opportunities.service.ts) → [shadow跳过信号](https://github.com/Kelows/million/blob/main/apps/api/src/trading/shadow.service.ts) → 纸上交易与结果/决策日志；[MCP工具](https://github.com/Kelows/million/blob/main/packages/million-mcp/README.md) 可询问为何跳过 | 钱包信号既要看独立性、有效交易条件，也要保存“被拒绝的交易”作为过滤反例 | 聚类是启发式、市场状态依赖数据；影子结果不等于执行后的反事实收益；MIT |
| [ScreenerBot](https://github.com/farfary/ScreenerBot)（执行与模拟账本） | [copy任务内核](https://github.com/farfary/ScreenerBot/blob/main/src/trader/copy/mod.rs)：观察→门禁→买/卖→按任务归属仓位→paper/受控live→延迟熔断→分析；[任务入口](https://github.com/farfary/ScreenerBot/blob/main/src/agent_control/tools/copy_trading.rs) 暴露可检查参数与日志 | 策略意图不是只有“跟卖开关”，还涉及任务库存、重复事件、延迟、回填和退出权属 | 有真实交易功能，不得直接在本仓启动；[BUSL 1.1 使用限制](https://github.com/farfary/ScreenerBot/blob/main/LICENSE)，不能当成 MIT 自由移植 |
| [dexterm](https://github.com/dexterm-xyz/dexterm)（AI研究 + 策略试验） | README 声称只读市场分析/MCP、聊天构建策略、历史留出验证、前向 paper，再由用户单独启用外部执行器；本轮主要是**公开说明层审查** | AI 可以提出策略和解释，但要隔离 AI 分析权与真实执行权 | README 自述预设策略未证明优势、交易功能实验性；[AGPL-3.0](https://github.com/dexterm-xyz/dexterm/blob/main/LICENSE) 的移植/网络服务义务与 MIT 不同 |
| [ricoboost wallet-cluster bot](https://github.com/ricoboost/meme-coin-trading-bot)（失败反例） | [策略原理与失败复盘](https://github.com/ricoboost/meme-coin-trading-bot/blob/main/docs/STRATEGY.md)：多个钱包群体信号→分时成交/风控→实盘；作者坦言历史有效、实际亏损 | 多钱包聚合买入不等于策略优势；拥挤、滑点、幸存者偏差、优先费和退出是同一业务链问题 | 作者回顾不能直接推导任何普遍成功率或单一失败因果 |

**共同的业务链不是四份模块清单**：发现事件 → 判断独立性/交易风格 → 确定信号是否已过时及可成交 → 用合适仓位和退出方式记账 → 记录执行与拒绝原因 → 与后续事实比较。各项目着力点不同，不必全数融合。

## 2｜高价值源码发现一：Million 的“独立性”与“同控”不是一回事

### A. 具体实现（已核对）

[owners.service.ts](https://github.com/Kelows/million/blob/main/apps/api/src/analysis/owners.service.ts) 定义：
- 资金边来自本地历史 SOL 转账汇总，最小累计 `FUNDING_MIN_SOL=1`；Fee Payer `share >=0.15` 可形成边；共同进入两个及以上 Mint 且 Jaccard ≥0.25 可记录 `coentry` 线索。
- 聚类使用 union-find，但显式**跳过 `coentry` 的合并**。注释提到共同买币曾令 182 钱包被误归到一个 owner 组。
- 节点度数 `>6` 被作为 Hub 排除条件；`ownerId` 全量重建且不稳定。资金边和 Fee Payer 边仍会参与合并；这些关系本身不是共同经济控制的证明。
- [consensus.service.ts](https://github.com/Kelows/million/blob/main/apps/api/src/analysis/consensus.service.ts) 按 ownerId 对持仓共识去重。[opportunities.service.ts](https://github.com/Kelows/million/blob/main/apps/api/src/opportunities/opportunities.service.ts) 的实时报价信号用 Copy/Consensus/Ladder 三种不同触发语义，且对群体信号检查买卖净流。

### B. 从源级逻辑产生的两个边界反例

**反例 1｜资金 Hub 阈值导致“不连续”的群体结果**：只按现有规则简化推算（不运行 Million 进程），F 分别给5个钱包提供符合阈值的资金 → F 度数5，5个钱包可因 F 被聚到同组；F 给7个钱包提供资金 → F 度数7，相关 funding 边不参与合并。5与7只差两条边，却可能改变“是不是一个独立信号源”的判断。资金提供者也可能是服务/交易所节点，因此**两种归属都不可当作确定身份**。

**反例 2｜用于说明关联的 `coentry` 也计入 Hub 度数**：代码先对**全部**存储边计算 degree，再排除 coentry 做 union。简化示例：F 有5条 funding 与2条 coentry，度数变为7，资金边也被 Hub 条件拒绝；若只计用于聚类的 funding 边则结论可能不同。**这是根据静态源码的边界条件推断，不代表作者当前生产数据已发生该错判。**

**实际启发**：不能直接把 Million 的 `ownerId` 当成 Gendan 的真同控标签。更稳妥的研究对象是三种不同计数：原始地址数、有关联证据但未定同控的候选群组数、在采用某一明确归并政策后得到的有效信号数；将三者差异用于风险提示和后续反证。当前 Gendan [engine.py](../gendan/engine.py) 已把共享出资与同槽买入作为候选而不确定归因，**不是没有底层研究**；但尚未将此用于独立信号的前向评价。

### C. 信号时间边界需独立验收

[opportunities.service.ts 的 tryConsensus](https://github.com/Kelows/million/blob/main/apps/api/src/opportunities/opportunities.service.ts) 查询 `liveEvent` 时仅按 Mint 与 Buy/Sell 过滤，**该函数未显式按时间截断**。但 [live-feed.service.ts](https://github.com/Kelows/million/blob/main/apps/api/src/live/live-feed.service.ts) 会每5分钟清理超过15分钟的事件，因此不能简单宣称“永远把全部历史算作共识”。

真正需要核对的是：**产品希望的“同一时间窗”是否就是约15分钟的数据库保留窗？** 在定期清理前，统计是否受到尚未清掉的旧事件影响？没有任何 owner/time 比较是否会误解释为短期同步共识？这属于 `STATIC_SOURCE_RISK / NOT_RUNTIME_REPRODUCED`，不能直接报已确认线上 Bug。

## 3｜高价值源码发现二：ScreenerBot 更强调“执行语义与仓位归属”

- [src/trader/copy/mod.rs](https://github.com/farfary/ScreenerBot/blob/main/src/trader/copy/mod.rs) 将 entries、exits、sizing、paper execution、guards、risk、analytics 等拆开；研究重点不是目录结构，而是**所有模块都围绕同一 Copy Task 的仓位和实际决策状态**。
- [paper_execution.rs](https://github.com/farfary/ScreenerBot/blob/main/src/trader/copy/paper_execution.rs) 对**每个任务**以有界队列和 FIFO 保持操作顺序，用 `activity:{signature}` 防止同一任务重复排队，并记录队列拥挤/不可用。不能由此推出跨任务同Mint一定不存在相互影响。
- [analytics.rs](https://github.com/farfary/ScreenerBot/blob/main/src/trader/copy/analytics.rs) 区分已验证 live 退出、paper 退出与无法报价的 paper 开仓；回填事件不计入正常到达延迟分布；`arrival_distance_ms` 用 `detected_at` 毫秒减去 `target_block_time` 秒级时间，属于**相对区块时间的到达距离**，不是毫秒精度的链上成交→可执行报价全链路延迟。
- [guards.rs](https://github.com/farfary/ScreenerBot/blob/main/src/trader/copy/guards.rs) 因恢复了旧存储、钱包监控源断开、长期延迟等条件暂停任务，并记录原因。特别是“监控已断开却假装任务正在运行”是产品操作层真实需要防止的情况。
- [AI copy task tools](https://github.com/farfary/ScreenerBot/blob/main/src/agent_control/tools/copy_trading.rs) 明确区分只读状态查看与变更任务的接口；创建任务始于 Paper，但其工具属于 `mutating` 和 `requires_confirmation`；**不能把整套 Agent 工具误认为只读**。

**实际启发**：Gendan 若要评价“某种钱包行为是否可以跟”，除了钱包类型，还要明确策略仓位的拥有者、任务、旧仓、重复信号、信号回填、暂停与恢复，以及不同软件 TP/SL/跟卖语义。否则即使资金调查很专业，也无法判断真正跟随会发生什么。

## 4｜第三个组合：AI 能否减少操作负担，而不是制造错误配置？

- [Million MCP 说明](https://github.com/Kelows/million/blob/main/packages/million-mcp/README.md) 公开 `why_not_bought`、`get_decisions`、`get_rules`、`get_flows`、`analyze_wallet` 等能力，同时也有 `update_rules`、`import_wallets`、`set_wallet_subscription` **可改变运行状态的工具**。无法启用 live ≠ 所有操作都是 read-only。
- dexterm 的只读分析接口与 paper 执行通道分离，作者公开说明 Agent 生成的策略并没有证明稳定优势。更成熟的目标是“用户简单问一句，AI 能解释已有规则、漏报/拒绝原因、当前风险及其他可选择的方案”，而不是直接授权 AI 持续改变实盘交易设置。
- 与 [ai-d](https://github.com/sunshihao001/ai-d) 的真正联系：专业意图理解应决定查哪种业务证据，AI 的可信度应由**是否减少误判、漏项和重复指挥**评价，而不是角色数量、长提示词或生成策略数量。

## 5｜把四套参考放回本项目：哪些已经有，哪些不能假装有？

| 所需能力 | Gendan/Blix 目前可复用 | 真正缺的条件 | 当前最省事的方向 |
| --- | --- | --- | --- |
| Token/资金边、同槽/转仓候选 | Gendan [离线引擎](../gendan/engine.py)及其 [测试](../tests/test_engine.py)；Blix 单Mint和钱包研究；PR#21候选工程 | 可核对真实签名、owner/覆盖时段、在指定Mint同样时间窗的连续事件 | 先消费/复用现有只读能力，而非重写第二个解析器 |
| 有效独立钱包共识 | Gendan已有共享来源和同槽候选，但没有统一的有效独立信号统计 | 定义时间窗、Hub来源、归并证据、同交易重复、卖出资金/Token方向及错误归因反例 | 用已有事件先做**“原始钱包数 vs 关联候选数 vs 证据允许的独立信号数”**对照，未知保留区间 |
| 跟随者实际操作/策略模拟 | Mark/Froggy实操字幕、Gendan 策略冲突理论与合成反例 | T_chain/T_seen/T_quote、任务仓位、费率、失败/无报价、卖出处理、仓位恢复 | 先研究 ScreenerBot 等成熟 paper 设计，不复制其受限源码或启动 live |
| AI 查询/解释 | ai-d 认知研究、Blix已有部分研究型源程序、Million/dexterm 现成工具思想 | 数据接口可靠性、权限隔离、结果真实性、是否确实减少操作 | 先评估用只读报告输出让 AI 解释，而非新造综合平台 |

授权内当前没有进行任何真实买卖、签名、RPC 直播监控或第三方服务部署。Blix 的 PR #21 等未合并工程仍须按分支和测试状态独立核验。

## 6｜从这轮对照得出的新专业判断

**判断 A｜独立性×共识最可能产生信息增量。** 单看“3钱包同时买”容易高估信号，单看“共享资金源”容易误归因。组合后可给出：原始地址数、是否重复计票、买卖净流、无法归属的上下界与是否应只作为观察。无需对未证实同控作肯定判断。

**判断 B｜跟单可复制性×真实退出管理最可能产生操作增量。** 仅有历史钱包排名无法回答用户可否获利；仅有软件参数也不知是否适合源钱包。组合后可以研究“某钱包的哪类可见动作适合哪一种退出方式”，计入失败与费用，才能对比纸上净结果。

**判断 C｜AI×工具只是实现手段，且权限设计是必要条件。** 应优先测试自然语言是否正确调用成熟只读信息、是否识别参数冲突，不因会调用 MCP 就称具备自主盈利能力。

**选择建议（可撤销）**：先以判断 A 做一次最小**离线信号独立性反例和证据边界核查**；它直接用得上本仓引擎，成本低、可先识别认知增量。随后沿 B 进入真实观察/纸上验证。若用户下一条明确指向某个软件参数、钱包或完整目标规划，则转向该意图，不强制从 A 开始。

## 7｜下一轮的单项验收，而不是扩建新体系

**候选实验 A（优先）**：
- 数据：可先用 Gendan 现有合成案例的共享 Funder、同 Slot、接收卖出事件，不虚构为真实链上；以后换真实签名。
- 基线：只按地址数量把同一时间窗买入视为 N 个信号。
- 组合：将明确同签名重复、疑似同源/同工具、Hub 与独立性未知作为**不同证据状态**保留。输出“确认独立数量的下界/未排除重复的上界”，不将共享 Funder 自动压成一人。
- 检查：同样事件能否改变“3地址支持”这一表述，并明确新信息来自哪条边；反例包括公共 Hub 与共同买入但没有共同控制证据。
- **通过标准**：输出一份具体可查的基线对照与准确的不确定性说明，并且不误把同槽当真实 Jito Bundle。**不是要求任何交易回报提高。**

**候选实验 B（其后按条件选择）**：
- 对一个已经选定的交易子集，冻结源事件、观察时点、报价与成交假设；比较完全跟卖、独立退出和只提醒，分开记录被跳过/未成交及多策略同Mint冲突。
- 数据不足时只给出何种信息缺失，不能用历史最优价补全；若没有真实 T_seen 就不声称验证前向可复制性。

### 风险锚点与停止条件

- 如果研究只是发现更多标签、参数或新文件，未改变任何解释/工具选择/可验证问题，则停止扩写。
- 如果“有效独立信号数”无法从现有资料限定，先改善数据或只说 UNKNOWN，不为了推出数值强行归因。
- 如果某现成工具已经实现相同能力且能可靠读写必要数据，不另开发。
- 如果 AI 新方案的效果不比简单基线明显改善，保留已有成熟工作方式，不因“更高级”而升级架构。

**本轮状态**：GitHub 源码/原始文档核查 + 简化阈值逻辑离线计算；**没有** Million/ScreenerBot/dexterm 在本机的全套运行、真实链上归因或前向跟单收益实验。新增的“源码风险”尚需作者最新改动/测试及实际数据进一步证实。
