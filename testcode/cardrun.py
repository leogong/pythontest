__author__ = 'leo'


def safe_float(obj):
    'safe version of float()'
    try:
        retval = float(obj)
    except (ValueError, TypeError), diag:
        retval = str(diag)
    return retval


def main():
    'handles all the data processing'
    log = open('../file/cardlog.txt', 'a')
    try:
        ccfile = open('../file/carddata.txt', 'r')
    except IOError, e:
        log.write("no txns this month \n")
        log.close()
        return

    txns = ccfile.readlines()
    ccfile.close()
    total = 0.00
    log.write('account log:\n')

    for eachTxn in txns:
        result = safe_float(eachTxn)
        if isinstance(result, float):
            total += result
            log.write('data .... processed %s \n' % result)
        else:
            log.write('ignored:%s' % result)

    print '$%.2f (new balance) ' % (total)

    log.close()


main()
