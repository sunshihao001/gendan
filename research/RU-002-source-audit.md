# RU-002｜俄语开源“跟单收益”方法审计：三项可复查的实质差异

核查于 2026-11-10。只读 GitHub 默认分支公开源码及样本，未请求 API、未接私钥、未运行真实跟单。数据审计中的所有数值仅来自仓库附带的**匿名示例**。

## 来源一：Ruslan Coefficient 的样本和交叉验证不一致

仓库：https://github.com/karusrus/solana-trading-analytics

源文件：
- https://github.com/karusrus/solana-trading-analytics/blob/main/src/analysis.py （本轮获取的 blob SHA 7334676e9d676201fd92ea31ae87c513d28d70d9）
- https://github.com/karusrus/solana-trading-analytics/blob/main/data/sample_roi.csv （blob SHA 2f37856f5316a3bb45efe42ff222be41c4a9501c）
- https://github.com/karusrus/solana-trading-analytics/blob/main/README.md

**发现 1：README 表述的 70%/30% CV 并未由相应函数实现。**
- find_optimal_P_cv() 每轮打乱数据后取前 70% 为 train。
- 它只在 train 上搜索最大期望收益 P*，并累积 P* 次数；没有对余下 30% 计算结果、保存或报告验证表现。
- 这可用于描述不同训练子集所选 P 的变化，但不能据此称完成独立样本外验证。
- 更进一步，README 的 “2,000+ token events”、 “>200% vs copy-trading” 是作者陈述；这些总体结果的数据与具体真实回放，本轮没有取得可以独立复算的原始明细。

**发现 2：匿名样本 CSV 的 ROI 列与其自己的价格列不能按源码公式一致复算。**
- 源码公式： ROI_pct = (highest_post_purchase_usd × 0.97 / (first_buy_price_usd × 1.03) − 1) × 100。
- 本轮逐行读取了 80 行 CSV 数据；采用上述公式，80 行与存储的 roi_pct 相差均大于四舍五入可解释的 0.05 个百分点。
- 可复核例：第一个样本的 first_buy_price_usd=0.00489503815、highest_post_purchase_usd=0.024626392173，按公式约 +373.78%，CSV 却写 -16.73%。
- 注意：CSV 明写 “anonymised sample — real wallet data replaced”。这些列可能出于匿名化目的被独立随机替换，因此**不能据此推断真实数据有错误或研究者造假**。只能证明随仓公开的示例**不能作为公式一致性或真实表现的验证数据集**。

**发现 3：论文式止盈命中不等于观察者真实退出。**
- fetch_highest_post_purchase_price() 把某个 Mint 在源钱包买入之后的历史最高交易价当作测试变量，不要求跟随者当时已看到提示、能成交足量、按策略实际卖出。
- 随后通过命中率推导固定盈利/亏损的期望值，与实际退出路径、部分卖出、仓位冲突、池深度和订单失败不同。
- 因此该项目提供一种**可探索的历史上限指标**，不是可靠的已证净收益策略。源码给出的 1.44 门槛为预设常数，独立校准材料尚未复核。

## 来源二：俄语开源 copytrade 的模拟和真实风险门禁不同

仓库：https://github.com/anchoys1337/solana-wallet-behavior-analysis

已读代码：
- https://github.com/anchoys1337/solana-wallet-behavior-analysis/blob/main/copytrade/engine.py ，尤其 _buy_block() / _freshness_block() / _risk_block()
- https://github.com/anchoys1337/solana-wallet-behavior-analysis/blob/main/copytrade/executor.py ，尤其 PaperExecutor
- https://github.com/anchoys1337/solana-wallet-behavior-analysis/blob/main/copytrade/strategy.py
- https://github.com/anchoys1337/solana-wallet-behavior-analysis/blob/main/tests/test_owner.py
- https://github.com/anchoys1337/solana-wallet-behavior-analysis/blob/main/README.ru.md

**源码可观察事实**：
- engine._buy_block() 在 DEMO_MODE 时直接放行，不检查真实模式的 signal age 和风险限制；注释也明确是有意让模拟接受回补历史。
- engine._freshness_block() 在 demo 时直接返回；真实模式才可阻止早于启动时刻/过期的买入。
- engine._risk_block() 在 demo 时直接返回；真实模式才应用最大持仓和当日损失限制。
- PaperExecutor 以委托给它的 price_sol 作为预期价格模拟买卖；README 说明价格一般来自目标钱包交易或事件时点的供应商价格，PAPER_APPLY_SLIPPAGE 默认 false，模拟未包含真实时延下的实际后续报价和订单失败分布。
- TREAT_TRANSFER_AS_SELL 默认 false，但 CLOSE_ON_TARGET_BALANCE_ZERO 默认 true。一个源钱包完全转出 Token 而非池内出售，也可能导致跟随持仓关闭：策略层“用于保护风险的退出动作”与链上事实“源钱包已经卖出”必须分离。
- 同一 Mint 多目标冲突通过 owner 主导机制处理，NOT_OWNER 买卖跳过；说明真实操作风险来自**多个策略竞争同一份持仓**，并非只是多钱包是否同控。

**审计结论**：此项目的模拟账本可用于回归/事件演示，但不能直接报告“若实盘复制会赚多少”；要另加真实首次可见时间、后续报价、同等限制及全量失败/未成交信号。未运行源码及测试，本轮只证明存在这些代码路径，不证明它们对实际市场运行准确或不安全。

## 方法学上的一条新决策

今后看到俄语视频、Bot、开源项目宣称某个过滤组合提高 ROI，先分别核查四种完全不同的东西：

1. **筛选后历史上限**：在已知结果后挑赢家/最高价能多好看？
2. **事前冻结的未来信号**：筛选前不知道结果，什么是当时可见且触发的？
3. **模拟环境下的条件一致性**：测试组和基线是否应用相同延迟、费用、仓位/预算限制、退出与历史回补规则？
4. **真正执行后的账本**：真实成交价格、部分/失败成交、未出仓及链上资金流，是否与模拟一致？

四种不能混为同一“跟单胜率”或“盈利能力”。这正是旧 Meme 知识中的时钟、资本、库存、重复归因与数据污染研究，如何实际改变专属跟单判断的例子。

## 证据边界及待验证

仓库 README 与源码可能更新；本轮固定可查 blob SHA 的仅为量化 analysis.py 与 sample ROI CSV；开源 copytrade 静态读源码未实跑。本轮未进行独立真实钱包回测、真实执行、费用/风险测试，也未证明某作者的策略有效。

再研究前先保存实际目标、筛选时点、原始全量钱包/Token 记录、测试规则版本和最早可见时间；没有这些数据，过度优化其他过滤阈值意义有限。
