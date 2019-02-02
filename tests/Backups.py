def record_mult(basefunc, branchfunc, evaluator, colorconstr, plist, clist, npoints, singleton):
    completefunc = basefunc+'('
    for i in range(0, npoints-1):
        base = branchfunc+'('
        evalbase = evaluator+'('
        point = plist[0]
        cx,cy = coord_to_percent(point[0],point[1])
        funcvars = str(cx)+', '+str(cy)+', '+colorconstr+'('+clist[0]+')'
        evalfunc = evalbase+funcvars+')'
        completefunc+=base+evalfunc+', '
    base = branchfunc + '('
    evalbase = evaluator + '('
    point = plist[npoints-1]
    cx, cy = coord_to_percent(point[0], point[1])
    funcvars = str(cx) + ', ' + str(cy) + ', ' + colorconstr + '(' + clist[0] + ')'
    evalfunc = evalbase + funcvars + '), '+str(singleton)+')'
    completefunc+=base+evalfunc+')'*(npoints-1)+', '+str(singleton)+')'
    #wait_for_one(color_comp(1, 1, c), wait_for_one(color_comp(1, 1, c), color_comp(1, 1, c)))
    return completefunc

def test_mult(func1, func2): #singleton is True
    if(not func1) or (not func2):
        return True
    else:
        return False

def wait_mult(func1, func2):
    #waits for all of the points to load
    while (not func1) or (not func2):
        print('waiting...')
        robot_sleep(250)
    print('finished!')
    return True

def test_one(func1, func2): #singleton is False
    if(not func1) and (not func2):
        return True
    else:
        return False

def wait_one(func1, func2):
    # waits for one of the points to load
    while (not func1) and (not func2):
        print('waiting...')
        robot_sleep(250)
    print('finished!')
    return