
import sys
import streamlit as st
import pandas as pd
import re
import io

try:
    from pypdf import PdfReader
except ImportError:
    st.error("❌ pypdf library not found. Please install: pip install pypdf")
    sys.exit(1)

try:
    from docx import Document
except ImportError:
    st.error("❌ python-docx library not found. Please install: pip install python-docx")
    sys.exit(1)


# ---------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------

st.set_page_config(
    page_title="AI Recruiter Profile Ranker",
    page_icon="🤖",
    layout="wide"
)


# ---------------------------------------------------
# SKILLS DATABASE
# ---------------------------------------------------

KNOWN_SKILLS = [
    "python",
    "django",
    "django rest framework",
    "drf",
    "fastapi",
    "flask",

    "postgresql",
    "mysql",
    "mongodb",
    "redis",

    "aws",
    "azure",
    "gcp",

    "docker",
    "kubernetes",

    "javascript",
    "typescript",
    "react",
    "angular",
    "node.js",

    "java",
    "spring boot",

    "selenium",
    "playwright",

    "html",
    "css",
    "bootstrap",

    "git",
    "github",
    "linux",

    "machine learning",
    "artificial intelligence",
    "data science",

    "sql",
    "power bi",
    "tableau",

    "devops",
    "jenkins",
    "terraform"
]


# ---------------------------------------------------
# EXTRACT SKILLS
# ---------------------------------------------------

def extract_skills(text):

    text = str(text).lower()

    found_skills = []

    for skill in KNOWN_SKILLS:

        # Avoid partial word matching
        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

        if re.search(pattern, text):
            found_skills.append(skill)

    return list(set(found_skills))


# ---------------------------------------------------
# EXTRACT EXPERIENCE FROM JD
# ---------------------------------------------------

def extract_experience(text):

    text = str(text).lower()

    # Example:
    # 4-8 years
    # 4 to 8 years

    match = re.search(
        r"(\d+(?:\.\d+)?)\s*(?:-|to)\s*(\d+(?:\.\d+)?)\s*(?:years?|yrs?)",
        text
    )

    if match:

        return float(match.group(1)), float(match.group(2))


    # Example:
    # 4+ years
    # 4 years

    match = re.search(
        r"(\d+(?:\.\d+)?)\s*\+?\s*(?:years?|yrs?)",
        text
    )

    if match:

        return float(match.group(1)), None


    return None, None


# ---------------------------------------------------
# EXTRACT EXPERIENCE FROM RESUME
# ---------------------------------------------------

def extract_candidate_experience(text):

    text = str(text).lower()

    experiences = []

    # Find patterns like:
    # 3 years
    # 4+ years
    # 5.5 years

    matches = re.findall(
        r"(\d+(?:\.\d+)?)\s*\+?\s*(?:years?|yrs?)",
        text
    )

    for match in matches:

        try:
            experiences.append(float(match))
        except:
            pass

    if experiences:

        # Usually the highest number is total experience
        return max(experiences)

    return 0


# ---------------------------------------------------
# EXTRACT PDF TEXT
# ---------------------------------------------------

def extract_text_from_pdf(uploaded_file):

    try:

        pdf_reader = PdfReader(uploaded_file)

        text = ""

        for page in pdf_reader.pages:

            extracted = page.extract_text()

            if extracted:
                text += extracted + "\n"

        return text

    except Exception as e:

        return ""


# ---------------------------------------------------
# EXTRACT DOCX TEXT
# ---------------------------------------------------

def extract_text_from_docx(uploaded_file):

    try:

        document = Document(uploaded_file)

        text = ""

        for paragraph in document.paragraphs:

            text += paragraph.text + "\n"

        return text

    except Exception as e:

        return ""


# ---------------------------------------------------
# EXTRACT RESUME TEXT
# ---------------------------------------------------

def extract_resume_text(uploaded_file):

    file_name = uploaded_file.name.lower()

    if file_name.endswith(".pdf"):

        return extract_text_from_pdf(uploaded_file)

    elif file_name.endswith(".docx"):

        return extract_text_from_docx(uploaded_file)

    return ""


# ---------------------------------------------------
# EXTRACT CANDIDATE NAME
# ---------------------------------------------------

def extract_candidate_name(text, filename):

    lines = text.split("\n")

    # Check first few lines of resume
    for line in lines[:10]:

        line = line.strip()

        # Ignore empty lines
        if not line:
            continue

        # Ignore common resume headings
        ignored_words = [
            "resume",
            "curriculum vitae",
            "profile",
            "contact",
            "email",
            "mobile",
            "phone"
        ]

        if any(word in line.lower() for word in ignored_words):
            continue

        # Avoid very long lines
        if len(line) < 60:

            # Usually name contains letters and spaces
            if re.match(r"^[A-Za-z\s\.\-]+$", line):

                return line.title()

    # If name is not detected, use filename
    name = filename.rsplit(".", 1)[0]

    name = name.replace("_", " ").replace("-", " ")

    return name.title()


# ---------------------------------------------------
# EXTRACT EMAIL
# ---------------------------------------------------

def extract_email(text):

    match = re.search(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text
    )

    if match:

        return match.group(0)

    return "Not Found"


# ---------------------------------------------------
# EXTRACT PHONE
# ---------------------------------------------------

def extract_phone(text):

    match = re.search(
        r"(?:\+91[\s\-]?)?[6-9]\d{9}",
        text
    )

    if match:

        return match.group(0)

    return "Not Found"


# ---------------------------------------------------
# EXTRACT LOCATION
# ---------------------------------------------------

def extract_location(text):

    common_locations = [
        "bangalore",
        "bengaluru",
        "hyderabad",
        "chennai",
        "mumbai",
        "pune",
        "delhi",
        "new delhi",
        "gurgaon",
        "gurugram",
        "noida",
        "kolkata",
        "ahmedabad",
        "coimbatore",
        "visakhapatnam"
    ]

    text_lower = text.lower()

    for location in common_locations:

        if location in text_lower:

            return location.title()

    return "Not Detected"


# ---------------------------------------------------
# EXTRACT CURRENT ROLE
# ---------------------------------------------------

def extract_current_role(text):

    common_roles = [
        "software engineer",
        "software developer",
        "python developer",
        "java developer",
        "full stack developer",
        "frontend developer",
        "backend developer",
        "data analyst",
        "data scientist",
        "devops engineer",
        "cloud engineer",
        "qa engineer",
        "test engineer",
        "automation engineer",
        "business analyst",
        "project manager",
        "technical recruiter",
        "hr recruiter"
    ]

    text_lower = text.lower()

    for role in common_roles:

        if role in text_lower:

            return role.title()

    return "Not Detected"


# ---------------------------------------------------
# CREATE RESUME SUMMARY
# ---------------------------------------------------

def create_resume_summary(text):

    text = text.replace("\n", " ")

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    # Keep first 500 characters
    summary = text[:500]

    return summary


# ---------------------------------------------------
# CALCULATE MATCH SCORE
# ---------------------------------------------------

def calculate_match(candidate, required_skills, min_exp, max_exp):

    candidate_skills = candidate.get("Skills", [])

    candidate_skills_lower = [
        skill.lower()
        for skill in candidate_skills
    ]

    # ------------------------------------------------
    # SKILL MATCHING - 60 POINTS
    # ------------------------------------------------

    matched_skills = []

    for skill in required_skills:

        if skill.lower() in candidate_skills_lower:

            matched_skills.append(skill)


    missing_skills = [

        skill

        for skill in required_skills

        if skill not in matched_skills

    ]


    if required_skills:

        skill_score = (
            len(matched_skills)
            / len(required_skills)
        ) * 60

    else:

        skill_score = 30


    # ------------------------------------------------
    # EXPERIENCE MATCHING - 25 POINTS
    # ------------------------------------------------

    experience = candidate.get("Experience", 0)


    if min_exp is None:

        experience_score = 25


    elif experience >= min_exp and (
        max_exp is None or experience <= max_exp
    ):

        experience_score = 25


    elif experience >= min_exp:

        experience_score = 20


    else:

        difference = min_exp - experience

        experience_score = max(
            0,
            25 - difference * 8
        )


    # ------------------------------------------------
    # ROLE RELEVANCE - 15 POINTS
    # ------------------------------------------------

    role = candidate.get(
        "Current Role",
        ""
    ).lower()


    role_score = 0


    for skill in required_skills:

        if skill.lower() in role:

            role_score = 15

            break


    # ------------------------------------------------
    # FINAL SCORE
    # ------------------------------------------------

    total_score = min(
        100,
        skill_score
        + experience_score
        + role_score
    )


    return (

        round(total_score, 1),

        ", ".join(matched_skills),

        ", ".join(missing_skills)

    )


# ---------------------------------------------------
# MAIN UI
# ---------------------------------------------------

st.title("🤖 AI Recruiter Profile Ranker")

st.caption(
    "Upload candidate resumes exported or downloaded through authorized recruiter access, "
    "paste the Job Description, and rank the best matching candidates."
)


# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

with st.sidebar:

    st.header("👥 Candidate Profiles")

    uploaded_files = st.file_uploader(

        "Upload Candidate Resumes",

        type=["pdf", "docx"],

        accept_multiple_files=True,

        help="Upload multiple candidate resumes in PDF or DOCX format."

    )


    if uploaded_files:

        st.success(
            f"{len(uploaded_files)} resume(s) uploaded."
        )

        st.write("### Uploaded Files")

        for file in uploaded_files:

            st.write(f"📄 {file.name}")


    st.divider()


    st.info(
        """
        📌 Workflow

        1. Search candidates using your authorized recruiter portal access.
        2. Download/export resumes you are authorized to use.
        3. Upload PDF or DOCX resumes here.
        4. Paste the Job Description.
        5. AI Recruiter ranks the candidates.
        """
    )


# ---------------------------------------------------
# JOB DESCRIPTION
# ---------------------------------------------------

st.subheader("📋 Job Description")

jd = st.text_area(

    "Paste Job Description (JD)",

    height=250,

    placeholder="""
Example:

We are looking for a Python Developer with 4-8 years of experience.

Required Skills:
Python
Django
FastAPI
PostgreSQL
AWS
Docker
    """

)


# ---------------------------------------------------
# ANALYZE BUTTON
# ---------------------------------------------------

if st.button(

    "🚀 Analyze Candidates and Generate Rankings",

    type="primary",

    use_container_width=True

):


    # -----------------------------------------------
    # VALIDATION
    # -----------------------------------------------

    if not jd.strip():

        st.warning(
            "⚠️ Please paste the Job Description."
        )


    elif not uploaded_files:

        st.warning(
            "⚠️ Please upload at least one candidate resume."
        )


    else:


        # -------------------------------------------
        # ANALYZE JOB DESCRIPTION
        # -------------------------------------------

        required_skills = extract_skills(jd)

        min_exp, max_exp = extract_experience(jd)


        st.divider()


        st.subheader("🔍 Job Description Analysis")


        col1, col2 = st.columns(2)


        with col1:

            st.write("### 🛠 Required Skills")

            if required_skills:

                st.success(
                    ", ".join(required_skills)
                )

            else:

                st.warning(
                    "No known skills detected."
                )


        with col2:

            st.write("### 💼 Experience Requirement")


            if min_exp is not None and max_exp is not None:

                st.success(
                    f"{min_exp:g} - {max_exp:g} Years"
                )


            elif min_exp is not None:

                st.success(
                    f"{min_exp:g}+ Years"
                )


            else:

                st.info(
                    "Experience requirement not detected."
                )


        # -------------------------------------------
        # PROCESS RESUMES
        # -------------------------------------------

        st.divider()

        st.subheader("📄 Processing Candidate Resumes")


        progress_bar = st.progress(0)

        candidates = []


        total_files = len(uploaded_files)


        for index, uploaded_file in enumerate(uploaded_files):


            with st.spinner(

                f"Analyzing {uploaded_file.name}..."

            ):


                # Extract resume text
                resume_text = extract_resume_text(
                    uploaded_file
                )


                # If text extraction fails
                if not resume_text.strip():

                    st.warning(

                        f"⚠️ Could not extract text from: "
                        f"{uploaded_file.name}"

                    )

                    continue


                # Extract information
                candidate_name = extract_candidate_name(

                    resume_text,

                    uploaded_file.name

                )


                candidate_skills = extract_skills(
                    resume_text
                )


                candidate_experience = (
                    extract_candidate_experience(
                        resume_text
                    )
                )


                candidate_email = extract_email(
                    resume_text
                )


                candidate_phone = extract_phone(
                    resume_text
                )


                candidate_location = extract_location(
                    resume_text
                )


                candidate_role = extract_current_role(
                    resume_text
                )


                resume_summary = create_resume_summary(
                    resume_text
                )


                # Create candidate profile
                candidate = {

                    "Candidate Name": candidate_name,

                    "Resume File": uploaded_file.name,

                    "Email": candidate_email,

                    "Phone": candidate_phone,

                    "Location": candidate_location,

                    "Current Role": candidate_role,

                    "Experience": candidate_experience,

                    "Skills": candidate_skills,

                    "Resume Summary": resume_summary

                }


                # Calculate match score
                score, matched, missing = calculate_match(

                    candidate,

                    required_skills,

                    min_exp,

                    max_exp

                )


                candidate["Match Score"] = score

                candidate["Matched Skills"] = matched

                candidate["Missing Skills"] = missing


                # Status
                if score >= 80:

                    candidate["Status"] = "🟢 Strong Match"


                elif score >= 60:

                    candidate["Status"] = "🟡 Good Match"


                else:

                    candidate["Status"] = "🔴 Review"


                candidates.append(candidate)


            # Update progress bar
            progress = int(
                ((index + 1) / total_files) * 100
            )

            progress_bar.progress(progress)


        progress_bar.empty()


        # -------------------------------------------
        # RESULTS
        # -------------------------------------------

        if not candidates:

            st.error(
                "❌ No resumes could be processed."
            )


        else:


            result_df = pd.DataFrame(candidates)


            # Convert skills list into text
            result_df["Skills"] = result_df["Skills"].apply(

                lambda x: ", ".join(x)

            )


            # Sort by score
            result_df = result_df.sort_values(

                "Match Score",

                ascending=False

            )


            # Add ranking
            result_df.insert(

                0,

                "Rank",

                range(1, len(result_df) + 1)

            )


            st.divider()


            # ---------------------------------------
            # TOP SUMMARY
            # ---------------------------------------

            st.subheader("🏆 Candidate Ranking Results")


            total_candidates = len(result_df)


            strong_matches = len(

                result_df[
                    result_df["Match Score"] >= 80
                ]

            )


            good_matches = len(

                result_df[
                    (result_df["Match Score"] >= 60)
                    &
                    (result_df["Match Score"] < 80)
                ]

            )


            col1, col2, col3 = st.columns(3)


            col1.metric(

                "Total Candidates",

                total_candidates

            )


            col2.metric(

                "Strong Matches",

                strong_matches

            )


            col3.metric(

                "Good Matches",

                good_matches

            )


            # ---------------------------------------
            # BEST CANDIDATE
            # ---------------------------------------

            best_candidate = result_df.iloc[0]


            st.success(

                f"""
                🥇 Best Match: **{best_candidate['Candidate Name']}**

                Match Score: **{best_candidate['Match Score']}%**

                Skills: {best_candidate['Matched Skills']}
                """

            )


            # ---------------------------------------
            # RESULTS TABLE
            # ---------------------------------------

            st.subheader("📊 All Candidate Rankings")


            display_columns = [

                "Rank",

                "Candidate Name",

                "Match Score",

                "Status",

                "Experience",

                "Current Role",

                "Location",

                "Skills",

                "Matched Skills",

                "Missing Skills",

                "Email"

            ]


            st.dataframe(

                result_df[display_columns],

                use_container_width=True,

                hide_index=True

            )


            # ---------------------------------------
            # CANDIDATE DETAILS
            # ---------------------------------------

            st.divider()


            st.subheader("👤 Candidate Details")


            for _, candidate in result_df.iterrows():

                with st.expander(

                    f"#{candidate['Rank']} - "
                    f"{candidate['Candidate Name']} "
                    f"({candidate['Match Score']}%)"

                ):


                    col1, col2 = st.columns(2)


                    with col1:

                        st.write(

                            "**📧 Email:**",

                            candidate["Email"]

                        )

                        st.write(

                            "**📱 Phone:**",

                            candidate["Phone"]

                        )

                        st.write(

                            "**📍 Location:**",

                            candidate["Location"]

                        )


                    with col2:

                        st.write(

                            "**💼 Experience:**",

                            f"{candidate['Experience']} Years"

                        )

                        st.write(

                            "**👨‍💻 Current Role:**",

                            candidate["Current Role"]

                        )

                        st.write(

                            "**📄 Resume File:**",

                            candidate["Resume File"]

                        )


                    st.write("### 🛠 Candidate Skills")

                    st.write(
                        candidate["Skills"]
                    )


                    st.write("### ✅ Matched Skills")

                    st.success(

                        candidate["Matched Skills"]
                        or "No matching skills detected."

                    )


                    st.write("### ❌ Missing Skills")

                    st.warning(

                        candidate["Missing Skills"]
                        or "No missing skills."

                    )


                    st.write("### 📝 Resume Preview")

                    st.write(
                        candidate["Resume Summary"]
                    )


            # ---------------------------------------
            # DOWNLOAD RESULTS
            # ---------------------------------------

            st.divider()


            csv = result_df.to_csv(
                index=False
            ).encode("utf-8")


            st.download_button(

                label="📥 Download Ranked Candidates",

                data=csv,

                file_name="ranked_candidates.csv",

                mime="text/csv",

                use_container_width=True

            )
