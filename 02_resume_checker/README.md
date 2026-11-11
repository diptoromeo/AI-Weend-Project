# 02 · Resume Checker

Grades a resume against a job listing: a match score, the job keywords you have, and the ones you're missing. With an API key it also gives AI feedback and suggested bullet rewrites.

## How it works
1. Extracts the top 30 keywords and phrases from the job listing with TF-IDF.
2. Checks which of them appear in your resume.
3. Computes overall text similarity (cosine similarity).
4. Score = 60% keyword coverage + 40% similarity, mapped to a grade A–F.
5. If `ANTHROPIC_API_KEY` is set, Claude writes strengths, gaps and rewrites.

## Setup
```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-...        # optional, for AI feedback
```

## Run
Save the job listing as a text file, then:
```bash
python app.py my_resume.pdf job.txt
```
```
Match score: 68/100  (grade B, text similarity 0.41)

✅ Matched keywords (19): python, sql, machine learning, ...
❌ Missing keywords (11): docker, kubernetes, a/b testing, ...
```
The resume can be `.pdf` or `.txt`.

## Limitations
- Keyword matching is literal: "ML" and "machine learning" count as different words.
- Scores are a guide for tailoring, not how a real recruiter or ATS will grade you.

## Ideas to extend
- Add a synonym list for common abbreviations.
- Compare one resume against many job listings and rank them.
