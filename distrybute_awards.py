#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import requests
import re

#os.system('fibos claim_reward.js')

### balance
pattern = re.compile(r'\d+') # 查找数字
bjson = json.loads(os.popen('fibos account.js').read())
balanceOBJ = re.search(r'[\d.]+',bjson['rows'][0]['balance']['quantity'],re.M|re.I)
balance = float(balanceOBJ.group())
print "balance is ", balance

### check voter
r = requests.get("http://explorer.fibos.rocks/api/voter?producer=ukfiboooooos")
hjson = json.loads(r.content)
length = len(hjson)
index = 0

r2 = requests.get("https://explorer.fibos.rocks/api/vote?producer=ukfiboooooos")
vote = float(r2.content)
while index < length:
    voter = hjson[index]['owner']
    stake = float(hjson[index]['staked'])
    weight = round(stake*0.99/vote, 4)
    share = round(balance * weight,2)
    memo = "返还 %s 抵押奖励，感谢您的支持！" % (str(share))
    print voter, stake, weight, memo

    ### transfer
    f_path = r'./transfer_template.js'
    f = open (f_path, "r+")
    content = re.sub(r'{{ voter }}', str(voter), f.read())
    content = re.sub(r'{{ share }}', str(share), content)
    content = re.sub(r'{{ memo }}', memo, content)
    t_path = './transfer_%s.js' % (str(voter))
    cat_t_path = "cat %s"  % (t_path)
    do_transfer = "fibos %s"  % (t_path)
    open(t_path, 'w').write(content)
    os.system(cat_t_path)
    #os.system(do_transfer)
    index = index + 1
