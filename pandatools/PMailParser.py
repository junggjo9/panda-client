import re

fromStrs = ['From: panda@bnl.gov','From: <atlpan@cern.ch>',
            'From: Atlas.Pangaea@cern.ch','From: Atlas Pangaea']

# get argiments of panda header
def getHeaderArgs():
    args = []
    if len(fromStrs) > 1:
        # use OR
        args.append('OR')
    for strVal in fromStrs:
        # extract name and value
        strVal = re.sub('\s*:\s*',' ',strVal)
        strVal = re.sub('<|>','',strVal)
        items = strVal.split()
        # ignore non email address
        if items[0] == 'From' and not '@' in items[-1]:
            continue
        # append
        args.append(items[0])
        args.append(items[-1])        
    return args


# check mail header
def checkHeader(res):
    # check From
    for line in res[1]:
        for strVal in fromStrs:
            if line.startswith(strVal):
                return True
    # non panda mail
    return False


# parse Notification to extract parameters
def parseNotification(res,type):
    attrMap = {}
    # check contents
    if type == 'pop3':
        lines = res[1]
        mailBody = 1
    else:
        lines = res.split('\r\n')
        mailBody = 0        
    for line in lines:
        # look for \n to find message body
        if mailBody > 0 and line == '':
            mailBody -= 1
            continue
        # skip header
        if mailBody > 0:
            continue
        # parser body
        match = re.search('[a-zA-Z]+\s+:\s+.+$',line)
        if match != None:
            # extract attr and val
            items = match.group(0).split(' : ')
            attr = items[0].strip()
            val  = items[-1].strip()
            # convert to int
            if re.search('^\d+$',val):
                val = int(val)
            # make list for In/Out
            if attr in ['In','Out']:
                if not attrMap.has_key(attr):
                    attrMap[attr] = []
                attrMap[attr].append(val)
            else:
                attrMap[attr] = val
    # return        
    return attrMap

