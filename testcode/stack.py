__author__ = 'leo'

stack = []


def pushIt():
    stack.append(raw_input(' Enter New string: ').strip())


def popIt():
    if len(stack) == 0:
        print 'Cannot pop from an empty stack!'
    else:
        print 'Remove [', stack.pop(), ']'


def viewStack():
    print stack


CMDS = {'u': pushIt, 'o': popIt, 'v': viewStack}


def showMenu():
    pr = """
    p(U)sh
    p(O)p
    (V)iew
    (Q)uit

    Enter choice: """
    while True:
        while True:
            try:
                choice = raw_input(pr).strip()[0].lower()
            except (EOFError, KeyboardInterrupt, IndexError):
                choice = 'q'

            print '\nYou picked: [%s]' % choice
            if choice not in 'uovq':
                print 'Invalid option ,try again'
            else:
                break
        if choice == 'q':
            break
        CMDS[choice]()

if __name__ == '__main__':
    showMenu()
