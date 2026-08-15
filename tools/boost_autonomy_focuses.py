from pathlib import Path


PATH = Path(r"E:\钢铁雄心4mod\common\national_focus\BJ80_student_autonomy.txt")
MARKER = "# Overpowered student-autonomy baseline"


def matching_brace(text: str, opening: int) -> int:
    depth = 0
    for index in range(opening, len(text)):
        if text[index] == "{":
            depth += 1
        elif text[index] == "}":
            depth -= 1
            if depth == 0:
                return index
    raise ValueError("unbalanced braces")


text = PATH.read_text(encoding="utf-8-sig")
# A previous UI-cost conversion accidentally left literal "$15" tokens in
# seventeen focus blocks. HOI4 stops parsing the focus at those tokens.
text = "\n".join(line for line in text.splitlines() if line.strip() != "$15") + "\n"
cursor = 0
changed = 0
while True:
    start = text.find("\n\tfocus = {", cursor)
    if start == -1:
        break
    opening = text.find("{", start)
    end = matching_brace(text, opening)
    block = text[start:end + 1]
    if "id = BJ80_" not in block:
        cursor = end + 1
        continue
    reward = block.find("completion_reward = {")
    if reward != -1 and MARKER not in block:
        insertion = reward + len("completion_reward = {")
        bonus = (
            "\n\t\t\t# Overpowered student-autonomy baseline"
            "\n\t\t\tadd_political_power = 100"
            "\n\t\t\tadd_stability = 0.03"
            "\n\t\t\tadd_manpower = 2500"
        )
        block = block[:insertion] + bonus + block[insertion:]
        text = text[:start] + block + text[end + 1:]
        changed += 1
        cursor = start + len(block)
    else:
        cursor = end + 1

PATH.write_text(text, encoding="utf-8")
print(f"boosted_focuses={changed}")
