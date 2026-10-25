"""Browser regression checks for DB theme contracts; requires Chromium."""
from pathlib import Path
import shutil
from playwright.sync_api import sync_playwright

root = Path(__file__).resolve().parents[1]
css = (root / 'custom.css').read_text()
# Offline: font availability is unrelated to the color/cascade checks.
css = '\n'.join(line for line in css.splitlines() if not line.startswith('@import'))
classes = ['ui__dropdown-menu-sub-content', 'ui__context-menu-sub-content', 'ui__popover-content', 'ui__select-content', 'ui__calendar']
# Reproduce the local variable declarations in upstream shui.css. Inherited
# root tokens cannot override variables set directly on these containers.
baseline = '\n'.join(f'html[data-theme=dark][data-color=logseq] .{c} {{ --accent: 190 100% 15%; --muted: 192 100% 13%; }}' for c in classes)
markup = ''.join(f'<div class="{c}"><span class="row">Menu</span></div>' for c in classes)
script = r'''
const failures=[];
function equal(label, actual, expected) {if(actual!==expected) failures.push(`${label}: ${actual} != ${expected}`);}
const style = el => getComputedStyle(el);
for (const color of ['logseq', 'tomato', 'none']) {
 document.documentElement.dataset.color=color;
 equal(color+' background',style(document.body).backgroundColor,'rgb(40, 42, 54)');
 for(const row of document.querySelectorAll('.row')) equal(color+' popup',style(row).backgroundColor,'rgb(58, 61, 74)');
 equal(color+' urgent', style(document.querySelector('.ls-icon-priorityLvlUrgent')).color,'rgb(255, 85, 85)');
 equal(color+' medium', style(document.querySelector('.ls-icon-priorityLvlMedium')).color,'rgb(241, 250, 140)');
 equal(color+' low', style(document.querySelector('.ls-icon-priorityLvlLow')).color,'rgb(80, 250, 123)');
 equal(color+' DB label',style(document.querySelector('span.priority')).fontSize,'16px');
 equal(color+' legacy label',style(document.querySelector('a.priority')).fontSize,'0px');
}
document.documentElement.dataset.theme='light';
equal('light background',style(document.body).backgroundColor,'rgb(255, 255, 255)');
equal('light icon',style(document.querySelector('.ls-icon-priorityLvlUrgent')).color,'rgb(0, 0, 0)');
document.getElementById('result').textContent=JSON.stringify(failures);
'''
html = '<html data-theme="dark" data-color="logseq"><meta charset="utf-8"><style>body {background:white;color:black;font-size:16px}.row{background:hsl(var(--accent))}</style><style>'+baseline+'</style><style>'+css+'</style><body>'+markup+'<div class="property-value-inner"><i class="ls-icon-priorityLvlUrgent"></i><i class="ls-icon-priorityLvlMedium"></i><i class="ls-icon-priorityLvlLow"></i><span class="priority">High</span></div><a class="priority" href="#/page/A">A</a><pre id="result"></pre><script>'+script+'</script></body></html>'
with sync_playwright() as pw:
    browser = pw.chromium.launch(executable_path=shutil.which('chromium'), args=['--no-sandbox', '--disable-dev-shm-usage'])
    page = browser.new_page()
    page.set_content(html)
    failures = page.locator('#result').text_content()
    browser.close()
    assert failures == '[]', failures
print('PASS: Chromium cascade checks across 3 DB accents, nested popups, priorities, legacy labels and light mode')
