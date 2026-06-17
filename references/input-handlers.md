# Input Handlers

不同设计稿输入类型的解析方法。Step 2 根据输入类型选用对应分支。

## 1. 图片 / 截图（PNG / JPG）

- 让模型直接 vision 看图，自顶向下分块：先识别页面骨架（header / sidebar / main / footer），再下钻到每个区块的内部模块
- 对每个模块抽取：bounding box（相对位置）、形状（圆角/阴影）、文字内容与层级、图标位置、状态指示（颜色变化）
- 多张图（如 hover/active 态）时，把它们标注为同一模块的不同 state，匹配时一并考虑组件是否支持该状态

## 2. Pencil 文件（.epgz / .ep）

- 优先：当 Pencil MCP 可用时，调用 MCP 拿结构化节点，节点名常已带语义（如 `card-user`、`btn-primary`）
- 次选：用户把 Pencil 导出为 PNG 后按"图片"分支处理
- Pencil variables（颜色/字号变量）→ 与项目 design tokens 做名称/值匹配，给出 token 映射建议

## 3. Figma

- 本 skill 不直接访问 Figma；引导用户：
  - 仅需还原视觉 → 配合 `figma` skill 拿到 node 数据后回到本 skill 第 3 步比对
  - 需要从 Figma 抽 token → 用 `figma-token-extractor`，跑完后再用本 skill 实现页面

## 4. 多模块 / 多页面设计稿

- 不要一次性匹配所有模块；按"页面 → 区块 → 子组件"逐层处理，每层都让用户确认一次
- 重复出现的模块（如多张卡片）只比对一次，复用同一决策

## 通用原则

- 解析阶段不写代码，只产出 modules[] 数据结构
- 模块语义标签 `candidate_role` 控制在一组受限词汇内：`navigation | sidebar | header | footer | card | list | list-item | table | form | form-field | button | icon-button | badge | tag | avatar | modal | drawer | popover | tabs | breadcrumb | pagination | chart | empty-state | banner | unknown`
- 用 `unknown` 而不是瞎猜；后续匹配阶段再借助上下文补充语义
