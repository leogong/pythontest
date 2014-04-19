__author__ = 'leo'

db = {}


def newUser():
    prompt = 'login desired :'
    while True:
        name = raw_input(prompt)
        if db.has_key(name):
            prompt = 'name taken ,try another:'
            continue
        else:
            break
    pwd = raw_input('password:')
    db[name] = pwd


def oldUser():
    name = raw_input('login:')
    pwd = raw_input('passWd:')
    password = db.get(name)
    if password == pwd:
        print 'welcome back', name
    else:
        print 'login incorrect'


def showMenu():
    prompt = """
        (N)ew User Login
        (E)xisting User Login
        (Q)uit
        Enter choice:
        """
    done = False
    while not done:
        chosen = False
        while not chosen:
            try:
                choice = raw_input(prompt).strip()[0].lower()
            except (EOFError, KeyboardInterrupt):
                choice = 'q'
            print '\nYou pricked : [%s]' % choice
            if choice not in 'neq':
                print 'invalid option,try again!'
            else:
                chosen = True
        if choice == 'q': done = True
        if choice == 'n': newUser()
        if choice == 'e': oldUser()


if __name__ == '__main__':
    showMenu()
