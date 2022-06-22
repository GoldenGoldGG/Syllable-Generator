from random import Random
from secrets import choice

# ---------------------------------------------------------------
#            ~~ Syllable Generator for Conlangs ~~
#                       by Golden Gold
#
# If you get an IndexError, it's because your rules are stupid
# (for example, nasals can't come after nasals, but you allowed
# every consonant to come before nasals (CN), which includes
# nasals.
#
# 
# • Consonant groups can be created in the 'groups.txt' file.
#   - GroupName: letters divided with ',' (spaces do not matter).
#   - Divide groups with new line.
# • Rules can be created in the 'rules.txt' file:
#   - "A~B": group 'B' must appear after group 'A'.
#   - "A!B": group 'B' cannot appear after group 'A'.
#   - Divide rules with new line.
# 
# Options:
# • Syllable structure: 
#   - '*' before group name means it is mandatory.
#   - Divide groups with ',' (spaces do not matter).
# • 'syllables': amount of syllables to create.
# • 'display': how to display the syllables in the console:
#   - '{index}': the syllable's index.
#   - '{syllable}':  the syllable itself.
#   - '\n': new line.
# ---------------------------------------------------------------

def options(option):
    opt = open(r'options.txt', mode='r', encoding='utf-8').read()
    return opt[int(opt.find(f'{option}: ') + len(f'{option}: ')):int(opt.find('\n', opt.find(f'{option}: ')))]



words = int(options('syllables'))

structure = options('structure').replace(" ", "").split(',')

groups = {}

groupsfile = open(r'groups.txt', mode='r', encoding='utf-8')
grp = groupsfile.readlines()
for g in grp:
    g = g.replace(" ", "").replace("\n", "")
    groups[g[:g.find(':')]] = []
    for l in g[g.find(':')+1:].split(','):
        groups[g[:g.find(':')]].append(l)
groupsfile.close()

rules = []

rulesfile = open(r'rules.txt', mode='r', encoding='utf-8')
rls = rulesfile.readlines()
for r in rls:
    r = r.replace(' ', '').replace('\n', '')
    rules.append(r)
rulesfile.close()

random = Random()

for i in range(words):
    output = ''
    forbbiden = [] # forbidden letters
    next = '' # next letter has to be this

    for s in structure: # s: group allowed in this spot
        if next != '':
            output += next
        
        allowed = [l for l in groups[s.replace('*', '')] if l not in forbbiden] # remove forbidden from allowed
        tmp = allowed if s[0] == '*' else allowed.append('') # first letter is '*'
        output += random.choice(tmp if tmp is not None or len(allowed) <= 0 else ['']) # add '' to choices if optional

        forbbiden = []
        next = ''

        # -- rules -- #
        for r in rules:
            y = r.find('~')
            n = r.find('!')
            if n != -1: # a cannot come after b
                if len(output) > 0 and output[-1] in groups[r[:n]]: # if last choice is part of 'a' group
                    forbbiden.extend(groups[r[n+1:]]) # make 'b' group forbidden
            elif y != -1: # a must come after b
                if output[-1] in groups[r[:y]]: # if last choice is part of 'a' group
                    next = random.choice(groups[r[y+1:]]) # set next letter as group 'b'

    print(options('display').replace("'", '').replace('{index}', f'{i+1}').replace('{syllable}', f'{output}').replace('\\n', '\n'), end='')

print('Program has ended.')
