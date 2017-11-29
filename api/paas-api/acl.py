import config
from log import LOG

def match_resource(pattern, resource):
    try:
        if pattern == '*':
            return True

        (res_type1, res_name1) = pattern.split('.')
        (res_type2, res_name2) = resource.split('.')

        if res_type1 != res_type2:
            return False

        if res_name1 == '*':
            return True
        elif res_name1 == res_name2:
            return True
        else:
            return False
    except:
        return False

def check_acl(account, resource, action):

    if 'ACL' not in dir(config):
        return True

    allow = None
    deny = None
    for rule in config.ACL:
        if not match_resource(rule['resource'], resource):
            continue

        if 'allow' in rule:
            if rule['allow'] == '*' or action in rule['allow']:
                allow = True
                break
        if 'deny' in rule:
            if rule['deny'] == '*' or action in rule['deny']:
                deny = True

    if allow == True:
        return True
    elif deny == True:
        return False
    else:
        return True

