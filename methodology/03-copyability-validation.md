# 03｜跟单可复制性与纸上验证：高 PnL ≠ 跟随收益

## 2026-11-10｜新证据与可推翻的策略假说：关联网络能否过滤错误共识

**先把发现网络和获得收益分开验收。** 2026-10-29 预印本 [Early-Buyer Groups and Fast-Wallet Teams](https://arxiv.org/abs/2610.39458) 在 88.3 小时 pump.fun 观察窗口中发现群体关联具有可描述性，但“最早群体信号”跟随者在作者的全部 32 种样本外设置中平均净收益为负；论文报告在其成本口径下未优于随机进入。**仅属作者的特定回测结果**：没有独立复现、没有身份真值标签、窗口很短，不能推广到所有钱包网络或所有退出策略。

现成代码参照：[`million/opportunities.service.ts`](https://github.com/Kelows/million/blob/main/apps/api/src/opportunities/opportunities.service.ts#L206-L252) 中独立 owner 数去重 + 可选净买卖流过滤；[`million/copyability.service.ts`](https://github.com/Kelows/million/blob/main/apps/api/src/copyability/copyability.service.ts#L17-L30) 用同池分钟 K 线把源交易与后移 60 秒的复制交易比较。源码存在不等于独立验证了该过滤的经济价值；60 秒和分钟收盘价是该作者的研究代理，不是用户真实下单的统一时差/报价。

从旧命题“找到疑似同组钱包即可形成跟单线索”，修正为一项可以失败的研究假说：**在首次可见时点，使用可辩护关系去重与已知净卖压信息，是否比只按地址数或单钱包历史表现减少错误跟买，而又不丢失过多真正机会？** 若前向同条件实验不优，就不把它升级为自动跟单条件。对关系图本身可继续评估风险解释与资金研究用途。


## 两个问题必须分开

**历史分析**：源钱包过去是否通过某类交易赚到钱？

**真实可跟随性**：在我能收到提醒、核实 Mint、获取可执行报价的时刻，按自己的规模买卖，扣除费用、延迟、滑点、失败单和流动性风险之后，是否仍有正的、稳定的结果？

前者是候选入口，不能替代后者。

## 必须冻结的四个时间

- T_chain：源地址交易实际发生的 Slot/blockTime。
- T_seen：Froggy / 监控平台首次对我显示该信号的时间。
- T_decide：完成筛查、决定采取何种纸上行动的时间。
- T_quote：可以取得模拟/历史可核验报价的时间（与 T_seen 不同）。

不能用 T_chain 的理论最低价、T_seen 之后才出现的最高点、未来才知道的 KOL 身份给自己算利润。历史回填用于解释，不能当已经可在当时观察。

## 收益核算要求

单笔收益研究至少记录源钱包成本和退出、我们的假设入场/离场时刻及对应可交易报价、市场深度、池子、两端手续费、优先费、预期/实测滑点、无法执行的订单、部分成交与未退出资产。PnL 需区分已实现、未实现、资金转入转出、LP/奖励、空投和多个地址之间转仓；不能把跨钱包流入当新收益。

**示意公式**：模拟净损益 = 实际可执行退出价值 − 入场成交成本 − 买卖全部费用 − 额外冲击成本。此公式仅为核算框架，不意味着拿到真实可执行报价。

## 五类典型「看似优秀但难以复制」

1. 创建 Slot 狙击：盈利发生在观察者看见交易之前。
2. 大资金/优先费优势：别人订单规模或流动性、路由条件完全不同。
3. 分散钱包转仓：单地址卖出缺失，排行榜利润失真。
4. 关联制造交易量：跟着买可能只成为退出流动性。
5. 以结果挑地址：幸存者偏差、只展示涨幅惊人的历史 Mint。

## 最小样本外比较（先纸上记录，不接私钥）

将候选钱包在筛选日冻结，保留**全部后续符合预先规则的信号**，不能看见亏损后删除。至少对照：

A. 简单基线：仅使用 Froggy 的历史绩效和固定过滤条件；
B. 研究增强：引入资金网络、库存、钱包角色、市场阶段；
C. 不跟或随机同时间窗口的候选对照，评估机会成本与行情影响。

对同一批信号，用相同的延迟、报价时点和费用假设对比。记录覆盖率、可执行比例、样本量、失联率、亏损尾部、最大回撤、各市场阶段和各钱包群体的表现；多币复用的钱包不能当作独立样本。观察期和最小样本量须预先登记，不得事后挑最有利窗口。

## 失效或降级的实际条件

- 数据字段无法解释、历史记录大量缺失；
- 首次可见时点价格已无法合理估算；
- 源钱包近期利润依赖不可复制的首槽交易；
- 关系归因需要假定所有同源/同槽都同控；
- 所谓网络增强方法没有优于不使用网络的简单基线；
- 真实成交/纸上核算和供应商显示差异持续不可解释。

这些情况应作**暂缓、仅观察或 UNKNOWN**，不是强行产生买卖建议。任何真实资金执行需另行授权、独立的密钥安全审查和风险控制；本项目不触发交易。

## 可复制的单次观察记录模板

- candidate_source / discovered_at / criteria / freeze_id：
- source_wallet / Mint / market_phase：
- T_chain / T_seen / T_decide / T_quote / provider_latency：
- buy-sell side / source estimated basis / open inventory：
- own simulated size / quote / liquidity / fees / slippage / failed execution：
- relationship hypotheses / negative controls / evidence signatures：
- simulated exit rule (pre-registered) / realized result / missing fields：
- decision at observation time / disconfirming event / revision：
