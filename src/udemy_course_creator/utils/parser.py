def parse_curriculum_markdown(markdown_text: str) -> dict:
    lines = [line.strip() for line in markdown_text.split('\n') if line.strip()]
    result = {"title": "", "sections": []}
    current_section = None
    i = 0

    while i < len(lines):
        line = lines[i]

        if line.startswith("# "):  # Course Title
            result["title"] = line[2:]

        elif line.startswith("## ") and ("Section" in line or "section" in line.lower()):
            if current_section:
                result["sections"].append(current_section)
            section_title = line[3:]
            if "." in section_title:
                section_title = section_title.split(".", 1)[-1].strip()
            current_section = {
                "title": section_title,
                "lectures": []
            }

        elif line.startswith("### "):
            lecture_line = line[4:].strip()

            if "." in lecture_line:
                lecture_title = lecture_line.split(".", 1)[-1].strip()
            else:
                lecture_title = lecture_line

            i += 1
            objective = ""
            activity = ""

            while i < len(lines) and not lines[i].startswith("### ") and not lines[i].startswith("## "):
                l = lines[i]
                if l.startswith("- Objective:"):
                    objective = l.replace("- Objective:", "").strip()
                elif l.startswith("- Activity:"):
                    activity = l.replace("- Activity:", "").strip()
                i += 1

            current_section["lectures"].append({
                "title": lecture_title,
                "objective": objective,
                "activity": activity
            })
            continue  # Skip auto-increment

        i += 1

    if current_section:
        result["sections"].append(current_section)

    if not result["title"]:
        result["title"] = "Untitled Course"

    if not result["sections"]:
        raise ValueError("No sections found in curriculum output.")

    return result