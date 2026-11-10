# Blix × Gendan × ai-d｜同一市场、不同决策：知识与能力对照审计 V0.1

> 核查日：2026-11-10。核查范围：`sunshihao001/grok@blix` 现存产品源码与审计文档、其未合并的 PR #16/#21、`sunshihao001/gendan@main` 的俄语跟单方法和实战规划、`sunshihao001/ai-d@main` 的研究知识入口。**目标不是再造总框架，而是纠正重复建设，把已经存在的东西用于一件真实跟单调查任务。**
>
> 证据范围：本轮直接读取 GitHub 文件、分支树、测试源码和 PR 状态；部分真实市场结果源于 Blix 此前对三份供应商原始归档的核验报告，本轮没有重新下载其 ZIP 或 RPC 原始逐笔交易。静态源码 ≠ 实际产品已运行；离线测试存在 ≠ 本轮运行通过；供应商快照重算 ≠ 真实钱包归因。

## 1｜共同底层问题和两个不同的终点

**Blix：** 市场发生了什么——发行、流动性、交易、钱包、Token/资金关系、库存、价格与群体演化；形成可追溯的市场事实与竞争解释。

**Gendan：** 在同一市场事实基础上，哪些地址和行为值得观察、哪些适合事前冻结纸上跟随、哪些是不能复制的首槽/网络库存/共用策略冲突；形成针对跟随者的行为选择、时效与独立收益验收。

**ai-d：** 为不同的实际问题自主选择相关知识与来源，独立研究后识别关键未知、实施、验收和纠错；并不直接提供 Solana 链上事实，也不替代两项业务程序。

因而三者的依赖是“共享事实层，区分业务判断，研究方法按问题调用”，不是 Blix 做完才能开 Gendan，也不是把两套 repo 合并/把 Blix 当跟单执行引擎。

## 2｜跨项目能力矩阵：已知事实、可继承机制与真正新增对象

| 市场/数据对象 | Blix 现有产品或源级依据 | Gendan 可直接继承（不重复建设） | Gendan 独有的追加问题 | 当前可证状态 |
| --- | --- | --- | --- | --- |
| **市场发现和发行阶段** | Blix Discover/Pulse、`server/engine.js`、`sources.js`、`pulse.js`；旧 Hermes 生命周期与 meme- 阶段知识 | Mint、发行/迁移、主要池、候选出现时间、噪声来源 | 钱包发出的信号是否在普通观察者可见后仍有交易窗口？Froggy 候选是否只来自历史成功币？ | 产品源码已存在；Gendan 首次发现时点 **NOT_RUN** |
| **单 Mint 市场/流动性** | `/api/coin/:mint`、`/api/token/:mint`、`coin.js`、`holders*.js`、DEX供应商历史快照 | 价格/池深/库存、多个池和币龄、原始提供方时点 | 同一信号在不同池、延迟和下单规模下是否可复制？ | Blix 有真实供应商快照案例；未核实时点的可执行报价 |
| **Holder/Owner/池基础设施** | `coin.js`、`holders.js`、`bubblemap.js`；`mint-cross-module-evidence-audit-v0.2.md`记录不同分母/历史口径 | Token Account ≠ owner ≠ pool/LP；不把公共池地址当私人鲸鱼 | 该“高持仓/大户”是否应从可跟钱包候选中排除或改为风险观察？ | 真实快照中的池相关 Holder 匹配；原始链上账户独立查询未做 |
| **资金/钱包群体关系** | `wallets.js`、`wtrack.js`、`bubblemap.js`；旧 Hermes/qb-多跳与经济角色；PR #21经济边接口候选 | 资金边、Token 转账、共同出资候选、接收者、时间与覆盖；保持共享服务竞争解释 | A 买入后将 Token 给 B、B 卖出时，复制 A 的买卖会漏掉什么？同一网络中谁更值得 WATCH？ | 知识/源码已有；PR #21 **仅离线测试/未合并未实跑** |
| **交易事件/钱包历史** | `server/wallets.js`、`wtrack.js`、`journal.js`；PR #21签名持久化与经济事件保存 | 保留 signature/slot/余额变更、区分 swap/transfer、补查缺口 | 目标交易发生 T_chain、供应商/使用者看到 T_seen、可报价 T_quote 不同；错过机会怎么办？ | 多路径源码；连续完整历史和真·首次看到时间未验收 |
| **Creator/Dev/KOL 关联** | `coin.js`、`devboard.js`、`dev-identity.js`；历史 Creator/利益研究 | 发行方、营销方与资金/库存的证据候选、反例 | 地址是否更多承担引流、组织行为、库存派发或风险提示，而非可复制正常买入？ | 源码/知识有，实际当前 Mint 关系未知 |
| **市场经济机制** | `knowledge/mechanisms/`：资本组织、价格/库存、钱包角色、执行经济与市场阶段 | 让同槽、涨价、转币、薄池、大额买入有多种可解释机制，不以“庄家”贴标签 | 哪一种解释**会改变 WATCH / PAPER-TEST / SKIP**？没有决策增量就不做长研究 | 研究型继承，非策略实证 |
| **策略/收益与风险** | Blix `triage.js`、`research.js`、`brain.js` 的市场研究/复盘；旧 meme- 反证实验设计 | 报告和数据检查、失败形态、样本外对照原则 | **独有**：按钱包冻结交易子集，处理重复 Mint / 多镜像共享仓位，入出价格/滑点/费用、信号过期、源盈利≠跟随盈利 | Gendan 俄语研究 001–003 与离线合成反例，真实纸上前向 **NOT_RUN** |
| **AI 工作方式** | ai-d `knowledge/INDEX.md`、`research/2026-11-07-problem-driven-unknown-discovery.md` | 一句话意图→选择问题→找证据→消除未知→验收→修订，不复制整个专家制度 | 自主发现“这个钱包的哪一部分动作可能有独立参考价值”，并向现成软件请求证据 | 方法阅读；工具联动任务尚未实测 |

### 不能直接复制/搬迁的东西

- **不用复制 Blix 全套终端和真实交易模块**：这会使 Gendan 从专属研究与策略验证变成重复市场/交易系统。
- **不用把 PR #21 当已部署接口**：新增`/api/evidence/...`只能在对应特性分支和适当权限/部署下成立。
- **不用把 ai-d 全量知识常驻每次跟单提示词**：它提供专业方法选择，不提供当前 Slot、真实余额或钱包身份事实。
- **不能以 Blix 某个源头指标直接代入跟单决策**：例如市场价格上涨是事实线索，源钱包有及时可复制优势则需要观察者时间、可执行报价和完整退出策略。

## 3｜这轮核实的工程资产：不是“只有理论”

### Blix 本分支的现成能力（源码已核对）

`grok@blix` 的 `docs/project/whole-product-cross-layer-audit-v0.1.md`与现成源码确认：

- 市场/生命周期 UI：Discover、Pulse、Coin；
- 币的多源详情：`/api/token/:mint`、`/api/coin/:mint`、`/api/holders/:mint`、`/api/bubblemap?mint=...`；各自数据时间、Holder 分母和历史覆盖不同；
- 钱包观察：`/api/wallets`、`/api/wallet/:addr`、`/api/wtrack`；`wallet_trades`、`wt_feed`、`wt_transfers`不是同一“完整交易流”；
- AI研究和跟踪：`triage.js`、`research.js`、`brain.js`、`wtrack.js`；不能把页面存在当作当前 fork 实际 24h 部署已验收。

**重要缺陷候选**：旧静态审计指出多个本地 API 的 Token/Holder 来源、时间和分母不一致，最早资金方可被历史截断错误判不存在；在重合真实项目中一定要保留 `HISTORY_TRUNCATED`、`PROVIDER_FAILURE`、`UNKNOWN`，不直接做跨模块“钱包同控概率”。

### Blix PR #16：有过真实供应商请求，不是完整链上运行

PR https://github.com/sunshihao001/grok/pull/16 当前为 **OPEN DRAFT，未合并**。旧真实 GitHub Actions曾查询 Mint `EYqygbhZjP7EbM4fSn8devctnksAvPAD1Bt57XBFpump`，DEX Screener 返回5个池记录，RugCheck缓存报告20个Top Holder Token Account候选；这是供应商响应证据，不等于20个互不关联私人钱包或完整上链归因。

### Blix PR #21：这才是 Gendan 当前最值得**参考而非重造**的工程候选

https://github.com/sunshihao001/grok/pull/21 当前为 **OPEN DRAFT，未合并，base=`fix/blix-evidence-v02-20261108`，不在`blix`分支**；特性分支`feat/blix-wallet-signature-continuity-20261108`。

本轮重新读取：
- `server/economic-events.mjs`：按签名保存完整 `getTransaction(jsonParsed)` 原始 RPC、原始哈希、指令索引，区分部分已获取与完整历史；
- `server/wallet-signature-coverage.mjs`：持续记录签名发现/RPC捕获/Reader完成、崩溃恢复、时间窗口截断、人工补查状态；
- `test/wallet-signature-coverage.test.mjs`：静态可见覆盖原子水位推进、重启前丢队列、后续正常扫描不抹掉历史缺口、同签名多钱包不同状态；
- `test/wallet-evidence-chain.test.mjs`：离线夹具下从钱包读取到Token转账候选、接收方本地卖出摘要、另一 Mint 时间候选，并明确**不能据此推出转入筹码是卖出筹码，也不能推出共同控制者**；
- `docs/project/economic-evidence-v0.1.md`：特性分支提出只读`/api/evidence/tx/:signature`、`/api/evidence/recipients/:wallet`、`/api/evidence/recipient-outcomes/:wallet`、`/api/evidence/cross-mint/:wallet`等 owner-only 本地接口；它们不主动订阅新接收钱包/不自动主网补查。

这些是**特性分支源码与离线测试定义已经存在**，文档记录 `OFFLINE_CI_CHECKED_PARTIAL`。本轮只读取测试源码，不运行 Node 测试、真实RPC、完整 Blix 主服务或服务器接口。未来先核验只读安全隔离、真正的测试结果及可达的本地/远程权限，然后再决定 Gendan 是否能调用现成结果；未授权时绝不调用交易/账户 API。

## 4｜把“共同知识”落实到一个真实 Mint 的同一份证据

[共享真实案例 001](../research/SHARED-CASE-001-BLIX-TO-GENDAN.md) 采用 **Blix 已独立重读过三份供应商在线归档**的 Mint，保留快照来源、绝对 UTC 时点、池和 Holder 地址、原数据含义、证据限度。

**Blix 的事实与机制问题**：约42分钟内主要池出现价格和两侧库存方向切换；RugCheck头部 Holder 的 Owner 与主要 PumpSwap 池完全匹配，说明把它解释为独立私人鲸鱼很可能是错误。

**Gendan 的具体判断变化**：把“Holder Top 1/约5.9%→可以跟的巨鲸”降级为 **POOL_INFRASTRUCTURE_CANDIDATE / SKIP_AS_COPY_TARGET**（该账户作为跟单钱包候选时），但仍作为市场库存观察对象；同段价格、流动性与池差异只能触发 **WATCH**，不能在没有具体钱包签名、信号首次可见时间、可执行报价与退出的情况下升级 **PAPER-TEST**。

这是真实来源上的“跨业务决策转化”，**不是“已找到这个币能盈利的地址”**，也不是已完成“买入→转新钱包→卖出→跨Mint”签名级闭环。

## 5｜怎样长期复用，而不把三个项目绑死

**单个事实不重复维护。** Gendan 的每个专业结论引用 `grok@blix` 中已有源文件、具体分支/PR及快照。若真需要机器可读输出，才定义最小只读字段适配，避免复制 Blix 数据库/知识体系。

**不同的知识结论应各放回适合的位置**：
- 新发现是 Token Account/Owner、流动性、钱包关系或采样规则 → 向 Blix 原知识位置建议修订；
- 新发现是信号延迟、钱包动作子集、策略冲突、跟随者账本 → 由 Gendan 原位维护；
- 新发现是“AI 如何更好决定查询哪条证据、什么时候停止” → ai-d 研究方法候选；
- 新发现是一个具体时间/钱包/交易签名 → 保存在可检查的案例与原始证据，不在三个仓库各复制一份。

**工作授权边界**：本次只实际修改 `gendan` 仓库；不擅改 `grok` 和 `ai-d`。

## 6｜下一项真正值得投入的工作

**P0 不再重复理论对照**：对上述 Mint 的实际一个 PumpSwap 池，取得可重查的 swap/LP 原始签名与资产净变化；或从已公开的钱包地址取得签名并确定其真实 Mint。然后让同一交易事实同时回答：

1. Blix：这是池交易、LP 调整、Token Transfer 还是某钱包的真实买卖？它与已有 Holder、Pool、Wallet 口径是否一致？
2. Gendan：相关地址是 WATCH、SKIP、UNKNOWN 还是 PAPER-TEST 候选？首次可见时有没有真实报价？若没有就仍是 WATCH/UNKNOWN。
3. ai-d：新证据对原先哪些判断产生反证？下一项最高信息价值的查验是什么？

若链上原始签名仍不可得，优先改变实际数据/成熟工具入口，不再增加抽象专家或第二套市场资料库。

## 冻结的来源入口

- Blix 能力审计：[baseline](https://github.com/sunshihao001/grok/blob/blix/docs/project/blix-heritage-capability-baseline-v0.1.md) / [cross-layer](https://github.com/sunshihao001/grok/blob/blix/docs/project/whole-product-cross-layer-audit-v0.1.md) / [Mint cross-module](https://github.com/sunshihao001/grok/blob/blix/docs/project/mint-cross-module-evidence-audit-v0.2.md)
- Blix 多跳钱包研究：[cross-project](https://github.com/sunshihao001/grok/blob/blix/knowledge/references/wallet-relations-cross-project-knowledge-20261106.md) / [multihop](https://github.com/sunshihao001/grok/blob/blix/knowledge/references/multihop-funding-evidence-audit.md)
- Blix 真实 Mint 档案：[single-mint](https://github.com/sunshihao001/grok/blob/blix/docs/project/single-mint-audit.md)
- PR #16：https://github.com/sunshihao001/grok/pull/16
- PR #21：https://github.com/sunshihao001/grok/pull/21
- PR #21 证据方案：https://github.com/sunshihao001/grok/blob/feat/blix-wallet-signature-continuity-20261108/docs/project/economic-evidence-v0.1.md
- PR #21 离线链条测试：https://github.com/sunshihao001/grok/blob/feat/blix-wallet-signature-continuity-20261108/test/wallet-evidence-chain.test.mjs
- ai-d：[knowledge index](https://github.com/sunshihao001/ai-d/blob/main/knowledge/INDEX.md) / [unknown discovery](https://github.com/sunshihao001/ai-d/blob/main/research/2026-11-07-problem-driven-unknown-discovery.md)
- Gendan 既有研究：[RU-003](../research/RU-003-deep-study.md) / [construction routes](CONSTRUCTION-ROUTES.md)
