---
name: design-to-code-reuse
description: 在已有成熟前端代码库中还原设计稿（Pencil/Figma/截图）时使用。强制让 AI 先比对设计稿模块与现有组件库，优先复用线上组件代码而不是直接写新代码，并把每次用户的修正沉淀为项目级"设计特征 → 组件映射"知识库，让复用越用越准。当用户提到「还原设计稿」「实现 Pencil 设计」「按这个设计图做页面」「把设计稿写成代码」「sketch 转代码」「图转代码」，且当前位于一个已有 src/components 或包含 design system 的成熟项目时，必须使用此 skill。即使用户没有明示"复用组件"，只要意图是把视觉稿落地到现有代码库，就应触发。
---

# Design-to-Code with Component Reuse

在成熟前端项目里，设计稿落地的核心痛点不是"能不能写出来"，而是"写出来的代码和已有组件库脱节"。开发者要的是：**先比对，再复用，剩下的才新写**。这个 skill 把这套纪律固化下来，并通过"用户修正 → 写入映射库"的回路让复用准确率随使用提升。

## 何时触发

- 用户上传设计稿（图片 / .epgz / Pencil 链接 / Figma 节点 / 截图）并要求实现到当前代码库
- 用户说"按这个设计稿做"、"还原一下这个页面"、"把设计图写成代码"
- 当前工作区是一个有组件库的项目（存在 `src/components`、`packages/ui`、`design-system/` 等目录，或 package.json 引用了内部 UI 包）

## 何时不触发

- 单纯做新项目脚手架（没有可复用资产）
- 用户只问"这个设计好不好看"、"这个布局怎么改"等设计评审类问题（交给 impeccable / design-framework-matcher）
- 用户只想从 Figma 抽 token，不写组件（交给 figma-token-extractor）

---

## 标准工作流（6 步）

### Step 1：项目首次接入 — 询问扫描策略

检查项目根目录是否存在 `.comate/component-inventory.md`：

- **存在** → 直接进入 Step 2，按需增量更新
- **不存在** → **必须先问用户**一个问题（不要默默全量扫描）：

  > 我注意到这是首次在该项目使用组件复用还原。你希望：
  > - **A. 按需扫描（推荐）**：边做边查，只索引当前设计稿涉及的组件类型（快、增量缓存）
  > - **B. 全量预扫**：现在就扫遍整个组件库建索引（慢，但后续匹配更稳）

用户选定后，把选择记录到 `.comate/component-inventory.md` 头部 `mode:` 字段。

清单文件结构见 `references/inventory-schema.md`。

### Step 2：解析设计稿

按输入类型分流（详见 `references/input-handlers.md`）：

- **图片/截图** → 视觉拆解：自顶向下识别区块（导航/侧栏/卡片/列表/表单/弹窗），并对每个区块抽取视觉特征：尺寸近似、圆角、阴影、文字层级、icon 位置、状态指示
- **.epgz / Pencil MCP** → 优先用 Pencil MCP 拿结构化节点（节点名、variables、嵌套关系），比纯视觉识别更可靠
- **Figma 链接** → 让用户改用 figma-token-extractor 或 figma skill 配合本 skill；本 skill 负责复用比对环节

输出：**设计模块树**（modules[]），每个模块带 id、语义标签（candidate_role）、视觉特征 features{}、子模块。

### Step 3：组件复用比对（最关键）

对 modules[] 中每个模块，按以下顺序匹配：

1. **查项目映射库** `.comate/component-mapping.md` — 这是用户历史修正沉淀的"设计特征 → 组件"硬规则，命中即优先采用
2. **查项目清单** `.comate/component-inventory.md` — 按语义 + 视觉特征模糊匹配
3. **若按需扫描模式且仍无命中** — 用 Explore subagent 检索一次该语义可能对应的组件路径（如 candidate_role=card 时搜 `Card|Tile|Panel`），把找到的组件追加进清单
4. **跨项目启发式** — 读 `references/heuristics.md`（如"圆角 ≥ 8px 且有阴影 → 大概率是 Card 容器"）
5. 仍未命中 → 标记为 NEW

每个模块产出三类结论：

- `REUSE`：直接 import，置信度 ≥ 0.8，列出组件路径与 props 映射
- `EXTEND`：复用但需要新增 variant / prop（如已有 Button 但缺 `tone="warning"`）
- `NEW`：必须新写，列出依赖的 design tokens

### Step 4：匹配确认（必须等用户确认）

把比对结果以表格呈现给用户：

```
| 模块 | 决策 | 组件 | 置信度 | 备注 |
|------|------|------|--------|------|
| 顶部导航 | REUSE | src/components/AppHeader | 0.95 | 完全匹配 |
| 用户卡片 | EXTEND | src/components/Card + 新 variant="profile" | 0.7 | 需加头像槽 |
| 数据图表 | NEW | — | — | 库内无折线图组件 |
```

询问："以上匹配方案是否 OK？需要我调整哪些？" — **未确认前不要写代码**。

如果用户调整了某项决策（如"用户卡片应该用 UserCard 不是 Card"），把这条修正立刻写入 `.comate/component-mapping.md`（见 Step 6 的写入格式）。

### Step 5：生成代码

- `REUSE` 项：直接 import 现有组件，props 按映射填，**禁止**复制粘贴组件内部样式
- `EXTEND` 项：先改组件源码（加 prop / variant），再使用；改动要遵循组件原有 prop 命名风格
- `NEW` 项：用项目 design tokens（颜色/间距/圆角变量），不写魔法值；文件位置参照同类组件的目录约定
- 全程匹配项目代码风格（缩进、引号、命名、import 顺序）—— 先读 2-3 个邻近文件再写

写完后简述："本次复用 N 个组件、扩展 M 个、新增 K 个文件"。

### Step 6：学习沉淀（让 skill 越用越准）

**触发条件**（任一即触发，无需用户主动要求）：

- 用户在 Step 4 调整了匹配决策
- 用户改了你写的代码，且 diff 涉及组件 import 替换（如把 `<div>` 改成 `<UserCard>`、把自写样式换成 import）
- 用户明确说"以后这种设计直接用 XX 组件"

**写入位置选择**：

- **项目独有规则**（依赖项目内部组件） → `<repo>/.comate/component-mapping.md`
- **跨项目通用启发**（视觉特征 → 组件类型的普适规律） → `~/.comate/skills/design-to-code-reuse/references/heuristics.md`

**写入格式**（在对应文件追加一条 rule）：

```markdown
## Rule [递增编号] — [简短标题]
- 触发条件：当设计稿模块满足 {视觉特征 / 语义角色}
- 决策：使用 `<组件路径>`，props: { ... }
- 反例：{ 何时不适用 }
- 来源：YYYY-MM-DD 用户修正于 [简短上下文]
```

写入后简短告诉用户："已学到一条规则：XXX，已写入 [文件路径]，下次同类设计会自动命中。"

详细 schema 见 `references/mapping-schema.md`。

---

## 关键原则

1. **先读后写**：动手生成代码前必须完成 Step 3 的比对 + Step 4 的确认。跳过比对直接写代码是这个 skill 最大的反模式。
2. **复用优于完美还原**：如果设计稿与现有组件有 5% 差异（如圆角差 2px），优先用现有组件并把差异告知用户，而不是为了像素级一致重写一份。除非用户明确要求"严格按设计稿"。
3. **学习是默认行为不是可选项**：每次用户修正都要尝试写入映射库；让用户来 review 这条规则是否合理，而不是等用户主动说"记下来"。
4. **不污染代码库**：`.comate/` 目录下的文件就是这个 skill 的工作产物，提示用户把它纳入版本控制以便团队共享。

---

## 文件引用

- `references/inventory-schema.md` — 组件清单文件结构与字段
- `references/mapping-schema.md` — 映射规则文件结构
- `references/heuristics.md` — 跨项目通用视觉→组件启发式（会随使用增长）
- `references/input-handlers.md` — 不同设计稿输入类型的解析方法
- `scripts/scan_components.py` — 组件库扫描脚本（提取 export、props、文件路径）
- `scripts/match_report.py` — 把匹配结果渲染成 Markdown 表格

