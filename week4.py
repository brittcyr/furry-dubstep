import urllib2
import sys
from time import sleep

def strxor(s1, s2):
    return "".join([ chr(ord(c2) ^ ord(c1)) for (c1, c2) in zip(s1, s2)])

def strrep(s, sub, pos):
    endpos = pos + len(sub)
    return s[:pos] + sub + s[endpos:]

TARGET = 'http://crypto-class.appspot.com/po?er='
#--------------------------------------------------------------
# padding oracle
#--------------------------------------------------------------
class PaddingOracle(object):
    def query(self, q):
        target = TARGET + urllib2.quote(q)    # Create query URL
        req = urllib2.Request(target)         # Send HTTP request to server
        try:
            f = urllib2.urlopen(req)          # Wait for response
        except urllib2.HTTPError, e:
            return e.code
        return 200

start_query='f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c001bd4a61044426fb515dad3f21f18aa577c0bdf302936266926ff37dbf7035d5eeb4'.decode('hex')

def try_byte(query, byte_at, pad):
    po = PaddingOracle()
    g200 = None

    def try_guess(g):
        sleep(0.1)
        g200 = 0
        last = query[byte_at]
        last = chr(ord(last) ^ pad ^ g)
        q = strrep(query, last, byte_at)
        http_status = po.query(q.encode('hex'))
        if http_status == 404:
            print "Good padding found: 0x%02x" % g
            return g
        if http_status == 200:
            g200 = g
        # if http_status not in (200, 403):
        print "  0x%02x failed (%d)..." % (g, http_status)
        return g200
    if try_guess(0x09): return 0x09
    if try_guess(0x20): return 0x20

    for i in xrange(0x7f, 0x00, -1):
        if try_guess(i): return i

    for i in xrange(0x80, 0xFF):
        if try_guess(i): return i

    if g200: print "Assuming: 0x%02x" % g200
    else: print 'Failed to guess query[%d]' % byte_at
    return g200

def oracle_byte_s(query, guess, start, end):
    for i in xrange(end - 1 - len(guess), start - 1, -1):
        print 'Guessing query[%d]' % i
        padlen = end - i
        subst = strxor(strxor(query[i+1:end], guess), chr(padlen) * padlen)
        q = strrep(query, subst, i+1)
        g = try_byte(q, i, padlen)
        if g is None:
            print '  Failed.'
            return None
        guess = chr(g) + guess
    return guess

def oracle_bytes(query, start, end):
    return oracle_byte_s(query, '', start, end)

if __name__ == "__main__":
    s3 = oracle_bytes(start_query, 32, 48)
    s2 = oracle_bytes(start_query[:48], 16, 32)
    s1 = oracle_bytes(start_query[:32], 0, 16)
    print s1 + s2 + s3
