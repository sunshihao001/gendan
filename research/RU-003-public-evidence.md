# RU-003｜公开地址、Mint、交易签名的可复查调查入口（真实来源，未完成链上取证）

**日期**：2026-11-10。此表是供后续开展真实调查的原始线索登记，**不是已确认的钱包盈利榜、不是同一群体的钱包关系图**。不使用合成交易替代原始签名，不因为地址出现在 Solscan URL 就声称其交易历史已读。

## 公共对象与来源

| 公开对象 | 完整标识 | 由谁公开 | 当前能够核实的事实 | 尚不能核实 |
| --- | --- | --- | --- | --- |
| 候选钱包 W | 5CcLBq4j7iQbhfocd63VafV2XBpEcWeF8383Ux6Lbxbt | Reddit 2024-11-24 [讨论](https://www.reddit.com/r/solana/comments/1gyehdz/how_is_this_wallet_doing_this_99_win_rate_306_mil/) | 原帖子确实公开此完整地址，讨论者声称其胜率很高、频繁短线交易；Solscan 对应地址页能访问 | 胜率/本金/手续费/转仓/实际获利都没独立核算，也没识别控制者 |
| 候选 Mint M | FRpTyMBDavKsdYN1FQZcEeZ2iwGvHaZKFSkvr5izpump | [Habr 2025-05-29 文章](https://habr.com/ru/articles/913768/) 的 GMGN 跳转链接 | 原文确实用这个 Mint 讨论某次交易/价格迅速变化，并链接到 GMGN | 文中没有完整可复算的源/跟单地址、入出仓签名与现金流 |
| 多腿交易签名 T | 5u42oXBS6E62KAkr5RxURHwAjT8wc4NVL5YqAyHTXLRvpHNkZzgSXAiDsfqoBPJu2yvBU6Q77qpW9URjcp6cAPJZ | [Yuno Research README](https://github.com/yuno-research/solana_copy_trading) | 作者用它说明一笔签名内发生 WSOL→DogeAI→USDC 两腿路由，文档还明确以 Slot、区块内 index、原子指令 index 排序 | 本轮未成功读取对应 RPC getTransaction 的原始 result，未对事件做独立解码 |

三个对象来自不同项目/不同时期，**不得**连成 “W 买 M → T 转币 → 接收钱包卖出” 的故事。

## 本轮真实失败点

尝试直接打开 Solscan 指定交易、Mint、账户与公开 RPC。账户路由仅返回基本页面、交易详情受访问限制、Shell 请求无法解析公网 RPC 域名。故原始数据证据为 **RPC_NOT_RETRIEVED**。没有原始交易时禁止构造 Transfer/Swap 的具体钱包边和利润。

## 第一条链的真实完成条件

要调查某个 Mint 是否存在**买入 A → 转给 B → B 卖出 → B/C 再买另一币**，至少收集：

1. A 的真实 swap 签名、Slot、BlockTime、签名内买入 Token 的 pre/post 余额及报价资产减少；独立区分池账户、费支付者与 Token owner。
2. Token Transfer 的签名、指令序号、Mint、原 Token Account 与接收 Token Account、双方 owner、Token 数量及手续费/扩展影响。区分同 owner 转仓、跨 owner 转仓及公共服务。
3. B 实际 swap 卖出的签名、Token 净减少、SOL/WSOL/USDC 或其他报价资产实际收到，去重 CPI 与多池腿。
4. 如追跨 Mint，B/C 的 SOL 账户间资金变化与下一 Mint 买入的先后顺序；多入多出、CEX/托管混合资金时不能宣称“一笔钱独占地被追到了下一币”。
5. 至少一种竞争解释（同源≠同控、共享 Bot/路由、公共 Funder、普通独立买方、做市/套利）和能改变结论的额外证据。

原始 RPC 格式参考：https://solana.com/docs/rpc/http/gettransaction ，https://solana.com/docs/core/transactions/transaction-introspection ，https://solana.com/docs/tokens/basics/transfer-tokens 。

## 联合“钱包交易子集”验证字段

同一条真实事件链还需要源地址的**每笔交易历史及发现时点**：交易发生 T_chain、Froggy/终端首次显示 T_seen、观察者收到 T_user、当时可执行报价 T_quote；钱包入场币龄、市值、买额、持仓、失败和退出；是否在规则冻结 T0 之后。只有这样才能证明这条网络证据是否改变了跟单判断，而不是发现群体后再事后解释收益。

## 暂停条件和优先级

- 只有 Mint 和宣传截图，无交易签名：SOURCE_ONLY。
- 已有一笔签名，缺前后资产或关键 Token Account owner：EVENT_PARTIAL。
- A→B 已证实，但无法证明同控：TRANSFER_VERIFIED / CONTROLLER_UNKNOWN。
- B 的卖出已证实，却缺真实跟随者首次可见报价：ECONOMIC_CHAIN_POSSIBLE / FOLLOWABILITY_UNKNOWN。
- 若能取得未来冻结后完整信号、每笔执行/未执行和费用，才允许进入 PAPER-TEST-VERIFIED；当前**不满足**。

后续优先选择一项最能消除 UNKNOWN 的真实只读材料，切忌用更多同类网页评分代替交易流水。
