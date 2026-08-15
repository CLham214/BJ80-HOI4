# The Eighty: 八十崛起

当前版本实现了真实国家标签 `B80`（脚本前缀仍使用 `BJ80_`）及学生自治国策线第一稿，包括：

- 校园民主化与学生共和国成立
- 校园工业、兵工厂与科研建设
- 学生公民军和首都防御
- 朝阳、北京、华北三个阶段的扩张
- 占领区公投核心化决议
- 自治共识动态修正
- 简体中文本地化

## 望京学期制特色机制

- 每 120 天结算一个学期，持续追踪学业进度、校园活力、升学压力与学校声望四项指标。
- 普通路线每学期安排 3 项重点项目；完成“学校属于学生”后开放第 4 个席位。
- 课程包含王选信科、王绶琯科学人才班、数理攻坚、百团招新、食堂改革、跑操制度、工程实践、国际交流与战时课程表。
- 升学压力划分五级：高压能提高科研效率，但会逐步损害稳定、政治点、建设与工厂产出；最高级会难受但不会锁死游戏。
- 食堂可由“超大但排不上队”逐级改造成错峰就餐和中央供餐体系；社团、跑操、睿德项目生、期末成绩单与校誉消费均有多选事件。
- 学生自治、同盟国、教育处、学生公社和日本合作路线各有不同联动加成。

## 国际反应与对手参与

- 新增 0–100 的“国际警觉”指标。八十中占有 2、5、9、16、26 个州时会触发一次性扩张里程碑；持续战争、地方宣战与吞并会继续推高警觉。
- 国际交流与均衡学期可以降低警觉。玩家也可召开记者会、秘密交涉、对中日递交照会、安排公开课程交流，或反向举行军演与边疆情报准备。
- 警觉依次跨过 10、25、45、65、85 后，将触发外国观察团、中日及中共评估、定向制裁、华北遏制会议和最后通牒。
- 中华民国、日本与中共由 AI 独立决定承认、提出条件、军援地方势力、保独、组织遏制或退让；不再只是八十中完成国策后单方面领取外交结果。
- 对察南、鲁系、蒙疆或满洲发动战争时，相关大国会选择旁观、提供装备顾问，或使用 `add_to_war` 真正加入现有战争。
- 拒绝最后通牒后会出现 60 天危机倒计时。玩家可妥协、请求路线赞助国、学生公投化解危机，或先发制人并获得 180 天受困校园动员。
- 高校誉与连续均衡学期（或三次外交胜利）可提交“八十中答卷”，取得永久国际承认并清除主要制裁。

## 国家与地图

HOI4 的国家标签只能使用三个字符，因此设计稿中的 `BJ80` 实际实现为 `B80`。

- 不再拆分自定义州，直接使用原版 `608 北京`，避免创意工坊地图定义错误。
- `608 北京` 开局归 `B80` 所有，并保留中国各势力的原有核心。
- 初始人口 5000、民用工厂 1、军用工厂 0、基础设施 2。
- 原版铁路、补给节点和战略区域继续使用，不修改地图贴图。

当前两个主要战争国策分别提供对察南 `HBC` 和鲁系军阀 `SND` 的吞并战争目标。占领地区仍可通过学生自治决议进行整合。

## 人物与核心

- 国家领导人：任炜东
- 政治顾问：罗静卿、李丁、梁吉峰
- `B80` 开局拥有所有中国势力核心地区的核心
- 国旗源于用户提供的八十中校徽，游戏旗帜已导出为 82×52、41×26 和 10×7 三种 TGA 尺寸

## 爽游平衡

- 全部普通国策统一为 35 天。
- 八个关键事件均为三选一，并提供和平吞并、附属国、外国保独、工业援助、科研跃迁或大规模军援。
- “周边学校的回应”可以无战争吞并察南；“山东问题”可以无战争吞并或附庸鲁系。
- “华北教育革命”可以直接获得京津、河北、察哈尔和山东地块。
- 开局增加 10000 人力、3000 步枪和“天选校园”国家精神。
- 地区整合公投只需 21 天，并会一次性核心化全部已拥有的非核心地区。

## 旧版综合国策草稿

- 从 `BSZ.xh4prj` 导入127个独立国策节点。
- 保留原工程的图标、耗时、前置关系和互斥关系。
- `newfocus_0` 至 `newfocus_92` 使用原汉化名称与描述。
- 后段缺失汉化的33个节点依据图标和分支位置补充了名称与描述。
- 效果按照原版常见强度设置，覆盖政治、外交、工业、科研、陆军、空军、海军和扩张。
- 新树坐标为45–131；既有学生自治线坐标为25–35，二者之间保留10格空隙。
- 生成脚本位于 `tools/generate_legacy_tree.py`，可以在原工程更新后重新导入。

## 四条政治路线

原草稿在“维持正常授课秩序”后设置了四个互斥入口。日本合作线保持原设计，另外三条现已补成完整路线：

- 同盟国民主线：接受英美法援助，可加入同盟国或建立国际教育国家联盟，最终成为东方民主灯塔。
- 教育处集权线：以纪律、考试和职业官僚恢复秩序，通过和平接管、附庸或战争统一华北，建立教育行政国家。
- 学生公社线：建设班级委员会、工学合作社和人民兵工厂，可依靠中共或坚持独立革命，最终建立中华学生公社联盟。
- 日本合作线：保留既有教育、代理扩张、帝国军备、反噬日本和反向傀儡日本内容。

三条续写路线共新增 52 个国策、6 个多选事件和 35 个路线国家精神。新增共享国策位于 `common/national_focus/B80_political_expansion_shared.txt`，不会被旧树生成器覆盖。

## 文件编码

脚本文件使用 UTF-8；HOI4 本地化文件必须保存为 UTF-8 with BOM。提交前应使用游戏错误日志检查本地化编码和脚本引用。

---

# 🤖 面向 AI 协作者的仓库说明（AI ReadMe）

> 本段专为 AI 编程助手编写：请先通读本节再改动本仓库。人类协作者可直接跳过。
> 本节会随仓库演进持续更新；改动任何系统后，请同步更新本节对应条目。

## 1. 仓库身份与模组定位

- 模组名：**The Eighty: 八十崛起**，北京市第八十中学（望京校区）题材的 HOI4 架空历史模组。
- `descriptor.mod`：`version="0.3.0"`，`supported_version="1.19.*"`，Steam 创意工坊 ID `3780267949`。
- 真实国家标签为 **`B80`**（HOI4 限制 3 字符，设计稿 `BJ80` 被缩短）。**脚本前缀两套并存**：学生自治等早期系统用 `BJ80_`，学期制、警觉系统、政治路线等新系统用 `B80_`。新增内容统一用 `B80_` 前缀，除非明确属于学生自治旧系统。
- 开局即拥有原版北京州 `608`（不新建自定义州），并拥有全中国势力的核心州核心（CHI/PRC/GXC/YUN/SHX/XSM/SIK/MAN/MEN/HBC/SND 的核心全部 `add_core_of = B80`）。
- 平衡哲学：**爽游**。开局 10000 人力、3000 步枪、四枚强力国家精神；普通国策统一 35 天；学生自治线每个国策都带"爽游基底"（+100 政治点 / +0.03 稳定 / +2500 人力）；关键事件多为三选一且数值慷慨。升学压力是唯一会"难受"的软惩罚，但刻意设计为不锁死游戏。

## 2. 目录地图

```
common/
  characters/           12 名人物：任炜东（开局领袖，despotism）、顾问、将领
  countries/            国家定义（graphical_culture = asian_gfx）
  country_leader/       领袖特质 B80_pragmatic_education_helmsman 等 8 个
  country_tags/         B80 = "countries/B80 - The Eighty.txt"
  decisions/            三个决策系统（学期项目 / 外交反应 / 占领区整合）
  decisions/categories/ 对应三个决策分类
  ideas/                六组国家精神：starting / campus_mechanic / opponent_reaction / political_route / legacy / student_autonomy
  national_focus/       三个国策文件（见第 3 节）
  on_actions/           学期初始化(on_startup)、警觉月度结算(on_monthly_B80)、战争/吞并反应(on_war_relation_added / on_annex)
  opinion_modifiers/    外交意见修饰符（value 必须为数字，decay 必须为数字，不能用 yes/no）
  scripted_effects/     三个系统的共享效果函数（命名全部 `B80_*` / `BJ80_*`）
  scripted_triggers/    共享触发条件
events/                 五个命名空间：BJ80_autonomy / B80_campus / B80_opponents / B80_political / B80_legacy
gfx/                    国旗（含各 cosmetic tag 与四种意识形态旗）、领导人/顾问 DDS 头像、旗帜源 PNG
history/countries/      国家历史（科技、政治、人物、开局国家精神、初始化调用）
history/states/         608 北京州（B80 所有，含 CHI/PRC 核心）
history/units/          学生警卫师模板 + 1 个开局师
interface/              B80_portraits.gfx 头像映射
localisation/simp_chinese/  8 个简体中文本地化文件（UTF-8 with BOM，必须！）
tools/                  4 个 Python 工具（见第 7 节）
```

## 3. 国策树结构（common/national_focus/）

| 文件 | 内容 | 维护方式 |
|---|---|---|
| `BJ80_student_autonomy.txt` | 手写学生自治主线（25 个 focus，坐标 x25–35），树尾部用 `shared_focus =` 挂载政治扩展与 127 个旧国策 | 手写维护；`# BEGIN/END` 注释段由生成器管理，手写段不要放进生成段 |
| `B80_political_expansion_shared.txt` | 手写续写的三条政治路线共 52 个 shared_focus（同盟国民主线 / 教育处集权线 / 学生公社线），坐标 x41–67 | 手写维护 |
| `B80_legacy_shared_focuses.txt` | 127 个旧版国策节点（`B80_legacy_newfocus_N`），坐标 x45–131，含日本合作线 | **生成文件，勿手改**；由 `tools/generate_legacy_tree.py` 重新生成 |

四条政治路线在旧树的四个互斥入口（`newfocus_9` 同盟国民主 / `newfocus_10` 教育处 / `newfocus_11` 学生公社 / `newfocus_12` 日本合作）之后分叉，每条最终 `set_cosmetic_tag`。所有 cosmetic tag：`BJ80_STUDENT_REPUBLIC`、`BJ80_NEW_BEIJING_REPUBLIC`、`BJ80_CHINESE_STUDENT_REPUBLIC`、`B80_EASTERN_DEMOCRATIC_REPUBLIC`、`B80_EDUCATION_ADMINISTRATION`、`B80_STUDENT_COMMUNE`、`B80_CHINESE_STUDENT_COMMUNE`。

## 4. 三个核心系统

### 4.1 望京学期制（B80_campus_* / campus mechanic）
- 以 **120 天任务倒计时**（decision `B80_semester_countdown`，`days_mission_timeout = 120`）为一个学期；超时触发隐藏事件 `B80_campus.10` → `B80_finish_semester` 结算 → 结算事件再通过 `B80_campus.70` 重新激活下个学期任务。
- 四项玩家可见变量（0–100，`B80_clamp_campus_values` 钳制）：`B80_academic_progress` 学业进度、`B80_campus_vitality` 校园活力、`B80_admission_pressure` 升学压力、`B80_school_reputation` 学校声望。另有内部变量 `B80_semester_projects`（本学期已做项目数）、`B80_semester_number`、`B80_balanced_semester_streak`（连续均衡学期数）。
- 每学期最多 3 个重点项目（完成国策 `BJ80_the_school_belongs_to_students` 后开放第 4 个，见触发器 `B80_has_semester_project_slot`）。9 个学期项目决策：王选信科、王绶琯科学人才班、数理攻坚、百团招新、食堂改革、跑操制度、工程实践、国际交流、战时课程表（`B80_took_*_project` 旗标防重复）。
- 升学压力五级国家精神（`B80_admission_pressure_relaxed/balanced/intense/all_out/breaking_point`），由 `B80_update_admission_pressure_idea` 依据变量动态切换；完成教育处国策 `B80_legacy_newfocus_10` 后阈值放宽。
- 其他子系统：食堂三级升级（`B80_improve_cafeteria`：排队→错峰→中央供餐）、社团四波（百团招新事件 `B80_campus.20`）、跑操三政策（`B80_campus.40`）、睿德项目生（`B80_campus.50`，240 天国家精神）、院士讲座、望京教育论坛（`B80_campus.60`）、校友网络。声望消耗型决策：睿德招生 25、院士讲座 25、教育论坛 40、校友网络 35。
- 连续 3 次均衡学期 → 永久国家精神 `B80_wangjing_education_model` +1 科研槽。

### 4.2 国际警觉系统（B80_opponents.* / opponent reaction）
- 玩家变量 `B80_expansion_alarm`（0–100）与 `B80_diplomatic_victories`；`on_monthly_B80` 调用 `B80_update_opponent_reaction` 月度结算：占领里程碑（2/5/9/16/25 州各一次性 +10~20）、战争状态 +2/月、声望 >70 −2/月。
- 警觉跨过 10/25/45/65/85 依次触发五阶段：外国观察团（`B80_opponents.1`）→ 中日/中共评估（`.10/.20/.30`，由 CHI/JAP/PRC 各自 AI 三选一）→ 定向制裁（`.40`）→ 华北遏制会议（`.50`）→ 最后通牒（`.60`）。
- 对察南 HBC / 鲁系 SND / 蒙疆 MEN / 满洲 MAN 开战时，`on_war_relation_added` 与 `on_annex` 驱动大国反应：军援、`add_to_war` 真正参战或旁观。
- 拒绝通牒 → 60 天危机倒计时任务 `B80_containment_crisis_countdown`（`B80_crisis_active` / `B80_crisis_against_china|japan` 旗标），超时后 CHI/JAP 获得吞并战争目标（隐藏事件 `B80_opponents.70`）。化解途径：妥协（`B80_last_minute_compromise`）、路线赞助国（`B80_seek_patron_support` → `B80_receive_route_patron_support`）、学生公投（`B80_public_student_referendum`）、先发制人（`B80_preempt_containment`）。
- 终局：声望 >50 且（连续均衡学期 ≥2 或外交胜利 ≥3）时可提交"八十中答卷"（`B80_submit_eighty_report` → `B80_secure_international_recognition`），获得永久国际承认并清除主要制裁。
- 相关国家精神集中在 `B80_opponent_reaction_ideas.txt`；外交决策在 `B80_opponent_reaction_decisions.txt`（记者会、密谈、军演、递交照会、边疆情报准备等）。

### 4.3 学生自治与占领区整合（BJ80_*）
- 学生自治线：学校属于学生 → 学生代表会 → 工业/军事双分支 → 学生共和国（`BJ80_proclaim_student_republic`，民主化，cosmetic tag）→ 朝阳/北京扩张 → 华北教育革命 → 青年的共和国（终局）。
- 自治共识五级国家精神（`BJ80_autonomy_consensus_1..5`），由 `BJ80_raise/lower_autonomy_consensus` 升降级；"学校属于学生"直接给 `_2`。
- 占领区整合三连决策：建立地方学生委员会（10 PP）→ 恢复教育秩序（15 PP）→ 举行加入共和国公投（25 PP，21 天，一次性把全部非核心州核心化并 +1 共享建筑槽）。

## 5. 命名、ID 与引用约定（AI 必读）

- **事件命名空间**：`BJ80_autonomy`（学生自治）、`B80_campus`（学期）、`B80_opponents`（警觉）、`B80_political`（政治路线）、`B80_legacy`（旧事件）。事件 ID 格式 `命名空间.数字`。
- **变量**：全部以 `B80_` 开头（见 4.1/4.2 清单），新增变量请先全局搜索避免与既有变量冲突。
- **旗标**：学期项目用 `B80_took_*_project`；系统初始化用 `B80_campus_system_initialized` / `B80_opponent_system_initialized`；警觉用 `B80_alarm_milestone_N`、`B80_opposition_stage_N`、`B80_crisis_*`、`B80_international_recognition_secured`；整合用 `BJ80_*_integration_enabled`。
- **国家精神**：`B80_*` / `BJ80_*` 小写下划线风格，`allowed = { original_tag = B80 }`（对手用的精神如 `B80_frontier_mobilization` 用 `allowed = { always = yes }`）。
- **本地化键**：国策 `id_desc`、事件 `id.t` / `id.d` / 选项 `id.a|b|c...`，全部在 `localisation/simp_chinese/` 下，**必须 UTF-8 with BOM**。新增任何文本都要补本地化，否则游戏内显示键名。
- **编码**：脚本文件 UTF-8 无 BOM；本地化文件 UTF-8 with BOM。`tools/validate_mod.py` 会检查。

## 6. 关键初始化链路

- 开局：`history/countries` 调用 `B80_initialize_campus_system = yes` 与 `B80_initialize_opponent_system = yes`（人类玩家）；`on_actions/on_startup` 对 AI 的 B80 做同样初始化（`is_ai = yes` 判断，`B80_*_initialized` 旗标防重）。
- 学期任务链：`B80_campus.1`（欢迎事件）→ `activate_mission = B80_semester_countdown` → 120 天后 `B80_campus.10` → `B80_finish_semester`（分支到 `B80_campus.11..16`）→ 各结算事件末尾 `B80_begin_new_semester`（重置项目数、扣底值、`B80_campus.70` 重启任务）。
- 警觉链：`on_monthly_B80` → `B80_update_opponent_reaction` → 各阶段事件（事件内 `ai_chance` 控制 AI 行为）→ 玩家决策/事件改变变量。

## 7. 工具（tools/）

| 脚本 | 用途 | 何时运行 |
|---|---|---|
| `validate_mod.py` | 全套静态校验：括号配平、BOM 检查、国策数量（127 legacy + 52 political + 25 学生自治爽游基底，ID 唯一、坐标不冲突、互斥对称）、事件/国家精神引用完整性、学期制不变量（120 天任务、四变量本地化、事件集、食堂三连等）、意见修饰符 decay 数值化、旧状态 1082 不存在等 | **每次提交前必跑**：`python tools/validate_mod.py`，输出 `VALIDATION_OK` 才可推送。⚠ 脚本内含数量/集合断言，**新增内容时必须同步修改**（见第 8 节） |
| `generate_legacy_tree.py` | 从 `BSZ.xh4prj`（XMind 工程）重新生成旧国策树与汉化；含缺失汉化补全表 | 仅当旧工程更新国策时；**会覆盖** `B80_legacy_shared_focuses.txt`，生成后必须重跑校验 |
| `boost_autonomy_focuses.py` | 一次性批量注入"爽游基底"的历史脚本（硬编码路径 `E:\钢铁雄心4mod`） | **不要再运行**（已生效，路径也是本机旧路径） |
| `sanitize_hoi4_text.py` | 一次性图片 token 迁移脚本 | 不要再运行 |

## 8. 新增内容操作规程（国策 / 国家精神 / 事件 / 其他）

> 本节回答一个问题：**未来新增内容时，仓库要动哪些文件、README 要动哪些条目、validate_mod.py 要动哪些断言**。
> 当前规模快照（与 validate 输出对应）：`shared_focuses=179 (legacy=127, political=52)`、`autonomy_focuses=25`、`custom_ideas=153`、`event_calls=47`、人物 12 名、事件命名空间 5 个。

### 8.1 总流程（所有新增通用）

1. **查重**：先全局搜索拟用的 ID / 变量 / 旗标 / 事件编号，避免与既有内容冲突（`grep` 全仓）。
2. **选归属文件**：按下方分类表决定内容放哪个文件；新系统可新建文件。
3. **写脚本 + 写本地化**：脚本 UTF-8 无 BOM；本地化 UTF-8 with BOM（键名与脚本引用逐字一致）。
4. **同步改 `tools/validate_mod.py`**：凡触及数量/集合断言的，必须同步修改（见 8.2–8.4），否则校验必然失败。
5. **跑校验**：`python tools/validate_mod.py` 直到 `VALIDATION_OK`。
6. **同步 README**：按 8.7 的清单更新本节及第 2–5 节相关条目。
7. **提交（遵守第 10 节第 4 条）**：AI 完成改动后**停在这里**，把改动清单报告给维护者；维护者本地校验（`validate_mod.py` 输出 `VALIDATION_OK` 等）通过后，由维护者本人提交，或明确指示 AI 提交（`git add` → commit 简短中文说明 → `git pull` 确认同步 → push main）。**AI 不得在未获指示前自行提交。**

### 8.2 新增国策（focus）

| 归属 | 文件 | 坐标区 | validate_mod.py 联动 |
|---|---|---|---|
| 学生自治主线 | `common/national_focus/BJ80_student_autonomy.txt`（手写段） | x25–35 | 若带"爽游基底"（`# Overpowered student-autonomy baseline` + 三件套），**必须**把 `autonomy.count(...) != 25` 的期望数改大（第 125 行附近） |
| 政治路线扩展 | `common/national_focus/B80_political_expansion_shared.txt` | x41–67 | **必须**更新 `len(political_focus_blocks) != 52` 的期望数（第 79 行附近），并在 `BJ80_student_autonomy.txt` 的 `BEGIN HAND-WRITTEN POLITICAL EXPANSION BRANCHES` 段用 `shared_focus =` 挂载 |
| 旧版树 | `common/national_focus/B80_legacy_shared_focuses.txt` | x45–131 | **勿手改**（生成文件）；改 `tools/generate_legacy_tree.py` 后重新生成；127 的断言由生成器保证 |

其他硬性要求（validate 自动检查）：
- 坐标 `(x,y)` 不得与任何既有节点重复；新增前先扫描同区域坐标。
- `mutually_exclusive` 必须对称（A 互斥 B，B 也要互斥 A）。
- `cost = 5`（35 天）为默认；终局国策可用 `cost = 10`。
- 本地化：`国策ID` + `国策ID_desc` 两个键。
- 图标用原版 `GFX_goal_*` / `GFX_focus_*`，不引入新图标文件。
- 若新国策引用 `add_ideas` / `country_event`，被引用的对象必须真实存在（validate 会查引用完整性）。

### 8.3 新增国家精神（idea）

- **归属**：按系统放入现有 6 个 ideas 文件（`B80_starting_ideas` / `B80_campus_mechanic_ideas` / `B80_opponent_reaction_ideas` / `B80_political_route_ideas` / `B80_legacy_ideas` / `BJ80_student_autonomy_ideas`）；全新系统可新建 `B80_xxx_ideas.txt`。
- `allowed = { original_tag = B80 }`（玩家精神）；对手专用精神用 `allowed = { always = yes }`（如 `B80_frontier_mobilization`）。
- `picture` 用原版 `generic_*`；本地化 `ID` + `ID_desc`。
- validate 自动校验：所有 `add_ideas` / `idea =` 引用必须存在；⚠ 下列 7 个"易重复授予"精神**只允许被一个国策直接授予**（`repeat_prone_ideas` 断言）：`B80_legacy_academic_network`、`B80_legacy_aviation_society`、`B80_legacy_campus_democracy`、`B80_legacy_japanese_manufacturers`、`B80_legacy_orderly_teaching`、`B80_legacy_student_welfare`、`B80_legacy_trade_committee`。升级类国家精神请用 `swap_ideas`，不要重复 `add_ideas`。
- 若需按国策解锁：在 idea 上加 `visible = { has_completed_focus = ... }`（参考人物顾问写法）。

### 8.4 新增事件（event）

- **归属**：按命名空间放入 5 个事件文件（`BJ80_autonomy` → `events/BJ80_student_autonomy_events.txt`；`B80_campus` → `events/B80_campus_mechanic_events.txt`；`B80_opponents` → `events/B80_opponent_reaction_events.txt`；`B80_political` → `events/B80_political_events.txt`；`B80_legacy` → `events/B80_legacy_events.txt`）。新系统新建文件并在文件首行 `add_namespace = B80_xxx`。
- 事件 ID 用 `命名空间.数字`，数字递增避免撞号；被引用的事件必须定义（validate 查 `country_event = { id = ... }` 引用完整性）。
- 本地化：`ID.t`（标题）、`ID.d`（正文）、每个选项 `ID.a` / `ID.b` ...；`hidden = yes` 事件只需保证被引用，本地化键可省略（validate 对隐藏事件跳过文本检查）。
- **validate 联动（campus 专用）**：`B80_campus` 命名空间的事件集被 `expected_campus_events` 集合严格断言（第 248 行附近）——**新增/删除 `B80_campus.N` 事件必须同步改该集合**；且非隐藏 campus 事件的 `t/d/选项` 本地化键会被逐一检查，缺一个就报错。其他命名空间无集合断言，但 `event_defs` 全集仍会做引用完整性检查。
- 跨国家事件（发给 CHI/JAP/PRC/HBC 等）：用 `ROOT`/`FROM` 语义，`ai_chance` 控制 AI 选择权重（参考 `B80_opponents.10/.20/.30`、`B80_political.10/.20/.30`）。

### 8.5 新增决策（decision）

- **归属**：放入对应系统的 decisions 文件（学期/外交/整合），新系统新建文件并在 `decisions/categories/` 加对应分类（`B80_xxx_categories.txt`）。
- 任务型决策（倒计时/可重复）参考 `B80_semester_countdown` 的写法：`days_mission_timeout` + `timeout_effect` + `selectable_mission = no`。
- 一次性决策用 `fire_only_once = yes`；冷却用 `days_re_enable`；`available`/`visible` 区分"可点"与"可见"。
- 本地化：分类 `分类ID` + `分类ID_desc`、决策 `决策ID` + `决策ID_desc`。

### 8.6 其他类型新增

- **变量 / 旗标**：一律 `B80_` 前缀（旧自治系统可 `BJ80_`）；新增前全局 grep；用后记得在 `B80_clamp_campus_values` / `B80_clamp_opponent_values` 等钳制函数中登记（如 0–100 变量）。README 第 5 节清单同步补充。
- **cosmetic tag**：`gfx/flags/`（大 82×52）、`medium/`（41×26）、`small/`（10×7）三个 TGA + 本地化 `TAG_意识形态` 三键（参考 `BJ80_STUDENT_REPUBLIC_democratic` 等）；源图放 `gfx/flags/source/`。
- **人物**：`common/characters/` + `gfx/leaders/B80/` 大头像 DDS + `gfx/interface/ideas/` 小头像 DDS + `interface/B80_portraits.gfx` 两个 sprite 映射 + 本地化姓名 + `history/countries` 里 `recruit_character`。
- **意见修饰符**：`common/opinion_modifiers/`，`value` 必须数字，`decay` 必须数字（不能 yes/no，validate 检查）。
- **开局配置**：改 `history/countries/B80 - The Eighty.txt` 或 `history/states/608-Beijing.txt`；不要新建自定义州（历史教训：旧自定义州 1082 已被移除，validate 会阻止它复活）。

### 8.7 对 README（本 AI ReadMe）的同步义务

每次新增内容后，至少更新以下条目，保证下一位 AI 协作者看到的是真实状态：

1. **本节开头"当前规模快照"**：国策数（179+新增）、国家精神数（153+新增）、事件命名空间数、人物数。
2. **第 2 节日录地图**：新文件、新目录、新本地化文件。
3. **第 3 节国策树**：国策数量与挂载位置变化。
4. **第 4 节系统描述**：新机制/新子系统的段落；新系统在这里加 4.x 小节。
5. **第 5 节命名约定**：新变量、新旗标、新命名空间、新 ID 规则。
6. **第 7 节工具表**：validate 断言数字的变化记录。
7. **第 8 节本节**：新增类型与联动断言（如新的集合断言、新的文件归属）。

## 9. 已知注意事项 / 陷阱

- `B80_legacy_shared_focuses.txt` 是生成文件：手写改动会在下次生成时丢失；需要改旧树请改生成脚本或改政治扩展文件。
- 学生自治树有 `# BEGIN/END GENERATED LEGACY SHARED FOCUSES` 注释段，生成器按注释段整段替换。
- 旧树国策 `B80_legacy_newfocus_5/1/4/6` 是"花钱买州"（−200 PP 换州核心），`B80_legacy_newfocus_38_5` 存在（校验允许 127 个 ID 中含此特例）。
- `history/states/608-Beijing.txt` 的人力和建筑是原版北京数据增强版（人口 964 万、infra 3、2 民用厂、空港 3、故宫地标），不要改成自定义州。
- 中国相关原版 TAG：CHI 民国、PRC 中共、HBC 察南、SND 鲁系、MEN 蒙疆、MAN 满洲；世界大国：ENG/USA/FRA/SOV/JAP。
- 若游戏内出现键名不翻译：先查本地化文件是否为 UTF-8 with BOM，再查键名与脚本引用是否一致。
- 新增国策/事件/国家精神后，若 validate_mod 报 missing，先全局 grep 确认拼写，再检查文件是否被 `allowed` 条件隐藏。

## 10. 协作约定（重要）

本仓库为 **两人团队** 共同维护，两位成员均通过 AI 辅助编程。约定如下：

1. **直接推 `main`**：不使用 fork，不强制走 PR。有需要就直接 commit + push 到 `main`。
2. **推送前先拉取**：`git pull`（或 `git fetch` + `git merge`）保持本地与 `origin/main` 同步，避免互相覆盖；冲突时优先保留双方意图（必要时在群里沟通）。
3. **git 身份独立**：两位成员各自使用独立的 `user.name` / `user.email`，提交时注意 `git config user.name` 是否为自己的身份。
4. **提交权限（最重要，强制）**：AI 助手完成任何文本改动后**不得自行 `git commit` / `git push`**。所有改动必须先由维护者在本地校验通过，之后**由维护者本人提交，或在维护者明确指示"提交"后** AI 才可执行 git 操作。AI 在未获指示前只能报告改动内容并等待确认。
5. **本地校验流程（提交前必做）**：维护者本地运行 `python tools/validate_mod.py`，必须输出 `VALIDATION_OK` 方可提交；必要时再用游戏错误日志复核（脚本 UTF-8 无 BOM、本地化 UTF-8 with BOM、无键名不翻译）。
6. **编码纪律**：脚本 UTF-8 无 BOM；本地化 UTF-8 with BOM；提交后可用游戏错误日志复核。
7. **改动留痕**：重大机制改动请同步更新本 README 的对应章节（尤其是本节 AI ReadMe），保证 AI 协作者在下一次会话能快速恢复上下文——AI 的记忆不跨会话，仓库文档才是持久记忆。
8. **提交信息**：简短中文描述即可（如 `学期制：新增期末成绩单事件`），方便另一人（和 AI）从 `git log` 快速定位改动。
