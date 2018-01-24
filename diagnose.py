## ----------------- INSTRUCTIONS -------------------------
## Use following command to execute
##
##  >> python hw2.py
##
## --------------------------------------------------------



import copy
def partition(pat):
    #Returns list of words in a pattern
    
    flag = False
    i, j = 0, 1
    stk = []
    parts = []
    
    if(i < len(pat) and pat[i]=='('):
        stk.append('(')
        flag = True
        i=i+1

    j=i+1
    
    while(i < len(pat)):
        if(flag):
            while(j < len(pat) and not (stk == [])):
                if(pat[j]==')'):
                    stk.pop()
                elif(pat[j]=='('):
                    stk.append('(')

                if(not pat[j]==')' or not (stk == [])):
                    j=j+1
                    
            parts.append(pat[i:j])
            flag = False
                
        else:
            while(j < len(pat) and not (pat[j]==' ' or pat[j]=='(')):
                j=j+1
            parts.append(pat[i:j])
            if(j < len(pat) and pat[j]=='('):
                stk.append('(')
                flag = True

        i = j + 1
        while( i < len(pat) and pat[i]==' '):
            i=i+1
        
        if(i < len(pat) and pat[i]=='('):
            stk.append('(')
            flag = True
            i=i+1
        j = i+1
    return parts

def unify(pat1, pat2, sub):
    #Returns substitutions resulted from matching two patterns
    
    if ('#f', '#f') in sub:
        return sub
    if (pat1 == pat2):
        return sub
    if (isVar(pat1)):
        return unify_var(pat1, pat2, sub)
    if (isVar(pat2)):
        return unify_var(pat2, pat1, sub)
    if (isAtom(pat1) or isAtom(pat2)):
        sub.append(('#f','#f'))
        return sub
    part1 = partition(pat1)
    part2 = partition(pat2)
    if(len(part1)!= len(part2)):
        if ('#f','#f') not in sub:
            sub.append(('#f','#f'))
        return sub

    temp_sub = []
    for i in range(0, len(part1)):
        temp_sub += unify(part1[i], part2[i], sub)
    if ('#f', '#f') not in temp_sub:
        for s in temp_sub:
            if s not in sub:
                sub.append(s)
    return sub
    

def unify_var(var, pat, sub):
    #unify patterns containing variables
    
    sb = {s[0]:s[1] for s in sub}
    if var in sb:
        return unify(sb[var], pat, sub)
    if pat in sb:
        return unify(var, sb[pat], sub)
    if var in pat:
        return [('#f','#f')]
    return [(var, pat)]

def execute(sub, patterns, wm):
    #returns newly found patterns using substituitions. Uses function substitute
    newpatt=[]
    for p in patterns:
        pat = substitute(sub, p)
        if pat not in wm:
            newpatt.append(pat)
    return newpatt

def substitute(sub, pat):
    #Returns pattern with variables replaced by substitutions
    
    sb = {s[0]:s[1] for s in sub}
    hashtab = {c:[] for c in [' ', '(', ')']}
    for i in range(0, len(pat)):
        if pat[i] in hashtab:
            hashtab[pat[i]].append(i)
    
    delimiters = [];
    if ' ' in hashtab:
        
        if '(' in hashtab and ')' in hashtab:
            delimiters += hashtab[' '] + hashtab[')'] + hashtab['(']
        else:
            delimiters += hashtab[' ']
    delimiters = sorted(delimiters)
    delimiters.append(len(pat))

    newpat = ''
    word = pat[0:delimiters[0]]
    if not word=='' and isVar(word) and word in sb:
        newpat += sb[word]
    else:
        newpat += word
    newpat += pat[delimiters[0]]
    
    for i in range(0, len(delimiters)-1):
        word = pat[delimiters[i]+1:delimiters[i+1]]
        if not word=='' and isVar(word) and word in sb:
            newpat += sb[word]
        else:
            newpat += word
        if delimiters[i+1] < len(pat):
            newpat += pat[delimiters[i+1]]
    if(newpat == pat):
        return newpat
    else:
        return substitute(sub, newpat)
    pass

def isVar(s):
    #Returns True if input is a variable
    s1 = s.split()
    s2 = s.split(')')
    s3 = s.split('(')
    if(len(s1)<=1 and len(s2)<=1 and len(s3)<=1 and s[0]=='?'):
        return True
    return False

def isAtom(s):
    #Returns True if input is a single word and not a variable
    
    s1 = s.split()
    s2 = s.split(')')
    s3 = s.split('(')
    if(len(s1)<=1 and len(s2)<=1 and len(s3)<=1 and s[0] not in ['?', ' ', '(', ')']):
        return True
    return False
    

def match_antecedent(anteceds, wm, sub):
    #Returns list of states, each state consisting of antecedents yet to be matched and the substitutions
    
    antec = copy.deepcopy(anteceds)
    states = []
    
    for ant in anteceds:
        for w in wm:
            
            sb = copy.deepcopy(sub)
            sub = unify(ant, w, sub)
                        
            if('#f','#f') not in sub:
                antec.remove(ant)
                                
                states.append((copy.deepcopy(antec),copy.deepcopy(sub)))
                antec.insert(0, ant)
                for s in sub:
                    if s not in sb:
                        sub.remove(s)
            else:
                while ('#f','#f') in sub:
                    sub.remove(('#f','#f'))
            
    return states
    pass

def match_rule(name, lhs, rhs, wm):
    #Matches input rule with working memory. Returns newly found patterns
    
    print('Attempting to match rule ',name,' ...')
    queue = match_antecedent(lhs, wm, [])
    new_wm = []
    while(len(queue)>0):
        #remove 1st state
        s = queue.pop(0)

        #if s is a goal state
        if(len(s[0])==0):
            new_wm += execute(s[1], rhs, wm)
        else:
            queue+=match_antecedent(s[0], wm, s[1])
    if(len(new_wm)>0):
        print("Match succeeds")
        print("Adding assertion to WM:")
        for item in new_wm:
            print('    "',item,'"')
        print(' ')
    else:
        print('Failing...')
        print(' ')
    return new_wm
    pass

def match_rules(rules, wm):
    #Matches rules in non-question mode
    
    newpatterns = []
    for r in rules:
        newpat = match_rule(r[0], r[1], r[2], wm)
        newpatterns = newpatterns + newpat
    return newpatterns


def q_match_rules(rules, wm, questions_asked):
    #Used to match rules in question mode
    #Makes use of function match_rule and match_antecedent
    
    is_question_asked = False
    for r in rules:
        if(len(r[1])>1):
            queue = match_antecedent(r[1], wm, [])
            while(len(queue)>0):
                state = queue.pop(0)
                if(len(state[0])==0 or len(state[0])==len(r[1]) or len(state[1]) == 0):
                    continue
                antec_not_found = state[0]
                sub = state[1]
                sub_hash = {s[0]:s[1] for s in sub}
                
                for ant in antec_not_found:
                    parts = partition(ant)
                    varlist = []
                    for p in parts:
                        if isVar(p):
                            varlist.append(p)
                    is_all_var_bound = True
                    for var in varlist:
                        if var not in sub_hash:
                            is_all_var_bound = False
                            break

                    if(len(varlist)>0 and is_all_var_bound):
                        assertion = substitute(sub, ant)
                        if assertion not in wm and assertion not in questions_asked:
                            is_question_asked = True
                            questions_asked.append(assertion)
                            quest = input("Assetion '" + assertion + "' is not in WM. Do you want to add it? (Yes/No/Quit) ")
                            while quest not in ['Yes', 'No', 'Quit']:
                                print("Wrong Input")
                                quest = input("Assertion " + assertion + " is not in the working memory. Do you want to add it? (Yes/No/Quit) ")
                            
                            if quest == "Yes":
                                wm.append(assertion)
                                new_patterns = match_rules(rules, wm)
                                flag = add_patterns(new_patterns, wm)
                                while(flag):       
                                    new_patterns = match_rules(rules, wm)
                                    flag = add_patterns(new_patterns, wm)
                            elif quest == "Quit":
                                return False
                
    return is_question_asked

                            

def add_patterns(patterns, wm):
    #Appends new pattern to a working memory
    flag = False
    for p in patterns:
        if p not in wm:
            wm.append(p)
            flag = True
    return flag
    pass


def run_ps(rules, wm, q_mode):

    print('CYCLE 1')
    print(' ')
    print("CURRENT WM: ")
    print(' ')
    for w in wm:
        print('    "',w,'"')
    print(' ')
    
    new_patterns = match_rules(rules, wm)
    flag = add_patterns(new_patterns, wm)

    print(' ')
    print("FINAL WM: ")
    for w in wm:
        print('    "',w,'"')
    print(' ')
    
    count = 2
    while(flag):
        print('CYCLE ', count)
        print(' ')
        print("CURRENT WM: ")
        print(' ')
        
        for w in wm:
            print('    "',w,'"')
        print(' ')
        
        new_patterns = match_rules(rules, wm)
        flag = add_patterns(new_patterns, wm)
        
        print(' ')
        print("FINAL WM: ")
        
        for w in wm:
            print('    "',w,'"')
            
        print(' ')
        count+=1

    if(q_mode):
        questions_asked = []
        flag = q_match_rules(rules, wm, questions_asked)
        while(flag):
            flag = q_match_rules(rules, wm, questions_asked)

    print(' ')
    print("FINAL WM: ")
        
    for w in wm:
        print('    "',w,'"')
            
    print(' ')
    
    return wm


rules = [\
    ('v-high-fever-implies-high-fever', ['has-symptom fever ?patient very-high'], ['has-symptom fever ?patient high']),\
    ('whooping-cough-causes-cough', ['has-disease ?patient whooping-cough'], ['has-symptom cough ?patient positive']),\
    ('touching-poison-ivy-causes-rash', ['has-disease ?patient poison-ivy'], ['has-symptom rash ?patient positive']),\
    ('high-fever-congestion-flue', ['has-symptom fever ?patient high', 'has-symptom congestion ?patient positive'], ['has-disease ?patient flue']),\
    ('rash-no-h-fever-poison-ivy', ['has-symptom rash ?patient positive', 'not has-symptom fever ?patient high'], ['has-disease ?patient poison-ivy']),\
    ('cough-v-high-fever-whooping-cough', ['has-symptom cough ?patient positive', 'has-symptom fever ?patient very-high'], ['has-disease ?patient whooping-cough']),\
    ('no-fever-cough-rash-healthy', ['has-symptom fever ?patient no', 'has-symptom cough ?patient no', 'has-symptom rash ?patient no'], ['is-healthy ?patient yes']),\
    ('spread-of-disease', ['has-disease ?patient ?disease', 'is-contagious ?disease yes', 'contacts ?patient ?patient2'], ['has-disease ?patient2 ?disease']),\
    ('doctor-says-true-disease', ['is-doctor ?person positive','says ?person ?patient has-disease ?disease'], ['has-disease ?patient ?disease']),\
    ('doctor-says-true-healthy', ['is-doctor ?person positive','says ?person ?patient healthy'], ['is-healthy ?patient yes'])]

wm = ['has-symptom fever Ed very-high', 'has-symptom cough Ed positive','not has-touched Alice poison-ivy','says Max Alice has-disease poison-ivy','says Grace Don healthy',\
      'is-doctor Grace positive', 'is-contagious whooping-cough yes','contacts Ed Alice']

q_mode = input("Run the program in question mode? (Yes/No) ")
while q_mode not in ['Yes', 'No']:
    print("Wrong Input")
    q_mode = input("Run the program in question mode? (Yes/No) ")
    
if q_mode == 'Yes':
    q_mode = True

if q_mode == 'No':
    q_mode = False
new_wm = run_ps(rules, wm, q_mode)
