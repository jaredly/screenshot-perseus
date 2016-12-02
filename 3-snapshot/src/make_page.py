text = '<!doctype html><meta charset=utf8>'
num = 0
import os
while os.path.isfile('shot-{}.png'.format(num)):
    text += '<img src="shot-{}.png"/>'.format(num)
    num += 1
text += '''
<style>
body {
    display: flex;
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    flex-wrap: wrap;
    align-items: center;
    flex-direction: column;
}
img {
    border: 1px solid #555;
    border-top: 0;
}
</style>
<script>
[].forEach.call(document.querySelectorAll('img'), img => {
img.onclick = () => document.body.removeChild(img)
})
</script>
'''
open('./view.html', 'w').write(text)
