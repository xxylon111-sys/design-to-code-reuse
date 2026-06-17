# Component Inventory Schema

`<repo>/.comate/component-inventory.md` 是项目级组件清单，由 design-to-code-reuse skill 维护。

## 文件头

```yaml
---
mode: on-demand | full-scan        # Step 1 用户选择
last_scan: 2026-06-17
scan_roots:
  - src/components
  - packages/ui/src
token_files:
  - src/styles/tokens.css
---
```

## 每个组件一节

```markdown
## Button
- path: `src/components/Button/index.tsx`
- exports: `Button` (default), `ButtonProps`
- variants: primary | secondary | ghost | danger
- sizes: sm | md | lg
- key_props: { onClick, disabled, loading, icon, tone }
- visual_signature:
  - 圆角: 6px (token: --radius-md)
  - 高度: 32/40/48 按 size
  - 主色: token --color-brand
- typical_use: "表单提交、行内 CTA"
- screenshot: assets/screenshots/Button.png   # 可选
- semantic_tags: [button, cta, action]
- last_seen: 2026-06-17
```

## 按需扫描行为

- `mode: on-demand` 时，仅在 Step 3 匹配未命中的语义 role 才追加扫描；扫描结果增量写入本文件
- `mode: full-scan` 时，首次执行 `scripts/scan_components.py` 全量构建
- 用户后续重命名/删除组件时，下次匹配若发现路径失效，标记 `stale: true` 并提示用户

## 与映射库的关系

`component-inventory.md` 描述"项目里有什么"；`component-mapping.md` 描述"什么样的设计应该用什么"。匹配时先查 mapping，未命中再查 inventory。
