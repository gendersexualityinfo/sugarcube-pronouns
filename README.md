# Pronouns for SugarCube

A pronoun picker for Twine games made with SugarCube 2. Players can choose:

- one set: she/her, he/him, they/them, or their own (like xe/xem or ey/em)
- two sets: some characters use one, and some use the other
- any pronouns: each character picks she, he, or they, and sticks with it
- just my name: everyone uses the player's name instead

Players can change their name and pronouns at any point, and their choice is kept in saves. The picker works with a keyboard, doesn't rely on color, and fits phone screens.

Made by Charlie Ocean (they/them). Tested with SugarCube 2.37.3.

## Setup

1. Copy everything in `pronouns.js` into your story's JavaScript (in Twine: **Story → JavaScript**).
2. Copy everything in `pronouns.css` into your story's stylesheet (**Story → Stylesheet**).
3. Put the start screen in a passage near the beginning. Name the passage to go to next, and the button text:

   ```
   <<pronounpicker "Chapter 1" "Start the story">>
   ```

   That shows a name box, the pronoun picker, and the button. If something's missing when the player clicks the button, a short note asks for it ("Please type your name.") and moves them right to it.

4. Let players change things later. Add this to your `StoryMenu` passage (make one if you don't have it):

   ```
   <<link "Name and pronouns">><<run setup.pronouns.open()>><</link>>
   ```

The player's name lives in `$playerName`. To use a different variable, change `nameVariable` at the top of `pronouns.js`. To let players skip the name, set `requireName` to `false` there. Then a blank name becomes "Friend" (or whatever you set `defaultName` to).

To build your own start screen instead, use plain `<<pronounpicker>>`. It shows just the picker, without the name box or button, and saves the player's choice as they make it, and `setup.pronouns.chosen()` tells you whether they've picked.

## Writing with it

Write the they/them version in curly braces, and it becomes whatever the player picked:

| Write | she/her | he/him | xe/xem | just my name |
|---|---|---|---|---|
| `{they}` | she | he | xe | Robin |
| `{them}` | her | him | xem | Robin |
| `{their}` | her | his | xyr | Robin's |
| `{theirs}` | hers | his | xyrs | Robin's |
| `{themself}` | herself | himself | xemself | Robin |
| `{they're}` | she's | he's | xe's | Robin's |
| `{they've}` | she's | he's | xe's | Robin's |
| `{they'll}` | she'll | he'll | xe'll | Robin will |
| `{they'd}` | she'd | he'd | xe'd | Robin would |

Start a token with a capital letter for a capital: `{They}`, `{Their}`, `{They're}`.

For the player's name, write `{name}`, or `{name's}` for the possessive. It uses "Friend" if the name is blank, so a sentence never ends up with a gap.

```
{name} grabs {their} coat. "Wait for me," {they} {call/calls}.
```

**Verbs:** write the they form first, then the she/he form, with a slash: `{are/is}`, `{run/runs}`, `{have/has}`. A verb follows the nearest `{they}` before it.

```
{They} {walk/walks} to the bus stop. {They're} late again.
```

They/them gets "They walk," and every other set gets the singular, so neopronouns and names read right too: "Xe walks," "Robin walks."

**Just my name:** `{themself}` becomes the name ("Robin made tea for Robin"), which can sound a little off. If a sentence reads strangely that way, try rewriting it so it doesn't need `{themself}`.

## Two sets and any pronouns

By default, everyone uses the player's first set. To have a character use the second set, add them to `secondSetSpeakers` at the top of `pronouns.js`:

```js
secondSetSpeakers: ["sam", "jo"],
```

Then tell the tokens who's talking, either in the token itself:

```
"I saved {them@sam} a seat," Sam says.
```

or around a whole block of text, which is handy in widgets:

```
<div data-speaker="sam">"I saved {them} a seat. {They} always {sit/sits} by the window."</div>
```

To use the second set without naming a speaker, write `@2`: `{they@2}`.

With any pronouns, the same speaker names decide which set each character uses, and each character always gets the same one.

## Good to know

- Tokens work anywhere text appears on screen: passages, widgets, links, `StoryCaption`, and text added later by macros like `<<linkreplace>>`.
- Tokens aren't filled in inside HTML attributes (like `title` or `alt`). For those, or anywhere else in your own code, use `setup.pronouns.fill()`.
- To show a token as written, put it inside `data-pronouns="off"`, or in code formatting (SugarCube's `{{{ }}}`).
- The newest choice always wins. If a player changes their pronouns, going back a screen, reloading, or loading an older save uses the new ones.
- Until the player picks, everyone uses they/them.

## For your own code

```js
setup.pronouns.fill("{They} waved.", "sam")  // fill tokens in any text; the speaker is optional
setup.pronouns.open()                        // open the "Name and pronouns" window
setup.pronouns.describe()                    // "she/her", "she/her and they/them", "any pronouns", or "just my name"
setup.pronouns.chosen()                      // true once the player has picked
setup.pronouns.name()                        // the player's name, or "Friend" if it's blank
setup.pronouns.choose("they")                // pick for the player: "she", "he", "they", "xe", "ze", "any", or "name"
setup.pronouns.choose("she", "they")         // two sets
```

Your own set works too: `setup.pronouns.choose({ subj: "ey", obj: "em", det: "eir", poss: "eirs", refl: "emself" })`.

## Try the demo

`demo/demo.twee` is a short story that uses all of this. In Twine, choose **Library → Import** and pick the file. Its "Read me first" passage explains what each passage does.

## Credits

Inspired by [Chapel's Pronoun Templates](https://github.com/ChapelR/custom-macros-for-sugarcube-2/blob/master/docs/pronoun-templates.md) and Sylveranty's tutorial [Coding Pronouns and Verbs in Twine SugarCube](https://sylveranty.itch.io/coding-pronouns-and-verbs-in-twine-sugarcube). Thank you both.

## License

Public domain ([The Unlicense](LICENSE)). Use it in any game, free or paid, and change it however you like. Credit isn't required, but it's always appreciated.

## Support and feedback

If this helped you, a star (the ☆ button at the top of this page) helps other Twine folks find it.

Found a bug, or want something added? [Open an issue](../../issues) and tell me. Ideas for updates are welcome too.

If you use this in a game, I'd love to see it! You can find my games and apps at [charlieocean.itch.io](https://charlieocean.itch.io), and more of my work at [gendersexuality.info](https://gendersexuality.info).
