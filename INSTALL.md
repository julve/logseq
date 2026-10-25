### [logseq](http://logseq.com)

You can install this theme from the logseq marketplace.

OR you can follow these old methods:

- Paste this line to your `logseq/custom.css` file:
- `@import url('https://cdn.jsdelivr.net/gh/dracula/logseq@master/custom.css');`

OR

- Paste this line to your `logseq/config.edn` file:
- `:custom-css-url "@import url('https://cdn.jsdelivr.net/gh/dracula/logseq@master/custom.css');"`

#### Activating theme

1. Open the side bar
2. Go to themes
3. Choose Dracula
4. Boom! It's working

## Logseq DB

Use dark mode and load this checkout's `custom.css` through Logseq's custom
CSS editor (Settings → General → Edit custom.css). Paste the CSS contents,
then reload Logseq. DB graphs do not require a filesystem `logseq/` folder.
If your build supports loading unpacked themes, select this checkout and
choose **Dracula theme** instead.

The theme includes DB semantic colors, property priority icons, menus and
popovers, while retaining the legacy file-graph colors. Light mode keeps
Logseq's own colors. The CDN instructions above load the published upstream
version; they do not include local changes until those changes are published.
