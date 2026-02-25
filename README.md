Design-to-Code Expert
Design-to-Code Expert 是一个专为 AI Agent 设计的高级 Skill，旨在将 HTML/CSS 设计稿精准还原为高质量、符合生产标准的 React/Next.js 组件。它拒绝 AI 常见的随机生成，通过结构化的工作流确保代码的稳定性、一致性和可维护性。

Installation
Bash
npx skills add github:bianxuerui/design-to-code-expert
或者通过 Agent Skills CLI：

Bash
npx agent-skills-cli install @bianxuerui/design-to-code-expert
Features
Progressive Loading - 核心逻辑与技术规范、检查清单分离，按需加载，最大限度节省上下文。

Tech Stack Alignment - 强制对齐项目现有的技术栈（如 Tailwind, Lucide-React, TypeScript）。

Design Decomposition - 深度解析 HTML 结构，自动提取颜色、间距并映射到项目的原子设计变量。

Component Sync - 优先复用项目已有的 UI 组件库，而非盲目重新实现基础标签。

Quality Guard - 内置交付前检查清单，涵盖响应式、交互态（Hover/Active）及可访问性。

Usage
安装完成后，在聊天窗口直接运行：

Bash
/design-to-code
支持参数：

--component <name>: 指定生成的组件名称。

--pure: 仅输出代码，跳过分析说明。

--ref <file>: 参考项目中现有的样式或组件实现。

Workflow
Preflight (⛔ BLOCKING) - 加载技术栈规范，扫描项目 Tailwind 配置和主题变量。

Analyze (⚠️ REQUIRED) - 分析 HTML 布局模式（Flex/Grid），提取色板与字阶。

Confirmation - 询问用户：复用现有组件还是全新构建？确认关键交互逻辑。

Generation - 按照 references/ 中的模板生成符合 Clean Code 规范的代码。

Pre-Delivery Check - 自动执行可访问性、响应式和交互态的自我核对。

Structure
Plaintext
design-to-code-expert/
├── SKILL.md                 # 主流程编排与指令核心
├── README.md                # 本文档
└── references/              # 渐进式加载的知识库
    ├── tech-stack-rules.md  # 框架规范 (Next.js/React/Tailwind)
    ├── ui-consistency.md    # UI 还原度与原子单位检查清单
    └── output-template.md   # 标准化的代码输出结构模板
Core Principles (The "Non-Slop" Way)
与普通 Prompt 不同，本 Skill 遵循：

省 (Efficiency): 超过 500 行的规范全部拆分到 references/。

准 (Precision): 采用“提问式指令”引导模型思考，而非模糊的描述。

稳 (Stability): 强制设置确认节点，确保 AI 不会自作主张。

License
MIT
