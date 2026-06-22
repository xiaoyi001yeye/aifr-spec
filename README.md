# aifr-spec

AIFR Spec 是一个用于需求结构化、版本解释、稳定命名与质量检查的 Codex skill。

它的第一个版本聚焦这些能力：

- 将自然语言需求描述转换为 AIFR YAML Spec。
- 检查 AIFR Spec 的结构完整性、规则可追溯性、场景质量和评审就绪度。
- 为单条需求维护语义版本、变更集和影响分析。
- 用稳定路径、manifest、index 和 canonical path 让 AI 与人类可靠找到需求文件。

## 需求转 Spec

当输入是一段产品需求、业务规则、会议纪要、issue 描述或功能说明时，该 skill 会提取并组织：

- 需求意图与业务价值
- 范围边界
- 参与者和外部系统
- 领域术语
- 前置条件
- 业务规则和计算公式
- Given/When/Then 场景
- 验收标准
- 接口影响
- 代码和测试追踪目标
- 风险与非功能要求

输出目标是可评审、可实现、可测试的 AIFR YAML Spec。

## 稳定命名协议

AIFR 的路径和文件名是长期协议，应该像 API 一样稳定。需求身份由稳定 `id` 决定，路径只负责定位，slug 只负责可读性。

推荐 canonical requirement path：

```text
aifr/requirements/items/<domain-path>/<requirement-id>--<frozen-slug>/spec.aifr.yaml
```

示例：

```text
aifr/requirements/items/pay/REQ-PAY-0012--refund-amount-calculation/spec.aifr.yaml
```

核心规则：

- 当前权威需求文件固定为 `spec.aifr.yaml`。
- 版本写在 `aifr_spec.version` 和可选 `versions/` 快照中，不进入主路径。
- 状态写在 `aifr_spec.status` 中，不通过移动目录表达。
- 标题、状态、负责人、团队或业务域理解变化，不自动改 ID、移动文件或重命名目录。
- 废弃和被替代的需求不删除、不移动，使用 `status: deprecated` 或 `status: superseded` 表达。
- Codex 和其他 AI 应优先读取 `aifr/manifest.aifr.yaml`、`aifr/indexes/`、`aifr_spec.id` 和 `identity.canonical_path`，不要靠模糊路径猜测。

完整命名标准见 `references/naming.md`。

## 质量检查

当输入是已有 AIFR Spec 时，该 skill 会检查：

- 必填字段是否完整
- 标识符格式是否一致
- 验收标准是否引用了存在的规则
- 场景是否包含清晰的 Given/When/Then
- 高风险需求是否包含审计、安全、合规或明确评审控制
- 接口、测试和代码追踪信息是否足够指导实现
- canonical path、identity、slug、baseline 和 index 是否符合命名标准

检查结果会优先指出阻塞问题，再给出警告和建议修复方式。

## Smoke Check

```bash
python3 scripts/validate_aifr_spec.py .
python3 scripts/validate_aifr_spec.py . --spec path/to/spec.yaml
```

该命令只做仓库结构和轻量 YAML 质量 smoke check。评审就绪仍需按 `references/quality-checklist.md`、`references/schema.md`、`references/naming.md`、`references/output-format.md` 和 `references/traceability.md` 人工检查。
