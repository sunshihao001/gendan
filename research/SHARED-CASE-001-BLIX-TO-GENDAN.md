# 共享真实案例 001｜Blix 的实际 Mint 快照怎样改变 Gendan 的钱包筛选判断

**对象 Mint**：`EYqygbhZjP7EbM4fSn8devctnksAvPAD1Bt57XBFpump`

**事实来源**：[Blix `docs/project/single-mint-audit.md` 真实三次归档重读](https://github.com/sunshihao001/grok/blob/blix/docs/project/single-mint-audit.md)（2026-11-07 原始研究记录）。其曾独立下载旧 GitHub Actions 的 DEX Screener 与 RugCheck 原始 JSON、记录 SHA256，并重算三时点差异。**本轮做的是从已归档报告到跟单判断的转换，没有重新下载 ZIP、执行主网 getTransaction 或独立复验原始池余额**。所以事实等级 **ARCHIVED_VENDOR_SNAPSHOTS_PREVIOUSLY_AUDITED**，绝非 `ONCHAIN_SIGNATURE_VERIFIED` 或实盘/纸上跟单收益。

## A｜冻结来源与时间，避免历史冒充未来可见信号

| 来源归档 | 2026-11-01 UTC采集时间 | 数据种类 | 文件/溯源 |
| --- | --- | --- | --- |
| [GitHub Actions run #41266389009](https://github.com/sunshihao001/grok/actions/runs/41266389009) | 02:44:23.396 | DEX Screener 原始快照 | Blix 原研究记 SHA256 `240dca2d3df8cfbf9e0f09d806d61b2ae6040abc07bcebc4b9dd3e07f3d09897` |
| [GitHub Actions run #41268982018](https://github.com/sunshihao001/grok/actions/runs/41268982018) | 03:23:31.969 | DEX Screener + RugCheck 原始快照 | Blix 已登记各原始 JSON SHA256；本轮未重取 |
| [GitHub Actions run #41269179918](https://github.com/sunshihao001/grok/actions/runs/41269179918) | 03:26:30.596 | DEX Screener + RugCheck 原始快照 | Blix 已登记各原始 JSON SHA256；本轮未重取 |

这些时间是**数据实际采集时间**，不是“一个跟单使用者 2026-11-01 当时首次看见钱包交易”的证据。Actions Artifact 可能过期，不能把链接长期可用视为已验收。

池：`81jgrpTMsQWc1rGWXutyYWW27ruiAtehUZwLydcHHWDB`（主要 PumpSwap 池，供应商匹配）；对应 quote mint 为 `So11111111111111111111111111111111111111112`。由供应商给出的 `pairCreatedAt` 为 2026-10-30 20:50:08 UTC，**不能当作原始链上 Mint 首次发行时间的独立证明**。

## B｜三份真实快照的共享市场事实

| PumpSwap 主要池/DEX供应商字段 | 02:44:23 | 03:23:31 | 03:26:30 |
| --- | ---: | ---: | ---: |
| USD价格 | 0.0008148 | 0.0007653 | 0.0007819 |
| 池内目标 Token 数 | 57,331,535 | 58,774,685 | 58,374,413 |
| 池内 SOL 数 | 465.47 | 457.4104 | 461.07165 |
| USD流动性 | 91,059.46 | 88,618.50 | 89,627.83 |

在 02:44 → 03:23 期间，价格约 **-6.075%**、池内 Token **+1,443,150**、SOL **-8.0596**；03:23 → 03:26 价格约 **+2.169%**，池内 Token **-400,272**、SOL **+3.66125**。这是供应商跨时点池状态变化的事实摘要，**不能自动反推交易者、净卖单金额、控制者**：LP 增减、费用及不同采样时间都可能影响快照。

同时返回的其他配对中，Orca 旁池美元流动性约 **47–48 美元**，主池约 **8.86–9.11 万美元**；“5个交易对”并不意味着5个同等有深度的可执行市场。旁池标注价差也不能自动计为可实现套利。

## C｜最重要的源级关联：看似约6%的头部 Holder 是谁

Blix 原报告的 RugCheck 快照记录：

- 头部 Token Account：`BYonfuCMtQL9rLeYLhLar7Jon87Nwj7PyurLFj6sNx3i`。
- 该 Token Account 的 **Owner**：`81jgrpTMsQWc1rGWXutyYWW27ruiAtehUZwLydcHHWDB`，与 DEX Screener 给出的主要 PumpSwap 池地址精确一致。
- 03:23 RugCheck top holder 余额约 58,487,680 Token，占供应商报告 **5.877731%**；03:26 报约 59,418,764、**5.971300%**。
- RugCheck `knownAccounts` 标为 `AMM/Pump Fun AMM`；`markets[0].liquidityAAccount.owner`亦与该池 Owner 匹配。

**Blix 市场解释**：这组相互独立的供应商字段强烈支持“头部持仓是池/基础设施相关候选”，不应仅凭 Top Holder 排名叫它“私人鲸鱼”或“聪明钱”。不同服务在不同时间报告的 Token 数不能直接相减，称为一个人3分钟内大量卖出或转币。

**Gendan 跟单判断改变**：
- 若工具把 Token Account 或池 Owner 当作“排名第一巨鲸地址”，**不把它列为可复制的独立交易者**；`SKIP_AS_COPY_WALLET`、`POOL_INFRASTRUCTURE_CANDIDATE`。
- 但该池本身可以作为**库存与流动性观察对象**：`WATCH_POOL`，关注实际资产变化和可能的成交/LP活动。
- 不因此排除市场中所有真实交易钱包，也不推出 Creator 和池同控；其他未辨识的前19个 Holder 候选仍 UNKNOWN，不能自动当19位不同经济主体。
- 一笔真实买入钱包的价值判断需要它自己的 Swap 签名、Mint、事件时间、其真实 owner、交易成本和跟随者首次可见时价。**本案例没有这些关键字段**，因此不能升级 `PAPER_TESTABLE`。

这不是纯粹名词映射：**如果只看 Holder 排行，我们可能把一个实际池相关账号当成跟单“高手”；调用 Blix 的 Owner/Pool 知识后，该候选立即降级，减少误选。** 这就是共同知识在另一业务内的可检验用途。

## D｜同一来源，两个项目应该作不同决策

| 原始事实/来源 | Blix：市场调查下一步 | Gendan：跟单实战下一步 | 当前不允许宣称 |
| --- | --- | --- | --- |
| 价格/Token/SOL库存有反向变化 | 追究 swap/LP/费用对变化的贡献，确认发行阶段和多池 | 市场环境进入 WATCH，判断该波动是否来自可及时观察的钱包行为 | 已确认有人组织性出货、已经产生可复制买点 |
| RugCheck Holder Owner 对上主 PumpSwap 池 | 在 Holder/分母和 bubble map 中隔离池相关基础设施 | 剔除该地址的“个人巨鲸可跟”资格；保留池作背景 | “第一大 Holder 是庄家”、其它地址同控 |
| 旁池流动性极薄 | 明确主要可交易池和非同步报价/LP状态 | 不拿旁池标价虚构跟随者应买卖的可执行价格 | 同一 Slot 可按该差价获利 |
| Provider 快照存在不同步和缺口 | 保存 source/time/coverage，进一步查原始 RPC 签名 | 禁止把 11/01 历史快照当成 T_seen 新信号；无未来观察记 UNKNOWN | 现在跟单这枚 Mint 是好策略 |
| PR #21 有接收者/跨Mint本地候选接口 | 先核验只读门禁、完整证据保留及 CI/真实数据 | 未来**可考虑直接消费已验收结果**，无需重写多跳钱包调查器 | 这些接口已在 `blix` main 产品中运行、已证实转入库存随后售出 |

## E｜本次“实战连接”达到哪里，下一步缺哪一条证据

**已经交付（可追溯研究成果）**：单一真实 Mint 的三份供应商快照历史、池/头部 Holder 关联、同一事实到 Blix/Gendan **两个不同业务判断**的显式转换，以及应排除的跟单候选类型。

**没有交付**：真实观察者 T_seen、真实钱包买卖签名、资金路径 A→B→卖出、可执行后续报价、前向纸上跟单结果、真实盈亏。

**能推翻当前判断的证据**：同 Slot 原始 Token Account owner/池程序身份与供应商记录不一致，可能要求撤销“池相关 Holder”归类；真实池库存变化主要由 LP/费用而非卖出导致，则应撤销“卖压”方向候选；某个独立真实钱包的可复制优势若有未来冻结后的信号/可执行报价，应单独评估，不能由本例一概拒绝。

**唯一优先补查**：在该 Mint 主要池 2026-11-01 02:44–03:26 UTC 之间，获取至少一笔可验证的原始 Swap 或 LP 交易签名，确认事件方向、实际交易者和 Token/WSOL 余额变化。之后才连接到钱包选择/跟单可复制性；若无法获得，继续用 GMGN/OKX/浏览器仅作可核实的市场观察，不虚构结果。

## 来源原位维护

- 市场事实/旧经济机制：Blix 仍为主：[单 Mint 原审计](https://github.com/sunshihao001/grok/blob/blix/docs/project/single-mint-audit.md)。
- 跟单业务判断和这次交接结果：Gendan 本文件。
- AI 过程改进（如果未来有真正不同的效率结果）：才考虑向 ai-d 报告，不把每次市场结论都写回 ai-d。
