__author__ = 'leo'

file_io = open("file/order", 'r')
order = file_io.readlines()
file_io.close()
orderResult = {}
orderLen = len(order)
print orderLen
for x in range(0, orderLen):
    rows = order[x].split("\t")
    # order_num = rows[0]
    ip = rows[1]
    seq = rows[2]
    # dateFormat = time.strptime(rows[3], "%Y-%m-%d %H:%M:%S")
    # order_date = datetime.datetime(dateFormat[0], dateFormat[1], dateFormat[2], dateFormat[3], dateFormat[4],
    #                                dateFormat[5])
    # order_status = rows[4]
    for j in range(x + 1, orderLen):
        l2 = order[j]
        if ip in l2 and seq in l2:
            if ip in orderResult:
                orderResult[ip].append(l2)
            else:
                lineList = [l2]
                orderResult[ip] = lineList

                # rows2 = l.split("\t")
                # order_num2 = rows2[0]
                # order_status2 = rows2[4]
                # if order_status2 != 3 and order_status != 4:
                #     # if
                #     continue
                # dateFormat2 = time.strptime(rows2[3], "%Y-%m-%d %H:%M:%S")
                # order_date2 = datetime.datetime(dateFormat2[0], dateFormat2[1], dateFormat2[2], dateFormat2[3],
                #                                 dateFormat2[4],
                #                                 dateFormat2[5])
                # order_status = rows[4]
                # cha = 0
                # if order_date2 > order_date:
                #     cha = (order_date2 - order_date).days
                #
                # else:
                #     cha = (order_date - order_date2).days
                #
                # if cha < 3:

print orderResult





