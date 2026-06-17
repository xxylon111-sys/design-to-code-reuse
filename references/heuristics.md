# Cross-Project Heuristics

跨项目通用的"视觉特征 → 组件类型"启发式。这里只放与具体项目无关的普适规律；项目独有的规则放在该项目的 `.comate/component-mapping.md` 里。

随着 skill 在不同项目中被使用，遇到反复出现的规律时往这里追加；遇到反例时修正或删除。

## H001 — Card 容器识别

- 视觉特征：圆角 ≥ 8px + 任一阴影/边框 + 内部多元素分组
- 候选组件名：`Card` / `Tile` / `Panel` / `Surface`
- 反例：全宽无圆角的 section（应是 layout 块而非 Card）

## H002 — 主操作按钮

- 视觉特征：实心填充 + 品牌主色 + 短文案（≤ 6 字）
- 候选组件名：`Button` 的 `primary` variant
- 反例：图标 + 圆形背景（应是 IconButton）

## H003 — 次操作按钮

- 视觉特征：描边或文字按钮 + 中性色
- 候选组件名：`Button` 的 `secondary` / `ghost` variant

## H004 — 表格行 vs 列表项

- 表格特征：横向多列对齐、表头分隔线、数据密度高 → `Table` / `DataGrid`
- 列表特征：单行图文混排、纵向无表头、可点击整行 → `List` + `ListItem` 或语义化 `XxxCard`

## H005 — Modal vs Drawer vs Popover

- Modal：居中、遮罩、阻塞主流程 → `Modal` / `Dialog`
- Drawer：侧边滑入、半阻塞 → `Drawer`
- Popover：贴附触发元素、轻量 → `Popover` / `Tooltip`

## H006 — 表单字段

- Label 在输入框上方且左对齐 + 输入框带边框 → `FormField` / `Input` 组合
- 注意必填星号、错误态颜色都用 token，不要硬编码

## H007 — 状态标签 / 徽章

- 视觉特征：小圆角 + 浅底深字 + 单词或数字
- 候选组件名：`Badge` / `Tag` / `Chip`
- 区分：可关闭 → `Tag closable`；纯计数 → `Badge`

## H008 — 头像与用户身份

- 圆形 + 占位符（首字母或 icon）→ `Avatar`
- 多个头像重叠 → `AvatarGroup`

## 追加新启发式时

1. 必须在至少 2 个不同项目中观察到同一规律才提升为跨项目启发式
2. 仅在单一项目命中的写到该项目的 mapping 文件，不要污染本文件
3. 编号 `H` 前缀递增；删除时保留编号不复用
