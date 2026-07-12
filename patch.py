import re

p = 'index.html'
s = open(p, encoding='utf-8').read()

# 1) inject data script tags after the MediaPipe hands script
marker = '  <script src="https://cdn.jsdelivr.net/npm/@mediapipe/hands/hands.js" crossorigin="anonymous"></script>\n'
assert marker in s, "hands.js marker not found"
inject = (marker +
          '\n'
          '  <!-- Full CET-4 / CET-6 vocabulary (generated from sufwis/english-vocabulary) -->\n'
          '  <script src="assets/cet4.js"></script>\n'
          '  <script src="assets/cet6.js"></script>\n')
s = s.replace(marker, inject, 1)

# 2) replace the two inline sample arrays with the full data vars
s2 = re.sub(r'cet4: \[.*?\],', 'cet4: CET4_DATA,', s, flags=re.S)
assert s2 != s, "cet4 replace failed"
s3 = re.sub(r'cet6: \[.*?\n    \};', 'cet6: CET6_DATA\n    };', s2, flags=re.S)
assert s3 != s2, "cet6 replace failed"
s = s3

# 3) gracefully handle empty phonetic / example fields
old = '''      uiEn.textContent = currentWord.en;
      uiPh.textContent = currentWord.ph;
      uiZh.textContent = currentWord.zh;
      uiEx.textContent = currentWord.ex;'''
new = '''      uiEn.textContent = currentWord.en;
      uiPh.textContent = currentWord.ph || '';
      uiPh.style.display = currentWord.ph ? 'block' : 'none';
      uiZh.textContent = currentWord.zh;
      uiEx.textContent = currentWord.ex || '（暂无例句）';'''
assert old in s, "updateCardData block not found"
s = s.replace(old, new)

open(p, 'w', encoding='utf-8').write(s)
print("patched OK")
