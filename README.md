# 跟单领域｜先建立 Solana Meme 通用专业认知，再研究跟单

> 仓库名 \`gendan\` 是历史项目名称；**当前知识入口与第一优先级是通用 Meme 市场认知**。跟单是从这套知识衍生的一个应用领域，而不是整个项目知识本体。当前任务以专业研究、成熟软件复用及可复核只读分析为主，不自动下单/签名/付款。

## 现在先读哪里？

**通用 Meme 专业知识（主入口）**

1. [通用 Meme 认知总入口](knowledge/meme/README.md)：把市场看作协议、经济组织、价格流动性、注意力、生命周期和观测系统。
2. [市场系统与利益组织](knowledge/meme/01-market-system.md)：发行、参与者、资本/费用与注意力反馈。
3. [资金、库存与价格](knowledge/meme/02-capital-inventory-price.md)：账户/owner、Swap/Transfer/LP、市场风险承接和可卖容量。
4. [数据与证据失效](knowledge/meme/03-evidence-and-failure.md)：采样、标签、时钟、样本选择和负例。
5. [AI 领域认知与专业研究方法](knowledge/meme/04-cognitive-research-method.md)：从口语问题到现象、机制、痕迹、竞争解释、关键未知。
6. [通用知识 → 不同应用](knowledge/meme/05-to-applications.md)：新币发现、单 Mint、跨 Mint 群体、经济机制和跟单。
7. [来源和继承边界](knowledge/meme/SOURCES.md)：源文件审读状态与历史研究对应。
8. [通用认知案例 001](research/MEME-CASE-001.md)：市场价格、地址数与库存现象的三种竞争解释（**教学假想，非实证**）。
9. [AI Meme 通用认知指令](prompts/AI-Meme通用认知指令.md)：可在任意 AI 研究会话中按需调用，不是全量强制流程。

**跟单领域（第二阶段应用，旧文档保留）**

- [钱包选择](methodology/01-wallet-selection.md) ｜ [钱包网络](methodology/02-wallet-network.md) ｜ [可复制性验证](methodology/03-copyability-validation.md)
- [Froggy 成熟工具研究](tools/froggy-playbook.md) ｜ [跟单专项 AI 提示词](prompts/AI-跟单研究指令.md)
- [当前台账](research/ACTIVE-LEDGER.md)：研究顺序、已查证内容、尚未解决的实际问题。

## 为什么要先理解通用 Meme？

只见「早期买入、涨幅、持币集中、许多钱包同槽交易」，无法解释：
- 创币者、买方、LP、机器人、服务商、KOL 各自可能赚什么、亏什么；
- Token 在地址间转移与新资金真正买入有什么不同；
- 某个价格为什么会升高，又为何不代表大仓位能卖得掉；
- 同源资金或同 Slot 是否可能由公共设施和共同事件造成；
- 终端的统计分母、事件分类和延迟是否改变了我们以为的市场规律。

这些全是 **Meme 市场通用专业问题**。先研究这些，再判断交易观察的真实用途；未来即使不用 Froggy 或不做跟单，知识仍可用于其他市场分析。

## 知识与能力的层次

\`\`\`text
上层方法：ai-d｜问题表征、知识选择、跨来源研究、反证、纠错
                    ↓
市场认知：Solana Meme｜协议 → 经济主体 → 资金/库存
                    ↕    市场阶段、价格、流动性、注意力
                    ↕    数据可见性、抽样和可验证性
                    ↓
多种用途：市场发现｜单Mint调查｜跨Mint监控｜经济机制
                                    └→ 跟单筛选、跟单风险
                    ↓
现成工具：Blix / OKX / GMGN / Froggy / 其他实际可用产品
\`\`\`

上图是**知识依赖**而非强制研究流程。按具体问题选需要的部分，不把旧 Grok 十二域/八层/22位专家复制成第二套框架。

## 上游来源

- 通用人机研究：https://github.com/sunshihao001/ai-d
- Meme 专业知识与 Blix 主体：https://github.com/sunshihao001/grok/tree/blix/knowledge
- 原 Hermes：https://github.com/sunshihao001/-
- 原 qb-：https://github.com/sunshihao001/qb-
- 原 meme-：https://github.com/sunshihao001/meme-
- Froggy 文档（将来用于应用验证）：https://froggy-v2-0-by-shit101.gitbook.io/frogy-v2-0-by-shit101

## 当前真实完成度

已提交：**通用知识入口、机制正文、认知方法、来源映射和教学示例**。这是对部分已读原始资料的知识综合；**不是全量历史资料都深读了，不是运行中的智能研究 Agent，也未通过独立认知提升或实盘收益验证**。

接下来应先检查本体系能否比「看标签/看价格」更准确解释一个不涉及跟单的真实 Meme 市场问题。若方法有效，再把通用能力应用到 Froggy 等成熟软件的跟单研究中。当前真实进度及遗留问题参见[台账](research/ACTIVE-LEDGER.md)。
