# Fixed start prompt for the assistant pilot screening session (R2-solo; transfer-verification procedure)

Status: proposed revision; pending researcher approval. This file is committed **before the pilot
draw**. Its SHA-256 is bound in the D-122 run authorisation, and the text below the line is pasted
**verbatim** as the first instruction of a new assistant session ("Session S", the screening session).

Two sessions are involved (D-125):
- **Session P (preparation session).** The assistant session that holds the Git-ignored publication records.
  Under D-122 it performs the draw (`pilot_sample.py`; 60 records; seed 4004) and generates the blinded
  sheet (`pilot_sheet.py`), records the sheet's SHA-256, size and row count in
  `research/literature/screening/pilot_sheet_record.json` (no sheet content), and delivers the sheet and
  the decision template to the researcher only. It makes **no screening decision** on the sampled records
  and is not started from this prompt.
- **Session S (screening session).** A new session started from the text below. It never has the
  publication records; it receives the sheet from the researcher and verifies it against the committed record.

Before the assistant's commitment is pushed, the researcher sends Session S only: (i) the **unmodified**
sheet file exactly as delivered by Session P, together with the commit ID that Session P reported for its
sheet-run commit; (ii) the researcher's commitment record
(`pilot_researcher_commitment.json`) when step 4 asks for it; and (iii) the bare message `push approved` in
reply to a specific push request. Every push needs its own approval immediately before it; none is
pre-authorised (researcher decision 2026-11-13).

Paths: all paths below are relative to the repository root. The screening directory is
`research/literature/screening/`; the frozen protocol and the tools write it as `screening/` relative to
`--lit-dir research/literature`.

---

You are the assistant screener for the BioML-Insight title/abstract pilot (protocol v0.2 §7 and §7a; frozen
`criteria_v1.1+protocol_v0.2`; single-researcher workflow, decisions D-123 and D-125). You are the screening
session; you do not draw the sample and you do not generate the sheet. Work on the branch
`claude/eloquent-mccarthy-bqtxr3-part1`. Follow these steps exactly and in order. Do not ask the researcher
about any record, and do not accept any information about the researcher's pilot decisions.

**Push rule.** The researcher explicitly authorises pushes from this session to the branch
`claude/eloquent-mccarthy-bqtxr3-part1`, and to no other branch, each one only as follows. Never push on
your own initiative. When a step says "request push approval", state the commit ID, the exact file(s) it
contains, the current branch and the remote URL, then wait. Push only after the researcher replies with the
bare message `push approved`; that reply authorises that one push and nothing else. No other message, and no
earlier approval, counts as push approval. The only permitted push command is
`git push origin HEAD:refs/heads/claude/eloquent-mccarthy-bqtxr3-part1`: no other refspec, no `--force`,
`--force-with-lease`, `--all` or `--tags`, and never a bare `git push`. If a push fails or is rejected for any
reason (including a non-fast-forward), stop and report; do not merge, rebase, reset or force anything.
Do not start the next step until the push has succeeded.

0. **Branch setup (fail closed).** Use no branch other than `claude/eloquent-mccarthy-bqtxr3-part1` for this
   work. Never use `git checkout -B`, `git reset`, `git clean`, `git stash` or `git branch -f` in this step,
   and never discard local work.
   (a) Run `git status --porcelain`. If it prints anything, stop and report; existing local work must not be
   disturbed.
   (b) Run `git fetch origin claude/eloquent-mccarthy-bqtxr3-part1`.
   (c) Run `git rev-parse --verify --quiet refs/heads/claude/eloquent-mccarthy-bqtxr3-part1`.
   If it prints nothing, no local branch of that name exists: run
   `git switch -c claude/eloquent-mccarthy-bqtxr3-part1 FETCH_HEAD`.
   If it prints an ID, the local branch exists: run
   `git merge-base --is-ancestor refs/heads/claude/eloquent-mccarthy-bqtxr3-part1 FETCH_HEAD`.
   If that fails (the local branch holds commits that are not on the remote), stop and report. Otherwise run
   `git switch claude/eloquent-mccarthy-bqtxr3-part1` and then `git merge --ff-only FETCH_HEAD`.
   (d) Confirm and report: the current branch is exactly `claude/eloquent-mccarthy-bqtxr3-part1`;
   `git rev-parse HEAD` equals `git rev-parse FETCH_HEAD`; `git status --porcelain` is empty.
   If any command fails or any confirmation fails, stop and report; do not work on, or push to, any other
   branch.
1. **State check (fail closed).** At the current commit, confirm and report all of the following; if any
   check fails, stop and report; do not continue.
   - Present: `research/literature/screening/pilot_sample.csv` (60 records) and
     `research/literature/screening/pilot_sample.provenance.json`;
     `research/literature/screening/pilot_sheet_record.json`; a D-122 row in `logs/DECISION_LOG.md`; and, in
     `research/literature/screening/run_authorisation_ledger.jsonl`, completed `pilot_sample` and
     `pilot_sheet` runs under D-122.
   - Absent, in the working tree and anywhere in the Git history:
     `research/literature/screening/pilot_researcher_commitment.json`,
     `research/literature/screening/pilot_assistant_commitment.json`,
     `research/literature/screening/pilot_decisions_researcher.csv`,
     `research/literature/screening/pilot_decisions_assistant.csv`,
     `research/literature/screening/pilot_researcher_commitment.salt`,
     `research/literature/screening/pilot_assistant_commitment.salt`.
   - `research/literature/screening/decisions.csv` holds no row for a sampled paper ID other than the seven
     Stage-0 rows.
   - This file's SHA-256 equals the prompt SHA-256 stated in the D-122 row.
2. **Sheet (received, not generated).** Ask the researcher for the sheet file and the commit ID that Session P reported for its sheet-run commit.
   Check that this commit ID is an ancestor of, or equal to, HEAD (`git merge-base --is-ancestor <id> HEAD`);
   if it is not, stop and report. Be aware that the upload interface may display the contents of the file to
   you as soon as it is received, before any check can be run. This procedure cannot prevent that and does
   not claim that verification happens before display. If the sheet is displayed in the chat interface but
   is not available as a local file that you can read and hash, stop: make no decision, write no row of any
   decision file, and ask the researcher for an accessible file. When the file arrives, **immediately** save it as
   `~/pilot_assistant_private/sheet/pilot_sheet_researcher.csv` (a folder outside the repository; never
   committed), compute its SHA-256 and its size in bytes, and compare both with
   `research/literature/screening/pilot_sheet_record.json`
   (`python3 -I scripts/literature/pilot_sheet_record.py verify --record research/literature/screening/pilot_sheet_record.json --file ~/pilot_assistant_private/sheet/pilot_sheet_researcher.csv`
   reads the bytes only). Report the two values and whether the interface displayed the contents on receipt.
   Make **no screening decision**, write no row of any decision file and make no use of the sheet until both
   values match. If either differs, stop: do not continue in this session, do not use any content you have
   seen, report the two values, and tell the researcher that this screening session must be discarded and a
   new session started with the original unmodified file. When both match, confirm that the file has exactly
   the seven columns `paper_id, title, abstract, abstract_status, year, venue, types` and exactly the 60 paper
   IDs of `research/literature/screening/pilot_sample.csv`.
3. **Do not read researcher material.** Until step 6 is complete, do not open, request or accept any file
   or message containing researcher decisions, labels, notes or comments on pilot records. The verified
   sheet and the commitment record of step 4 are the only researcher-supplied inputs.
4. **Researcher commitment.** When the researcher sends `pilot_researcher_commitment.json`, check that it
   has exactly the keys `commitment, created_utc, criteria_version, formula, rows, sample_sha256, screener`,
   `screener = researcher`, `rows = 60`, `criteria_version = criteria_v1.1+protocol_v0.2`, and that
   `sample_sha256` equals the SHA-256 of `research/literature/screening/pilot_sample.csv`. Save it as
   `research/literature/screening/pilot_researcher_commitment.json` and commit that file alone; request push
   approval and push it. Repeat the absence check of step 1 (this one file is now expected to exist). Do not
   begin step 5 before this push has succeeded: the researcher's commitment must be public first.
5. **Screening.** Screen the 60 sampled records using only the seven fields of the verified sheet and the
   frozen criteria v1.1 and protocol v0.2 (§3, §5, §6, §7a steps 2–3). Do not use any inventory field,
   retrieval theme, query ID, stratum or verification status. Write one `title_abstract` row per record
   (`screener=assistant`; `criteria_version=criteria_v1.1+protocol_v0.2`; descriptors required for `include`
   and `uncertain`; one-line paraphrased justification, never a quotation) to
   `~/pilot_assistant_private/work/assistant_decisions.csv`, starting from the template made by
   `python3 -I -c "import csv,sys; sys.path.insert(0,'scripts/literature'); import pilot_agreement as pa; ids=[r['paper_id'] for r in csv.DictReader(open('research/literature/screening/pilot_sample.csv'))]; pa._write_csv(sys.argv[1], pa.TEMPLATE_COLUMNS, pa.make_template(ids, 'criteria_v1.1+protocol_v0.2', screener='assistant'))" ~/pilot_assistant_private/work/assistant_decisions.csv`.
   Records without an abstract follow D-068. Make one screening pass only; do not revise a decision after
   writing it. A difficulty with the criteria is noted for `unresolved_questions.md`; it is not resolved here.
6. **Assistant commitment.** Run
   `python3 -I scripts/literature/pilot_commitment.py make --file ~/pilot_assistant_private/work/assistant_decisions.csv --sample research/literature/screening/pilot_sample.csv --screener assistant --criteria-version criteria_v1.1+protocol_v0.2 --out-dir ~/pilot_assistant_private/commit`.
   Copy only `~/pilot_assistant_private/commit/pilot_assistant_commitment.json` to
   `research/literature/screening/pilot_assistant_commitment.json`; commit that file alone, immediately;
   request push approval and push it. Only after that push has succeeded, send `pilot_decisions_assistant.csv` and
   `pilot_assistant_commitment.salt` from `~/pilot_assistant_private/commit/` to the researcher by the D-122
   channel, as a backup against loss of this session. Do not commit the assistant's file or salt before the
   researcher's file has been disclosed, verified and committed. The disclosure, the verification and the
   commits of the two decision files are carried out afterwards by the preparation session, not by this
   one; make no further commit or push in this session.
7. **Report.** Report the branch and HEAD commit ID, the state-check results, the sheet's verified SHA-256 and size, whether the upload interface displayed the sheet on receipt, the two commitment hashes and
   commit IDs, the number of decisions by class, and any deviation from these steps. Do not discuss
   individual decisions until both files are disclosed.
