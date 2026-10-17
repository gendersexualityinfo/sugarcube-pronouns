"""Builds demo/demo.twee from the demo passages below plus pronouns.js and
pronouns.css, so the demo always has the current code.

    python3 tools/make-demo.py

Optional: pass a compiled SugarCube 2 game (.html) to also write a playable
demo page, using that file's copy of the SugarCube engine:

    python3 tools/make-demo.py path/to/any-sugarcube-game.html out.html
"""
import html
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
IFID = "7B1E2C4A-5D3F-4E8B-9A61-2F0C8D4B7E35"

PASSAGES = [
    ("StoryInit", "", '<<set $playerName to "">>'),
    ("StoryMenu", "", '<<link "Name and pronouns">><<run setup.pronouns.open()>><</link>>'),
    ("Widgets", "widget", """<<widget "say" container>><div class="say" @data-speaker="_args[0]"><strong>_args[1]:</strong> _contents</div><</widget>>"""),
    ("Start", "", """What's your name?
<<textbox "$playerName" "">>

<<pronounpicker>>

[[Start the story|Porch]]"""),
    ("Porch", "", """It's a gray morning. $playerName steps out onto the porch, and {they're} glad {they} brought a sweater. {They} {sit/sits} on the top step with {their} coffee.

<<say "sam" "Sam">>Morning! I saved {them} a muffin. {They're} going to love it.<</say>>

<<say "jo" "Jo">>Sam's been guarding that muffin all week. It's {theirs}, Sam. Hand it over.<</say>>

<<linkreplace "Ask what's going on">>Sam grins at Jo. "Nothing! {They@sam} always {worry/worries} too much about breakfast." Sam passes over the muffin, and {they} {laugh/laughs}.<</linkreplace>>

Right now your pronouns are: <<= setup.pronouns.describe() || "not picked yet">>.

You can change your name and pronouns anytime from "Name and pronouns" in the menu.

[[Go back inside|Inside]]"""),
    ("Inside", "", """Inside, it's warm. $playerName hangs up {their} sweater. {They've} got the whole afternoon free, so {they} {make/makes} tea and {treat/treats} {themself} to the last muffin.

[[Back to the porch|Porch]]
[[Start over|Start]]"""),
]

SETUP_JS = """
/* demo only: Sam uses the second set if the player picks two */
setup.pronouns.config.secondSetSpeakers = ["sam"];
"""

DEMO_CSS = """
/* demo only */
.say { margin: 1em 0; padding: 0.5em 1em; border-left: 4px solid currentColor; }
"""


def code():
    js = (ROOT / "pronouns.js").read_text(encoding="utf-8") + SETUP_JS
    css = (ROOT / "pronouns.css").read_text(encoding="utf-8") + DEMO_CSS
    return js, css


def twee():
    js, css = code()
    out = [
        ":: StoryTitle\nPronouns for SugarCube: demo\n",
        ':: StoryData\n{\n  "ifid": "%s",\n  "format": "SugarCube",\n  "format-version": "2.37.3",\n  "start": "Start"\n}\n' % IFID,
        ":: Story JavaScript [script]\n" + js + "\n",
        ":: Story Stylesheet [stylesheet]\n" + css + "\n",
    ]
    for name, tags, text in PASSAGES:
        if tags == "script-extra":
            continue
        out.append(":: %s%s\n%s\n" % (name, " [%s]" % tags if tags else "", text))
    return "\n".join(out)


def page(engine_file):
    js, css = code()
    src = pathlib.Path(engine_file).read_text(encoding="utf-8")
    a = src.index("<tw-storydata")
    b = src.index("</tw-storydata>") + len("</tw-storydata>")
    pid = 0
    parts = []
    for name, tags, text in PASSAGES:
        if tags == "script-extra":
            continue
        pid += 1
        parts.append('<tw-passagedata pid="%d" name="%s" tags="%s" position="%d,100" size="100,100">%s</tw-passagedata>'
                     % (pid, html.escape(name), tags, pid * 150, html.escape(text)))
    start = 1 + [p[0] for p in PASSAGES if p[1] != "script-extra"].index("Start")
    data = ('<tw-storydata name="Pronouns demo" startnode="%d" creator="make-demo.py" creator-version="1" '
            'format="SugarCube" format-version="2.37.3" ifid="%s" options="" tags="" zoom="1" hidden>'
            '<style role="stylesheet" id="twine-user-stylesheet" type="text/twine-css">%s</style>'
            '<script role="script" id="twine-user-script" type="text/twine-javascript">%s</script>%s</tw-storydata>'
            % (start, IFID, css, js, "".join(parts)))
    head = src[:a]
    # the engine file's own <title> is replaced so the page never names another game
    t1, t2 = head.find("<title>"), head.find("</title>")
    if t1 != -1 and t2 != -1:
        head = head[:t1] + "<title>Pronouns demo</title>" + head[t2 + len("</title>"):]
    return head + data + src[b:]


if __name__ == "__main__":
    (ROOT / "demo").mkdir(exist_ok=True)
    (ROOT / "demo" / "demo.twee").write_text(twee(), encoding="utf-8")
    print("wrote demo/demo.twee")
    if len(sys.argv) == 3:
        pathlib.Path(sys.argv[2]).write_text(page(sys.argv[1]), encoding="utf-8")
        print("wrote", sys.argv[2])
