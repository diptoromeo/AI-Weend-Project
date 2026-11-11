"""Grade a resume against a job listing.
Usage:  python app.py resume.pdf job.txt
Gives a keyword-match score offline; adds AI feedback if ANTHROPIC_API_KEY is set.
"""
import os, re, sys
from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer, ENGLISH_STOP_WORDS
from sklearn.metrics.pairwise import cosine_similarity

MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-5-5")


def read(path):
    if path.lower().endswith(".pdf"):
        return "\n".join(p.extract_text() or "" for p in PdfReader(path).pages)
    with open(path, encoding="utf-8", errors="ignore") as f:
        return f.read()


def keywords(text, top_n=30):
    vec = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), max_features=500)
    scores = vec.fit_transform([text]).toarray()[0]
    ranked = sorted(zip(vec.get_feature_names_out(), scores), key=lambda x: -x[1])
    return [w for w, _ in ranked if not w.isdigit()][:top_n]


def analyze(resume, job):
    tfidf = TfidfVectorizer(stop_words="english").fit([resume, job])
    similarity = cosine_similarity(tfidf.transform([resume]), tfidf.transform([job]))[0][0]

    job_kw = keywords(job)
    resume_lower = resume.lower()
    matched = [k for k in job_kw if re.search(rf"\b{re.escape(k)}\b", resume_lower)]
    missing = [k for k in job_kw if k not in matched]

    score = round(100 * (0.6 * len(matched) / max(len(job_kw), 1) + 0.4 * similarity))
    return score, similarity, matched, missing


def ai_feedback(resume, job):
    import anthropic
    prompt = (f"JOB LISTING:\n{job}\n\nRESUME:\n{resume}\n\n"
              "Grade this resume for the job from A to F. Then give: 3 strengths, "
              "3 gaps, and 5 concrete bullet rewrites that would improve the match.")
    msg = anthropic.Anthropic().messages.create(
        model=MODEL, max_tokens=1200, messages=[{"role": "user", "content": prompt}])
    return msg.content[0].text


def main():
    if len(sys.argv) != 3:
        sys.exit("Usage: python app.py <resume.pdf|txt> <job.txt>")
    resume, job = read(sys.argv[1]), read(sys.argv[2])
    score, sim, matched, missing = analyze(resume, job)

    grade = "A" if score >= 80 else "B" if score >= 65 else "C" if score >= 50 else "D" if score >= 35 else "F"
    print(f"\nMatch score: {score}/100  (grade {grade}, text similarity {sim:.2f})")
    print(f"\n✅ Matched keywords ({len(matched)}): {', '.join(matched)}")
    print(f"\n❌ Missing keywords ({len(missing)}): {', '.join(missing)}")

    if os.getenv("ANTHROPIC_API_KEY"):
        print("\n--- AI feedback ---\n" + ai_feedback(resume, job))
    else:
        print("\n(Set ANTHROPIC_API_KEY for detailed AI feedback.)")


if __name__ == "__main__":
    main()
