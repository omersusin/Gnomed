# TEST — draw `stride` (a comparison run, 2026-11-23, round 2)

The owner compares models on the same app. Draw the icon of `stride` (all four styles), the way
the repository's documents say. Nothing else.

0. Draw YOUR OWN: never open another branch or another model's work (`compare/*`, `test/*`,
   `git log --all`, `git show <branch>:...`). The owner compares models.
1. Read, in this order: START-HERE.md, docs/METHOD.md (the most important: how to think and what
   to draw), REDESIGN.md §5, docs/BATCH.md §3. Look at docs/kit.png (the ready carriers) and METHOD.md's idea patterns (§1b).
2. `python3 tools/fetch_refs.py stride`, then `python3 tools/next.py stride --app-only` and do what
   it prints. Write the `ideas:` block before choosing anything (METHOD.md §1b).
3. This is a batch run: write the approved/keep lines exactly as docs/BATCH.md §3 step 4 shows. Do
   NOT ask the owner anything while you work.
4. `python3 tools/make_icon.py stride` takes up to a few minutes and prints only at the end - wait.
5. Look at it: `python3 tools/overview.py stride --out ~/Downloads/gnomed/stride-deepseek.png` and
   look at the picture. Fix what the gate and your eye find (METHOD.md §5) until
   `python3 tools/next.py stride --app-only` says ASK_Q2.
6. Do NOT run pack_add / pack_refresh. Commit and push ONLY to this branch:
   `git add -A && git commit -m "stride by <model>" && git push origin test/deepseek-stride`
7. Tell the owner (Turkish, short): the picture's path, your four ideas, the last `summary:` line.
