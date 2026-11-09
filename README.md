# 跟单｜Solana Meme 钱包跟单研究方法论

> 定位：独立的「跟单研究与决策知识库」，不是自制交易终端、自动买卖机器人，也不是宣称有稳定盈利策略的信号群。初期只读调查与纸上跟单；实际交易、授权、签名、付款均不在本仓库当前任务范围。

## 目标

让普通人仅用自然语言提出「找什么钱包、这笔为什么异常、该不该跟、为什么失败」，AI 结合专业知识与已经成熟的分析软件，完成**发现 → 核实 → 钱包/群体角色识别 → 跟单可复制性分析 → 持续跟踪 → 反证和复盘**。

本项目特别关注：多钱包并非孤立交易者；出资、买入、捆绑/同步、刷量、接收转仓、卖出、KOL 扩散、跨 Mint 资金接力可能由不同地址承担。**角色是任务和时段相关的证据候选，不是身份定罪。**

## 不重复造轮子

- **Froggy / Frogy Parser**：优先用其现有命令发现/过滤候选地址、交叉代币钱包和开发者关联地址；不要把供应商的 ROI、PnL、Win Rate 直接当真实跟单收益。
- **GMGN / OKX / Blix 等现有软件**：按实际可用功能复核钱包交易、代币阶段、持仓、池子与资金关系；不同工具统计口径可能不同。
- **ai-d**：继承短意图专业转化、按需调查、竞争解释、可核查交付和「防研究空转」方法。
- **grok/blix**：引用 Solana 协议、钱包/Token Account、资金网络、库存、市场机制及旧 Hermes / qb- / meme- 专业知识。不机械复制整个项目，也不声称其未验证研究已证实。

## 直接进入

| 真实问题 | 方法论入口 | 当前成品工具 |
| --- | --- | --- |
| 哪些钱包值得关注？ | [钱包发现与筛选](methodology/01-wallet-selection.md) | Froggy / GMGN |
| 多地址实际怎样配合？ | [钱包角色和网络调查](methodology/02-wallet-network.md) | Froggy 开发者关联导出、Blix 只读调查方法 |
| 这钱包赚钱，我为什么未必赚？ | [可复制性与实证](methodology/03-copyability-validation.md) | 钱包历史 + 纸上跟单记录 |
| Froggy 具体怎样配合？ | [Froggy 操作与研究手册](tools/froggy-playbook.md) | Froggy Parser |
| 只说一句「继续研究」怎么办？ | [AI 长提示词 / 工作约定](prompts/AI-跟单研究指令.md) | ai-d 方法 + 相关工具 |
| 上轮哪里错了？下一轮做什么？ | [研究与交付台账](research/ACTIVE-LEDGER.md) | GitHub 版本历史 |

## 三条第一性问题

1. 钱包**历史获利的原因**是什么？是选择能力、发行时点、持币/分发角色、提前知道的信息、执行技术，还是历史样本偏差？
2. 其买卖在**我真正能看到的时间之后**，是否仍有可复制价值？必须扣除时差、价差、手续费、滑点、坏币不可卖、延迟退出。
3. 这个地址是独立决策者，还是某群体里的**分工节点**？同一交易团队也可能用不同钱包分别承担买入、转仓、营销、卖出。

## 证据及边界

每项结论必须区分：原始链上事实 / 软件提供的标签或统计 / 自己的结构推断 / 未验证假设 / UNKNOWN。跨软件的一致标签不等于独立实证。历史回填不能冒充事前信号；同一 Slot、同一出资平台或可达多跳，均不能单独证明共同控制。

与旧项目区别：先研究「怎样借助成熟软件建立可靠的专业跟单方法」，只有在明确出现不可替代且可验收的能力缺口后才考虑小规模程序扩展。旧离线原型可以留作辅助实验，不是本项目的主体。

## 来源入口（2026-11-10 复核）

- Froggy 官方介绍：https://froggy-v2-0-by-shit101.gitbook.io/frogy-v2-0-by-shit101
- Froggy 命令文档：https://froggy-v2-0-by-shit101.gitbook.io/frogy-v2-0-by-shit101/getting-started/kak-polzovatsya-froggy
- Froggy 跟单教程：https://froggy-v2-0-by-shit101.gitbook.io/frogy-v2-0-by-shit101/getting-started/obuchayushie-video/video-1-chto-takoe-kopitreiding
- 研究方法上游：https://github.com/sunshihao001/ai-d
- Meme 专业知识上游：https://github.com/sunshihao001/grok/tree/blix/knowledge
- 关键钱包可跟随性原研究：https://github.com/sunshihao001/grok/blob/blix/knowledge/methods/key-wallet-investigation-brief.md

**来源状态**：已读取 Froggy 官方 GitBook 搜索可用文本和上述上游仓库部分原文；Froggy 主站本轮无法直接打开、未登录机器人、未付费、未验证其实际输出或历史数据完整度。仓库中所有参数/步骤是**研究方法候选**，不是盈利承诺。
