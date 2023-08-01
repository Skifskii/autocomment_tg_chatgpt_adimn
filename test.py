s = """"193.187.145.2:8000:xncc7J:qscRHp"
"193.187.144.80:8000:xncc7J:qscRHp"
"193.187.147.148:8000:xncc7J:qscRHp"
"81.177.182.134:8000:Hw6RYz:7pnoYh"
"193.187.147.175:8000:xncc7J:qscRHp"
"193.187.147.175:8000:xncc7J:qscRHp"
"193.187.144.80:8000:xncc7J:qscRHp"
"81.177.183.185:8000:Hw6RYz:7pnoYh"
"185.192.109.245:8000:Hw6RYz:7pnoYh"
"193.187.145.2:8000:xncc7J:qscRHp"
"185.192.109.245:8000:Hw6RYz:7pnoYh"
"193.187.145.214:8000:xncc7J:qscRHp"
"193.187.145.214:8000:xncc7J:qscRHp"
"81.177.182.134:8000:Hw6RYz:7pnoYh"
"193.187.147.148:8000:xncc7J:qscRHp"
""".split('\n')

set_s = set(s)
for i in set_s:
    print(i, s.count(i))
