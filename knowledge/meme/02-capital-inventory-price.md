# 02｜资产、交易、库存、定价与财富变现：一条完整经济链

> 本文把旧 D01/D03/D04/D05/D06/D09 连接成「真实事件 → 经济账本 → 市场约束」，不是单钱包跟单教程。

## 首先正确读懂 Solana 的事实

- **Mint**：某类 Token 的身份与供给/权限等信息，不能直接当作普通交易钱包。
- **Token Account**：针对一个 Mint 存储某 owner 的 Token 数量；一个 owner 可拥有多个同 Mint 的 Token Account，ATA 是按 owner / Mint / Token Program 派生的默认账户。
- **token owner / program owner / signer / fee payer / delegate / PDA**：授权与程序关系不同，不保证与最后的经济受益人相同。
- **交易签名与指令树**：一个 transaction 可含多个顶层及 CPI 指令；一次 swap 可能含 wrap/unwrap、跨池、账户创建、费用等多个资产移动。不能把每一条 transfer 都记为一次独立买卖。
- **交易版本和查询覆盖**：legacy/v0、地址查找表、扩展以及版本变化要以实际 parser 支持为准；不支持时是 INCOMPLETE，不是没交易。

原始协议入口：https://solana.com/docs/tokens 、https://solana.com/docs/tokens/basics/create-token-account 。

## 四类行为不能合并

| 行为 | 直接改变什么 | 后续分析重点 |
| --- | --- | --- |
| Transfer | 指定账户资产位置 | owner 是否相同、是否支付链下对价、资金去向 |
| Swap | 至少两种资产之间的市场交换 | 净资产变化、池/报价资产、费用、价格冲击 |
| Mint/Burn | 供应量 | 有效供给、授权与可交易性 |
| LP add/remove | 池储备及 LP 权利 | 深度、库存权利、退出容量、费收 |

例如：Token 从 A 转到 B，通常没有公开可证的 Token 买入对价；B 随后卖给池，才是可确认的市场出售候选。若 A/B 同属一名受益人，也不能仅靠 Token 转移证明；如果没有完整经济主体归因，不能把 B 的出金计作 A 的已实现利润。

## 资产守恒与「双重记账」风险

研究某个 owner 的 Token 库存，概念上分解为：

\`Δ Token_owner = swap 净买入 + 外部转入 − 外部转出 + mint 分配 − burn + 协议调整\`

同 owner 内 Token Account A→B 转移在合并后的 owner 库存内应抵消。不同 owner 的 Token 转移在**确定的群体边界内**可能互相抵消，但群体边界本身是待证假设。

同时观察**报价资产**（如 SOL、WSOL、USDC）、手续费、优先费、tips、租金及 LP 权利。原生 SOL↔WSOL 的包装/解绑不等于新增风险资金；同一签名中的多个内部 token 腿不等于多次总成交。

**区分五种数字**：累计成交额、成交笔数、净 Token 风险头寸、池子中的可交换报价储备、独立外部风险资本。彼此相关，但不能互相替代。

## 价格为什么不等于可兑现财富？

设某 AMM 池处于给定储备状态，买入会改变边际报价，卖出也会改变报价。理论常数乘积池可用 \`x·y=k\` 辅助理解价格冲击；**真实场景必须先确认池类型、曲线、手续费、流动性位置、其他池与路由**，不能把所有 Meme 市场当作一个 CPMM。

需要同时区分：
- 最新成交价 / UI 展示价；
- 在特定时刻和数量下能获得的执行报价；
- 整体 Token 持仓的账面市值；
- 将特定库存全部转换成报价资产时的实际/可模拟退出价值。

**重要推论**：薄池小额买入造成的高显示价格，不保证巨额库存能以该价出售。价格上涨可能与新增资本相关，也可能受薄池冲击、LP 调整、跨池差异、聚合器路径和供应量变化影响。

## 资本功能与利益组织

同样的 SOL 流动可以是：
1. 交易本金（承担 Token 价格风险）；
2. 手续费/优先费/执行预算；
3. 托管结算；
4. LP 两资产投入；
5. 收费/返佣及其他服务结算。

「F 给 A 打款，A 买 Token」仅证明可见的资金边和后续行为，不能确定 F 是受益人；如果 F 为公共平台出金地址，其证明力更弱。链上可达多跳也不能保证 SOL 同质资产保持身份连续性。

### 完整经济链的研究模板

\`出资候选 → 执行买入 → Token 持仓 → 分发/转仓 → 接收者实际 swap → 报价资产流出 → 下游资金活动\`

在每一边保留：交易签名、Mint、池、账户和 owner、资产/数量、Slot/时间、来源/是否补查、观测边界、竞争解释。如果在某一边出现公共 Hub/历史缺口，**主动断开过度归因**，不强迫画成闭环。

## 关联至市场循环与群体行为

- 高成交额但群体净库存几乎没变化：可能是套利、短线换手、库存管理或疑似刷量；不足以确认 wash trading。
- 钱包数增加但真实 owner 不增：可能是 ATA/多账户或群体拆分；不是独立需求增加的证据。
- 旧 Holder 不再持币但新地址持续卖出：需还原实际转仓与卖出；不能因旧地址清零就认定全体退出。
- K线在某个历史 AVWAP/POC 位置反应：只是成交价格的统计锚，不能直接得出某个控制者的真实成本或意图。
- 某地址跨 Mint 重用资金：先查是否同一资产风险敞口、是否经过公共设施、是否重新承担市场风险。

进一步研究：
- https://github.com/sunshihao001/grok/blob/blix/knowledge/foundations/solana-chain-and-market.md
- https://github.com/sunshihao001/grok/blob/blix/knowledge/mechanisms/actor-economic-mechanisms-deep-study.md
- https://github.com/sunshihao001/grok/blob/blix/knowledge/references/multihop-funding-evidence-audit.md
- https://github.com/sunshihao001/grok/blob/blix/knowledge/mechanisms/market-price-mechanism-research.md
