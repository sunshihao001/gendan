# Gendan V0.2｜可运行只读工作台

这次交付的是**程序与测试**，不是新一轮研究规划。完整用 Python 标准库，不安装依赖；无密钥、无交易、无钱包签名代码。研究型标签仅代表可观察事实或待验证候选。

## 三个真实操作入口

### A. 处理曾经审计过的真实供应商快照

```bash
python -m tools.snapshot_case data/blix_archived_mint_vendor_summary.json --out output
```

打开 `output/case_report.html`，可看到主要池的状态变化，以及为什么近 6% 的 Token Account 是池相关基础设施候选，而不是可跟单的私人巨鲸。这里的 JSON 是根据 Blix 旧归档审计**摘录的真实历史数值**，不是原始供应商 API 响应，更不是从当前市场获取的实时数据。

### B. 检查一笔 Solana 原始交易

本地已有合法获得的 `getTransaction(jsonParsed)` 结果时：

```bash
python -m tools.inspect_signature --input-rpc path/to/getTransaction.json --mint <真实Mint> --out output/tx_inspection.json
```

在自己能访问公共 RPC 的环境按**真实交易签名**只读查询（此功能当前环境无法联网验证）：

```bash
python -m tools.inspect_signature --signature <真实签名> --mint <真实Mint> --out output/tx_inspection.json
```

只调用 `getTransaction`，不调用 `sendTransaction`，不接密钥。输出 Token Account 的原始数量变化、Owner、解析后的 SPL Token 转移指令；不凭净余额直接判断 Swap、资金同控或买卖利润。默认公共主网 RPC 可能限流、缺历史或无结果。出现缺字段直接失败提示而非填充假事实。

### C. 已有的离线多钱包关系图引擎

```bash
python -m gendan.cli data/demo_case.json --out output
```

打开 `output/demo_report.html`。这个版本的原始演示是**完全合成**的多钱包样本，只用于确认钱包转入、后续卖出候选、同槽/同源等关系标签及反证显示，不能当成已恢复的真实钱包关系。

## 验证

```bash
python -m unittest discover -s tests -v
```

预期共 **22 项**：旧图谱12项 + 池快照6项 + RPC交易4项。注意此前的历史归档里原引擎源码/测试确实存在，但还没有被接进 GitHub 主仓库；本交付已将原文件与新程序打包在一起。提交 GitHub 或服务端部署必须单独核对版本、权限和公开数据质量。

## 目前能做／不能做

| 能做 | 尚不能做 |
| --- | --- |
| 离线核对钱包、池、Holder归属候选 | 自动发现全市场盈利钱包 |
| 从原始RPC交易结果提取可查的Token账户净变动/已解析转账 | 无损还原全部Swap、CPI和历史签名 |
| 输出可查看的HTML/JSON实际报告 | 多钱包全量历史、自动持续监控、前向跟单收益 |
| 使用已保存真实供应商历史快照筛掉池相关账户 | 宣称已连接实时Solana主网或实盘盈利 |

后续应**让现成平台导出或真实 RPC 交易进入上述程序**，先验证“有输入→有可靠输出”，再做自动化；不需要继续新建专家制度、理论目录或交易机器人。
