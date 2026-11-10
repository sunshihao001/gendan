# 俄语资料、来源分级与后续专属搜索词

优先俄文原始内容和失败/回访案例；不是因为俄语就默认正确。供应商宣传、作者自述、可读源码、复算、实际运行是不同证据等级。

| 资料 | 本次读到的实质内容 | 边界 |
| --- | --- | --- |
| [用户提供的 Mark 俄语视频](https://youtu.be/dxZqcCNAp3Y) | Froggy 导出约 215 地址、初批 5 拟跟＋2 观察、个体化交易过滤、二次剔除、买卖/转账分开跟踪、约十日回访 | 自动字幕可能识别错误；作者有付费工具推广；收益自述没有独立签名审计 |
| [Froggy 官方俄语产品页](https://froggy-v2-0-by-shit101.gitbook.io/frogy-v2-0-by-shit101) / [命令页](https://froggy-v2-0-by-shit101.gitbook.io/frogy-v2-0-by-shit101/getting-started/kak-polzovatsya-froggy) | 代币钱包导出、跨代币共现、开发者相关地址、PnL/ROI 筛选等文档功能 | 尚未真实登录 Bot 验收、未校验目前套餐和字段；跨币命令写法有差异 |
| [Froggy 俄语教程 #1](https://froggy-v2-0-by-shit101.gitbook.io/frogy-v2-0-by-shit101/getting-started/obuchayushie-video/video-1-chto-takoe-kopitreiding) | 筛选→分析→监控→反复换钱包的作者教学顺序 | 不是独立的可复制盈利结果 |
| [Habr 2025-05-29 俄语个人案例](https://habr.com/ru/articles/913768/) | 作者反思高频、套利镜像和低频策略的差异；不同镜像可能相互干扰 | +$2000 属作者自报；个人案例不可直接外推 |
| [Habr 2024-04-18 俄语大样本研究](https://habr.com/ru/articles/808635/) | 对跟单排行榜存活偏差、隐藏亏损、交易费、仓位重叠的具体反证方法 | 研究的是 CEX 组合，不是 Solana Meme 的发生率 |
| [GitHub 俄语 README：anchoys1337/solana-wallet-behavior-analysis](https://github.com/anchoys1337/solana-wallet-behavior-analysis/blob/main/README.ru.md) | 交易余额变化、转仓与卖出边界、演示和实盘模式区分的公开源码方案 | 可读源码并不等于独立运行或统计准确 |
| [GitHub：karusrus/solana-trading-analytics](https://github.com/karusrus/solana-trading-analytics) | 研究止盈目标与历史命中率的量化方案 | 使用事后最高价构造指标，需要防未来信息泄漏和成交不可得 |
 
## 对照研究发现的冲突

- 俄语视频偏好按每个钱包设过滤，Habr 2025 的个人案例偏好低频钱包：前者更注重**交易子集**，后者更注重**跟随者时效和资金占用**。两者可以结合，但都没有公开样本外证明普遍有效。
- 俄语视频回访时展示部分获利，同时说明账户混用其他交易：检验时必须分开源钱包、跟随策略、总账户以及入出金，不能只看截图。
- 同样的“高胜率”可能由首槽优势、少量样本或入选偏差造成：先提出哪个解释会改变 WATCH/PAPER-TEST 决策，不要堆指标。

## 优先搜索的俄语原词

- копитрейдинг Solana отбор кошельков фильтры реальные убытки
- Froggy Parser экспорт кошельков PnL ROI winrate
- кошелёк снайпер копирование сделки задержка проскальзывание
- TradeWiz min market cap min entry copy sells настройка
- связка кошельков токены перевод на новый кошелёк продажа
- копитрейдинг несколько кошельков разные стратегии конфликт
- RayBot отслеживание переводов SOL токенов и сделок
- копитрейдинг через неделю результаты комиссии просадки

## 术语直接映射到研究问题

- кошелёк（钱包）：哪个地址、哪个 Mint、哪个时间窗口？
- связка кошельков（关联组合）：交易相似、资金连通还是确有共同控制证据？
- снайпер（狙击）：优势是否发生在我们能看到之前？
- винрейт / рой / профит（胜率 / ROI / 盈利）：怎么算、漏了多少亏损？
- вход / сайз / холд（进场 / 规模 / 持有）：具体哪个交易子集有价值？
- капа（市值）：是交易时还是今天的市值？
- переводы（转账）：有没有真的换回报价资产？
- проскальзывание（滑点）：容忍上限与真实成交损失不同。

用户完整俄文字幕继续保留在个人 ChatGPT 资料库；本公开 GitHub 只登记视频、研究摘录和可检索关键词，避免不必要地公开整篇第三方视频逐字稿。


## 2026-11-10｜研究 002 新增源级记录

- [Habr evgeny2234，2025-05-29 俄语跟单回顾](https://habr.com/ru/articles/913768/)：作者报告 HFT 半分钟超过 100 笔、套利复制 30–50 秒延迟、低频更易管控，并披露同 Mint 双镜像冲突、手动与机器人交易相互干扰；这些是**作者叙述**，非公开独立 PnL 复算。网页显示 6 条评论，本轮尝试读取评论页失败，因此未引用评论观点。
- [anchoys1337 俄文 README 与代码](https://github.com/anchoys1337/solana-wallet-behavior-analysis)：源码的 owner 优先、重复信号跳过、transfer 与卖出区别、模拟/实盘不同风险门禁值得专业比较。**只读源码，未运行。**
- [karusrus 量化示例、分析代码](https://github.com/karusrus/solana-trading-analytics)：70/30 CV 的代码未评价剩余 30% 验证表现；CSV 的匿名示例 80/80 行 ROI 与源码价格公式不一致。不要把此断言扩展为其真实交易数据错误。详见 [独立审查结果](../../research/RU-002-source-audit.md)。

本轮决策改变：不再把“按钱包单独过滤”直接当成进阶技巧，而是研究**过滤规则事前冻结、同 Mint 策略竞争与纸上/实盘一致性**三项必要条件。


## 研究 003｜新增高信息价值源：公开失败反馈优于泛泛高胜率

- **[Yuno Research /solana_copy_trading](https://github.com/yuno-research/solana_copy_trading)**：不是俄文，但属于深入理解俄语源中“筛钱包/去重/执行价”的直接开源参照。FBFS、按钱包时间窗口排序、1秒延迟模型和同 Mint 去重有源码；其 [Issue #10](https://github.com/yuno-research/solana_copy_trading/issues/10) 的维护者 2025-12 自述策略当时未在新窗口盈利，并提出过拟合及研究方法问题。这里既有“成熟工程实现”也有“真实未成功研发反馈”，不能只选其中一面。[Issue #9](https://github.com/yuno-research/solana_copy_trading/issues/9) 另有卖出可能失败且重复重试的问题。研究 003 的脚本基于其代码逻辑构造合成反例，不是全仓运行复现。
- **[OKX 俄语官方帮助](https://web3.okx.com/ru/help/how-do-i-use-the-okx-wallet-smart-account-for-copy-trading)**（2026-08 更新）：展示目标买入金额、市值、流动性、币龄和预算/风险等跟单参数；部分筛选只影响买入、卖出语义独立。这是“成熟工具已经能表达部分行为子集”的功能事实，不代表已验证净收益。
- **[Raiden Terminal Wallet API 公开文档](https://docs.raiden.wtf/terminal/wallets)**（2026-10-12 文档更新）：提供延迟 0/1/2/5 Slot 的 copytrade 检查、跟随成本和失败交易研究模型。这是供应商算法定义；本文未获取需 Key 的真实钱包响应，不宣称已运行。其 bundled 的同 Slot 邻近标记不应被当成真实 Jito Bundle 的严格证据。
- **[Habr 2024-04-18 评论页](https://habr.com/ru/articles/808635/comments/)**：评论者报告选择高绩效复制对象后亏损，属于社区个案，只提供竞争解释；不是 Solana Meme 实证。
- **[Reddit 2026-09 的跟单亏损叙述](https://www.reddit.com/r/SolanaMemeCoins/comments/1wf6cgq/has_anyone_actually_made_money_copy_trading_my/)**：作者称源钱包盈利但跟随者被薄池高价差及源钱包卖压打亏。该帖子不能核验损益，但与“跟随者首次可见价格、可卖流动性”专业问题吻合。
- **[Reddit 2024-11-24 公共钱包讨论](https://www.reddit.com/r/solana/comments/1gyehdz/how_is_this_wallet_doing_this_99_win_rate_306_mil/)**：提供完整公开钱包地址作为后续只读调查入口，而不是认可帖子宣称的 99% 胜率。
- **[Yuno 交易签名示例](https://github.com/yuno-research/solana_copy_trading)**：README 给出同一签名两段 swap 的具体例子，尚无独立 RPC 解码。详情见 [真实证据入口](../../research/RU-003-public-evidence.md)。
