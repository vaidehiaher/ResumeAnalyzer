import re


# ----------------------------
# Extract Email
# ----------------------------
def extract_email(text):

    pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

    match = re.search(pattern, text)

    if match:
        return match.group()

    return ""


# ----------------------------
# Extract Phone Number
# ----------------------------
def extract_phone(text):

    pattern = r"(\+91[\-\s]?)?[6-9]\d{9}"

    match = re.search(pattern, text)

    if match:
        return match.group()

    return ""


# ----------------------------
# Extract Name
# ----------------------------
def extract_name(text):

    lines = text.split("\n")

    for line in lines:

        line = line.strip()

        if len(line.split()) >= 2 and len(line) < 40:

            return line

    return ""


# ----------------------------
# Extract Resume Sections
# ----------------------------
def extract_section(text, headings):

    lines = text.split("\n")

    collecting = False

    section = []

    for line in lines:

        clean = line.strip()

        # Check if current line is one of the headings
        if clean.lower() in headings:

            collecting = True
            continue

        if collecting:

            # Stop when a blank line is found
            if clean == "":
                break

            section.append(clean)

    return section


# ----------------------------
# Main Resume Parser
# ----------------------------
def parse_resume(text):

    education = extract_section(
        text,
        ["education"]
    )

    projects = extract_section(
        text,
        ["projects"]
    )

    experience = extract_section(
        text,
        ["experience"]
    )

    certifications = extract_section(
        text,
        ["certifications"]
    )

    result = {

        "name": extract_name(text),

        "email": extract_email(text),

        "phone": extract_phone(text),

        "education": education,

        "projects": projects,

        "experience": experience,

        "certifications": certifications

    }

    return result


# ----------------------------
# Testing
# ----------------------------
if __name__ == "__main__":

    sample = """
    Vaidehi Aher

    vaidehi@gmail.com

    9876543210

    Education
    B.Tech Electronics and Telecommunication
    Cummins College of Engineering

    Projects
    CareerPilot AI
    AI Resume Analyzer

    Experience
    IIT Bombay Internship

    Certifications
    MATLAB Onramp
    HCL Cybersecurity
    """

    print(parse_resume(sample))