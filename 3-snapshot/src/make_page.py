text = '<!doctype html><meta charset=utf8>'
num = 0
import os
while os.path.isfile('shot-{}.png'.format(num)):
    text += '<img src="shot-{}.png"/>'.format(num)
    num += 1
text += '''
<script>
[].forEach.call(document.querySelectorAll('img'), img => {
img.onclick = () => document.body.removeChild(img)
})
</script>
'''
open('./view.html', 'w').write(text)
