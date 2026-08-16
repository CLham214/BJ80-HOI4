from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from pathlib import Path


WORKSPACE = Path(r"E:\钢铁雄心4mod")
WORKSPACE = Path(__file__).resolve().parents[1]
PROJECT = Path(r"C:\Users\sst21\Desktop\BSZ\BSZ.xh4prj")
SOURCE_LOC = Path(
    r"C:\Users\sst21\Documents\xwechat_files\wxid_d30a15pzmfir12_bca7"
    r"\msg\file\2026-08\new_l_simp_chinese.yml.txt"
)
FOCUS_OUTPUT = WORKSPACE / "common/national_focus/B80_legacy_shared_focuses.txt"
LOC_OUTPUT = WORKSPACE / "localisation/simp_chinese/B80_legacy_focus_l_simp_chinese.yml"
TREE_FILE = WORKSPACE / "common/national_focus/BJ80_student_autonomy.txt"

FOCUS_NS = "focusesNs"
SER_NS = "http://schemas.microsoft.com/2003/10/Serialization/"
NS = {"a": FOCUS_NS, "z": SER_NS}
ID_ATTR = f"{{{SER_NS}}}Id"
REF_ATTR = f"{{{SER_NS}}}Ref"


MISSING_NAMES = {
    "newfocus_93": "推进生产现代化",
    "newfocus_94": "建设新校区",
    "newfocus_95": "完善校园交通网",
    "newfocus_96": "工程队专业化",
    "newfocus_97": "推行标准化建设",
    "newfocus_98": "建设校园防御工程",
    "newfocus_99": "开展建设总动员",
    "newfocus_100": "发展合成资源",
    "newfocus_101": "打开对外贸易窗口",
    "newfocus_102": "完善航空工业配套",
    "newfocus_103": "成立校园贸易委员会",
    "newfocus_106": "扩建民用工业",
    "newfocus_107": "开展国际科研合作",
    "newfocus_108": "改善学生生活",
    "newfocus_109": "提升生产标准",
    "newfocus_110": "建设校园交通干线",
    "newfocus_111": "综合建设计划",
    "newfocus_112": "工业扩张第二阶段",
    "newfocus_113": "校园建设总动员",
    "newfocus_114": "引进外国资本",
    "newfocus_115": "建设航空制造中心",
    "newfocus_116": "建设海军船坞",
    "newfocus_117": "扩建国防工业",
    "newfocus_118": "技术情报合作",
    "newfocus_119": "建立教育外交网络",
    "newfocus_120": "全球学术交流",
    "newfocus_121": "追加研究经费",
    "newfocus_122": "前沿武器研究",
    "newfocus_123": "火箭工程",
    "newfocus_124": "国际科研情报网",
    "newfocus_125": "现代海军理论",
    "newfocus_127": "永久中立校园",
    "newfocus_156": "构筑首都防御圈",
}


def child_text(node: ET.Element, name: str, default: str = "") -> str:
    child = node.find(f"a:{name}", NS)
    return child.text.strip() if child is not None and child.text else default


def object_id(node: ET.Element) -> str | None:
    return node.attrib.get(REF_ATTR) or node.attrib.get(ID_ATTR)


def load_localisation() -> tuple[dict[str, str], dict[str, str]]:
    names: dict[str, str] = {}
    descriptions: dict[str, str] = {}
    for raw_line in SOURCE_LOC.read_text(encoding="utf-8-sig").splitlines():
        match = re.match(r'^\s*(newfocus_[^:]+):"(.*)"?\s*$', raw_line)
        if not match:
            continue
        key, value = match.groups()
        # The old file has one missing quote on newfocus_88_desc.
        value = value.rstrip('"')
        if key.endswith("_desc"):
            descriptions[key[:-5]] = value
        else:
            names[key] = value
    return names, descriptions


def generated_source_name(node: ET.Element) -> str:
    name = child_text(node, "name")
    # The old project accidentally assigned newfocus_123 twice. The propaganda
    # node at object 1059 occupies the missing newfocus_113 slot.
    if name == "newfocus_123" and node.attrib.get(ID_ATTR) == "1059":
        return "newfocus_113"
    return name


def generated_id(source_name: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9_]", "_", source_name)
    return f"B80_legacy_{safe}"


def tech_bonus(category: str, suffix: str, uses: int = 2, bonus: float = 0.5) -> list[str]:
    number_match = re.search(r"(\d+)", suffix)
    if number_match:
        variant = int(number_match.group(1)) % 3
        if variant == 1:
            return ["add_political_power = 50"]
        if variant == 2:
            return ["add_stability = 0.03"]
    return [
        "add_tech_bonus = {",
        f"\tname = B80_legacy_{suffix}_bonus",
        f"\tbonus = {bonus}",
        f"\tuses = {uses}",
        f"\tcategory = {category}",
        "}",
    ]


def named_tech_bonus(category: str, suffix: str, uses: int = 1, bonus: float = 0.5) -> list[str]:
    """A deliberate research reward for focuses whose names promise research."""
    return [
        "add_tech_bonus = {",
        f"\tname = B80_legacy_{suffix}_bonus",
        f"\tbonus = {bonus}",
        f"\tuses = {uses}",
        f"\tcategory = {category}",
        "}",
    ]


def unique_idea_reward(idea: str, fallback: list[str]) -> list[str]:
    """Grant a generic spirit once, then give a useful repeat-safe reward."""
    return [
        "if = {",
        f"\tlimit = {{ NOT = {{ has_idea = {idea} }} }}",
        f"\tadd_ideas = {idea}",
        "}",
        "else = {",
        *[f"\t{line}" for line in fallback],
        "}",
    ]


def effects_for(source_name: str, display_name: str, icon: str) -> list[str]:
    # Bespoke political/diplomatic effects for the named early branches.
    bespoke: dict[str, list[str]] = {
        "newfocus_0": ["add_political_power = 100", "add_stability = 0.05"],
        "newfocus_1": ["add_political_power = -200", "522 = { transfer_state_to = B80 add_core_of = B80 }"],
        "newfocus_4": ["add_political_power = -200", "623 = { transfer_state_to = B80 add_core_of = B80 }"],
        "newfocus_5": ["add_political_power = -200", "671 = { transfer_state_to = B80 add_core_of = B80 }"],
        "newfocus_6": ["add_political_power = -200", "672 = { transfer_state_to = B80 add_core_of = B80 }"],
        "newfocus_7": ["add_stability = 0.05", "add_political_power = 50"],
        "newfocus_8": ["add_stability = 0.05", "add_war_support = 0.05"],
        "newfocus_9": ["ENG = { give_guarantee = B80 }", "add_offsite_building = { type = industrial_complex level = 2 }"],
        "newfocus_10": ["set_politics = { ruling_party = neutrality elections_allowed = no }", "add_stability = 0.10"],
        "newfocus_11": ["set_politics = { ruling_party = democratic elections_allowed = yes }", "add_stability = 0.05", "add_political_power = 100"],
        "newfocus_12": ["JAP = { give_guarantee = B80 }", "add_war_support = 0.10", "add_offsite_building = { type = arms_factory level = 1 }"],
        "newfocus_13": ["JAP = { give_guarantee = B80 }", "add_political_power = 100"],
        "newfocus_14": ["if = { limit = { HBC = { exists = yes } } create_wargoal = { type = annex_everything target = HBC } }", "add_war_support = 0.05", "add_political_power = 50"],
        "newfocus_15": ["if = { limit = { MEN = { exists = yes } } create_wargoal = { type = annex_everything target = MEN } }", "add_war_support = 0.05", "add_political_power = 50"],
        "newfocus_16": ["if = { limit = { MAN = { exists = yes } } create_wargoal = { type = annex_everything target = MAN } }", "add_war_support = 0.05", "add_political_power = 50"],
        "newfocus_18": ["add_state_claim = 525", "add_state_claim = 527", "add_state_claim = 1028", "add_state_claim = 1029", "add_state_claim = 1030", "add_state_claim = 1031", "if = { limit = { KOR = { exists = yes } } create_wargoal = { type = annex_everything target = KOR } }", "add_war_support = 0.05"],
        "newfocus_20": ["add_research_slot = 1", "add_political_power = 50"],
        "newfocus_23": ["if = { limit = { JAP = { exists = yes } } create_wargoal = { type = annex_everything target = JAP } }", "add_war_support = 0.10"],
        "newfocus_38": ["add_ideas = B80_anti_japanese_hegemony", "add_war_support = 0.10"],
        "newfocus_38.5": ["add_stability = 0.05", "add_political_power = 75", "add_war_support = 0.05"],
        "newfocus_47": ["add_research_slot = 1", "add_stability = 0.05"],
        "newfocus_39": ["country_event = { id = B80_legacy.1 days = 1 }"],
        "newfocus_40": ["country_event = { id = B80_legacy.2 days = 1 }"],
        "newfocus_21": ["country_event = { id = B80_legacy.3 days = 1 }"],
        "newfocus_50": ["country_event = { id = B80_legacy.4 days = 1 }"],
        "newfocus_51": ["country_event = { id = B80_legacy.7 days = 1 }"],
    }
    # These rewards are keyed to the actual Chinese focus names. This table is
    # intentionally explicit: a focus about spies should never degrade into a
    # generic stability or political-power reward when the tree is regenerated.
    bespoke.update({
        "newfocus_2": ["add_political_power = 100", "add_stability = -0.03", "country_event = { id = B80_legacy.5 days = 1 }"],
        "newfocus_3": [
            "if = { limit = { NOT = { has_idea = B80_legacy_academic_network } } add_ideas = B80_legacy_academic_network }",
            *named_tech_bonus("electronics", "innovation_class", 2, 0.5),
        ],
        "newfocus_7": [
            "if = { limit = { NOT = { has_idea = B80_legacy_orderly_teaching } NOT = { has_idea = B80_legacy_education_department_order } } add_ideas = B80_legacy_orderly_teaching }",
            "add_stability = 0.05",
        ],
        "newfocus_8": ["add_war_support = 0.10", "add_political_power = 75"],
        "newfocus_9": ["ENG = { give_guarantee = B80 }", "add_offsite_building = { type = industrial_complex level = 2 }"],
        "newfocus_10": [
            "set_politics = { ruling_party = neutrality elections_allowed = no }",
            "if = {",
            "\tlimit = { has_idea = B80_legacy_orderly_teaching }",
            "\tswap_ideas = { remove_idea = B80_legacy_orderly_teaching add_idea = B80_legacy_education_department_order }",
            "}",
            "else = { add_ideas = B80_legacy_education_department_order }",
            "add_stability = 0.10",
        ],
        "newfocus_11": ["set_politics = { ruling_party = communism elections_allowed = no }", "set_popularities = { communism = 55 democratic = 20 neutrality = 20 fascism = 5 }", "add_ideas = B80_commune_emergency_committee", "add_political_power = 100"],
        "newfocus_12": ["JAP = { give_guarantee = B80 }", "add_offsite_building = { type = industrial_complex level = 1 }", "add_stability = 0.05"],
        "newfocus_13": ["JAP = { give_guarantee = B80 }", "add_offsite_building = { type = arms_factory level = 2 }", "add_political_power = 75"],
        "newfocus_17": ["add_offsite_building = { type = industrial_complex level = 2 }", "add_ideas = B80_legacy_japanese_patronage"],
        "newfocus_19": ["add_research_slot = 1", "add_political_power = 50"],
        "newfocus_20": ["add_ideas = B80_legacy_japanese_higher_education", *named_tech_bonus("electronics", "study_in_japan", 1, 0.5)],
        "newfocus_22": [
            "if = {",
            "\tlimit = { has_idea = B80_legacy_japanese_higher_education }",
            "\tswap_ideas = { remove_idea = B80_legacy_japanese_higher_education add_idea = B80_legacy_integrated_japanese_education }",
            "}",
            "else = { add_ideas = B80_legacy_integrated_japanese_education }",
            "add_stability = 0.05",
        ],
        "newfocus_24": ["add_ideas = B80_legacy_imperial_armed_forces", "add_manpower = 5000", "add_equipment_to_stockpile = { type = infantry_equipment_0 amount = 1000 producer = B80 }"],
        "newfocus_25": [
            "if = { limit = { NOT = { has_idea = B80_legacy_aviation_society } NOT = { has_idea = B80_legacy_expanded_aviation_society } } add_ideas = B80_legacy_aviation_society }",
            "air_experience = 25",
            "capital_scope = { add_building_construction = { type = air_base level = 2 instant_build = yes } }",
        ],
        "newfocus_26": ["add_ideas = B80_legacy_campus_fleet", "navy_experience = 25", "add_offsite_building = { type = dockyard level = 1 }"],
        "newfocus_27": ["army_experience = 30", *named_tech_bonus("land_doctrine", "imperial_army_doctrine", 1, 0.5)],
        "newfocus_28": [
            "if = {",
            "\tlimit = { has_intelligence_agency = no }",
            "\tcreate_intelligence_agency = yes",
            "}",
            "if = {",
            "\tlimit = { NOT = { has_done_agency_upgrade = upgrade_blueprint_stealing } }",
            "\tupgrade_intelligence_agency = upgrade_blueprint_stealing",
            "}",
            "add_ideas = B80_legacy_japanese_espionage_methods",
            "if = { limit = { JAP = { exists = yes } } add_intel = { target = JAP civilian_intel = 10 army_intel = 10 navy_intel = 10 airforce_intel = 10 } }",
        ],
        "newfocus_29": ["add_equipment_to_stockpile = { type = fighter_equipment_0 amount = 100 producer = JAP }", "air_experience = 15", *named_tech_bonus("air_equipment", "zero_fighter", 1, 0.5)],
        "newfocus_30": [
            "add_political_power = -50",
            "create_ship = { type = ship_hull_light_1 equipment_variant = \"Mutsuki Class\" creator = JAP name = \"八十丸\" }",
            "create_ship = { type = ship_hull_light_1 equipment_variant = \"Mutsuki Class\" creator = JAP name = \"竞时丸\" }",
            "add_equipment_to_stockpile = { type = convoy_1 amount = 30 producer = JAP }",
            "navy_experience = 15",
        ],
        "newfocus_31": ["add_offsite_building = { type = arms_factory level = 2 }", "add_ideas = B80_legacy_japanese_arms_contracts"],
        "newfocus_32": ["capital_scope = { add_building_construction = { type = infrastructure level = 1 instant_build = yes } }", "add_ideas = B80_legacy_physical_education"],
        "newfocus_33": ["capital_scope = { add_building_construction = { type = infrastructure level = 2 instant_build = yes } }", "add_political_power = 50"],
        "newfocus_34": ["add_offsite_building = { type = arms_factory level = 2 }", "army_experience = 15"],
        "newfocus_35": ["add_ideas = B80_legacy_student_welfare", "add_offsite_building = { type = industrial_complex level = 1 }"],
        "newfocus_36": [
            "add_offsite_building = { type = arms_factory level = 2 }",
            "if = {",
            "\tlimit = { has_idea = B80_legacy_japanese_arms_contracts }",
            "\tswap_ideas = { remove_idea = B80_legacy_japanese_arms_contracts add_idea = B80_legacy_japanese_industrial_consortium }",
            "}",
            "else = { add_ideas = B80_legacy_japanese_industrial_consortium }",
        ],
        "newfocus_37": ["if = { limit = { NOT = { has_idea = war_economy } NOT = { has_idea = tot_economic_mobilisation } } add_ideas = war_economy }", "add_war_support = 0.05"],
        "newfocus_38.5": ["add_stability = 0.10", "add_political_power = 100", "country_event = { id = B80_legacy.6 days = 1 }"],
        "newfocus_41": ["capital_scope = { add_extra_state_shared_building_slots = 1 add_building_construction = { type = industrial_complex level = 1 instant_build = yes } add_building_construction = { type = infrastructure level = 1 instant_build = yes } }"],
        "newfocus_42": ["add_political_power = 75", "capital_scope = { add_extra_state_shared_building_slots = 1 }"],
        "newfocus_43": [*named_tech_bonus("electronics", "subject_competitions", 2, 0.5), "add_political_power = 50"],
        "newfocus_44": ["add_ideas = B80_legacy_wang_shouguan_science_system", *named_tech_bonus("electronics", "wang_shouguan_class", 2, 0.5)],
        "newfocus_45": ["country_event = { id = B80_legacy.10 days = 1 }"],
        "newfocus_46": ["add_ideas = B80_legacy_american_education_model", *named_tech_bonus("electronics", "american_education", 1, 0.5)],
        "newfocus_48": [
            "if = {",
            "\tlimit = { has_idea = B80_legacy_campus_democracy }",
            "\tswap_ideas = { remove_idea = B80_legacy_campus_democracy add_idea = B80_legacy_campus_democracy_2 }",
            "}",
            "else = { add_ideas = B80_legacy_campus_democracy_2 }",
            "add_stability = 0.05",
        ],
        "newfocus_49": ["add_political_power = 100", "add_ideas = B80_legacy_model_educators"],
        "newfocus_52": ["add_ideas = B80_legacy_student_officer_corps", "army_experience = 20", "add_command_power = 25"],
        "newfocus_53": ["608 = { add_building_construction = { type = bunker level = 3 province = 9843 instant_build = yes } add_building_construction = { type = anti_air_building level = 2 instant_build = yes } }", "add_war_support = 0.05"],
        "newfocus_54": ["add_manpower = 5000", "army_experience = 20", "add_equipment_to_stockpile = { type = infantry_equipment_0 amount = 1000 producer = B80 }"],
        "newfocus_55": [*named_tech_bonus("infantry_weapons", "catch_up_weapons", 2, 0.75), *named_tech_bonus("artillery", "catch_up_artillery", 1, 0.75)],
        "newfocus_56": ["add_equipment_to_stockpile = { type = infantry_equipment_0 amount = 2500 producer = B80 }", "add_manpower = 2500"],
        "newfocus_57": ["add_equipment_to_stockpile = { type = motorized_equipment_1 amount = 500 producer = B80 }", *named_tech_bonus("motorized_equipment", "motorization", 1, 0.5)],
        "newfocus_58": ["add_equipment_to_stockpile = { type = artillery_equipment_1 amount = 500 producer = B80 }", *named_tech_bonus("artillery", "advanced_artillery", 2, 0.5)],
        "newfocus_59": ["add_ideas = B80_legacy_school_canteen_logistics", "add_equipment_to_stockpile = { type = support_equipment_1 amount = 500 producer = B80 }"],
        "newfocus_60": ["add_manpower = 2500", *named_tech_bonus("support_tech", "military_clinic", 2, 0.5)],
        "newfocus_61": [
            "add_ideas = B80_legacy_cavalry_tank_group",
            "army_experience = 25",
            "add_equipment_to_stockpile = { type = motorized_equipment_1 amount = 400 producer = B80 }",
            *named_tech_bonus("armor", "cavalry_tank_plan", 1, 0.5),
            *named_tech_bonus("motorized_equipment", "cavalry_motorization", 1, 0.5),
        ],
        "newfocus_62": [
            "add_ideas = B80_legacy_infantry_tank_coordination",
            "army_experience = 25",
            "add_equipment_to_stockpile = { type = support_equipment_1 amount = 500 producer = B80 }",
            *named_tech_bonus("armor", "infantry_tank_plan", 1, 0.5),
            *named_tech_bonus("support_tech", "infantry_tank_support", 1, 0.5),
        ],
        "newfocus_63": [
            "add_ideas = B80_legacy_hakimi_medium_tank_program",
            "if = {",
            "\tlimit = { has_dlc = \"No Step Back\" }",
            "\tset_technology = { basic_medium_tank_chassis = 1 }",
            "\tcreate_equipment_variant = {",
            "\t\tname = \"哈基米中型坦克\"",
            "\t\ttype = medium_tank_chassis_1",
            "\t\tparent_version = 0",
            "\t\tallow_without_tech = yes",
            "\t\tmodules = {",
            "\t\t\tmain_armament_slot = tank_small_cannon_2",
            "\t\t\tturret_type_slot = tank_medium_two_man_tank_turret",
            "\t\t\tsuspension_type_slot = tank_christie_suspension",
            "\t\t\tarmor_type_slot = tank_welded_armor",
            "\t\t\tengine_type_slot = tank_diesel_engine",
            "\t\t\tspecial_type_slot_1 = sloped_armor",
            "\t\t}",
            "\t\tupgrades = { tank_nsb_engine_upgrade = 5 tank_nsb_armor_upgrade = 2 }",
            "\t}",
            "\tadd_equipment_to_stockpile = { type = medium_tank_chassis_1 variant_name = \"哈基米中型坦克\" amount = 120 producer = B80 }",
            "}",
            "else = { add_equipment_to_stockpile = { type = medium_tank_equipment_1 amount = 120 producer = B80 } }",
            *named_tech_bonus("armor", "hakimi_medium_tank", 1, 0.75),
            "add_offsite_building = { type = arms_factory level = 1 }",
        ],
        "newfocus_64": [
            "add_ideas = B80_legacy_doraemon_heavy_tank_program",
            "if = {",
            "\tlimit = { has_dlc = \"No Step Back\" }",
            "\tset_technology = { basic_heavy_tank_chassis = 1 }",
            "\tcreate_equipment_variant = {",
            "\t\tname = \"哆啦B梦重型坦克\"",
            "\t\ttype = heavy_tank_chassis_1",
            "\t\tparent_version = 0",
            "\t\tallow_without_tech = yes",
            "\t\tmodules = {",
            "\t\t\tmain_armament_slot = tank_medium_cannon",
            "\t\t\tturret_type_slot = tank_heavy_three_man_tank_turret",
            "\t\t\tsuspension_type_slot = tank_torsion_bar_suspension",
            "\t\t\tarmor_type_slot = tank_welded_armor",
            "\t\t\tengine_type_slot = tank_diesel_engine",
            "\t\t}",
            "\t\tupgrades = { tank_nsb_engine_upgrade = 3 tank_nsb_armor_upgrade = 5 }",
            "\t}",
            "\tadd_equipment_to_stockpile = { type = heavy_tank_chassis_1 variant_name = \"哆啦B梦重型坦克\" amount = 60 producer = B80 }",
            "}",
            "else = { add_equipment_to_stockpile = { type = heavy_tank_equipment_1 amount = 60 producer = B80 } }",
            *named_tech_bonus("armor", "doraemon_heavy_tank", 1, 0.75),
            "add_offsite_building = { type = arms_factory level = 1 }",
        ],
        "newfocus_65": [
            "if = {",
            "\tlimit = { has_idea = B80_legacy_imperial_armed_forces }",
            "\tswap_ideas = { remove_idea = B80_legacy_imperial_armed_forces add_idea = B80_legacy_modern_army }",
            "}",
            "else = { add_ideas = B80_legacy_modern_army }",
            "army_experience = 30",
            "add_command_power = 25",
        ],
        "newfocus_66": [
            "if = {",
            "\tlimit = { has_idea = B80_legacy_aviation_society }",
            "\tswap_ideas = { remove_idea = B80_legacy_aviation_society add_idea = B80_legacy_expanded_aviation_society }",
            "}",
            "else = { add_ideas = B80_legacy_expanded_aviation_society }",
            "air_experience = 20",
        ],
        "newfocus_67": ["air_experience = 30", "capital_scope = { add_building_construction = { type = air_base level = 1 instant_build = yes } }"],
        "newfocus_68": [
            "add_ideas = B80_legacy_multirole_air_tactics",
            "add_equipment_to_stockpile = { type = fighter_equipment_0 amount = 120 producer = B80 }",
            *named_tech_bonus("air_equipment", "multirole_aircraft", 1, 0.5),
        ],
        "newfocus_69": [
            "add_ideas = B80_legacy_strategic_bombing_tactics",
            "if = { limit = { has_dlc = \"By Blood Alone\" } add_equipment_to_stockpile = { type = large_plane_airframe_0 amount = 40 producer = B80 } }",
            "else = { add_equipment_to_stockpile = { type = strat_bomber_equipment_1 amount = 40 producer = B80 } }",
            *named_tech_bonus("air_doctrine", "strategic_bombing_tactics", 1, 0.5),
            *named_tech_bonus("air_equipment", "strategic_bombers", 1, 0.5),
        ],
        "newfocus_70": [
            "add_ideas = B80_legacy_rapid_air_assault",
            "add_equipment_to_stockpile = { type = fighter_equipment_0 amount = 100 producer = B80 }",
            "add_equipment_to_stockpile = { type = transport_plane_equipment_1 amount = 20 producer = B80 }",
            *named_tech_bonus("air_doctrine", "rapid_air_assault", 1, 0.5),
        ],
        "newfocus_71": [*named_tech_bonus("jet_technology", "future_aviation", 2, 0.75), "air_experience = 20"],
        "newfocus_72": ["capital_scope = { add_building_construction = { type = air_base level = 4 instant_build = yes } add_building_construction = { type = radar_station level = 1 instant_build = yes } }"],
        "newfocus_73": ["add_offsite_building = { type = arms_factory level = 2 }", "add_ideas = B80_legacy_aerospace_industry"],
        "newfocus_74": [*named_tech_bonus("air_equipment", "aircraft_components", 2, 0.5), "air_experience = 15"],
        "newfocus_75": ["air_experience = 35", "add_ideas = B80_legacy_elite_flight_training"],
        "newfocus_76": ["air_experience = 30", "add_command_power = 15"],
        "newfocus_77": ["capital_scope = { add_building_construction = { type = air_base level = 2 instant_build = yes } add_building_construction = { type = radar_station level = 1 instant_build = yes } }"],
        "newfocus_78": [*named_tech_bonus("air_equipment", "advanced_aviation", 2, 0.75), "air_experience = 20"],
        "newfocus_79": ["country_event = { id = B80_legacy.8 days = 1 }"],
        "newfocus_80": ["add_offsite_building = { type = dockyard level = 2 }", "navy_experience = 10"],
        "newfocus_81": ["capital_scope = { add_extra_state_shared_building_slots = 1 add_building_construction = { type = synthetic_refinery level = 1 instant_build = yes } add_resource = { type = steel amount = 8 } }"],
        "newfocus_82": [*named_tech_bonus("naval_equipment", "expanded_naval_research", 2, 0.5), "navy_experience = 15"],
        "newfocus_83": ["navy_experience = 40", "add_command_power = 15"],
        "newfocus_84": [
            "add_ideas = B80_legacy_big_gun_fleet",
            *named_tech_bonus("naval_equipment", "big_gun_fleet", 2, 0.75),
            "add_offsite_building = { type = dockyard level = 1 }",
            "navy_experience = 20",
        ],
        "newfocus_85": [
            "add_ideas = B80_legacy_submarine_blade",
            *named_tech_bonus("naval_equipment", "submarine_blade", 1, 0.75),
            *named_tech_bonus("naval_doctrine", "submarine_doctrine", 1, 0.5),
            "navy_experience = 25",
        ],
        "newfocus_86": [
            "add_ideas = B80_legacy_naval_aviation",
            *named_tech_bonus("air_equipment", "naval_aviation", 2, 0.5),
            "add_equipment_to_stockpile = { type = cv_fighter_equipment_0 amount = 80 producer = B80 }",
            "navy_experience = 15",
            "air_experience = 20",
        ],
        "newfocus_87": [*named_tech_bonus("naval_equipment", "heavy_cruisers", 2, 0.5), "add_offsite_building = { type = dockyard level = 1 }"],
        "newfocus_88": ["add_equipment_to_stockpile = { type = cv_fighter_equipment_0 amount = 100 producer = B80 }", *named_tech_bonus("air_equipment", "carrier_aircraft", 1, 0.5)],
        "newfocus_89": [*named_tech_bonus("naval_equipment", "torpedoes_and_mines", 2, 0.5), "navy_experience = 15"],
        "newfocus_90": ["add_offsite_building = { type = dockyard level = 2 }", *named_tech_bonus("naval_equipment", "screens", 1, 0.5)],
        "newfocus_91": ["add_equipment_to_stockpile = { type = cv_small_plane_naval_bomber_airframe_0 amount = 100 producer = JAP variant_name = \"B2M\" }", *named_tech_bonus("air_equipment", "naval_bombers", 1, 0.5)],
        "newfocus_92": ["navy_experience = 50", "add_ideas = B80_legacy_tianjin_sailors", "add_command_power = 25"],
        "newfocus_93": ["add_ideas = B80_legacy_modern_industry", *named_tech_bonus("industry", "modern_production", 1, 0.5)],
        "newfocus_94": ["capital_scope = { add_extra_state_shared_building_slots = 2 add_building_construction = { type = industrial_complex level = 2 instant_build = yes } }"],
        "newfocus_95": ["capital_scope = { add_building_construction = { type = infrastructure level = 2 instant_build = yes } }", "add_political_power = 50"],
        "newfocus_96": ["add_ideas = B80_legacy_construction_corps", "add_political_power = 50"],
        "newfocus_97": ["add_ideas = B80_legacy_standardized_production", "add_stability = 0.03"],
        "newfocus_98": ["608 = { add_building_construction = { type = bunker level = 3 province = 9843 instant_build = yes } add_building_construction = { type = anti_air_building level = 2 instant_build = yes } }", "army_experience = 10"],
        "newfocus_99": ["add_offsite_building = { type = industrial_complex level = 1 }", "add_offsite_building = { type = arms_factory level = 1 }", "add_political_power = 50"],
        "newfocus_100": ["capital_scope = { add_extra_state_shared_building_slots = 1 add_building_construction = { type = synthetic_refinery level = 1 instant_build = yes } }", *named_tech_bonus("industry", "synthetic_resources", 1, 0.5)],
        "newfocus_101": ["add_offsite_building = { type = industrial_complex level = 1 }", "add_ideas = B80_legacy_trade_committee"],
        "newfocus_102": ["add_offsite_building = { type = arms_factory level = 2 }", "capital_scope = { add_building_construction = { type = air_base level = 1 instant_build = yes } }", *named_tech_bonus("air_equipment", "aviation_industrial_support", 1, 0.5)],
        "newfocus_103": ["add_ideas = B80_legacy_expanded_trade_network", "add_political_power = 75"],
        "newfocus_106": ["add_offsite_building = { type = industrial_complex level = 2 }"],
        "newfocus_107": ["add_ideas = B80_legacy_international_research_partnerships", *named_tech_bonus("electronics", "international_research", 2, 0.5)],
        "newfocus_108": [
            "if = {",
            "\tlimit = { has_idea = B80_legacy_student_welfare }",
            "\tswap_ideas = { remove_idea = B80_legacy_student_welfare add_idea = B80_legacy_comprehensive_student_welfare }",
            "}",
            "else = { add_ideas = B80_legacy_comprehensive_student_welfare }",
            "add_stability = 0.05",
        ],
        "newfocus_109": ["add_offsite_building = { type = industrial_complex level = 1 }", *named_tech_bonus("industry", "production_standards", 1, 0.5)],
        "newfocus_110": ["capital_scope = { add_building_construction = { type = infrastructure level = 2 instant_build = yes } }", "add_offsite_building = { type = industrial_complex level = 1 }"],
        "newfocus_111": ["add_offsite_building = { type = industrial_complex level = 1 }", "add_offsite_building = { type = arms_factory level = 1 }", "add_stability = 0.03"],
        "newfocus_112": ["add_offsite_building = { type = industrial_complex level = 2 }", "add_offsite_building = { type = arms_factory level = 1 }"],
        "newfocus_113": ["add_ideas = B80_legacy_construction_mobilization", "add_political_power = 100"],
        "newfocus_114": ["add_offsite_building = { type = industrial_complex level = 2 }", "add_political_power = 50"],
        "newfocus_115": ["add_offsite_building = { type = arms_factory level = 2 }", "add_ideas = B80_legacy_aircraft_manufacturing_center", "air_experience = 20"],
        "newfocus_116": ["add_offsite_building = { type = dockyard level = 2 }", *named_tech_bonus("naval_equipment", "campus_shipyards", 1, 0.5), "navy_experience = 20"],
        "newfocus_117": ["add_offsite_building = { type = arms_factory level = 2 }", "add_ideas = B80_legacy_defense_industrial_base", "army_experience = 20"],
        "newfocus_118": [
            "if = { limit = { has_intelligence_agency = no } create_intelligence_agency = yes }",
            "if = { limit = { NOT = { has_done_agency_upgrade = upgrade_economy_civilian } } upgrade_intelligence_agency = upgrade_economy_civilian }",
            *named_tech_bonus("electronics", "technical_intelligence", 1, 0.5),
        ],
        "newfocus_119": ["add_ideas = B80_legacy_education_diplomacy_network", "add_political_power = 100", "add_stability = 0.03"],
        "newfocus_120": ["add_ideas = B80_legacy_global_academic_exchange", *named_tech_bonus("electronics", "global_academic_exchange", 2, 0.5)],
        "newfocus_121": [*named_tech_bonus("electronics", "research_funding", 2, 0.75), *named_tech_bonus("industry", "research_funding_industry", 1, 0.75)],
        "newfocus_122": [*named_tech_bonus("infantry_weapons", "advanced_weapons", 2, 0.75), "add_offsite_building = { type = arms_factory level = 1 }"],
        "newfocus_123": [*named_tech_bonus("rocketry", "rocket_engineering", 2, 0.75), "air_experience = 15"],
        "newfocus_124": [
            "if = { limit = { has_intelligence_agency = no } create_intelligence_agency = yes }",
            "if = { limit = { NOT = { has_done_agency_upgrade = upgrade_form_department } } upgrade_intelligence_agency = upgrade_form_department }",
            "add_ideas = B80_legacy_international_intelligence_network",
        ],
        "newfocus_125": [*named_tech_bonus("naval_doctrine", "modern_naval_theory", 2, 0.75), "navy_experience = 30"],
        "newfocus_127": ["add_ideas = B80_legacy_permanent_neutrality", "add_stability = 0.10"],
        "newfocus_156": ["608 = { add_building_construction = { type = bunker level = 5 province = 9843 instant_build = yes } add_building_construction = { type = anti_air_building level = 3 instant_build = yes } add_building_construction = { type = radar_station level = 1 instant_build = yes } }", "army_experience = 20"],
    })
    if source_name in bespoke:
        return bespoke[source_name]

    text = f"{display_name} {icon}".lower()
    number_match = re.search(r"(\d+)", source_name)
    variant = int(number_match.group(1)) % 4 if number_match else 0

    # Keep the old tree at roughly vanilla strength, but make its rewards varied
    # enough that completing a focus changes the campaign immediately.
    if any(word in text for word in ["army", "infantry", "artillery", "tank", "armor", "weapon"]):
        rewards = [
            ["army_experience = 15", "add_equipment_to_stockpile = { type = infantry_equipment_0 amount = 500 producer = B80 }"],
            [*unique_idea_reward("B80_legacy_student_officer_corps", ["add_manpower = 2500", "army_experience = 15"])],
            ["add_offsite_building = { type = arms_factory level = 1 }", "army_experience = 10"],
            ["add_command_power = 25", *tech_bonus("infantry_weapons", source_name, 1, 0.5)],
        ]
        return rewards[variant]
    if any(word in text for word in ["air", "aviation", "fighter", "bomber"]):
        rewards = [
            ["air_experience = 20", "add_equipment_to_stockpile = { type = fighter_equipment_0 amount = 50 producer = B80 }"],
            [*unique_idea_reward("B80_legacy_aviation_society", ["air_experience = 25"])],
            ["add_offsite_building = { type = arms_factory level = 1 }", "air_experience = 10"],
            [*tech_bonus("air_equipment", source_name, 1, 0.5)],
        ]
        return rewards[variant]
    if any(word in text for word in ["navy", "naval", "dockyard", "submarine", "cruiser"]):
        rewards = [
            ["add_offsite_building = { type = dockyard level = 1 }", "navy_experience = 10"],
            [*unique_idea_reward("B80_legacy_campus_fleet", ["navy_experience = 25"])],
            ["add_political_power = 50", "navy_experience = 20"],
            [*tech_bonus("naval_equipment", source_name, 1, 0.5)],
        ]
        return rewards[variant]
    if any(word in text for word in ["research", "scientific", "education", "electronics", "secret_weapon"]):
        rewards = [
            [*tech_bonus("electronics", source_name, 1, 0.5)],
            [*unique_idea_reward("B80_legacy_academic_network", ["add_political_power = 75", "add_stability = 0.03"])],
            ["add_offsite_building = { type = industrial_complex level = 1 }", "add_stability = 0.02"],
            ["add_political_power = 75", "add_stability = 0.03"],
        ]
        return rewards[variant]
    if "construct_civ" in text or "construct_civilian" in text or "民用工业" in text:
        return ["capital_scope = { add_extra_state_shared_building_slots = 1 add_building_construction = { type = industrial_complex level = 1 instant_build = yes } }"]
    if "construct_mil" in text or "军工" in text or "军备建设" in text:
        return ["capital_scope = { add_extra_state_shared_building_slots = 1 add_building_construction = { type = arms_factory level = 1 instant_build = yes } }"]
    if "naval_dockyard" in text or "船坞" in text:
        return ["capital_scope = { add_extra_state_shared_building_slots = 1 add_building_construction = { type = dockyard level = 1 instant_build = yes } }", "navy_experience = 10"]
    if "infrastructure" in text or "基础设施" in text or "交通" in text:
        return ["capital_scope = { add_building_construction = { type = infrastructure level = 1 instant_build = yes } }", *tech_bonus("industry", source_name, 1)]
    if "fortify" in text or "防御工程" in text or "八十之盾" in text:
        return ["capital_scope = { add_building_construction = { type = bunker level = 2 instant_build = yes } }", "army_experience = 10"]
    if "oil_refinery" in text or "合成资源" in text:
        return ["capital_scope = { add_extra_state_shared_building_slots = 1 add_building_construction = { type = synthetic_refinery level = 1 instant_build = yes } }", *tech_bonus("industry", source_name, 1)]
    if any(word in text for word in ["navy", "海军", "战舰", "巡洋", "潜艇", "鱼雷", "水雷", "舰载", "屏卫", "碧蓝"]):
        category = "naval_doctrine" if "doctrine" in text or "训练" in text else "naval_equipment"
        return ["navy_experience = 15", *tech_bonus(category, source_name)]
    if any(word in text for word in ["air_", "air ", "空军", "航空", "战机", "飞机", "轰炸", "飞行", "制空"]):
        category = "air_doctrine" if "doctrine" in text or "战术" in text or "训练" in text else "air_equipment"
        return ["air_experience = 15", *tech_bonus(category, source_name)]
    if any(word in text for word in ["tank", "坦克", "装甲"]):
        return ["army_experience = 15", *tech_bonus("armor", source_name)]
    if any(word in text for word in ["artillery", "火炮", "打炮"]):
        return ["army_experience = 15", *tech_bonus("artillery", source_name)]
    if any(word in text for word in ["army", "陆军", "步兵", "军队", "枪", "骑兵", "医务室"]):
        return ["army_experience = 15", *tech_bonus("infantry_weapons", source_name)]
    if any(word in text for word in ["research", "scientific", "wonder", "rocketry", "secret_weapon", "科研", "科学", "实验班", "竞赛", "教育"]):
        return [*tech_bonus("electronics", source_name), "add_political_power = 50"]
    if any(word in text for word in ["construction", "production", "工业", "生产", "建设", "设施", "生活水平", "食堂"]):
        return [*tech_bonus("industry", source_name), "add_offsite_building = { type = industrial_complex level = 1 }"]
    if any(word in text for word in ["trade", "贸易", "资本", "国际化", "improve_relations", "alliance"]):
        return ["add_political_power = 75", "add_stability = 0.03"]
    if any(word in text for word in ["propaganda", "national_unity", "政治", "秩序", "委员会", "主人", "诗会", "歌手"]):
        return ["add_political_power = 75", "add_stability = 0.05"]
    if any(word in text for word in ["attack", "territory", "demand", "战争", "接管", "进驻", "进军"]):
        return ["add_political_power = 50", "add_war_support = 0.05", "army_experience = 10"]
    return ["add_political_power = 50", "add_stability = 0.03"]


def indent_effect(lines: list[str], level: int = 2) -> list[str]:
    result: list[str] = []
    depth = level
    for line in lines:
        stripped = line.strip()
        if stripped == "}":
            depth -= 1
        result.append("\t" * depth + stripped)
        if stripped.endswith("{"):
            depth += 1
    return result


def main() -> None:
    names, descriptions = load_localisation()
    root = ET.parse(PROJECT).getroot()
    nodes = [
        node
        for node in root.iter()
        if ID_ATTR in node.attrib
        and node.find("a:name", NS) is not None
        and node.find("a:x", NS) is not None
        and node.find("a:y", NS) is not None
    ]

    id_to_node = {node.attrib[ID_ATTR]: node for node in nodes}
    id_to_source = {oid: generated_source_name(node) for oid, node in id_to_node.items()}
    source_to_node = {generated_source_name(node): node for node in nodes}

    # HOI4 requires mutual exclusion to be declared on both focuses. The old
    # editor project only stored some links on one side, so normalize them.
    mutual_map: dict[str, set[str]] = {oid: set() for oid in id_to_node}
    for oid, node in id_to_node.items():
        mutuals = node.find("a:mutually_exclusives", NS)
        if mutuals is None:
            continue
        for pair in list(mutuals):
            for side in list(pair):
                target_oid = object_id(side)
                if target_oid and target_oid != oid and target_oid in id_to_node:
                    mutual_map[oid].add(target_oid)
                    mutual_map[target_oid].add(oid)

    shared_lines = ["# Generated from BSZ.xh4prj. Do not edit by hand; rerun tools/generate_legacy_tree.py.", ""]
    ordered = sorted(nodes, key=lambda n: (int(child_text(n, "x", "0")), int(child_text(n, "y", "0"))))

    for node in ordered:
        oid = node.attrib[ID_ATTR]
        source_name = id_to_source[oid]
        focus_id = generated_id(source_name)
        display_name = names.get(source_name, MISSING_NAMES.get(source_name, source_name))
        icon = child_text(node, "image", "goal_generic_national_unity")
        icon = {
            "newfocus_19": "focus_research",
            "newfocus_28": "focus_generic_secret_service_agency",
            "newfocus_37": "goal_generic_construct_mil_factory",
            "newfocus_61": "goal_generic_cavalry",
            "newfocus_62": "goal_generic_army_tanks",
            "newfocus_64": "goal_generic_army_tanks",
            "newfocus_85": "goal_generic_navy_submarine",
            "newfocus_86": "goal_generic_navy_carrier",
        }.get(source_name, icon)
        x = int(child_text(node, "x", "0")) + 45
        y = int(child_text(node, "y", "0"))
        # The old editor project connected the submarine plan to carrier
        # aircraft and the naval-air plan to torpedo research. Keep the UI
        # lanes straight while putting each descendant under the right plan.
        x = {"newfocus_88": 113, "newfocus_89": 111}.get(source_name, x)
        cost = max(2, int(child_text(node, "cost", "5")))

        block = [
            "shared_focus = {",
            f"\tid = {focus_id}",
            f"\ticon = GFX_{icon}",
            f"\tx = {x}",
            f"\ty = {y}",
            f"\tcost = {cost}",
        ]

        if source_name in {"newfocus_1", "newfocus_4", "newfocus_5", "newfocus_6"}:
            block.append("\tavailable = { has_political_power > 199 }")
        elif source_name == "newfocus_30":
            block.append("\tavailable = { has_political_power > 49 }")

        prereqs = node.find("a:prerequisites", NS)
        prerequisite_overrides = {
            "newfocus_88": ["newfocus_86"],
            "newfocus_89": ["newfocus_85"],
        }
        if source_name in prerequisite_overrides:
            links = [generated_id(item) for item in prerequisite_overrides[source_name]]
            block.append("\tprerequisite = { " + " ".join(f"focus = {item}" for item in links) + " }")
        elif prereqs is not None:
            for prereq in list(prereqs):
                linked = prereq.find("a:linked_foci", NS)
                links: list[str] = []
                if linked is not None:
                    for target in list(linked):
                        target_oid = object_id(target)
                        if target_oid in id_to_source:
                            links.append(generated_id(id_to_source[target_oid]))
                if links:
                    block.append("\tprerequisite = { " + " ".join(f"focus = {item}" for item in links) + " }")

        mutual_targets = {
            generated_id(id_to_source[target_oid])
            for target_oid in mutual_map[oid]
        }
        for target in sorted(mutual_targets):
            block.append(f"\tmutually_exclusive = {{ focus = {target} }}")

        block.append("\tcompletion_reward = {")
        block.extend(indent_effect(effects_for(source_name, display_name, icon), 2))
        block.extend(["\t}", "\tai_will_do = { factor = 1 }", "}", ""])
        shared_lines.extend(block)

    FOCUS_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    FOCUS_OUTPUT.write_text("\n".join(shared_lines), encoding="utf-8")

    loc_lines = ["l_simp_chinese:", ' B80_legacy_branch_title: "八十中旧版综合国策"']
    for source_name, node in sorted(source_to_node.items(), key=lambda item: (int(child_text(item[1], "x", "0")), int(child_text(item[1], "y", "0")))):
        focus_id = generated_id(source_name)
        display_name = names.get(source_name, MISSING_NAMES.get(source_name, source_name))
        description = descriptions.get(
            source_name,
            f"推进“{display_name}”计划，为八十中学下一阶段的发展奠定基础。",
        )
        display_name = display_name.replace('"', '\\"')
        description = description.replace('"', '\\"')
        loc_lines.append(f' {focus_id}: "{display_name}"')
        loc_lines.append(f' {focus_id}_desc: "{description}"')
    LOC_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    LOC_OUTPUT.write_text("\n".join(loc_lines) + "\n", encoding="utf-8-sig")

    marker_start = "\t# BEGIN GENERATED LEGACY SHARED FOCUSES"
    marker_end = "\t# END GENERATED LEGACY SHARED FOCUSES"
    include_lines = [marker_start]
    for source_name in sorted(source_to_node, key=lambda name: (int(child_text(source_to_node[name], "x", "0")), int(child_text(source_to_node[name], "y", "0")))):
        include_lines.append(f"\tshared_focus = {generated_id(source_name)}")
    include_lines.append(marker_end)
    include_block = "\n".join(include_lines)

    tree_text = TREE_FILE.read_text(encoding="utf-8-sig")
    pattern = re.compile(re.escape(marker_start) + r".*?" + re.escape(marker_end), re.S)
    if pattern.search(tree_text):
        tree_text = pattern.sub(include_block, tree_text)
    else:
        closing = tree_text.rfind("}")
        if closing == -1:
            raise RuntimeError("Could not find focus tree closing brace")
        tree_text = tree_text[:closing].rstrip() + "\n\n" + include_block + "\n" + tree_text[closing:]
    TREE_FILE.write_text(tree_text, encoding="utf-8")

    print(f"generated_focuses={len(nodes)}")
    print(f"focus_output={FOCUS_OUTPUT}")
    print(f"localisation_output={LOC_OUTPUT}")


if __name__ == "__main__":
    main()
