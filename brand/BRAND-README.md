# Heloe 品牌矢量文件（2026-10-09）

本目录是 Heloe 品牌标识的标准矢量交付包。所有图形均为 SVG，可无损缩放，可直接给设计、印刷、外包或工程使用。

## 文件清单

| 文件 | 用途 | 说明 |
|---|---|---|
| `heloe-app-icon.svg` | App 图标 / 头像 / 圆角方块 | 靛蓝渐变圆角块 + 白色符号，**应用当前使用的就是这一版**（等于前端 `public/logo.svg`） |
| `heloe-mark.svg` | 品牌符号（单色靛蓝） | 透明底，用于浅色背景上的符号单独出现 |
| `heloe-mark-white.svg` | 品牌符号（白色） | 用于深色背景、照片、彩色底 |
| `heloe-mark-mono.svg` | 品牌符号（单色） | 用 `currentColor`：**内联**到页面里时，父元素设 `color` 即可换色（单色印刷/丝印/暗色主题）。注意用 `<img src>` 引用时 `currentColor` 会回退成黑色，那种场景请改用 `heloe-mark.svg` 或 `heloe-mark-white.svg` |
| `heloe-wordmark.svg` | 字标“Heloe” | 深色 `#0F172A`，仅文字，不含符号 |
| `heloe-lockup-horizontal.svg` | 横版组合（符号 + 字标） | 浅色背景使用 |
| `heloe-lockup-horizontal-dark.svg` | 横版组合（深色背景版） | 字标为白色，用于深底 |
| `png/` | 位图导出 | 512 / 256 / 180 / 128 / 64 / 48 / 32 / 24 / 16 px 与 `favicon.ico`、`apple-touch-icon.png` |

## 颜色

| 名称 | 值 | 用途 |
|---|---|---|
| Brand Indigo | `#4F46E5` | 主色：符号单色版、按钮、链接 |
| Gradient Start | `#6159F0` | 图标渐变起点（左上） |
| Gradient End | `#4338CA` | 图标渐变终点（右下），135° |
| Ink | `#0F172A` | 字标、正文标题 |
| Interface Light | `#EEF2FF` | 品牌淡底（选中态、标签底色） |

## 使用规范（简版）

- **留白**：四周至少留出符号高度 25% 的空白，不要把文字或图形贴到标识边上。
- **最小尺寸**：App 图标 16 px 起（低于 16 px 用 `favicon.ico`）；单符号 16 px 起；横版组合宽度 96 px 起。
- **背景**：浅底用 `heloe-mark.svg` / `heloe-lockup-horizontal.svg`；深底或照片上用 `heloe-mark-white.svg` / `heloe-lockup-horizontal-dark.svg`；单色印刷用 `heloe-mark-mono.svg`。
- **不要**：拉伸变形、旋转、加描边或阴影、改渐变色、把白色符号放到浅色底上、在深色底上用深色字标。
- **圆角比例**：App 图标圆角固定为边长 24%（100 单位里 `rx="24"`），做 maskable 图标时不要把圆角改小。

## 应用内引用

前端工程里用的是 `public/logo.svg`（等同本包的 `heloe-app-icon.svg`），侧边栏的横版锁定由「图标 + HTML 文本 Heloe」组成，并没有单独引用横版 SVG；如果以后要做邮件签名或对外物料，用本包的 `heloe-lockup-horizontal.svg`。
