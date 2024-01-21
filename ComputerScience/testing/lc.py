def minWindow(s, t):
    if len(t) > len(s): return ""
    if len(t) == 0: return ""

    if s == t: return s
    tmap = {}
    smap = {}

    for i in range(len(t)):
        tmap[t[i]] = tmap.get(t[i], 0) + 1
        smap[s[i]] = smap.get(s[i], 0) + 1
    
    if tmap == smap:
        return s
    
    for right in range(len(t), len(s)):
        windowsize = len(t)
        left = s[right - windowsize]

        if tmap == smap: return s[left:right]

        smap[s[right]] = smap.get(s[right], 0) + 1

        



