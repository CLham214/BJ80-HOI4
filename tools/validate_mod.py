from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def blocks(text: str, header: str) -> list[str]:
    result: list[str] = []
    for match in re.finditer(rf"(?m)^{re.escape(header)}\s*=\s*\{{", text):
        opening = text.find("{", match.start())
        depth = 0
        for index in range(opening, len(text)):
            depth += text[index] == "{"
            depth -= text[index] == "}"
            if depth == 0:
                result.append(text[match.start():index + 1])
                break
    return result


errors: list[str] = []

if (ROOT / "history/states/1082-BJ80 Campus.txt").exists():
    errors.append("obsolete custom state 1082 still exists")

country_history = (ROOT / "history/countries/B80 - The Eighty.txt").read_text(encoding="utf-8")
beijing_state = (ROOT / "history/states/608-Beijing.txt").read_text(encoding="utf-8")
if not re.search(r"(?m)^capital\s*=\s*608\s*$", country_history):
    errors.append("B80 capital must be vanilla Beijing state 608")
if not re.search(r"(?m)^\s*owner\s*=\s*B80\s*$", beijing_state):
    errors.append("state 608 must be owned by B80")
if "9843" not in beijing_state:
    errors.append("Beijing province 9843 is missing from state 608")

oob_path = ROOT / "history/units/B80_1936.txt"
division_names_path = ROOT / "common/units/names_divisions/B80_names_divisions.txt"
if not oob_path.exists() or not division_names_path.exists():
    errors.append("B80 starting OOB or division name groups are missing")
else:
    oob_text = oob_path.read_text(encoding="utf-8")
    division_names_text = division_names_path.read_text(encoding="utf-8")
    if len(re.findall(r"(?m)^\s*division\s*=\s*\{", oob_text)) != 4:
        errors.append("B80 must start with four campus divisions")
    required_name_groups = {"B80_INF_01", "B80_GAR_01", "B80_CAV_01", "B80_ARM_01"}
    present_name_groups = set(re.findall(r"(?m)^(B80_[A-Z0-9_]+)\s*=\s*\{", division_names_text))
    if not required_name_groups.issubset(present_name_groups):
        errors.append(f"missing division name groups: {sorted(required_name_groups - present_name_groups)}")

for variant_name in ["八十式校卫步枪", "望京综合保障套件"]:
    if variant_name not in country_history:
        errors.append(f"missing starting equipment variant: {variant_name}")

opinion_modifiers = (ROOT / "common/opinion_modifiers/BJ80_opinion_modifiers.txt").read_text(encoding="utf-8")
if re.search(r"(?m)^\s*decay\s*=\s*(?:yes|no)\s*$", opinion_modifiers):
    errors.append("opinion modifier decay must be numeric, not yes/no")

script_files = [
    path for path in ROOT.rglob("*.txt")
    if "localisation" not in path.parts
]
for path in script_files:
    data = path.read_bytes()
    text = data.decode("utf-8-sig")
    if data.startswith(b"\xef\xbb\xbf"):
        errors.append(f"BOM in script file: {path.relative_to(ROOT)}")
    if text.count("{") != text.count("}"):
        errors.append(f"unbalanced braces: {path.relative_to(ROOT)}")

required_campus_files = [
    ROOT / "common/decisions/B80_campus_semester_decisions.txt",
    ROOT / "common/decisions/categories/B80_campus_mechanic_categories.txt",
    ROOT / "common/ideas/B80_campus_mechanic_ideas.txt",
    ROOT / "common/on_actions/B80_campus_on_actions.txt",
    ROOT / "common/scripted_effects/B80_campus_mechanic_effects.txt",
    ROOT / "common/scripted_triggers/B80_campus_mechanic_triggers.txt",
    ROOT / "events/B80_campus_mechanic_events.txt",
    ROOT / "localisation/simp_chinese/B80_campus_mechanic_l_simp_chinese.yml",
]
missing_campus_files = [str(path.relative_to(ROOT)) for path in required_campus_files if not path.exists()]
if missing_campus_files:
    errors.append(f"missing campus mechanic files: {missing_campus_files}")

tree_path = ROOT / "common/national_focus/B80_legacy_shared_focuses.txt"
tree = tree_path.read_text(encoding="utf-8")
legacy_focus_blocks = blocks(tree, "shared_focus")
legacy_focus_ids = [re.search(r"(?m)^\s*id\s*=\s*(\S+)", block).group(1) for block in legacy_focus_blocks]
if len(legacy_focus_ids) != 127 or len(set(legacy_focus_ids)) != 127:
    errors.append(f"expected 127 unique legacy shared focuses, got {len(legacy_focus_ids)}/{len(set(legacy_focus_ids))}")

political_tree_path = ROOT / "common/national_focus/B80_political_expansion_shared.txt"
political_tree = political_tree_path.read_text(encoding="utf-8")
political_focus_blocks = blocks(political_tree, "shared_focus")
political_focus_ids = [re.search(r"(?m)^\s*id\s*=\s*(\S+)", block).group(1) for block in political_focus_blocks]
if len(political_focus_ids) != 52 or len(set(political_focus_ids)) != 52:
    errors.append(f"expected 52 unique political shared focuses, got {len(political_focus_ids)}/{len(set(political_focus_ids))}")

endgame_tree_path = ROOT / "common/national_focus/B80_political_endgame_shared.txt"
endgame_tree = endgame_tree_path.read_text(encoding="utf-8")
endgame_focus_blocks = blocks(endgame_tree, "shared_focus")
endgame_focus_ids = [re.search(r"(?m)^\s*id\s*=\s*(\S+)", block).group(1) for block in endgame_focus_blocks]
if len(endgame_focus_ids) != 32 or len(set(endgame_focus_ids)) != 32:
    errors.append(f"expected 32 unique political endgame focuses, got {len(endgame_focus_ids)}/{len(set(endgame_focus_ids))}")

focus_blocks = legacy_focus_blocks + political_focus_blocks + endgame_focus_blocks
focus_ids = legacy_focus_ids + political_focus_ids + endgame_focus_ids
if len(focus_ids) != len(set(focus_ids)):
    errors.append("duplicate IDs across legacy and political shared focuses")

focus_by_id = dict(zip(focus_ids, focus_blocks))
all_refs = set(re.findall(r"focus\s*=\s*(B80_[A-Za-z0-9_]+)", tree + "\n" + political_tree + "\n" + endgame_tree))
missing_refs = all_refs - set(focus_ids)
if missing_refs:
    errors.append(f"missing focus references: {sorted(missing_refs)}")

tree_membership = (ROOT / "common/national_focus/BJ80_student_autonomy.txt").read_text(encoding="utf-8")
political_roots = {
    "B80_allied_public_broadcast",
    "B80_discipline_code",
    "B80_all_student_congress",
}
endgame_roots = {
    "B80_endgame_national_education_assembly",
    "B80_endgame_national_examination_government",
    "B80_endgame_second_all_student_congress",
    "B80_endgame_tear_up_the_unequal_school_pact",
}
included_political_roots = set(re.findall(r"shared_focus\s*=\s*(B80_[A-Za-z0-9_]+)", tree_membership))
if not political_roots.issubset(included_political_roots):
    errors.append(f"political shared roots missing from B80 tree: {sorted(political_roots - included_political_roots)}")
if not endgame_roots.issubset(included_political_roots):
    errors.append(f"political endgame roots missing from B80 tree: {sorted(endgame_roots - included_political_roots)}")

coordinates: dict[tuple[int, int], str] = {}
for focus_id, block in zip(focus_ids, focus_blocks):
    x_match = re.search(r"(?m)^\s*x\s*=\s*(-?\d+)", block)
    y_match = re.search(r"(?m)^\s*y\s*=\s*(-?\d+)", block)
    if not x_match or not y_match:
        continue
    coordinate = (int(x_match.group(1)), int(y_match.group(1)))
    if coordinate in coordinates:
        errors.append(f"shared focus coordinate collision {coordinate}: {coordinates[coordinate]} / {focus_id}")
    coordinates[coordinate] = focus_id

mutual: dict[str, set[str]] = {}
for focus_id, block in focus_by_id.items():
    mutual[focus_id] = set(re.findall(r"mutually_exclusive\s*=\s*\{\s*focus\s*=\s*(\S+)", block))
for focus_id, targets in mutual.items():
    for target in targets:
        if focus_id not in mutual.get(target, set()):
            errors.append(f"asymmetric mutual exclusion: {focus_id} -> {target}")

autonomy = (ROOT / "common/national_focus/BJ80_student_autonomy.txt").read_text(encoding="utf-8")
if "$15" in autonomy:
    errors.append("literal $15 remains in autonomy focus tree")
autonomy_focus_count = len(re.findall(r"(?m)^\s*focus\s*=\s*\{", autonomy))
if autonomy_focus_count != 25:
    errors.append(f"expected 25 autonomy focuses, got {autonomy_focus_count}")
if "# Overpowered student-autonomy baseline" in autonomy:
    errors.append("obsolete overpowered autonomy baseline remains")

required_snippets = {
    "B80_legacy_newfocus_19": "add_research_slot = 1",
    "B80_legacy_newfocus_28": "create_intelligence_agency = yes",
    "B80_legacy_newfocus_37": "add_ideas = war_economy",
    "B80_legacy_newfocus_47": "add_research_slot = 1",
    "B80_legacy_newfocus_72": "type = air_base level = 4",
    "B80_legacy_newfocus_83": "navy_experience = 40",
    "B80_legacy_newfocus_91": "cv_small_plane_naval_bomber_airframe_0",
    "B80_legacy_newfocus_115": "type = arms_factory level = 2",
}
for focus_id, snippet in required_snippets.items():
    if snippet not in focus_by_id.get(focus_id, ""):
        errors.append(f"semantic assertion failed for {focus_id}: {snippet}")

# Legacy focuses are generated from a name-only draft. Guard the hand-designed
# route identities so future generator changes cannot silently turn mutually
# exclusive choices back into identical generic rewards.
route_identity_snippets = {
    "B80_legacy_newfocus_61": "B80_legacy_cavalry_tank_group",
    "B80_legacy_newfocus_62": "B80_legacy_infantry_tank_coordination",
    "B80_legacy_newfocus_63": "哈基米中型坦克",
    "B80_legacy_newfocus_64": "哆啦B梦重型坦克",
    "B80_legacy_newfocus_68": "B80_legacy_multirole_air_tactics",
    "B80_legacy_newfocus_69": "B80_legacy_strategic_bombing_tactics",
    "B80_legacy_newfocus_70": "B80_legacy_rapid_air_assault",
    "B80_legacy_newfocus_84": "B80_legacy_big_gun_fleet",
    "B80_legacy_newfocus_85": "B80_legacy_submarine_blade",
    "B80_legacy_newfocus_86": "B80_legacy_naval_aviation",
    "B80_legacy_newfocus_88": "focus = B80_legacy_newfocus_86",
    "B80_legacy_newfocus_89": "focus = B80_legacy_newfocus_85",
}
for focus_id, snippet in route_identity_snippets.items():
    if snippet not in focus_by_id.get(focus_id, ""):
        errors.append(f"route identity assertion failed for {focus_id}: {snippet}")

# These ideas used to be granted literally by multiple focuses, making every
# later grant a no-op. Conditional upgrade/fallback references are allowed, but
# direct grants in completion rewards must now be unique.
repeat_prone_ideas = {
    "B80_legacy_academic_network",
    "B80_legacy_aviation_society",
    "B80_legacy_campus_democracy",
    "B80_legacy_japanese_manufacturers",
    "B80_legacy_orderly_teaching",
    "B80_legacy_student_welfare",
    "B80_legacy_trade_committee",
}
for idea_id in repeat_prone_ideas:
    granting_focuses = sum(
        bool(re.search(rf"add_ideas\s*=\s*{re.escape(idea_id)}\b", block))
        for block in focus_blocks
    )
    if granting_focuses > 1:
        errors.append(f"repeat-prone idea is referenced as a reward by {granting_focuses} focuses: {idea_id}")

idea_ids: set[str] = set()
for path in (ROOT / "common/ideas").glob("*.txt"):
    idea_ids.update(re.findall(r"(?m)^\s{2,}([A-Za-z0-9_]+)\s*=\s*\{", path.read_text(encoding="utf-8")))
idea_refs = set()
for path in [tree_path, political_tree_path, endgame_tree_path, ROOT / "common/national_focus/BJ80_student_autonomy.txt", *list((ROOT / "events").glob("*.txt"))]:
    text = path.read_text(encoding="utf-8")
    idea_refs.update(re.findall(r"add_ideas\s*=\s*(B(?:80|J80)_[A-Za-z0-9_]+)", text))
    idea_refs.update(re.findall(r"idea\s*=\s*(B(?:80|J80)_[A-Za-z0-9_]+)", text))
missing_ideas = idea_refs - idea_ids
if missing_ideas:
    errors.append(f"missing custom ideas: {sorted(missing_ideas)}")

event_defs: set[str] = set()
for path in (ROOT / "events").glob("*.txt"):
    event_defs.update(re.findall(r"(?m)^\s*id\s*=\s*(B(?:80|J80)_[A-Za-z0-9_.]+)", path.read_text(encoding="utf-8")))
event_calls = set()
event_call_paths = [
    tree_path,
    political_tree_path,
    endgame_tree_path,
    ROOT / "common/national_focus/BJ80_student_autonomy.txt",
    *list((ROOT / "common/decisions").glob("*.txt")),
    *list((ROOT / "common/scripted_effects").glob("*.txt")),
]
for path in event_call_paths:
    event_calls.update(re.findall(r"country_event\s*=\s*\{\s*id\s*=\s*(B(?:80|J80)(?:_[A-Za-z0-9_]+)?\.[A-Za-z0-9_.]+)", path.read_text(encoding="utf-8")))
missing_events = event_calls - event_defs
if missing_events:
    errors.append(f"missing events: {sorted(missing_events)}")

# Wangjing semester mechanic invariants. These assertions guard the 120-day
# loop, the four player-facing variables and the delayed mission restart.
if not missing_campus_files:
    campus_decisions = (ROOT / "common/decisions/B80_campus_semester_decisions.txt").read_text(encoding="utf-8")
    campus_effects = (ROOT / "common/scripted_effects/B80_campus_mechanic_effects.txt").read_text(encoding="utf-8")
    campus_events = (ROOT / "events/B80_campus_mechanic_events.txt").read_text(encoding="utf-8")
    campus_ideas = (ROOT / "common/ideas/B80_campus_mechanic_ideas.txt").read_text(encoding="utf-8")
    campus_on_actions = (ROOT / "common/on_actions/B80_campus_on_actions.txt").read_text(encoding="utf-8")
    campus_loc_path = ROOT / "localisation/simp_chinese/B80_campus_mechanic_l_simp_chinese.yml"
    campus_loc_data = campus_loc_path.read_bytes()
    campus_loc = campus_loc_data.decode("utf-8-sig")

    campus_assertions = {
        "120-day semester mission": "days_mission_timeout = 120" in campus_decisions,
        "one-day semester projects": campus_decisions.count("days_remove = 1") >= 9,
        "delayed semester restart": "country_event = { id = B80_campus.70 hours = 1 }" in campus_effects,
        "mission restart event": "activate_mission = B80_semester_countdown" in campus_events,
        "supported breakthrough specializations": "specialization = all" not in campus_decisions + campus_events,
        "new-game initialization": "B80_initialize_campus_system = yes" in country_history and "is_ai = yes" in campus_on_actions,
        "student fourth project slot": "has_completed_focus = BJ80_the_school_belongs_to_students" in campus_decisions,
        "medium pressure penalty": "industrial_capacity_factory = -0.15" in campus_ideas,
        "cafeteria progression": all(idea in campus_ideas for idea in ["B80_cafeteria_queue", "B80_staggered_cafeteria", "B80_central_cafeteria_system"]),
        "campus variable panel": all(var in campus_loc for var in ["B80_academic_progress", "B80_campus_vitality", "B80_admission_pressure", "B80_school_reputation"]),
    }
    for label, passed in campus_assertions.items():
        if not passed:
            errors.append(f"campus mechanic assertion failed: {label}")
    if not campus_loc_data.startswith(b"\xef\xbb\xbf"):
        errors.append("campus mechanic localisation must use UTF-8 BOM")

    campus_event_blocks = blocks(campus_events, "country_event")
    campus_event_ids = {
        re.search(r"(?m)^\s*id\s*=\s*(B80_campus\.\d+)", block).group(1)
        for block in campus_event_blocks
        if re.search(r"(?m)^\s*id\s*=\s*(B80_campus\.\d+)", block)
    }
    expected_campus_events = {"B80_campus.1", *{f"B80_campus.{number}" for number in [10, 11, 12, 13, 14, 15, 16, 20, 30, 40, 50, 60, 70]}}
    if campus_event_ids != expected_campus_events:
        errors.append(f"campus event set mismatch: {sorted(campus_event_ids ^ expected_campus_events)}")

    loc_keys = set(re.findall(r"(?m)^\s*([A-Za-z0-9_.]+):", campus_loc))
    for block in campus_event_blocks:
        if "hidden = yes" in block:
            continue
        event_id_match = re.search(r"(?m)^\s*id\s*=\s*(B80_campus\.\d+)", block)
        if not event_id_match:
            continue
        event_id = event_id_match.group(1)
        for suffix in ["t", "d"]:
            if f"{event_id}.{suffix}" not in loc_keys:
                errors.append(f"missing campus event localisation: {event_id}.{suffix}")
        for option_key in re.findall(r"(?m)^\s*name\s*=\s*(B80_campus\.[A-Za-z0-9_.]+)", block):
            if option_key not in loc_keys:
                errors.append(f"missing campus option localisation: {option_key}")

if errors:
    print("VALIDATION_FAILED")
    print("\n".join(f"- {error}" for error in errors))
    raise SystemExit(1)

print("VALIDATION_OK")
print(f"shared_focuses={len(focus_ids)} (legacy={len(legacy_focus_ids)}, political={len(political_focus_ids)}, endgame={len(endgame_focus_ids)})")
print("autonomy_focuses=25")
print(f"custom_ideas={len(idea_ids)}")
print(f"event_calls={len(event_calls)}")
