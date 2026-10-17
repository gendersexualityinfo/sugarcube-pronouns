# Pronouns for SugarCube

A pronoun picker for Twine games made with SugarCube 2. Players can choose:

- one set: she/her, he/him, they/them, or their own (like xe/xem or ey/em)
- two sets: some characters use one, and some use the other
- any pronouns: each character picks she, he, or they, and sticks with it
- just my name: everyone uses the player's name instead

Players can also pick the name and pronouns of another character, like a rival or a love interest.

You write each line once, and it reads right for every choice. Players can change names and pronouns at any point, and their choices are kept in saves. The picker works with a keyboard, doesn't rely on color, and fits phone screens at large text sizes.

Made by Charlie Ocean (they/them). Tested with SugarCube 2.37.3.

## Try it first

There are two short demos in the `demo` folder. To get one, click the file here on GitHub, then the download button at the top right of the file. Open the downloaded file in your browser:

- `demo.html`: the player picks their own first name and pronouns, including two sets.
- `character-demo.html`: the player picks the name and pronouns of someone they met at a bookstore.

To see how a demo is built, import it into Twine (**Library → Import**, then pick the `.html` or `.twee` file). Its "Read me first" passage explains what each passage does.

## Which files you need

| You use | Get these |
|---|---|
| The Twine app | `pronouns.js` and `pronouns.css` |
| Tweego | `pronouns.twee` |

You don't need anything else. The `demo` and `tools` folders are only for trying it out and building the files.

## Setup in Twine

1. Copy everything in `pronouns.js` into your story's JavaScript (in Twine: **Story → JavaScript**).
2. Copy everything in `pronouns.css` into your story's stylesheet (**Story → Stylesheet**).
3. In a passage near the beginning, add the start screen. Give it the passage to go to next and the button's text:

   ```
   <<pronounpicker "Chapter 1" "Start the story">>
   ```

   That shows a first-name box, the pronoun picker, and the button. If something's missing when the player clicks the button, a short note asks for it ("Please type your first name.") and moves them right to it.

4. Let players change their name and pronouns later. Add this to your `StoryMenu` passage (make one if you don't have it):

   ```
   <<link "Name and pronouns">><<run setup.pronouns.open()>><</link>>
   ```

That's it. Now write your story with the tokens below.

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

For the player's first name, write `{name}`, or `{name's}` for the possessive. If the name is blank, it says "Friend" instead, so a sentence never ends up with a gap.

**Verbs:** write the they form first, then the she/he form, with a slash: `{are/is}`, `{were/was}`, `{run/runs}`, `{have/has}`. The they form always goes first, even if you're used to writing "is/are." A verb matches the nearest pronoun before it: `{they}`, `{they're}`, `{they've}`, or a character's `{crush:they}`. That works across line breaks, links, and bold or italic text too.

```
{name} grabs {their} coat. {They} {run/runs} for the bus.
```

With they/them, that reads "Robin grabs their coat. They run for the bus." With any other set, the verb is singular, so neopronouns and names read right too: "Xe runs," "Robin runs."

**Just my name:** `{themself}` becomes the name ("Robin made tea for Robin"), which can sound a little off. If a sentence reads strangely that way, try rewriting it so it doesn't need `{themself}`.

## Two sets of pronouns

Some people use two sets, like she/her and they/them. When a player picks two, you decide which characters use which set:

1. Make up a short label for each character who should use the second set: lowercase, with no spaces, like `pip` or `ms-lee`. List the labels in your story's JavaScript, below the code you pasted in:

   ```js
   setup.pronouns.config.secondSetSpeakers = ["pip"];
   ```

   Everyone not on the list (the narrator, every other character, and any text you don't label) uses the first set.

2. Make a passage tagged `widget` and paste in this `say` widget. It marks whose line is whose:

   ```
   <<widget "say" container>><div class="say" @data-speaker="_args[0]"><strong>_args[1]:</strong> _contents</div><</widget>>
   ```

3. Write each character's lines with it. The first word is the label, and the second is the name shown on screen:

   ```
   <<say "pip" "Pip">>Has anyone seen {name}? {They're} late again.<</say>>
   <<say "marisol" "Marisol">>Give {them} a minute. {They} always {stop/stops} for coffee.<</say>>
   ```

For a single word outside the widget, put the label right in the token: `{them@pip}`. To use the second set without a character at all, write `@2`: `{they@2}`.

With she/her first and they/them second, players see:

> **Pip:** Has anyone seen Robin? They're late again.
>
> **Marisol:** Give her a minute. She always stops for coffee.

You don't have to plan for players who pick something else. With one set, Pip uses it like everyone does. With just my name, everyone uses the name. With any pronouns, see below.

## Any pronouns

When a player picks any pronouns, each character picks she, he, or they and keeps it for the whole story. The labels from the last section decide who's who, so Pip always says the same thing, and so does Marisol. Unlabeled text counts as the narrator, which also keeps one set. You don't need to change anything for this to work.

## Other characters

Your player can also pick the name and pronouns of someone else in the story: a rival, a best friend, or a love interest.

1. Set the character up in your story's JavaScript, below the code you pasted in. Give them a label (lowercase, with no spaces), the names to choose from, and a stand-in name and pronouns, so the player can just click through if they'd rather not choose:

   ```js
   setup.pronouns.character("crush", {
   	names: ["Jordan", "Maya", "Andre"],
   	name: "Jordan",
   	pronouns: "they"
   });
   ```

2. Add the picker to a passage, with the passage to go to next and the button's text. Write your own question above it:

   ```
   Who was it?

   <<characterpicker "crush" "Bookstore" "Tell Riley">>
   ```

   The player sees name buttons for Jordan, Maya, and Andre, then she/her, he/him, and they/them, with room to write their own. Jordan and they/them start out picked.

3. Write the character's lines with their label and a colon in front of each token:

   ```
   {crush:name} pulls a book off the shelf. {crush:They} {say/says} it's {crush:their} favorite.
   ```

   With Maya and she/her, that reads "Maya pulls a book off the shelf. She says it's her favorite." The verb matches the nearest pronoun before it, so `{say/says}` follows the crush here.

4. Let players change their mind later. Add this to your `StoryMenu` passage:

   ```
   <<link "Crush's name and pronouns">><<run setup.pronouns.open("crush")>><</link>>
   ```

Every token works with a label: `{crush:they}`, `{crush:them}`, `{crush:their}`, `{crush:theirs}`, `{crush:themself}`, `{crush:they're}`, `{crush:name}`, `{crush:name's}`, and so on. Tokens without a label still mean the player, so you can use both in the same sentence.

More options for `setup.pronouns.character()`:

| Option | What it does |
|---|---|
| `names` | The names to choose from, shown as buttons. Leave it out for a first-name box instead |
| `name` | The stand-in name, until the player picks |
| `pronouns` | The stand-in pronouns: `"she"`, `"he"`, `"they"`, `"xe"`, or `"ze"` (or a set of your own, like `{ subj: "ey", obj: "em", det: "eir", poss: "eirs", refl: "emself" }`) |
| `customPronouns` | Set to `false` to offer only she/her, he/him, and they/them, without the boxes for writing your own |
| `title` | The title of the window that `setup.pronouns.open("crush")` opens |

## Settings

Change these in your story's JavaScript, below the code you pasted in. That way you can paste in a new version of `pronouns.js` later without losing them.

```js
setup.pronouns.config.secondSetSpeakers = ["pip"];
setup.pronouns.config.requireName = false;
```

| Setting | What it does | Starts as |
|---|---|---|
| `secondSetSpeakers` | Labels of the characters who use the second set | `[]` (nobody) |
| `nameVariable` | The story variable that holds the player's first name | `"playerName"` |
| `defaultName` | What `{name}` says if the name is blank | `"Friend"` |
| `requireName` | `true`: players must type a name to continue. `false`: they can skip it | `true` |
| `rememberLastChoice` | `true`: a new game fills in this browser's last name and pronouns. `false`: a new game starts blank, so nobody sees the last player's choice on a shared computer | `false` |
| `dialogTitle` | The title of the "Name and pronouns" window | `"Name and pronouns"` |

## Good to know

- Tokens work anywhere text appears on screen: passages, widgets, links, `StoryCaption`, and text added later by macros like `<<linkreplace>>`.
- Tokens aren't filled in inside HTML attributes (like `title` or `alt`). For those, or anywhere else in your own code, use `setup.pronouns.fill()`.
- To show a token as written, put it inside `data-pronouns="off"`, or in code formatting (SugarCube's `{{{ }}}`).
- When a player changes their name or pronouns, the change sticks. Going back a screen, reloading, or loading an earlier save from the same playthrough uses the new ones. Saves from other playthroughs keep their own.
- Until the player picks, everyone uses they/them.
- Names keep the capital letters the player types, so "Mary Jane," "Jean-Luc," and all-lowercase names come out the way they wrote them.
- SugarCube records changes when the player moves to the next screen. So if a player changes their pronouns and saves on that same screen, the save holds the old ones. In the same browser, the newest choice still wins, so this only matters for a save exported to a file and loaded somewhere else.
- To build your own start screen instead, use plain `<<pronounpicker>>`. It shows just the picker, without the name box or button, and saves the choice as the player makes it. `setup.pronouns.chosen()` tells you whether they've picked.

## For your own code

```js
setup.pronouns.fill("{They} waved.", "pip")  // fill tokens in any text; the label is optional
setup.pronouns.open()                        // open the "Name and pronouns" window
setup.pronouns.describe()                    // "she/her", "she/her and they/them", "any pronouns", or "just my name"
setup.pronouns.chosen()                      // true once the player has picked
setup.pronouns.name()                        // the player's first name, or "Friend" if it's blank
setup.pronouns.choose("they")                // pick for the player: "she", "he", "they", "xe", "ze", "any", or "name"
setup.pronouns.choose("she", "they")         // two sets

setup.pronouns.open("crush")                 // a character's "Name and pronouns" window
setup.pronouns.name("crush")                 // their name (or the stand-in, until the player picks)
setup.pronouns.describe("crush")             // their pronouns, like "they/them"
setup.pronouns.chosen("crush")               // true once the player has picked for them
setup.pronouns.chooseFor("crush", "she", "Maya")  // pick for them from code
```

Your own set works too: `setup.pronouns.choose({ subj: "ey", obj: "em", det: "eir", poss: "eirs", refl: "emself" })`.

To react when a choice changes, listen for `:pronounschange`. It passes `""` for the player, or the character's label:

```js
$(document).on(":pronounschange", function (event, who) {
	// who is "" for the player, or a label like "crush"
});
```

## Credits

Inspired by [Chapel's Pronoun Templates](https://github.com/ChapelR/custom-macros-for-sugarcube-2/blob/master/docs/pronoun-templates.md) and Sylveranty's tutorial [Coding Pronouns and Verbs in Twine SugarCube](https://sylveranty.itch.io/coding-pronouns-and-verbs-in-twine-sugarcube). Thank you both.

The demo pages (`demo.html` and `character-demo.html`) include [SugarCube](https://www.motoslave.net/sugarcube/2/) by Thomas Michael Edwards, under its own license ([demo/SUGARCUBE-LICENSE.txt](demo/SUGARCUBE-LICENSE.txt)).

## License

Public domain ([The Unlicense](LICENSE)). Use it in any game, free or paid, and change it however you like. Credit isn't required, but it's always appreciated. (SugarCube itself, inside the demo pages, keeps its own license.)

## Support and feedback

If this helped you, a star (the ☆ button at the top of this page) helps other Twine folks find it.

Found a bug, or want something added? [Open an issue](../../issues) and tell me. Ideas for updates are welcome too.

If you use this in a game, I'd love to see it! You can find my games and apps at [charlieocean.itch.io](https://charlieocean.itch.io), and more of my work at [gendersexuality.info](https://gendersexuality.info).
