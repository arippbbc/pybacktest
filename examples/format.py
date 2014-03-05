def fixmicro(s):
    return s[:s.rfind(':')+1]+'%06d' % (int(s[s.rfind(':')+1 : s.find(',')])%1000000)+s[s.find(','):]

f = open('aud.csv', 'r')
out = open('aud-fixed.csv', 'w')
once = False
for line in f.readlines():
    if not once:
        out.writelines(line)
        once = True
    else:
        out.writelines(fixmicro(line))
f.close()
out.close()
