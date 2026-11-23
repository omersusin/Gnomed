# TEST — draw `mornye` (a comparison run, 2026-11-23)

The owner compares models on the same app. Draw the icon of `mornye` (all four styles), the way
the repository's documents say. Nothing else.

1. Read, in this order: START-HERE.md, docs/METHOD.md (the most important: how to think and what
   to draw), REDESIGN.md §5, docs/BATCH.md §3. Look at docs/kit.png (the ready carriers).
2. `python3 tools/fetch_refs.py mornye`, then `python3 tools/next.py mornye --app-only` and do what
   it prints. Write the `ideas:` block before choosing anything (METHOD.md §1b).
3. This is a batch run: write the approved/keep lines exactly as docs/BATCH.md §3 step 4 shows. Do
   NOT ask the owner anything while you work.
4. `python3 tools/make_icon.py mornye` takes up to a few minutes and prints only at the end - wait.
5. Look at it: `python3 tools/overview.py mornye --out ~/Downloads/gnomed/mornye-deepseek.png` and
   look at the picture. Fix what the gate and your eye find (METHOD.md §5) until
   `python3 tools/next.py mornye --app-only` says ASK_Q2.
6. Do NOT run pack_add / pack_refresh. Commit and push ONLY to this branch:
   `git add -A && git commit -m "mornye by <model>" && git push origin test/deepseek-mornye`
7. Tell the owner (Turkish, short): the picture's path, your four ideas, the last `summary:` line.
