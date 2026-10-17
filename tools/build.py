"""Builds the files people download, so they always have the current code:

    pronouns.twee     the picker's JavaScript and styles, for Tweego users
    demo/demo.twee    the demo story, to import into Twine

    python3 tools/build.py

To also build demo/demo.html (a playable demo that Twine can import too),
point it at SugarCube 2's format.js:

    python3 tools/build.py path/to/sugarcube-2/format.js
"""
import html
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
IFID = "7B1E2C4A-5D3F-4E8B-9A61-2F0C8D4B7E35"
TITLE = "Pronouns for SugarCube: demo"

PASSAGES = [
    ("Read me first", "", """This is the demo for Pronouns for SugarCube. To try it, choose Build, then Play.

What each passage does:

Start: the player types a name and picks pronouns. The button won't move on until both are filled in.
Porch and Inside: two short scenes that use the name and pronoun tokens.
StoryInit: starts the name out blank.
StoryMenu: adds "Name and pronouns" to the sidebar, so players can change them anytime.
Widgets: a "say" widget, so each character's lines use that character's pronouns.

The picker's code is in Story, then JavaScript, and its styles are in Story, then Stylesheet.

Nothing links to this passage, so players never see it."""),
    ("StoryInit", "", '<<set $playerName to "">>'),
    ("StoryMenu", "", '<<link "Name and pronouns">><<run setup.pronouns.open()>><</link>>'),
    ("Widgets", "widget", """<<widget "say" container>><div class="say" @data-speaker="_args[0]"><strong>_args[1]:</strong> _contents</div><</widget>>"""),
    ("Start", "", """Welcome! This short story shows how the pronoun picker works.

<<pronounpicker "Porch" "Start the story">>"""),
    ("Porch", "", """It's a cool fall morning. {name} steps out onto the porch with a mug of coffee. {They} {sit/sits} on the top step and {wave/waves} to the neighbors across the street.

<<say "jo" "Jo">>Morning, {name}! You're up early.<</say>>

<<say "sam" "Sam">>Jo, look. {name's} got the good mug out. {They're} having a nice day.<</say>>

<<say "jo" "Jo">>Leave {them} alone, Sam. {They've} had a long week.<</say>>

<<linkreplace "Wave back">>{name} waves back and laughs. Sam jogs over with a paper bag. "I saved {them@sam} a muffin," Sam tells Jo. "{They@sam} {deserve/deserves} it."<</linkreplace>>

<div class="note">How this demo works: the narrator and Jo use your first set of pronouns. If you picked two sets, Sam uses your second set. With any pronouns, each character picks she, he, or they, and keeps it.

Your pronouns right now: <<= setup.pronouns.describe()>>. You can change your name and pronouns anytime from "Name and pronouns" in the sidebar.</div>

[[Head inside|Inside]]"""),
    ("Inside", "", """Inside, it's warm. {name} hangs {their} jacket by the door. {They've} got the whole afternoon free, so {they} {make/makes} tea and {curl/curls} up with a good book.

[[Back out to the porch|Porch]]"""),
]

# Where each passage sits on Twine's story map: (x, y, size). The notes and
# setup passages go in a column on the left; the story runs on the right,
# laid out so no arrow crosses a passage.
LAYOUT = {
    "Read me first": (50, 50, "200,200"),
    "StoryInit": (50, 300, "100,100"),
    "StoryMenu": (175, 300, "100,100"),
    "Widgets": (50, 425, "100,100"),
    "Start": (375, 50, "100,100"),
    "Porch": (375, 300, "100,100"),
    "Inside": (600, 300, "100,100"),
}

SETUP_JS = """
/* demo only: Sam uses the second set if the player picks two */
setup.pronouns.config.secondSetSpeakers = ["sam"];
"""

DEMO_CSS = """
/* demo only */
.say { margin: 1em 0; padding: 0.5em 1em; border-left: 4px solid currentColor; }
.note { margin: 1.5em 0; padding: 0.75em 1em; border: 1px dashed currentColor; border-radius: 0.5em; font-size: 0.9em; }
"""


def code():
    js = (ROOT / "pronouns.js").read_text(encoding="utf-8") + SETUP_JS
    css = (ROOT / "pronouns.css").read_text(encoding="utf-8") + DEMO_CSS
    return js, css


def twee():
    js, css = code()
    out = [
        ":: StoryTitle\n" + TITLE + "\n",
        ':: StoryData\n{\n  "ifid": "%s",\n  "format": "SugarCube",\n  "format-version": "2.37.3",\n  "start": "Start"\n}\n' % IFID,
        ":: Story JavaScript [script]\n" + js + "\n",
        ":: Story Stylesheet [stylesheet]\n" + css + "\n",
    ]
    for name, tags, text in PASSAGES:
        x, y, size = LAYOUT[name]
        meta = '{"position":"%d,%d","size":"%s"}' % (x, y, size)
        out.append(":: %s%s %s\n%s\n" % (name, " [%s]" % tags if tags else "", meta, text))
    return "\n".join(out)


def library_twee():
    js = (ROOT / "pronouns.js").read_text(encoding="utf-8")
    css = (ROOT / "pronouns.css").read_text(encoding="utf-8")
    return ("/* Pronouns for SugarCube 2, by Charlie Ocean. Public domain (The Unlicense).\n"
            "   For Tweego: add this file to your project. Twine users can paste\n"
            "   pronouns.js and pronouns.css into Story > JavaScript and Story > Stylesheet. */\n\n"
            ":: Pronouns JavaScript [script]\n" + js + "\n\n"
            ":: Pronouns Stylesheet [stylesheet]\n" + css + "\n")


def page(format_js):
    """The demo as a playable page, built the same way Twine publishes a story."""
    js, css = code()
    src = pathlib.Path(format_js).read_text(encoding="utf-8").strip()
    if not src.startswith("window.storyFormat(") or not src.endswith(");"):
        sys.exit("That doesn't look like a story format's format.js file.")
    fmt = json.loads(src[len("window.storyFormat("):-2])
    if fmt.get("name") != "SugarCube" or not str(fmt.get("version", "")).startswith("2."):
        sys.exit("Please use SugarCube 2's format.js.")
    pid = 0
    parts = []
    for name, tags, text in PASSAGES:
        x, y, size = LAYOUT[name]
        pid += 1
        parts.append('<tw-passagedata pid="%d" name="%s" tags="%s" position="%d,%d" size="%s">%s</tw-passagedata>'
                     % (pid, html.escape(name), tags, x, y, size, html.escape(text)))
    start = 1 + [p[0] for p in PASSAGES].index("Start")
    data = ('<tw-storydata name="%s" startnode="%d" creator="Pronouns for SugarCube" creator-version="1" '
            'format="SugarCube" format-version="%s" ifid="%s" options="" tags="" zoom="1" hidden>'
            '<style role="stylesheet" id="twine-user-stylesheet" type="text/twine-css">%s</style>'
            '<script role="script" id="twine-user-script" type="text/twine-javascript">%s</script>%s</tw-storydata>'
            % (html.escape(TITLE), start, fmt["version"], IFID, css,
               js, "".join(parts)))
    out = fmt["source"].replace("{{STORY_NAME}}", html.escape(TITLE)).replace("{{STORY_DATA}}", data)
    return out


if __name__ == "__main__":
    (ROOT / "demo").mkdir(exist_ok=True)
    (ROOT / "pronouns.twee").write_text(library_twee(), encoding="utf-8")
    print("wrote pronouns.twee")
    (ROOT / "demo" / "demo.twee").write_text(twee(), encoding="utf-8")
    print("wrote demo/demo.twee")
    if len(sys.argv) == 2:
        (ROOT / "demo" / "demo.html").write_text(page(sys.argv[1]), encoding="utf-8")
        print("wrote demo/demo.html")
