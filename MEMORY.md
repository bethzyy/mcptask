# MCPMark 项目记忆

## 项目概述

MCPMark是一个用于测试AI模型MCP工具使用能力的基准测试框架。

### 核心概念
- **MCP (Model Context Protocol)**: Anthropic的工具集成标准
- **Playwright MCP**: 浏览器自动化工具，用于web任务
- **LiteLLM**: 统一接口调用不同LLM提供商

## 任务设计要求（重要！）

### 基本要求
| 指标 | 要求 | 说明 |
|------|------|------|
| 交互轮次 | >15 | AI回复消息的次数（assistant消息数） |
| Tool Call次数 | >20 | 调用MCP工具的总次数 |
| 通过率 | ≤50% | 对目标模型（如qwen3.5-plus）的通过率 |

### 轮次计数方式
- **交互轮次**：每次AI生成文本消息算1轮
- **Tool Call次数**：browser_navigate、browser_click、browser_snapshot等每个调用算1次

### 任务类型区别

| 类型 | 特点 | 示例 |
|------|------|------|
| eval_web | 固定URL，静态页面 | 访问特定网页提取信息 |
| web_search | 开放搜索，多页面 | 搜索多个来源对比信息 |

**web_search类型更容易产生更多轮次**，因为需要：
- 搜索多个关键词
- 访问多个网站
- 对比和整合信息

## 模型配置

### 环境变量文件 (.mcp_env)
```
# 阿里云百炼 DashScope
DASHSCOPE_API_KEY="sk-xxx"
DASHSCOPE_BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1"

# 智谱AI (Anthropic兼容)
ZHIPU_API_KEY="xxx"
ZHIPU_BASE_URL="https://open.bigmodel.cn/api/anthropic"
```

### model_config.py 配置格式
```python
MODEL_CONFIGS = {
    # 阿里云
    "qwen3.5-plus": {
        "provider": "qwen",
        "api_key_var": "DASHSCOPE_API_KEY",
        "base_url_var": "DASHSCOPE_BASE_URL",
        "litellm_input_model_name": "dashscope/qwen-plus",
    },
    # 智谱AI (必须用Anthropic兼容接口)
    "glm-5": {
        "provider": "zhipu",
        "api_key_var": "ZHIPU_API_KEY",
        "base_url_var": "ZHIPU_BASE_URL",
        "litellm_input_model_name": "anthropic/glm-5",
    },
}
```

### 智谱AI注意事项
- **必须使用Anthropic兼容接口**：`https://open.bigmodel.cn/api/anthropic`
- LiteLLM模型名需要`anthropic/`前缀
- 非Anthropic接口可能没有配额

## 任务文件结构

```
tasks/playwright/standard/web_search/{task_id}/
├── description.md    # 任务描述（模型唯一输入）
├── meta.json        # 元数据
└── verify.py        # 验证脚本
```

---

## 📝 description.md 撰写规范

### 核心原则
```
┌─────────────────────────────────────────────────────────┐
│  description.md = 模型收到的唯一指令                    │
│                                                         │
│  要求：必须纯英文                                       │
└─────────────────────────────────────────────────────────┘
```

### 标准模板（直接复制使用）

```markdown
# [Task Title]

## Task
[1-2 sentence clear statement of the goal]

## Tools
IMPORTANT: The Playwright MCP server is pre-configured and already registered.
Use the available `browser_*` tools directly.

Do NOT spawn a subprocess or manually start the MCP process.

### Step 1: Investigate [Page Name]
Navigate to `[URL]` and extract:
- field1
- field2

### Step 2: Investigate [Another Page]
Navigate to `[URL]` and extract:
- field3
- field4

### Step 3: Cross Analysis
Determine:
- FieldA (based on comparison)
- FieldB (calculated from extracted values)

## Output Format

You MUST output EXACTLY:

<answer>
FieldA|value
FieldB|value
FieldC|number
</answer>

## Important Notes

- Only count required dependencies
- Values must be comma-separated
- Output ONLY the `<answer>` block
- Solve the task by yourself
```

### 模板要点

| 部分 | 要求 |
|------|------|
| **Task** | 1-2句清晰目标陈述 |
| **Tools** | 必须声明MCP已配置，禁止手动启动 |
| **Steps** | 2-5个步骤，每个步骤明确URL和提取字段 |
| **Output Format** | 必须用`<answer>`标签，明确字段分隔符 |
| **Notes** | 禁止模型询问用户，要求独立完成 |

### ❌ 常见错误

```
❌ 错误1：使用中文
   "请访问维基百科..."

❌ 错误2：没有声明MCP已配置
   模型可能尝试自己启动MCP进程

❌ 错误3：输出格式不明确
   "输出答案" → 应该明确 <answer>field|value</answer>

❌ 错误4：允许模型询问
   缺少 "Solve the task by yourself"
```

---

## 📋 题目可解性分析（提交必填）

### 提交时需要在问卷中说明的内容

```
┌─────────────────────────────────────────────────────────┐
│  对照 verify.py 的每个验证点，说明任务为什么可解       │
└─────────────────────────────────────────────────────────┘
```

### 标准格式示例

```markdown
任务: [一句话描述任务目标]

执行路径:
打开页面 → [步骤1] → [步骤2] → ... → 按指定格式输出

页面特点:
- [说明页面结构特点]
- [说明交互复杂度]
- [核心考察点]

稳定性说明:
- 使用 [网页来源]
- 页面内容与结构固定
- 无动态数据与外部依赖
- Playwright 执行环境一致、页面可复现
- 不会出现结果随机波动，满足基准测试稳定要求
```

### 实例参考

```markdown
任务: 从页面表格中筛选出 Engineering 部门、薪资大于 $100,000 的员工

执行路径:
打开页面 → 定位表格 → 逐行筛选 → 按指定格式输出

页面特点:
- 页面结构单一、无多页跳转与复杂交互
- 核心考察表格理解与条件筛选能力
- 逻辑清晰、可正常完成

稳定性说明:
- 任务使用 MCPMark 官方静态页面 eval-web.mcpmark.ai
- 页面内容与结构固定、无动态数据与外部依赖
- Playwright 执行环境一致、页面可复现
- 不会出现结果随机波动，满足基准测试稳定要求
```

### 可解性分析检查表

```
□ 任务目标是否清晰？
□ 执行路径是否明确（步骤1→2→3→输出）？
□ 页面是否稳定（无动态数据）？
□ 核心考察点是否说明？
□ 为什么不会出现 Flaky 结果？
```

---

## 🔍 Verify 脚本设计原则：三层校验

```
┌─────────────────────────────────────────────────────────┐
│  三层校验保证评分准确、公平、鲁棒                       │
└─────────────────────────────────────────────────────────┘
```

### 第1层：输出格式校验
```
目的：检验指令遵循能力

检查项：
- 必须包含 <answer> 标签
- 未按格式输出 → 直接判错

代码示例：
answer_pattern = r'<answer>(.*?)</answer>'
if not re.search(answer_pattern, response, re.DOTALL):
    return False, "Missing <answer> tag"
```

### 第2层：数据准确性校验
```
目的：检查提取内容是否正确

检查项：
- 提取标签内内容
- 与标准答案逐项比对
- 检查是否漏选、错选、字段错误

关键技巧：
✅ 用集合比对（set comparison）
   → 不强制要求顺序一致

代码示例：
expected_set = {"item1", "item2", "item3"}
found_set = set(found_items)
if expected_set == found_set:
    return True
```

### 第3层：格式归一化容错
```
目的：避免非智力因素误判

归一化处理：
- 空格清洗（strip）
- 大小写统一（lower）
- 符号清洗（去除 $、逗号等）
- 数值转换（薪资转为数字比较）

代码示例：
def normalize(value):
    # 去除符号
    value = re.sub(r'[$,%]', '', value)
    # 去除空格、转小写
    return value.strip().lower()

# 薪资数值比较
def compare_salary(found, expected):
    found_num = float(normalize(found))
    expected_num = float(normalize(expected))
    return found_num > expected_num
```

### 三层校验示意图

```
模型输出
    │
    ▼
┌─────────────────────────────────────┐
│ 第1层: 格式校验                      │
│ 有 <answer> 标签？                  │
│   ├─ 否 → ❌ 直接判错               │
│   └─ 是 → 继续                      │
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│ 第2层: 数据准确性                    │
│ 内容是否匹配标准答案？               │
│   ├─ 集合比对（不要求顺序）          │
│   └─ 逐项检查                        │
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│ 第3层: 归一化容错                    │
│ 格式差异是否影响核心信息？           │
│   ├─ 空格、大小写、符号清洗          │
│   └─ 只评判核心信息正确性            │
└─────────────────────────────────────┘
    │
    ▼
  ✅ 通过 / ❌ 失败
```

### 🚫 verify.py 质量红线（严禁违反）

```
┌─────────────────────────────────────────────────────────┐
│  以下行为 禁止：                                        │
└─────────────────────────────────────────────────────────┘

❌ 读取本地文件
   错误：open("/workspace/answer.txt")
   原因：必须从MCP_MESSAGES读取AI输出

❌ 过严匹配
   错误：必须完全匹配字符串
   正确：normalize / contains / 集合比对

❌ 未捕获 Exception
   错误：直接执行可能失败的代码
   正确：必须 try/except 包裹

❌ 使用动态数据
   错误：当天价格、最新版本号
   正确：使用 label.txt 固定答案
```

### 出题校准要求

```
校准模型：qwen3.5-plus
运行次数：Pass@4（运行4次）
目标通过率：Pass@4 ≤ 2（4次中最多通过2次）
交互要求：tool call 次数 > 20

出题必须反复校准，确保：
1. 难度适中（通过率≤50%）
2. 轮次足够（>20次tool calls）
3. 人工可完成（答案真实存在）
```

### verify.py 检查清单
```json
{
  "task_id": "jasminum_nudiflorum_info",
  "task_name": "Winter Jasmine Botanical Info Search",
  "category_id": "web_search",
  "difficulty": "L3",
  "tags": ["search aggregation", "data extraction"],
  "mcp": ["playwright"]
}
```

## 运行命令

```bash
# 基本运行格式
pixi run python pipeline.py \
    --mcp playwright \
    --models glm-5 \
    --tasks web_search/task_id \
    --exp-name experiment_name \
    --timeout 600 \
    --k 4

# 参数说明
# --mcp: MCP服务类型
# --models: 模型名称（逗号分隔）
# --tasks: 任务ID（category/task_id格式）
# --exp-name: 实验名称（k>1时必须）
# --timeout: 超时时间（秒）
# --k: 运行次数
```

## 常见问题

### 1. 环境变量被覆盖
- **问题**：系统环境变量覆盖了.mcp_env文件
- **解决**：在pipeline.py中使用`load_dotenv(override=True)`

### 2. 任务被跳过
- **问题**：MCPMark自动跳过已完成的任务
- **解决**：删除results目录后重新运行

### 3. 通过率太高
- **问题**：任务太简单，AI轻松完成
- **解决**：增加任务复杂度，添加更多子任务

### 4. 轮次不足
- **问题**：AI提前结束，没有完成所有步骤
- **解决**：
  - 增加任务复杂度（多个网站、多个对象对比）
  - 要求分阶段报告中间结果
  - 添加截图保存等必须步骤

## 任务设计技巧

### 如何增加轮次
1. **多对象对比**：研究3-4个相似对象，比较差异
2. **多源验证**：要求从3+个网站获取信息并交叉验证
3. **分阶段输出**：要求每个阶段输出中间结果
4. **强制步骤**：要求截图、滚动查看完整内容等

### 如何降低通过率
1. **复杂输出格式**：要求特定格式（如`<answer>`标签）
2. **精确匹配**：要求精确提取数字、名称等
3. **信息整合**：要求对比、分析、总结

---

## ⚠️ 重要教训：任务设计正确流程（必读！）

### 错误的设计流程（我之前犯的错）
```
❌ 错误做法：
1. 想到一个任务主题
2. 凭记忆编写"标准答案"
3. 编写description.md
4. 编写verify.py
5. 直接测试

问题：
- 没有验证答案是否在网页上
- 没有人工测试任务可完成性
- 可能设计出无法完成的任务
```

### 正确的设计流程
```
✅ 正确做法：

Step 1: 选择网页
  - 选择稳定的网页（Wikipedia、百度百科）
  - 禁止使用动态网页（热搜、实时新闻）
  - 确认页面不会频繁变化

Step 2: 人工访问验证
  - 亲自用浏览器打开目标网页
  - 确认信息确实存在于页面上
  - 截图记录信息位置

Step 3: 记录真实答案
  - 基于网页实际内容记录答案
  - 不要凭记忆填写
  - 每个字段都要验证

Step 4: 编写任务文件
  - description.md：基于真实网页编写
  - verify.py：基于真实答案编写
  - meta.json：填写元信息

Step 5: 人工测试
  - 自己按description.md执行一遍
  - 确认能找到所有答案
  - 确认输出格式可行

Step 6: AI测试
  - 用Claude 4.6测试（验证可完成）
  - 用qwen3.5-plus测试（验证难度）
  - 检查轮次>15，tool calls>20，通过率≤50%
```

### 网页选择要求（出题专家建议）

#### 优先级排序
```
1️⃣ 最高优先级：官方评测站
   eval-web.mcpmark.ai
   - 官方维护，最稳定
   - 专为测试设计

2️⃣ 次优先级：带版本号的静态网页
   - PyPI 历史版本页面
   - 技术文档归档版本
   - 固定版本不会变化

3️⃣ 第三优先级：稳定知识库网站
   - Wikipedia
   - 百度百科

❌ 禁止使用：
   - 实时内容（热搜、新闻）
   - 社交媒体（微博、Twitter）
   - 搜索引擎结果页
```

| ✅ 推荐的网页 | ❌ 禁止的网页 |
|--------------|--------------|
| eval-web.mcpmark.ai | 百度热搜 |
| PyPI（指定版本） | 实时新闻 |
| 技术文档归档 | 社交媒体 |
| Wikipedia | 搜索引擎结果 |
| 百度百科 | 排行榜 |

#### 🚫 严禁使用（黑名单）
```
以下类型网页 禁止用于 Benchmark：

动态数据网页：
- 百度热搜
- 实时新闻
- X / Twitter 帖子流
- 股票行情
- 实时排行榜

原因：
- 数据每天变化
- 页面结构可能频繁改版
- 无法保证长期稳定

后果：
⚠️ Flaky Benchmark
   今天评测通过，明天评测失败
```

### 核心原则
```
┌─────────────────────────────────────────────────────────┐
│  任务必须满足：                                         │
│  1. 人工可以完成（信息确实在网页上）                    │
│  2. AI容易失败（执行复杂、格式严格）                    │
│                                                         │
│  关键：让"找答案"容易，让"完成任务"难                  │
└─────────────────────────────────────────────────────────┘
```

### 交互轮次的本质
- **description.md**：定义任务复杂度（要做什么）
- **AI自己**：决定实际执行多少步（做多少）
- **代码**：只设置上限（MAX_TURNS=100）

**轮次不足的原因**：不是description写得不够复杂，而是AI"偷懒"没完成所有步骤。这就是MCPMark要测试的能力。

### 验证清单
在提交任务前，确认：
- [ ] 已人工访问目标网页
- [ ] 已确认信息真实存在于页面上
- [ ] 标准答案基于真实网页内容
- [ ] 已人工测试任务可完成
- [ ] 网页是稳定的（不会频繁变化）
- [ ] 只涉及读操作，无写操作

---

## 📋 出题三要素（必读！）

### 1️⃣ 多步骤推理链

```
✅ 好的任务设计：
   - 访问 2-5 个页面
   - 逐步提取信息
   - 页面间有依赖关系

❌ 禁止：
   - 一个页面即可回答
   - 过于简单的任务
```

### 2️⃣ 信息提取精准性

```
✅ 要求：
   - 明确字段（如：版本号、API字段、枚举值）
   - 明确格式（如：YYYY-MM-DD、x.x.x）

❌ 禁止：
   - "总结页面内容"
   - 模糊的提取要求

原因：verify.py 只能解析具体字段，无法评判"总结"
```

**示例对比：**

| ❌ 错误要求 | ✅ 正确要求 |
|------------|------------|
| "总结这个页面的内容" | "提取以下字段：版本号、发布日期、作者" |
| "介绍一下这个项目" | "输出：PROJECT_NAME, VERSION, LICENSE" |
| "这个库有什么功能" | "列出API endpoint列表，格式：GET /path" |

### 3️⃣ 结构化输出约束

```
✅ 必须要求：
   模型必须输出 <answer>...</answer> 格式

   原因：
   - verify.py 只解析 MCP_MESSAGES
   - 从 messages.json 提取 answer 块
   - 结构化才能自动评判

❌ 禁止：
   - 写入本地文件
   - 违背 Playwright 浏览器获取信息的要求
```

**输出格式示例：**
```
<answer>
PROJECT_NAME: react
VERSION: 18.2.0
LICENSE: MIT
AUTHOR: Facebook
</answer>
```

### 三要素检查表

| 要素 | 检查项 |
|------|--------|
| 多步骤 | 是否需要访问2-5个页面？ |
| 精准性 | 是否要求提取明确字段？ |
| 结构化 | 是否要求`<answer>`格式输出？ |

```
┌─────────────────────────────────────────────────────────┐
│  三个要素缺一不可！                                     │
│                                                         │
│  缺少任何一个 = 任务设计不合格                          │
└─────────────────────────────────────────────────────────┘
```

## 文件路径参考

| 文件 | 路径 |
|------|------|
| 环境配置 | `.mcp_env` |
| 模型配置 | `src/model_config.py` |
| 主程序 | `pipeline.py` |
| 任务目录 | `tasks/playwright/standard/` |
| 结果目录 | `results/{exp_name}/` |
