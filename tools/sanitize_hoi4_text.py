import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "common/ideas/BJ80_student_autonomy_ideas.txt",
    ROOT / "common/decisions/categories/BJ80_student_integration_categories.txt",
    ROOT / "common/ideas/B80_starting_ideas.txt",
    ROOT / "common/ideas/B80_legacy_ideas.txt",
]

PICTURE_REPLACEMENTS = {
    "picture = generic_democratic_reformer": "picture = generic_democratic_opposition",
    "picture = generic_industry": "picture = generic_improved_industries",
    "picture = generic_propaganda": "picture = generic_pp_unity_bonus",
    "picture = generic_intelligence_exchange": "picture = generic_spy_intel",
    "picture = generic_allies_build_infantry": "picture = generic_infantry_bonus",
    "picture = generic_scientific_exchange": "picture = generic_research_bonus",
    "picture = generic_national_unity": "picture = generic_pp_unity_bonus",
    "picture = generic_trade": "picture = generic_foreign_capital",
    "picture = generic_neutrality_idea": "picture = generic_neutrality_drift_bonus",
    "picture = generic_manpower": "picture = generic_manpower_bonus",
    "picture = generic_attack": "picture = generic_infantry_bonus",
}

for path in TARGETS:
    text = path.read_text(encoding="utf-8-sig")
    for old, new in PICTURE_REPLACEMENTS.items():
        text = re.sub(
            rf"(?m)^(\s*){re.escape(old)}\s*$",
            rf"\1{new}",
            text,
        )
    path.write_text(text, encoding="utf-8", newline="\n")
    print(f"utf8_no_bom={path.relative_to(ROOT)}")
