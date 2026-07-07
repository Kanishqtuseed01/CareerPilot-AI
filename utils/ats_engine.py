import re


def calculate_ats_score(text):

    text = text.lower()

    result = {}

    total_score = 0

    # ---------------- CONTACT ----------------

    contact = 0

    if "@" in text:
        contact += 3

    if re.search(r"\d{10}", text):
        contact += 3

    if "linkedin" in text:
        contact += 2

    if "github" in text:
        contact += 2

    result["contact_information"] = contact

    total_score += contact

    # ---------------- EDUCATION ----------------

    education = 0

    education_words = [
        "b.tech",
        "bachelor",
        "university",
        "college",
        "cgpa",
        "gpa",
        "education"
    ]

    for word in education_words:

        if word in text:

            education += 3

    education = min(20, education)

    result["education"] = education

    total_score += education

    # ---------------- SKILLS ----------------

    skills = 0

    skill_words = [
        "python",
        "java",
        "sql",
        "c++",
        "excel",
        "git",
        "machine learning",
        "deep learning",
        "communication",
        "teamwork",
        "leadership"
    ]

    for word in skill_words:

        if word in text:

            skills += 2

    skills = min(15, skills)

    result["skills"] = skills

    total_score += skills

    # ---------------- PROJECTS ----------------

    projects = 0

    if "project" in text:
        projects += 10

    if "github" in text:
        projects += 5

    result["projects"] = projects

    total_score += projects

    # ---------------- EXPERIENCE ----------------

    experience = 0

    experience_words = [
        "intern",
        "experience",
        "developer",
        "engineer",
        "company",
        "worked"
    ]

    for word in experience_words:

        if word in text:

            experience += 4

    experience = min(20, experience)

    result["experience"] = experience

    total_score += experience

    # ---------------- ATS KEYWORDS ----------------

    ats = 0

    ats_words = [
        "developed",
        "designed",
        "implemented",
        "optimized",
        "managed",
        "created",
        "led",
        "improved",
        "analyzed",
        "built"
    ]

    for word in ats_words:

        if word in text:

            ats += 1

    ats = min(10, ats)

    result["ats_keywords"] = ats

    total_score += ats

    # ---------------- FORMATTING ----------------

    formatting = 10

    if len(text.split()) < 200:

        formatting -= 4

    result["formatting"] = formatting

    total_score += formatting

    return {
        "overall_score": total_score,
        "section_scores": result
    }