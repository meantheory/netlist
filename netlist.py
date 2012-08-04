
import sys
import requests

def arin_search(url, qtype, q):
    data = []
    r = requests.get(url.format(q), headers = {'Accept': 'application/json'})

    if r.status_code == requests.codes.ok:
        results = r.json[qtype + u's'][qtype + u'Ref']
        if type(results) == type(dict()):
            data.append(results)
        else:
            data += results
    elif r.status_code == requests.codes.not_found: 
        pass
    else: 
        raise Exception('Unknown error occurred while performing search.')
    return data

def run(q):
    #todo: sanitize q input
    org_search = 'http://whois.arin.net/rest/orgs;name={0}*'
    net_search = 'http://whois.arin.net/rest/org/{0}/nets'

    orgs = arin_search(org_search, 'org', q)
    for org in orgs:
        print(u'Name: {@name} Handle: {@handle}'.format(**org))
        t = ' ' * 4
        nets = arin_search(net_search, 'net', org[u'@handle'])
        for net in nets:
            print(t + u'{@name} ({@handle}): {@startAddress} - {@endAddress}'.format(**net))

        if len(nets) == 0:
            print(t + 'No networks related to organization')

    if len(orgs) == 0:
        print('No organizations found in search.')

if __name__ == '__main__':
    if len(sys.argv) == 2:
        run(sys.argv[1])
    else:
        print 'Error: Unexpected number of arguments or no arguments'