#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Claude Code 2026 功能迭代详细报告生成器
"""

from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import datetime


def set_cell_shading(cell, color):
    """设置单元格背景色"""
    shading = OxmlElement('w:shd')
    shading.set(qn('w:fill'), color)
    cell._tc.get_or_add_tcPr().append(shading)


def add_hyperlink(paragraph, text, url):
    """添加超链接"""
    part = paragraph.part
    r_id = part.relate_to(url, 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink', is_external=True)
    hyperlink = OxmlElement('w:hyperlink')
    hyperlink.set(qn('r:id'), r_id)
    new_run = OxmlElement('w:r')
    rPr = OxmlElement('w:rPr')
    c = OxmlElement('w:color')
    c.set(qn('w:val'), '0563C1')
    rPr.append(c)
    u = OxmlElement('w:u')
    u.set(qn('w:val'), 'single')
    rPr.append(u)
    new_run.append(rPr)
    new_run.text = text
    hyperlink.append(new_run)
    paragraph._p.append(hyperlink)


def create_report():
    doc = Document()

    # 设置文档默认字体
    style = doc.styles['Normal']
    font = style.font
    font.name = '微软雅黑'
    font.size = Pt(11)
    style.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')

    # ==================== 封面 ====================
    for _ in range(4):
        doc.add_paragraph()

    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = title.add_run('Claude Code 2026 年度\n功能迭代分析报告')
    run.bold = True
    run.font.size = Pt(32)
    run.font.color.rgb = RGBColor(0, 82, 155)
    run.font.name = '微软雅黑'
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')

    doc.add_paragraph()

    subtitle = doc.add_paragraph()
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = subtitle.add_run('基于官方 GitHub、官网及社区数据的深度分析')
    run.font.size = Pt(16)
    run.font.color.rgb = RGBColor(100, 100, 100)

    for _ in range(3):
        doc.add_paragraph()

    info_para = doc.add_paragraph()
    info_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = info_para.add_run(f'报告日期：{datetime.datetime.now().strftime("%Y年%m月%d日")}\n版本范围：v2.1.0 - v2.1.128+\n数据来源：Anthropic 官方 GitHub、docs.anthropic.com、Claude World 社区')
    run.font.size = Pt(12)
    run.font.color.rgb = RGBColor(80, 80, 80)

    doc.add_page_break()

    # ==================== 目录页 ====================
    toc_title = doc.add_heading('目录', level=1)
    toc_title.alignment = WD_ALIGN_PARAGRAPH.LEFT

    toc_items = [
        ('一、执行摘要', 3),
        ('二、年度重大里程碑', 4),
        ('三、核心功能迭代详解', 5),
        ('    3.1 Skills & 插件系统大重构', 5),
        ('    3.2 Hooks 生命周期系统', 7),
        ('    3.3 Agent 系统与多代理架构', 9),
        ('    3.4 安全与权限系统强化', 10),
        ('    3.5 模型与上下文能力', 12),
        ('    3.6 终端与用户体验', 13),
        ('    3.7 语音与无障碍功能', 15),
        ('    3.8 MCP (Model Context Protocol) 增强', 16),
        ('    3.9 VSCode & IDE 集成', 17),
        ('    3.10 企业级功能与部署', 18),
        ('    3.11 性能优化', 19),
        ('    3.12 平台兼容性增强', 20),
        ('四、版本发布频率统计', 21),
        ('五、年度 TOP 10 最重要功能', 22),
        ('六、发展趋势与洞察', 23),
        ('七、竞争格局分析', 24),
        ('八、信息来源与参考', 25),
    ]

    for item, page in toc_items:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(6)
        run = p.add_run(item)
        run.font.size = Pt(12)

    doc.add_page_break()

    # ==================== 一、执行摘要 ====================
    doc.add_heading('一、执行摘要', level=1)

    summary_text = """
本报告对 Anthropic 公司开发的 AI 编程工具 Claude Code 在 2026 年（1月至5月）的功能迭代进行了全面深入的分析。通过对官方 GitHub 仓库、Anthropic 官方文档、Claude World 技术社区以及多个权威来源的数据收集和整理，我们梳理出了 Claude Code 在这一时期内的完整演进路径。

核心发现：

• 版本发布活跃度极高：2026年至今已发布 130+ 个版本，平均每天 0.9 个版本，累计 610 次 commits，52 位贡献者参与开发

• 架构质变：从单一的 AI 编码助手演进为完整的 AI 开发平台，构建了 Skills + Hooks + Agent 三层架构体系

• 模型能力飞跃：Opus 4.6 和 Sonnet 4.6 双旗舰发布，价格降低 67%，1M Token 上下文正式商用

• 企业级就绪：MDM 部署模板、Console 认证、Managed Settings 等企业功能完善，企业市场成为战略重点

• 安全持续加固：多个严重安全漏洞修复、细粒度权限系统、凭据保护机制全面升级

• 生态整合加速：MCP 协议深度集成、VSCode/GitHub 原生支持、20 种语音语言覆盖

本报告将按照功能模块分类，详细阐述每一项重要功能的迭代背景、技术实现和应用价值，为开发者、技术决策者和研究人员提供全面的参考依据。
"""
    p = doc.add_paragraph(summary_text.strip())
    p.paragraph_format.first_line_indent = Cm(0.75)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE

    doc.add_page_break()

    # ==================== 二、年度重大里程碑 ====================
    doc.add_heading('二、年度重大里程碑', level=1)

    doc.add_paragraph('以下是 2026 年 Claude Code 发展历程中的关键里程碑事件：')

    table = doc.add_table(rows=7, cols=4)
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    headers = ['时间', '里程碑事件', '版本/模型', '战略意义']
    for i, header in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = header
        set_cell_shading(cell, '00529B')
        for paragraph in cell.paragraphs:
            for run in paragraph.runs:
                run.font.bold = True
                run.font.color.rgb = RGBColor(255, 255, 255)
                run.font.size = Pt(11)

    milestones = [
        ['2026-01-08', 'v2.1.1 重大更新', 'v2.1.1', 'CLI 109项改动，Skills系统革新，奠定平台基础'],
        ['2026-02-05', 'Claude Opus 4.6 发布', 'Opus 4.6', '新旗舰模型，SWE-bench 80.8%，价格降67%'],
        ['2026-02-17', 'Claude Sonnet 4.6 发布', 'Sonnet 4.6', '新默认模型，OSWorld得分72.5%'],
        ['2026-03-04', 'v2.1.69 超大版本', 'v2.1.69', '100+项改动，史上最大更新'],
        ['2026-03-14', '1M Token上下文GA', 'Opus/Sonet 4.6', '长上下文正式商用，无需Beta Header'],
        ['2026-05-05', 'v2.1.128 最新版', 'v2.1.128', 'GitHub 121K stars，持续活跃开发'],
    ]

    for row_idx, milestone in enumerate(milestones, start=1):
        for col_idx, value in enumerate(milestone):
            cell = table.rows[row_idx].cells[col_idx]
            cell.text = value
            for paragraph in cell.paragraphs:
                for run in paragraph.runs:
                    run.font.size = Pt(10)
            if row_idx % 2 == 0:
                set_cell_shading(cell, 'F2F2F2')

    doc.add_paragraph()
    doc.add_page_break()

    # ==================== 三、核心功能迭代详解 ====================
    doc.add_heading('三、核心功能迭代详解', level=1)

    # 3.1 Skills & 插件系统
    doc.add_heading('3.1 Skills & 插件系统大重构', level=2)

    intro = doc.add_paragraph()
    intro.add_run('背景与意义：').bold = True
    intro.add_run('Skills 系统是 Claude Code 从"工具"进化为"平台"的核心基础设施。2026年的重构使得第三方开发者可以构建、分享和商业化自己的 Claude Code 扩展，形成了类似 VS Code 插件市场的生态系统。')

    doc.add_paragraph()
    doc.add_heading('v2.1.0 - v2.1.1 (1月) 基础架构革新', level=3)

    skills_v1 = [
        ('Skills 热重载支持', '修改 ~/.claude/skills 目录下的文件后，无需重启会话即可生效，极大提升开发调试效率'),
        ('子代理执行 Skills/Commands', '可以生成"子Claude"在独立上下文中执行任务，如运行脚本而不干扰主任务流程'),
        ('多目录插件种子支持', 'CLAUDE_CODE_PLUGIN_SEED_DIR 环境变量支持多路径配置（Unix用:分隔，Windows用;分隔）'),
        ('Skills 与 Slash Commands 合并 (v2.1.3)', '统一了自定义命令的入口，简化用户学习曲线'),
    ]

    for feature, desc in skills_v1:
        p = doc.add_paragraph(style='List Bullet')
        p.add_run(feature + ': ').bold = True
        p.add_run(desc)

    doc.add_paragraph()
    doc.add_heading('v2.1.69 (3月) 开发者功能飞跃', level=3)

    skills_v2 = [
        ('新增 /claude-api Skill', '这是本版最重磅的内置 Skill。专为基于 Claude API 和 Anthropic SDK 构建应用的开发者设计，可以在同一会话中直接让 Claude Code 脚手架 API 调用、处理流式响应、管理 tool use payload、调试 SDK 集成问题——无需在文档标签和编辑器之间切换'),
        ('${CLAUDE_SKILL_DIR} 变量', 'Skill 可以在运行时引用自身目录路径，解决了之前需要硬编码路径或依赖脆弱的相对路径假设的问题。SKILL.md 可以便携地指向配套脚本、数据文件或模板'),
        ('插件源类型 git-subdir', '支持从 Git 仓库的子目录安装插件，而不仅限于仓库根目录'),
        ('/reload-plugins 命令', '不重启会话即可应用插件配置变更，提升开发体验'),
        ('插件 ZIP 包支持 (v2.1.128)', '--plugin-dir 标志现在接受 .zip 插件归档文件，使插件分发更加便捷'),
    ]

    for feature, desc in skills_v2:
        p = doc.add_paragraph(style='List Bullet')
        p.add_run(feature + ': ').bold = True
        p.add_run(desc)

    impact = doc.add_paragraph()
    impact.add_run('\n影响评估：').bold = True
    impact.add_run('Skills 系统的重构标志着 Claude Code 正式进入"平台化"阶段。特别是 /claude-api Skill 的引入，使得 Claude Code 成为构建 Claude 应用的首选 IDE，形成了"用 Claude Code 构建 Claude 应用"的正向循环。')

    doc.add_page_break()

    # 3.2 Hooks 生命周期系统
    doc.add_heading('3.2 Hooks 生命周期系统', level=2)

    hooks_intro = doc.add_paragraph()
    hooks_intro.add_run('背景与意义：').bold = True
    hooks_intro.add_run('Hooks 系统是 Claude Code 自动化和集成的核心机制。2026年的增强使其从简单的 shell 命令钩子演变为完整的生命周期管理框架，支持 HTTP 回调、条件执行、身份识别等高级特性。')

    doc.add_paragraph()
    doc.add_heading('v2.1.69 (3月) Hooks 系统重大增强', level=3)

    hooks_features = [
        ('InstructionsLoaded Hook', '每次加载 CLAUDE.md 文件或 .claude/rules/*.md 下的规则文件时触发。结合新的 HTTP Hooks 支持，可以轻松地将指令元数据发送到外部服务进行审计或分析'),
        ('HTTP Hooks', '除了 shell-command hooks 外，现在可以定义 POST JSON payload 到 URL 的 hooks。当 hook 逻辑已经存在于 Web 服务、serverless 函数或内部 webhook 接收器时，无需本地包装脚本'),
        ('Agent/Hook 身份标识', 'Hook 事件现在包含 agent_id 和 agent_type 字段，hook 处理器可以区分是哪个 agent 触发了事件。对于运行多个专业 agent（如代码审查 agent vs 测试生成 agent）且共享相同 hook 基础设施但需要不同处理逻辑的团队至关重要'),
        ('ConfigChange Hook', '配置变更时触发，可用于配置审计、同步或验证'),
        ('PostCompact Hook', '上下文压缩后触发，可用于清理临时资源或记录压缩事件'),
        ('PreCompact Hook', '支持阻塞式压缩前钩子，可以在压缩前执行必要的保存操作'),
        ('StopFailure Hook', '任务失败时触发，可用于告警通知或故障恢复'),
        ('PermissionDenied Hook', '权限拒绝时触发，可用于安全审计或权限规则调优'),
        ('CwdChanged/FileChanged Hooks', '工作目录或文件变更时触发，可实现实时的项目状态监控'),
        ('条件化 Hooks', '支持 if 字段条件执行，使 hooks 更加智能和精准'),
    ]

    for feature, desc in hooks_features:
        p = doc.add_paragraph(style='List Bullet')
        p.add_run(feature + ': ').bold = True
        p.add_run(desc)

    use_case = doc.add_paragraph()
    use_case.add_run('\n典型应用场景：').bold = True
    use_case.add_run('\n• CI/CD 集成：通过 StopFailure Hook 自动创建 GitHub Issue\n• 安全合规：PermissionDenied Hook 记录所有被拒绝的操作到 SIEM 系统\n• 配置管理：ConfigChange Hook 将配置变更同步到 Git 仓库\n• 审计追踪：InstructionsLoaded Hook 记录所有指令文件的加载历史')

    doc.add_page_break()

    # 3.3 Agent 系统
    doc.add_heading('3.3 Agent 系统与多代理架构', level=2)

    agent_intro = doc.add_paragraph()
    agent_intro.add_run('背景与意义：').bold = True
    agent_intro.add_run('多 Agent 并行执行是 Claude Code 2026年最重要的架构方向之一。Worktree 隔离技术解决了多 Agent 同时工作时可能产生的代码冲突问题，为大规模 AI 辅助开发奠定了基础。')

    doc.add_paragraph()
    doc.add_heading('Worktree 隔离机制 (v2.1.69)', level=3)

    agent_features = [
        ('声明式 Worktree 隔离', 'Agent 定义现在支持 isolation: worktree，使 agent 在独立的 Git worktree 中运行。提供干净的工作目录而不影响主 checkout——非常适合执行探索性重构、运行破坏性测试套件或生成不应触及主分支的一次性代码的 agent'),
        ('EnterWorktree 路径参数', '支持自定义 worktree 路径，提供更灵活的隔离策略'),
        ('Worktree 配置共享', '主分支的配置自动同步到 worktree，确保一致性'),
        ('Worktree 会话恢复修复', '支持从 worktree 会话恢复工作状态'),
    ]

    for feature, desc in agent_features:
        p = doc.add_paragraph(style='List Bullet')
        p.add_run(feature + ': ').bold = True
        p.add_run(desc)

    doc.add_paragraph()
    doc.add_heading('后台任务与并行执行', level=3)

    bg_features = [
        ('统一后台任务控制', 'Ctrl+B 发送所有运行中的任务到后台，可继续其他工作'),
        ('任务输出文件存储', '输出存储在文件中，无需一直盯着终端等待结果'),
        ('子代理进度摘要缓存优化', '约 3 倍缓存创建减少，显著降低 API 成本'),
        ('禁用特定代理', '可通过配置禁用不需要的 agent，减少资源消耗'),
    ]

    for feature, desc in bg_features:
        p = doc.add_paragraph(style='List Bullet')
        p.add_run(feature + ': ').bold = True
        p.add_run(desc)

    architecture = doc.add_paragraph()
    architecture.add_run('\n架构意义：').bold = True
    architecture.add_run('Worktree 隔离 + 后台任务的组合，使得 Claude Code 可以同时运行多个专门的 Agent（如一个负责写代码、一个负责跑测试、一个负责做代码审查），每个 Agent 在自己的 worktree 中独立工作，互不干扰。这是向"AI 开发团队"愿景的关键一步。')

    doc.add_page_break()

    # 3.4 安全与权限
    doc.add_heading('3.4 安全与权限系统强化', level=2)

    security_intro = doc.add_paragraph()
    security_intro.add_run('背景与意义：').bold = True
    security_intro.add_run('安全性是 AI 编程工具最受关注的话题之一。2026年 Claude Code 在安全方面投入了大量精力，从漏洞修复到权限系统升级，再到沙箱加固，构建了多层防护体系。')

    doc.add_paragraph()
    doc.add_heading('安全修复（贯穿全年）', level=3)

    security_fixes = [
        ('敏感信息泄漏修复 (v2.1.1)', 'Debug 日志不再泄露 API 密钥、OAuth Token 等敏感信息'),
        ('命令注入漏洞修复 (v2.1.2)', '严重级别安全漏洞修补，防止恶意代码注入'),
        ('Bash 安全加固', '子进程 PID 命名空间沙箱隔离，防止逃逸攻击'),
        ('凭据清洗', '自动移除日志和输出中的敏感信息'),
        ('PowerShell 加固权限 (Windows 预览)', 'Windows 平台的 PowerShell 执行权限严格控制'),
    ]

    for feature, desc in security_fixes:
        p = doc.add_paragraph(style='List Bullet')
        p.add_run(feature + ': ').bold = True
        p.add_run(desc)

    doc.add_paragraph()
    doc.add_heading('权限系统升级', level=3)

    permission_features = [
        ('通配符权限匹配', '更灵活的权限规则定义，支持模式匹配'),
        ('.gitignore 感知', '自动忽略 node_modules、.env 等敏感目录'),
        ('"defer" PreToolUse 权限', '延迟权限决策，允许工具先执行部分操作'),
        ('更宽泛的 skip-permissions (v2.1.26)', '--dangerously-skip-permissions 现在对 .claude/、.git/、.vscode/ 等路径也生效（灾难性删除仍会提示）'),
        ('allowRead 沙箱设置', '精细控制读取权限范围'),
        ('环境变量隐藏账户信息', 'CLAUDE_CODE_HIDE_ACCOUNT_INFO 用于演示录制等场景'),
    ]

    for feature, desc in permission_features:
        p = doc.add_paragraph(style='List Bullet')
        p.add_run(feature + ': ').bold = True
        p.add_run(desc)

    doc.add_page_break()

    # 3.5 模型与上下文
    doc.add_heading('3.5 模型与上下文能力', level=2)

    model_intro = doc.add_paragraph()
    model_intro.add_run('背景与意义：').bold = True
    model_intro.add_run('2026年是 Claude 模型的"大年"。Opus 4.6 和 Sonnet 4.6 的发布不仅在性能上实现了突破，更在定价策略上做出了重大调整，使得顶级 AI 编程能力更加普及。')

    doc.add_paragraph()
    doc.add_heading('新模型支持', level=3)

    model_table = doc.add_table(rows=5, cols=4)
    model_table.style = 'Table Grid'

    model_headers = ['模型', '发布日期', '关键指标', '定价']
    for i, header in enumerate(model_headers):
        cell = model_table.rows[0].cells[i]
        cell.text = header
        set_cell_shading(cell, '00529B')
        for paragraph in cell.paragraphs:
            for run in paragraph.runs:
                run.font.bold = True
                run.font.color.rgb = RGBColor(255, 255, 255)

    model_data = [
        ['Opus 4.6', '2026-02-05', 'SWE-bench: 80.8%\nTerminal-Bench: 74.7%', '$5 / $25 (输入/输出)'],
        ['Sonnet 4.6', '2026-02-17', 'SWE-bench: 79.6%\nOSWorld: 72.5%', '$3 / $15 (输入/输出)'],
        ['Fast Mode (Beta)', '2026-02-05', '~2.5x 输出速度提升', '6倍标准价格'],
        ['Haiku 4.6', '2026年初', '轻量级快速任务', '$0.80 / $4 (输入/输出)'],
    ]

    for row_idx, data in enumerate(model_data, start=1):
        for col_idx, value in enumerate(data):
            cell = model_table.rows[row_idx].cells[col_idx]
            cell.text = value
            for paragraph in cell.paragraphs:
                for run in paragraph.runs:
                    run.font.size = Pt(10)

    doc.add_paragraph()
    doc.add_heading('推理与思考模式', level=3)

    thinking_features = [
        ('Adaptive Thinking', '替代 Extended Thinking 的新模式，模型根据任务难度动态决定是否深度推理，无需手动设置 budget_tokens'),
        ('Effort 参数控制', '/effort 命令可显式控制思考强度（low/medium/high/auto）'),
        ('64K/128K 输出 Token', 'Opus 4.6 支持超大输出，适合生成长文档或大型代码文件'),
        ('high effort 默认值', 'API和企业用户默认使用 high effort 模式'),
    ]

    for feature, desc in thinking_features:
        p = doc.add_paragraph(style='List Bullet')
        p.add_run(feature + ': ').bold = True
        p.add_run(desc)

    doc.add_paragraph()
    doc.add_heading('上下文管理革命', level=3)

    context_features = [
        ('1M Token 上下文 GA (3月14日)', 'Opus 4.6 和 Sonnet 4.6 的 100万 Token 上下文从 Beta 转为正式商用。不再需要 context-1m-2025-08-07 Beta Header，超过 200K Token 的请求自动处理，标准定价全额覆盖——900K Token 的请求和 9K Token 的输出在同一价格内'),
        ('Context Compaction', '长时间 Agent 任务中，系统自动压缩旧上下文，防止任务因上下文超限中途失败。这是实现长时间运行 Agent 的关键技术'),
        ('自动压缩修复', '1M 上下文会话不再误报 "Prompt is too long"，实际到达 API 限制前不会错误阻断'),
        ('/context 可操作建议', '提供上下文管理的智能建议，帮助用户优化 token 使用'),
        ('modelOverrides 设置', '自定义模型覆盖规则，根据任务类型自动选择最优模型'),
    ]

    for feature, desc in context_features:
        p = doc.add_paragraph(style='List Bullet')
        p.add_run(feature + ': ').bold = True
        p.add_run(desc)

    pricing_impact = doc.add_paragraph()
    pricing_impact.add_run('\n定价影响分析：').bold = True
    pricing_impact.add_run('Opus 4.6 的价格从 Opus 4.1 时代的 $15/$75 大幅下调至 $5/$25，降幅达 67%。这意味着原本只有大型企业才能承担的旗舰模型能力，现在中小型团队和个人开发者也可以广泛使用。结合 1M 上下文的标准化，Claude Code 在处理大型代码库时的性价比大幅提升。')

    doc.add_page_break()

    # 3.6 终端与用户体验
    doc.add_heading('3.6 终端与用户体验', level=2)

    ux_intro = doc.add_paragraph()
    ux_intro.add_run('背景与意义：').bold = True
    ux_intro.add_run('终端体验是 Claude Code 的核心竞争力所在。2026年在 CLI 交互、多语言支持、快捷键、视觉反馈等方面进行了大量优化，使得终端使用体验接近甚至超越 GUI 应用。')

    doc.add_paragraph()
    doc.add_heading('CLI 体验优化', level=3)

    cli_features = [
        ('多语言支持', '可通过 language: "japanese" 等配置让 Claude Code 以指定语言响应，完美支持多语言开发团队'),
        ('Shift+Enter 兼容性', 'iTerm2、WezTerm、Kitty 等主流终端原生支持，无需手动配置'),
        ('图片粘贴支持', 'Ctrl+V 直接粘贴截图到命令行，iTerm2 已支持此功能'),
        ('斜杠命令自动补全', '输入 / 后自动完成命令，不一定需要以 / 开头也能工作'),
        ('随机会话颜色 (v2.1.128)', '/color 无参数时随机选择会话颜色，增加视觉区分度'),
        ('流式逐行显示', '更流畅的输出体验，减少视觉卡顿感'),
        ('终端闪烁消除', 'CLAUDE_CODE_NO_FLICKER 环境变量解决工具切换时的闪烁问题'),
        ('专注视图', 'Ctrl+O 切换焦点模式，减少干扰'),
        ('AI 生成会话标题 (v2.1.79)', '会话标签页根据首条消息自动生成有意义的标题'),
        ('改进思考显示', '修复思考 pill 显示 "Thought for Ns" 而非通用 "Thinking" 文本'),
        ('轮次持续时间可见性', '/config 菜单中新增 "Show turn duration" 切换选项'),
    ]

    for feature, desc in cli_features:
        p = doc.add_paragraph(style='List Bullet')
        p.add_run(feature + ': ').bold = True
        p.add_run(desc)

    doc.add_paragraph()
    doc.add_heading('新增命令一览表', level=3)

    commands_table = doc.add_table(rows=17, cols=3)
    commands_table.style = 'Table Grid'

    cmd_headers = ['命令', '版本', '功能说明']
    for i, header in enumerate(cmd_headers):
        cell = commands_table.rows[0].cells[i]
        cell.text = header
        set_cell_shading(cell, '00529B')
        for paragraph in cell.paragraphs:
            for run in paragraph.runs:
                run.font.bold = True
                run.font.color.rgb = RGBColor(255, 255, 255)

    commands_data = [
        ['/plan', 'v2.1.1', '快速进入规划模式'],
        ['/copy', 'v2.1.x', '复制内容到剪贴板'],
        ['/branch', 'v2.1.x', 'Git 分支管理'],
        ['/focus', 'v2.1.x', '聚焦当前任务'],
        ['/recap', 'v2.1.x', '会话上下文回顾'],
        ['/undo', 'v2.1.x', '撤销操作别名'],
        ['/proactive', 'v2.1.x', '主动模式别名'],
        ['/tui', 'v2.1.x', 'TUI 全屏模式'],
        ['/powerup', 'v2.1.x', '交互式教程引导'],
        ['/team-onboarding', 'v2.1.x', '团队入门引导流程'],
        ['/doctor', 'v2.1.x', '诊断状态可视化'],
        ['/release-notes', 'v2.1.x', '交互式发行说明查看'],
        ['/remote-control', 'v2.1.79', 'VSCode 桥接到浏览器/移动端'],
        ['/effort', 'v2.1.x', '控制模型思考强度'],
        ['/claude-api', 'v2.1.69', 'Claude API 开发辅助'],
        ['/reload-plugins', 'v2.1.69', '刷新插件配置'],
    ]

    for row_idx, data in enumerate(commands_data, start=1):
        for col_idx, value in enumerate(data):
            cell = commands_table.rows[row_idx].cells[col_idx]
            cell.text = value
            for paragraph in cell.paragraphs:
                for run in paragraph.runs:
                    run.font.size = Pt(10)

    doc.add_page_break()

    # 3.7 语音与无障碍
    doc.add_heading('3.7 语音与无障碍功能', level=2)

    voice_intro = doc.add_paragraph()
    voice_intro.add_run('背景与意义：').bold = True
    voice_intro.add_run('语音交互是无障碍设计的核心，也是提升开发效率的重要手段。v2.1.69 版本将语音语言支持翻倍，体现了 Anthropic 对全球化和包容性的重视。')

    doc.add_paragraph()
    doc.add_heading('v2.1.69 (3月) 语音语言扩展', level=3)

    voice_text = """
语音转文字支持从 10 种语言翻倍至 20 种语言。新增的 10 种语言包括：
"""
    doc.add_paragraph(voice_text.strip())

    lang_table = doc.add_table(rows=3, cols=5)
    lang_table.style = 'Table Grid'

    languages = [
        ['俄语 (Russian)', '希腊语 (Greek)', '波兰语 (Polish)', '捷克语 (Czech)', '土耳其语 (Turkish)'],
        ['丹麦语 (Danish)', '荷兰语 (Dutch)', '瑞典语 (Swedish)', '乌克兰语 (Ukrainian)', '挪威语 (Norwegian)'],
    ]

    for row_idx, row_data in enumerate(languages):
        for col_idx, lang in enumerate(row_data):
            cell = lang_table.rows[row_idx].cells[col_idx]
            cell.text = lang
            for paragraph in cell.paragraphs:
                for run in paragraph.runs:
                    run.font.size = Pt(10)

    impact_voice = doc.add_paragraph()
    impact_voice.add_run('\n影响评估：').bold = True
    impact_voice.add_run('这次扩展使得 Claude Code 对偏好使用母语进行语音提示的开发者更加友好，降低了国际团队采用语音驱动工作流的门槛。对于无障碍需求用户来说，这是一个重要的包容性改进。')

    doc.add_page_break()

    # 3.8 MCP 增强
    doc.add_heading('3.8 MCP (Model Context Protocol) 增强', level=2)

    mcp_intro = doc.add_paragraph()
    mcp_intro.add_run('背景与意义：').bold = True
    mcp_intro.add_run('MCP 是 Anthropic 推出的开放协议，用于连接 AI 模型与外部数据源和工具。2026年 Claude Code 对 MCP 的支持达到了新的高度，使其成为 MCP 生态的最佳客户端之一。')

    doc.add_paragraph()
    doc.add_heading('MCP 工具改进', level=3)

    mcp_features = [
        ('MCP 工具计数显示', '/mcp 命令现在显示已连接服务器的工具数量，并标记连接但零工具的服务器'),
        ('MCP 查询折叠', '减少重复查询，提升效率'),
        ('MCP 500K 结果覆盖', '支持超大结果返回'),
        ('MCP headersHelper 多服务器环境变量', '简化多服务器配置'),
        ('MCP OAuth 手动 URL 粘贴回退', '当浏览器回调无法到达 localhost 时（WSL2、SSH、容器），可手动粘贴 OAuth 代码'),
        ('--channels MCP 研究预览', '新的 channels 功能与 API 密钥认证配合使用'),
        ('保留 workspace 名称', 'workspace 现在是保留的服务器名称，防止冲突'),
        ('重连静音处理', 'MCP 服务器重连不再用完整工具名称列表淹没对话，重新公告的工具按服务器前缀汇总'),
        ('OTEL 隔离', '子进程（Bash、hooks、MCP、LSP）不再继承 OTEL_* 环境变量'),
        ('claude.ai MCP 连接器', '官方连接器集成，无缝访问 claude.ai 服务'),
    ]

    for feature, desc in mcp_features:
        p = doc.add_paragraph(style='List Bullet')
        p.add_run(feature + ': ').bold = True
        p.add_run(desc)

    doc.add_page_break()

    # 3.9 VSCode & IDE
    doc.add_heading('3.9 VSCode & IDE 集成', level=2)

    ide_intro = doc.add_paragraph()
    ide_intro.add_run('背景与意义：').bold = True
    ide_intro.add_run('虽然 Claude Code 定位为终端原生工具，但对 IDE 的深度集成仍然是很多开发者的刚需。2026年 VSCode 扩展在远程协作、会话管理、模型选择等方面都有显著提升。')

    doc.add_paragraph()
    doc.add_heading('VSCode 扩展增强', level=3)

    ide_features = [
        ('Remote Control Bridge (v2.1.79)', '新的 /remote-control 命令可将 VSCode 会话无缝桥接到 claude.ai/code，允许从浏览器或移动设备继续工作'),
        ('AI 生成会话标题', '会话标签页根据首条消息自动获得有意义的标题'),
        ('改进思考显示', '正确显示 "Thought for Ns" 而非通用 "Thinking" 文本'),
        ('会话差异按钮恢复', '从左侧边栏打开会话时恢复缺失的差异按钮'),
        ('Gateway 模型选择器 (v2.1.26)', '当 ANTHROPIC_BASE_URL 指向 Anthropic 兼容网关时，/model 选择器列出网关的 /v1/models 端点模型'),
        ('IDE 工作区连接配置', 'auto_connect 和 open_diff_on_edit 新配置项'),
    ]

    for feature, desc in ide_features:
        p = doc.add_paragraph(style='List Bullet')
        p.add_run(feature + ': ').bold = True
        p.add_run(desc)

    doc.add_page_break()

    # 3.10 企业级功能
    doc.add_heading('3.10 企业级功能与部署', level=2)

    enterprise_intro = doc.add_paragraph()
    enterprise_intro.add_run('背景与意义：').bold = True
    enterprise_intro.add_run('企业市场是 Claude Code 2026年的战略重点。MDM 部署模板、Console 认证、Managed Settings 等功能的推出，表明 Anthropic 正在积极推动 Claude Code 在企业环境的规模化部署。 ')

    doc.add_paragraph()
    doc.add_heading('企业功能清单', level=3)

    enterprise_features = [
        ('MDM 部署模板 (4月)', 'examples 目录添加企业部署示例模板，支持通过 MDM（移动设备管理）在受管设备上规模化部署'),
        ('Console 认证 (v2.1.79)', 'claude auth login 新增 --console flag，启用 Anthropic Console 认证用于 API 计费管理'),
        ('企业限速重试修复', '企业用户现在可以正确重试限速 (429) 错误'),
        ('WSL 继承 Windows 设置', 'wslInheritsWindowsSettings 策略键允许 WSL on Windows 继承 Windows 端的 managed settings'),
        ('managed-settings.d/ drop-in 配置', '支持配置片段 drop-in，便于分层管理'),
        ('Bedrock Mantle 支持', 'AWS Bedrock 新一代接口支持'),
        ('Vertex AI 向导', 'Google Cloud Vertex AI 集成向导'),
        ('强制远程设置刷新', 'forceRemoteSettingsRefresh 确保配置同步'),
        ('pluginTrustMessage 自定义', '托管环境中插件请求信任审批时显示的自定义消息'),
        ('oauth.authServerMetadataUrl', '为 MCP 服务器指定 OpenID Connect / OAuth 发现 URL，简化联合认证设置'),
    ]

    for feature, desc in enterprise_features:
        p = doc.add_paragraph(style='List Bullet')
        p.add_run(feature + ': ').bold = True
        p.add_run(desc)

    doc.add_page_break()

    # 3.11 性能优化
    doc.add_heading('3.11 性能优化', level=2)

    perf_intro = doc.add_paragraph()
    perf_intro.add_run('背景与意义：').bold = True
    perf_intro.add_run('性能是用户体验的基础。2026年 Claude Code 在内存占用、启动速度、API 成本、处理大输入等多个维度进行了优化。')

    doc.add_paragraph()
    doc.add_heading('内存与速度优化', level=3)

    perf_features = [
        ('启动内存减少 18MB (v2.1.79)', '跨所有场景减少约 18MB 启动内存使用，对资源受限环境尤为重要'),
        ('SSE 线性时间性能', '事件流处理从可能的二次复杂度优化到线性时间，长会话性能显著提升'),
        ('SDK Token 成本降低 12 倍', '通过提示缓存和优化策略，SDK 使用成本大幅下降'),
        ('提示缓存启用', 'ENABLE_PROMPT_CACHING_1H 环境变量启用 1 小时提示缓存'),
        ('大输入处理优化', '修复 >10MB stdin 到 claude -p 的崩溃循环'),
        ('子进程挂起修复', 'claude -p 作为子进程调用且没有显式 stdin 时的挂起问题'),
        ('API 超时管理', '非流式 API 回退改进，每次尝试 2 分钟超时，防止无限挂起'),
        ('中断处理修复', '修复 print 模式下 Ctrl+C 功能'),
        ('缓存命中优化 (v2.1.128)', '子代理进度摘要现在命中提示缓存（约 3 倍 cache_creation 减少），静态 transcript 不再重复触发摘要'),
    ]

    for feature, desc in perf_features:
        p = doc.add_paragraph(style='List Bullet')
        p.add_run(feature + ': ').bold = True
        p.add_run(desc)

    doc.add_page_break()

    # 3.12 平台兼容性
    doc.add_heading('3.12 平台兼容性增强', level=2)

    platform_intro = doc.add_paragraph()
    platform_intro.add_run('背景与意义：').bold = True
    platform_intro.add_run('跨平台支持是工具普及的前提。2026年 Claude Code 在 Windows、Linux 以及非 Git VCS 方面都有重要改进。')

    doc.add_paragraph()
    doc.add_heading('Windows 增强', level=3)

    windows_features = [
        ('PowerShell 工具 (Windows 预览)', '原生 PowerShell 支持，不再是二等公民'),
        ('PowerShell 7 检测', '支持通过 Microsoft Store、MSI（无 PATH）、.NET global tool 安装的 PowerShell 7'),
        ('PowerShell 作为主 Shell', '启用 PowerShell 工具后，Claude 将 PowerShell 视为主 Shell 而非默认 Bash'),
        ('Windows PS-as-Shell 完整支持', '完整的 PowerShell 生态集成'),
    ]

    for feature, desc in windows_features:
        p = doc.add_paragraph(style='List Bullet')
        p.add_run(feature + ': ').bold = True
        p.add_run(desc)

    doc.add_paragraph()
    doc.add_heading('Linux 改进', level=3)

    linux_features = [
        ('Linux 沙箱 seccomp 修复', '修复 Linux 平台上 apply-seccomp 相关问题'),
        ('OS CA 证书库默认信任', '默认信任操作系统 CA 证书库，简化 HTTPS 配置'),
    ]

    for feature, desc in linux_features:
        p = doc.add_paragraph(style='List Bullet')
        p.add_run(feature + ': ').bold = True
        p.add_run(desc)

    doc.add_paragraph()
    doc.add_heading('其他 VCS 支持', level=3)

    vcs_features = [
        ('Jujutsu (jj) 支持', '新兴 Git 兼容 VCS 的排除规则支持'),
        ('Sapling 支持', 'Meta 出品的 VCS 工具支持'),
        ('Perforce 模式', 'CLAUDE_CODE_PERFORCE_MODE 环境变量启用 Perforce 支持'),
    ]

    for feature, desc in vcs_features:
        p = doc.add_paragraph(style='List Bullet')
        p.add_run(feature + ': ').bold = True
        p.add_run(desc)

    install_note = doc.add_paragraph()
    install_note.add_run('\n安装方式变更：').bold = True
    install_note.add_run('Anthropic 已完全弃用 npm 安装方式。旧的 npm install -g @anthropic-ai/claude-code 方法已废弃。推荐使用 macOS、Linux、Windows 的原生安装器，包括 Homebrew 和 WinGet。如果早期尝试过但遇到安装摩擦，现在的体验应该有很大改善。')

    doc.add_page_break()

    # ==================== 四、版本发布统计 ====================
    doc.add_heading('四、版本发布频率统计', level=1)

    stats_intro = doc.add_paragraph()
    stats_intro.add_run('2026年 Claude Code 的版本发布极其频繁，体现了团队的敏捷开发和快速迭代能力。')

    doc.add_paragraph()
    stats_table = doc.add_table(rows=6, cols=4)
    stats_table.style = 'Table Grid'

    stats_headers = ['月份', '主要版本数', '代表版本', '特点']
    for i, header in enumerate(stats_headers):
        cell = stats_table.rows[0].cells[i]
        cell.text = header
        set_cell_shading(cell, '00529B')
        for paragraph in cell.paragraphs:
            for run in paragraph.runs:
                run.font.bold = True
                run.font.color.rgb = RGBColor(255, 255, 255)

    stats_data = [
        ['1月', 'v2.1.0 - v2.1.10 (~11个)', 'v2.1.0, v2.1.1', 'Skills系统重构，109项CLI改动'],
        ['2月', 'v2.1.11 - v2.1.56 (~46个)', 'v2.1.52-56', 'Opus/Sonet 4.6发布，密集迭代（4天4版本）'],
        ['3月', 'v2.1.57 - v2.1.79 (~23个)', 'v2.1.69', 'v2.1.69超大版本(100+改动)，1M上下文GA'],
        ['4月', 'v2.1.80 - v2.1.123 (~44个)', 'v2.1.123', '企业功能增强，安全加固'],
        ['5月', 'v2.1.124 - v2.1.128+ (5+)', 'v2.1.128', '持续优化，最新版'],
    ]

    for row_idx, data in enumerate(stats_data, start=1):
        for col_idx, value in enumerate(data):
            cell = stats_table.rows[row_idx].cells[col_idx]
            cell.text = value
            for paragraph in cell.paragraphs:
                for run in paragraph.runs:
                    run.font.size = Pt(10)
            if row_idx % 2 == 0:
                set_cell_shading(cell, 'F2F2F2')

    summary_stats = doc.add_paragraph()
    summary_stats.add_run('\n总计统计：').bold = True
    summary_stats.add_run('\n• 2026年至今已发布 130+ 个版本\n• 平均每天 0.9 个版本\n• 累计 610 次 commits\n• 52 位贡献者\n• CHANGELOG 达 3162 行（2624 loc），236KB')

    doc.add_page_break()

    # ==================== 五、TOP 10 ====================
    doc.add_heading('五、年度 TOP 10 最重要功能', level=1)

    top10_table = doc.add_table(rows=11, cols=3)
    top10_table.style = 'Table Grid'

    top10_headers = ['排名', '功能/里程碑', '影响力分析']
    for i, header in enumerate(top10_headers):
        cell = top10_table.rows[0].cells[i]
        cell.text = header
        set_cell_shading(cell, 'D4AF37')
        for paragraph in cell.paragraphs:
            for run in paragraph.runs:
                run.font.bold = True
                run.font.color.rgb = RGBColor(255, 255, 255)

    top10_data = [
        ['🥇', '1M Token 上下文正式商用', '改变长文档/代码库处理方式，消除 Beta 不确定性，标准定价覆盖'],
        ['🥈', 'Skills 热重载 + /claude-api Skill', '开发者体验质变，形成"用CC开发CC应用"正向循环'],
        ['🥉', 'Worktree Agent 隔离', '多Agent并行开发基础，实现真正的"AI开发团队"'],
        ['4️⃣', 'HTTP Hooks + InstructionsLoaded Hook', '自动化能力飞跃，支持Webhook驱动的CI/CD集成'],
        ['5️⃣', 'Adaptive Thinking + Effort 控制', '智能推理模式，平衡质量与成本'],
        ['6️⃣', 'Opus 4.6 价格降低 67%', '旗舰模型普及，中小企业可负担'],
        ['7️⃣', 'Context Compaction', '长任务不再中断，Agent可持续运行'],
        ['8️⃣', '语音语言扩展至 20 种', '全球化支持，无障碍改进'],
        ['9️⃣', 'MDM 企业部署模板', '企业级落地，规模化部署基础'],
        ['🔟', 'Remote Control Bridge', '跨设备协作，移动端接入'],
    ]

    for row_idx, data in enumerate(top10_data, start=1):
        for col_idx, value in enumerate(data):
            cell = top10_table.rows[row_idx].cells[col_idx]
            cell.text = value
            for paragraph in cell.paragraphs:
                for run in paragraph.runs:
                    run.font.size = Pt(10)

    doc.add_page_break()

    # ==================== 六、发展趋势 ====================
    doc.add_heading('六、发展趋势与洞察', level=1)

    doc.add_heading('6.1 从助手到平台的演进', level=2)

    trend1 = doc.add_paragraph()
    trend1.add_run('核心观察：').bold = True
    trend1.add_run('Claude Code 正在经历从"AI 编码助手"到"AI 开发平台"的根本性转变。这一转变体现在三个层面：\n\n')
    trend1.add_run('• 架构层：').bold = True
    trend1.add_run('Skills + Hooks + Agent 三层架构提供了完整的扩展能力\n')
    trend1.add_run('• 生态层：').bold = True
    trend1.add_run('插件市场、MCP 协议、GitHub 集成构成繁荣生态\n')
    trend1.add_run('• 应用层：').bold = True
    trend1.add_run('/claude-api Skill 使得 CC 成为构建 Claude 应用的元工具')

    doc.add_heading('6.2 Agent 优先架构', level=2)

    trend2 = doc.add_paragraph()
    trend2.add_run('核心观察：').bold = True
    trend2.add_run('多 Agent 并行执行是 Claude Code 2026年最重要的架构方向。Worktree 隔离、多 Agent 身份标识、后台任务系统等技术组件表明，Anthropic 的愿景是让多个专业化的 AI Agent 协同工作，形成真正的"AI 开发团队"。')

    doc.add_heading('6.3 企业级就绪', level=2)

    trend3 = doc.add_paragraph()
    trend3.add_run('核心观察：').bold = True
    trend3.add_run('MDM 部署模板、Console 认证、Managed Settings、Bedrock/Vertex AI 支持等功能的集中推出，明确信号是企业市场已成为战略重点。121K GitHub stars 和 20K forks 中，forks 数据尤其值得关注——通常意味着团队在进行定制化。')

    doc.add_heading('6.4 安全持续加固', level=2)

    trend4 = doc.add_paragraph()
    trend4.add_run('核心观察：').bold = True
    trend4.add_run('多个安全漏洞修复（包括严重的命令注入漏洞）、细粒度权限系统、凭据保护机制、沙箱隔离等措施，显示安全性是重中之重。这与行业内 AI 编程 Agent 导致数据库删除等事故的新闻背景相呼应。')

    doc.add_heading('6.5 生态整合加速', level=2)

    trend5 = doc.add_paragraph()
    trend5.add_run('核心观察：').bold = True
    trend5.add_run('MCP 协议深度集成、VSCode/GitHub 原生支持、Microsoft 365 连接器开放、Claude Cowork 桌面自动化工具发布，显示 Anthropic 正在构建以 Claude 为中心的完整生产力生态。同时，对 OpenCode 等第三方工具的法律行动也表明了对生态控制的重视。')

    doc.add_page_break()

    # ==================== 七、竞争格局 ====================
    doc.add_heading('七、竞争格局分析', level=1)

    comp_table = doc.add_table(rows=5, cols=3)
    comp_table.style = 'Table Grid'

    comp_headers = ['竞争对手', '差异化定位', 'Claude Code 的优势']
    for i, header in enumerate(comp_headers):
        cell = comp_table.rows[0].cells[i]
        cell.text = header
        set_cell_shading(cell, '00529B')
        for paragraph in cell.paragraphs:
            for run in paragraph.runs:
                run.font.bold = True
                run.font.color.rgb = RGBColor(255, 255, 255)

    comp_data = [
        ['GitHub Copilot CLI', 'IDE 内嵌为主，CLI 为辅', '终端原生体验、Agent 自主性、Hooks 自动化'],
        ['Cursor / Windsurf', 'GUI IDE 非常强大', '非 IDE 路线瞄准硬核终端开发者、更轻量'],
        ['OpenClaw / Cline', '第三方 Claude 封装', '官方支持、法律保障、持续更新、企业功能'],
        ['Aider', '开源 AI 编程工具', '商业支持、更大社区、更深度的 IDE 集成'],
    ]

    for row_idx, data in enumerate(comp_data, start=1):
        for col_idx, value in enumerate(data):
            cell = comp_table.rows[row_idx].cells[col_idx]
            cell.text = value
            for paragraph in cell.paragraphs:
                for run in paragraph.runs:
                    run.font.size = Pt(10)

    competitive_insight = doc.add_paragraph()
    competitive_insight.add_run('\n竞争洞察：').bold = True
    competitive_insight.add_run('Claude Code 的独特定位在于"终端原生"。大多数 AI 编码助手都生活在 IDE 内部，而 Claude Code 运行在终端作为独立 Agent。这改变了谁能使用它以及如何使用它。对于花费大部分时间在 shell 会话中、运行构建、管理容器或审查 diff 的开发者来说，Claude Code 解决了一个根本性的摩擦问题。')

    doc.add_page_break()

    # ==================== 八、信息来源 ====================
    doc.add_heading('八、信息来源与参考', level=1)

    sources = [
        ('官方 GitHub 仓库', 'https://github.com/anthropics/claude-code', '121K stars, 3162行CHANGELOG, 610次commits, 52位贡献者'),
        ('官方文档', 'https://docs.anthropic.com/claude/docs', 'Anthropic 官方 Claude Code 文档中心'),
        ('Claude World 技术社区', 'https://claude-world.com', '版本发布详细分析和深度解读'),
        ('Claude FAQ 完整版本历史', 'https://claudefa.st/blog/guide/changelog', '从 v0.2 Beta 到最新的完整 changelog'),
        ('社区维护指南', 'https://github.com/FlorianBruniaux/claude-code-ultimate-guide', '结构化 release 记录和机器可读格式'),
        ('Anthropic 官方发布说明', 'https://platform.claude.com/docs/en/release-notes/overview', '模型和平台更新官方公告'),
        ('Augment Code 分析', 'https://www.augmentcode.com/learn/claude-code-121k-stars', '第三方深度分析和采用趋势'),
    ]

    for name, url, desc in sources:
        p = doc.add_paragraph(style='List Bullet')
        p.add_run(name + ': ').bold = True
        add_hyperlink(p, url, url)
        p.add_run(f' - {desc}')

    doc.add_paragraph()
    disclaimer = doc.add_paragraph()
    disclaimer.add_run('免责声明：').bold = True
    disclaimer.add_run('本报告基于公开可用的信息编制，功能可用性因套餐和地区而异，请以 Anthropic 官方最新文档为准。报告中的版本信息和功能描述截至 2026 年 5 月 11 日。')

    doc.add_paragraph()

    final_note = doc.add_paragraph()
    final_note.alignment = WD_ALIGN_PARAGRAPH.CENTER
    final_note.add_run('— 报告完 —').italic = True

    output_path = '/workspace/Claude_Code_2026_Feature_Iteration_Report.docx'
    doc.save(output_path)
    return output_path


if __name__ == '__main__':
    output = create_report()
    print(f'✅ 报告已成功生成: {output}')
