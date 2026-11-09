# Froggy Parser｜现成软件操作与研究方法对接

> 2026-11-10 来源状态：基于 Froggy 官方 GitBook 可检索文本；主站 https://froggy-scanner.su/ 本轮未能直接读取；未登录机器人、未测试付费功能、未获取其真实 CSV。这里是「文档宣称的可用命令 → 应怎样研究」的映射，不是功能实跑验收。

## Froggy 的定位

Froggy / Frogy Parser 是以 Telegram Bot 为入口的 Solana 钱包筛选与数据导出工具。官方描述通过代币合约反向收集交易钱包，并按 ROI、Win Rate、PnL 等指标过滤。其官方教程提出：用 Parser 找地址 → 用分析工具核实 → 通过外部跟单机器人执行 → 追踪交易 → 定期淘汰/新增地址。我们只继承**研究流程**，不把「开始自动下单」设为默认下一步。

官方介绍：https://froggy-v2-0-by-shit101.gitbook.io/frogy-v2-0-by-shit101
命令页：https://froggy-v2-0-by-shit101.gitbook.io/frogy-v2-0-by-shit101/getting-started/kak-polzovatsya-froggy
官方视频 #1 摘要：https://froggy-v2-0-by-shit101.gitbook.io/frogy-v2-0-by-shit101/getting-started/obuchayushie-video/video-1-chto-takoe-kopitreiding

## 命令 → 研究任务

| 官方文档出现的命令 | 其描述的输出/动作 | 跟单方法论的用途 | 需要复查 |
| --- | --- | --- | --- |
| /start | 功能介绍与 DEEP 筛选 | 确认当前可选条件、口径及版本 | DEEP 是否属某套餐、字段定义 |
| /parse_ca_accounts | 指定代币的交易者 | 从 Mint 逆向获取候选钱包 | 是否覆盖失败交易和多池 |
| /export_token_top_wallets | 按代币导出按 ROI/PnL 排列的地址 | 做正样本候选，而非直接跟买名单 | 分母、数据窗口和交易费口径 |
| /find_tokens_cross_traders | 多个指定代币的共同交易者 | 查跨 Mint 重复参与/共同行为 | 原始交集不等于同控、好收益 |
| /parse_pools_creations | 一段时期迁移代币列表 | 设计按时间冻结的代币母样本 | 是否遗漏未迁移/失败币 |
| /parse_mcap_hit_tokens | 按市值命中过滤代币 | 研究特定阶段的参与者 | 按历史涨幅回推存在幸存者偏差 |
| /export_token_devs | 导出开发者及 connected wallets | 发行侧关系候选、分发及危险信号追踪 | connected 的证据定义、误报 |
| /get_pumpfun_boom_growth | 近 15 分钟相对前 45 分钟的 PumpFun 增长榜（官方示例） | 市场发现及对照入口 | 计算窗口、同步时点/Token 阶段 |
| /sol_dash_link | 代币/池/平台看板 | 市场环境与阶段对照 | 可追溯历史窗口与资料来源 |

**命名不一致待核**：官方首页写 /parse_cross_traders，命令页写 /find_tokens_cross_traders。不得猜哪个在当前 Bot 一定能运行，使用时从 /start 菜单或实际提示确认并记录日期/截图。

## 三套实际研究流程

### A｜从一个 Mint 出发

输入：真实 Mint + 冻结时间。通过 /parse_ca_accounts 或 /export_token_top_wallets 取得候选，留存导出来源、时点、参数、总条数。选择具有不同角色的少量地址，至 GMGN/OKX/Blix 复核进出、Token Account owner、资金来源、库存和卖出。输出：不是「最佳钱包十强」，而是**已见事实、群体关系、可复制型/发现型/风险型分类、缺口**。

### B｜从多个 Mint 出发

输入：同类型/同期不同结局的多个 Mint（包括失败者）。尝试交集命令，不要从已经暴涨的几个 Mint 唯一抽样。记录地址重复、资金交叉、阶段差异、是否共同服务节点、是否存在显著跨币行为。输出：**重复参与候选群体**与竞争解释，而非「庄家名单」。

### C｜从开发者/资金网络出发

输入：一枚 Mint 或开发者候选。通过 /export_token_devs 的 connected wallets 取得候选，再以交易签名和 Token 资金转移核查：发行者 → 出资 → 早期买入 → 转入新钱包 → 实际卖出 → 是否跨 Mint 再参与。公共平台 Hub、同槽、交易费支付钱包必须单独标注。输出：**有向、按时间的资金与库存图**，置信边界清楚。

## 能组合的成熟工具与具体分工

- **Froggy**：批量发现及过滤候选；具体数据范围以导出为准。
- **GMGN / OKX**：可供交叉核实钱包记录、池、交易和平台标签；同一上游索引的结果不能当独立来源。
- **Blix**：原有钱包、Mint、资金/交易研究代码及知识；不能仅因存在代码就宣称当前部署可直接使用。
- **RayBot / Axiom / 其他终端或 Bot**：官方视频提及追踪/终端/执行实例；本仓库仅将其作为可选参考，未作安全、成本、能力背书。

## 风险/来源核查

1. Froggy 官方的性能或产品覆盖宣称是**供应商陈述**，不等于独立实测。
2. 官网本轮无法直接打开，不代表它不安全，也不能据此认定安全。不要向未知域名或机器人提交助记词/私钥；先核对官方链接与账号，优先只读操作。
3. 目前没有真实机器人样本导出，未核实价格、套餐限额、是否开放 API、更新频率和可复现性；不用第三方评论直接判断实情。
4. 俄语教学视频历史材料：https://youtu.be/dxZqcCNAp3Y 。用户已提供双语字幕作为候选研究来源；其中展示的策略步骤是**作者经验/演示**，成功收益需单独核实，且本仓库暂未把原视频全文上传。
5. 任何付费订阅和自动复制订单均需用户自行做独立风险判断与授权。本仓库不自动访问交易账户、不签名、不付款。
