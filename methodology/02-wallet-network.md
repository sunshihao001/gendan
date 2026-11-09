# 02｜多钱包关系图谱：行为角色、经济资产和反证

## 图谱不是给每个节点贴「庄家」的照片

目标是重建**资金进入 → 钱包买入 → Token 转仓 → 接收钱包卖出 → 资产可能流向另一 Mint**，同时保留对同一条证据的竞争解释。

### 节点

钱包 owner、Token Account、程序/合约、池/LP vault、交易平台或公共服务地址、Token Mint、交易签名及可确认的组织账号（可选）。不得把 Token Account、其 owner、fee payer、authority 和最终经济主体都合并成一个「钱包」。

### 边（保留方向和时间）

| 边 | 可以断言 | 不可直接断言 |
| --- | --- | --- |
| SOL/WSOL 转移 | 指定时点发生特定资产变化，需区分 wrapping、fees、CPI | 同一出资人最终控制接收方 |
| Token 转移 | Token Account 之间数量转移 | 已按市场价格出售 |
| DEX 买卖 | 经交易解析确认的 swap 与净资产变化 | 任意账户都能同价复制 |
| 同槽/相近时间买入 | 交易具有时间相近性 | 真实 Jito Bundle、共用决策者 |
| 共用资金路径 | 一定观察边界下存在资金可达路径 | 共用 CEX/机器人地址就是关联团队 |
| 跨 Mint 重复参与 | 同一地址多次参与相关代币 | 盈利策略已被证实或存在内幕 |

## 角色不是互斥标签

建议可叠加的研究角色标签：
- FUNDER：候选资金源（标明是否为 CEX/公共节点）。
- EARLY-BUYER / SNIPER：早期买入者（只说明时间/执行位置）。
- SAME-SLOT / BUNDLE-CANDIDATE：同期或可能关联执行候选，真实 Bundle 需另外证明。
- VOLUME-CYCLER：疑似反复成交/刷量模式，需排除做市/套利/多池迁移。
- INVENTORY-HOLDER：持币/可售库存相关地址。
- TOKEN-RECEIVER：收到转仓资产的新钱包。
- SELLER：确实通过交易卖出的角色。
- DEV-RELATED / KOL-RELATED：发行/营销相关关联候选；来源及关联类型必填。
- CROSS-MINT-REUSER：跨 Mint 重复出现的地址/网络节点。
- SERVICE / POOL / CEX：公共服务或流动性设施，通常不应当作私人控制证据。

对每个标签同时保存：**对象、Mint、观测时窗、来源工具、签名、原始资产变化、推断条件、置信边界、反例、有效期和 UNKNOWN**。

## 一条可追问的完整业务链

假设（示例，无真实地址）：
1. F 向 A 提供 SOL；A 在 Mint-X 创建后买入 Token-X。
2. A 将 Token-X 转至新地址 B。此时只能说「转仓」，不能说「卖出」。
3. B 后续在可确认的池子 swap Token-X 换回 SOL/WSOL。此时是 B 的卖出行为，不自动代表 A 的实现盈利。
4. B 把部分 SOL 送到 C；C 后来买入 Mint-Y。此时只能说「存在按时间可达的资金路径」，不能说「同一笔资金唯一地被循环利用」或「同一老板」。
5. 如果出现 CEX/共享路由器/归集账户，分支需标「公共 Hub/归因受阻」；不能为了让图好看而忽略。

## 竞争解释和停止条件

假说 H1：A/B 是分工转仓派发；H2：A 向独立接收人出售/转让；H3：公共托管/服务造成表面关联。优先寻找能区分三者的签名、长期共同行为、非同类地址对照与成交现金流。若无法区分，结论保持「关联候选，控制者 UNKNOWN」。

Hub、Token-2022、交易版本、v0 ALT、CPI、SOL/WSOL、同签名多钱包、多池、索引缺口及历史截断都是必须显式承认的解释边界。不要因为五跳无结果便认定没有隐藏关联钱包。

## 对跟单决策的不同价值

- A 的首槽买入可能只能作为观察发行侧优势的线索，而非可复制买点。
- B 的连续卖出可能是未来卖压的早期研究对象；若观察太晚也没有预测价值。
- C 的跨币新买入可作为候选发现，而非自动「聪明钱」。
- 真正应衡量的是这种多钱包解释相对于「只看单钱包历史表现」是否产生**额外的、事前可用的、可检验的信息**。

上游来源：
- https://github.com/sunshihao001/grok/blob/blix/knowledge/references/multihop-funding-evidence-audit.md
- https://github.com/sunshihao001/grok/blob/blix/knowledge/references/wallet-relations-cross-project-knowledge-20261106.md
- https://github.com/sunshihao001/grok/blob/blix/knowledge/methods/key-wallet-investigation-brief.md
