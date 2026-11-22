# apple_music - fixes (the owner's review of overview ara-2)
group: ara-2
owner: "Bıktım bana prompt vermenden, yaz depoya" (2026-11-22)
review: ~/Downloads/gnomed/ara-2.png, written down by Claude in the owner's session (2026-11-22)
shown:

Change EXACTLY these styles; the others stay as they are. Rules: REDESIGN.md 5 (the mark
stays on every style; Faithful = the object closest to the logo). How: docs/PLAYBOOK.md#owner-fix

- [ ] all: the Apple Music note is in NO style - the measured note - put_mark(ic, SLUG, box) - on every style, >= 36 px of 128 (gate mark)
- [ ] faithful: the turntable is not the closest to the logo - make the note itself a solid object (L1), red-pink like the Apple Music logo (HIG Red ramp); the note is reserved for apple_music (categories.py RESERVED)
- [ ] symbol: the cassette with a pencil is not recognisable, and the cassette is Deezer's (music) - a new object you can name, the note on it; no record, cassette or bar chart (deezer uses them)
- [ ] disc: the microphone/record mix is odd - one round object you can name (not a record), the note on it
- [ ] rimmed: the radio is good - put the note on its front (grille or dial), >= 36 px
