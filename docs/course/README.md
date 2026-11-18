# The Gnomed icon course

A step-by-step course for **anyone who makes Gnomed icons — people and AI models of
any size**. It assumes nothing. Every lesson shows real pictures from this project,
the exact commands, and what you should see after each command.

If you are an AI agent, also obey [`../../AGENTS.md`](../../AGENTS.md).

## How to take the course

Read the lessons **in order**, the first time completely. Later you only need lesson 5
(the routine) and lesson 4 (the fixes).

| # | Lesson | You will learn |
|---|---|---|
| 1 | [Concepts](01-concepts.md) | what an icon pack is, appfilter, ComponentInfo, the four styles |
| 2 | [Anatomy of a GNOME icon](02-gnome-anatomy.md) | face, chin, lift, negative space, colours, the numbers |
| 3 | [The pipeline](03-pipeline.md) | what every tool does and which file it writes |
| 4 | [Recipes: symptom → fix](04-recipes.md) | how to repair every problem we have met (with before/after pictures) |
| 5 | [Worked example: one app from zero](05-worked-example.md) | the routine, command by command, with expected output |
| 6 | [Hand-built icons](06-hand-built.md) | when the automatic route fails: posters, crops, boxes, blurry sources |
| 7 | [Shipping](07-shipping.md) | adding to the pack, pull request, what the maintainer does |

## The three things that matter most

1. **The quality gate decides, not your feeling.** Run `python3 tools/check_icon.py <slug>`.
   Fix every `FAIL`. Each line tells you which recipe (R1 … R15) to apply.
2. **Never draw a logo from memory, never use an image generator.** Everything is
   measured from `work/<slug>/source.png`.
3. **Never invent an app's ComponentInfo, never delete anything from the pack.**

## If you cannot see images

Some AI models cannot look at pictures. You can still do the job:

* `tools/check_icon.py` measures what a reviewer would look for (visibility on light
  and dark wallpapers, stripes, box inside the plate, floating symbols, small-size
  legibility, trace accuracy) and prints the fix.
* Every picture in this course is described in words next to it.
* At the end, write in your pull request: *"I could not look at the images; the
  maintainer must review work/&lt;slug&gt;/styles.png."* That is honest and fine.

## Regenerating the pictures

All pictures are produced from the project's own files:
`python3 docs/course/make_figures.py`. The "before" images are real: the same app built
with the fix switched off.
