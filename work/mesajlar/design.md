# mesajlar - design note (REDESIGN.md)

source: work/mesajlar/source.png (white speech bubble with three green lines on a green tile)
store: system app (Android Messages; GNOME Chatty is the model)
kind: app
category: messaging
ladder: L1 (the bubble as an object) + L2 (a message that travels)
characters: no
references: GNOME Chatty (a speech bubble), Android Messages (white bubble + green lines).
anchors (2-4 things that make the app recognisable; they must survive):
  1. the speech bubble with three lines (the source mark)
  2. green + white (the source palette)
  3. sending a message
function object (what the app does, as a physical thing): a message - speech bubble, two bubbles,
  a notification bubble, mailbox.

concepts (work/mesajlar/concepts.png) - four different ideas:
  A: L1 - the source bubble in the app's green with light lines (Faithful, closest to the logo).
  B: L2 - two chat bubbles: a green one behind and a dark one with light lines in front (main).
  C: L2 round - a round chat bubble with a red notification badge (Disc).
  D: L2 - a mailbox on a post with a letter and a red flag (Rimmed).

approved: B - "batch: Biz onayladıktan sonra hepsini yapsın" (2026-11-22)
keep: A, C, D - "batch: hepsi kullanılsın" (2026-11-22)
final:
styles: symbol=B faithful=A disc=C rimmed=D
decisions I made myself (and why; mention them in Q2):
  - the bubble is white in the source tile; it is green here so it reads on a light wallpaper
  - no paper plane (Telegram's logo) and no envelope (Telegram uses it): the main is two bubbles
  - four different message objects: one bubble, two bubbles, a notification bubble, a mailbox
  - the owner: the Disc looked like a medal, so it is a round bubble with a badge (2026-11-22)
techniques used (min. 3): thickness / material gradient / top light / recess / secondary object
palette (GNOME HIG names): Green 1-5 (#8ff0a4 #57e389 #33d17a #2ec27e #26a269),
  Light 1-4 (#ffffff #f6f5f4 #deddda #c0bfbc), Dark 1-4 (#77767b #5e5c64 #3d3846 #241f31),
  Red 1-5 (#f66151 #ed333b #e01b24 #c01c28 #a51d2d)
review (phone.png + review.png: light + dark, holes, baseline, what is still weak):
