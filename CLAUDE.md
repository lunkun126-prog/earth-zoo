# 地球动物园(Earth Zoo) — 项目规则

> 本文件叠加在全局 `~/.claude/CLAUDE.md` 之上,只写本项目特有的东西。
> 其他项目的 CLAUDE.md 已复制到 `docs/_references/`,写代码前可对照风格。
> 灵感来源:EchoBraid 平台的 "地球动物园" demo(姊妹应用 "地球花园")。

---

## 一、是什么

3D 地球可视化:把 334 种动物按真实栖息地放到地球上,可点击查看简介、
听叫声、按分类/地区/栖息地/保护状态筛选,叠加天气粒子(雨雪风沙)。

**当前阶段:MVP**(方案 B:fork `janarosmonaliev/github-globe` 风格 +
`vasturiano/r3f-globe` 数据层,10 个动物 sprite + 点击弹简介)。

完整规划见 `docs/PLAN.md`(P1-P8 共 8 个阶段)。

---

## 二、技术栈

| 层 | 选型 | 备注 |
|---|---|---|
| 构建 | Vite 6 + React 19 | 纯前端 SPA,**无后端** |
| 3D | three.js + @react-three/fiber + @react-three/drei | r3f 是 React 风格 three.js |
| 地球 | r3f-globe(`vasturiano/r3f-globe`) | 经纬度→3D 坐标、贴片层 |
| 状态 | Zustand | 筛选条件全局共享 |
| 音频 | 原生 Audio API(`src/lib/sound.js`) | 动物叫声懒加载,不用 Howler.js |
| 数据 | 静态 JSON(`src/data/animals.json`) | 不接后端,纯静态 |
| 语言 | JavaScript(暂不上 TS,MVP 阶段保持轻) | MVP 跑通后再考虑 TS |

**端口固定 5173**(Vite 默认),`npm run dev` 起开发服。

---

## 三、运行

```powershell
# 首次
npm install

# 开发
npm run dev          # http://localhost:5173

# 生产构建
npm run build
npm run preview      # 本地预览构建产物
```

---

## 四、文件结构(MVP 阶段)

```
earth-zoo/
├── CLAUDE.md                # 本文件
├── docs/
│   ├── PLAN.md              # P1-P8 完整规划
│   └── _references/         # 5 份其他项目的 CLAUDE.md(写代码风格参考)
├── public/
│   ├── earth-blue.jpg       # 地球贴图(NASA Blue Marble,后续加)
│   └── animals/             # 动物 sprite PNG(MVP 用 emoji 占位)
├── src/
│   ├── main.jsx
│   ├── App.jsx              # 顶层布局
│   ├── components/
│   │   ├── Earth.jsx        # 3D 地球 + 动物 sprite 层
│   │   ├── AnimalSprite.jsx # 单个动物 billboard sprite
│   │   └── AnimalCard.jsx   # 选中动物的简介卡
│   ├── data/
│   │   └── animals.json     # 10 种动物的测试数据
│   └── store/
│       └── useStore.js      # Zustand:选中动物 / 筛选条件
├── .claude/
│   └── settings.json        # 项目级权限白名单(减少弹窗)
└── package.json
```

---

## 五、约定与雷区(Windows + R3F 特有)

### 1. R3F 版本对齐
- `@react-three/fiber` 9.x 需要 React 19+,本项目用 React 19
- **`r3f-globe` 不支持 React 19**(issue #3 open 状态,2026-05 仍未修),
  本项目**不用 r3f-globe**,用原生 `<sphereGeometry>` 自己画地球。
  该依赖已于 2026-06-10 从 `package.json` 移除,代码里不要 `import Globe from 'r3f-globe'`。
- `useTexture` 走 React Suspense,Canvas 内必须包一层 `<Suspense fallback={null}>`

### 2. WebGL 性能
- 动物 sprite 用 `<Billboard>` + `<Sprite>` 实现"永远朝向相机"
- 超过 50 个 sprite 后必须用 `InstancedMesh` 合批,否则 FPS 暴跌
- 动物图片必须先压成 WebP / 限制 256×256 以内

### 3. Vite 静态资源
- 动物 sprite/叫声放 `public/animals/`,代码里直接用绝对路径 `/animals/xxx.png`
- **不要**用 `import imgUrl from './xxx.png'`(MVP 阶段动物多,会爆 bundle)

### 4. 中文 Windows 雷区
- `package.json` / `vite.config.js` 注释一律写英文(中文 GBK 解析坑)
- 数据文件 `animals.json` 中文 OK(UTF-8 编码)
- 终端用 PowerShell,不要写 `&&` 链式(PS 5.1 不支持,改用 `;`)

### 5. 经纬度坐标系
- GeoJSON 标准:`[longitude, latitude]`(经度在前)
- three.js 球面坐标:`(radius, theta_经度, phi_纬度)`
- **统一用 `lonLatToVec3(lon, lat, r)` 工具函数转换**,不要散落在多处

---

## 六、Git 与提交

- **每改完一个能跑的功能就 `git commit` 一版**(沿用其他项目习惯,方便回退)
- commit message 格式:`feat: 加 10 种动物 sprite` / `fix: 经纬度转换符号错误`
- 不要 `git push --force` / `git reset --hard`(全局规则)
- MVP 跑通后再决定是否上 GitHub 私有仓

---

## 七、调试与验证

- 改完前端必须**在浏览器实际打开**看效果,不要只靠"代码看起来对"
- 用 Chrome DevTools 的 Performance tab 监控 FPS,目标 60fps
- WebGL 报错走 console,r3f 的 `<Stats />` 组件可叠加 FPS 显示
- 用户验收:能转动、能点动物、能弹简介 → MVP 通过

---

## 八、参考资源(都是 MIT 可商用)

| 仓库 | 用途 |
|---|---|
| `vasturiano/three-globe`(1.6k⭐) | 底层地球库 |
| `vasturiano/r3f-globe`(51⭐) | R3F 封装,本项目主用 |
| `janarosmonaliev/github-globe`(1.2k⭐) | GitHub 主页地球的着色 shader,可借鉴美术风格 |
| NASA Blue Marble | 地球贴图免费下载 |
| Poly Haven | 星空 HDRI 免费 |

---

## 九、阶段路线图

| 阶段 | 产出 | 状态 |
|---|---|---|
| **P1 MVP** | 地球 + 10 动物 sprite + 点击弹简介 + 银河背景 | 🚧 进行中 |
| P2 数据管线 | IUCN/GBIF/维基 抓数据脚本,凑齐 100+ 种 | 待办 |
| P3 素材脚本 | AI 批量出动物图 + 抠图 + 命名 | 待办 |
| P4 筛选 UI | 底部所有筛选控件(分类/地区/栖息地/状态) | 待办 |
| P5 详情面板 | 飞行镜头 + 食性条 + 保护状态可视化 | 待办 |
| P6 天气粒子 | 雨/雪/风/沙 4 种粒子叠加 | 待办 |
| P7 音频 | 原生 Audio 懒加载 334 条叫声 | 待办 |
| P8 植物剪影 | 地球边缘装饰性植物层 + 性能优化 | 待办 |

---

## 十、参考的其他项目规范(`docs/_references/`)

写代码风格参考下列项目(都是用户自己的项目):

- **`Dream-CLAUDE.md`** — 单进程 Flask + Vite 前端,`requirements.txt` 纯 ASCII 雷区
- **`math-tutor-CLAUDE.md`** — Next.js + Tailwind + Anthropic SDK,端口固定 3003
- **`tashi-CLAUDE.md`** — 严格 TypeScript + Supabase,有完整产品哲学/文案禁用词
- **`claude-biz-explore-CLAUDE.md`** — Flask 多模块,Path A 技术选型方法,PowerShell 弹窗规避
- **`kline-CLAUDE.md`** — Streamlit + DTW,历史决策路径(避免走回头路)

共性:技术栈写死、运行命令完整、约定列雷区、每改一个功能就 commit。

---

**首次新对话**:Claude Code 看完本文件,先报一句"已确认 earth-zoo 项目规则,当前 P1 MVP 阶段"。

---

## 体检记录

- 2026-06-10:修复音频泄漏(playSound 加 ended 监听 + onEnd 回调,AnimalCard 关闭/切换时 stopSound 并复位 playing);从 package.json 移除未使用且与 React 19 不兼容的 r3f-globe 依赖。
