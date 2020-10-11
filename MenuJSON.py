import curses, os, json
myMenu = screen = highlighted = nHighlighted = None

def getJSONFromFile(path):
    if os.path.exists(path) == False:
        file = open(path, 'w')
        file.write('{\n\t"title": "Demo",\n\t"type": "MENU",\n\t"subtitle": "Select an option",\n\t"options": [\n\t\t{ "title": "Execute a demo command", "type": "COMMAND", "command": "echo \'Hello World\'", "wait": true }\n\t]\n}')
        file.close()
    with open(path, encoding = 'utf-8-sig') as json_file:
        json_data = json.load(json_file)
        return json_data

def displayMessage(errorType):
    screen.clear()
    screen.border(0)
    screen.addstr(2, 2, errorType['title'], curses.A_STANDOUT)
    screen.addstr(4, 2, errorType['description'], curses.A_BOLD)
    screen.addstr(5, 2, 'Press Enter to continue...', curses.A_BOLD)
    screen.refresh()
    screen.getch()
    screen.clear()

def initializeMenu():
    global screen, highlighted, nHighlighted
    screen = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.start_color()
    screen.keypad(1)

    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    highlighted = curses.color_pair(1)
    nHighlighted = curses.A_NORMAL
    curses.curs_set(0)

def listOptionsInMenu(menu, parent):
    if parent is None:
        lastOption = "Exit"
    else:
        lastOption = "Return to %s" % parent['title']
    options = len(menu['options'])

    index = 0
    indexOld = loopIndex = None
    while loopIndex != ord('\n'):
        if index != indexOld:
            indexOld = index
            screen.border(0)
            screen.addstr(2, 2, menu['title'], curses.A_STANDOUT)
            screen.addstr(4, 2, menu['subtitle'], curses.A_BOLD)

            for i in range(options):
                textStyle = nHighlighted
                if index == i:
                    textStyle = highlighted
                screen.addstr(6 + i, 4, "%d - %s" % (i + 1, menu['options'][i]['title']), textStyle)
            
            textStyle = nHighlighted
            if index == options:
                textStyle = highlighted
            screen.addstr(6 + options, 4, "%d - %s" % (options + 1, lastOption), textStyle)
            screen.refresh()

        loopIndex = screen.getch()

        if loopIndex == 258:
            if index < options:
                index += 1
            else:
                index = 0
        elif loopIndex == 259:
            if index > 0:
                index -= 1
            else:
                index = options
    return index

def renderMenu(menu, parent = None):
    global myMenu
    options = len(menu['options'])
    exitMenu = False
    if parent == None:
        menu = myMenu
    while not exitMenu:
        currentPosition = listOptionsInMenu(menu, parent)
        if currentPosition == options:
            exitMenu = True
        elif menu['options'][currentPosition]['type'].upper() == "MENU":
            screen.clear()
            menu = myMenu
            renderMenu(menu['options'][currentPosition], menu)
            screen.clear()
        elif menu['options'][currentPosition]['type'].upper() == "COMMAND":
            screen.clear()
            curses.def_prog_mode()
            os.system('reset')
            os.system(menu['options'][currentPosition]['command'])
            if menu['options'][currentPosition]['wait'] == True:
                print('The job is finished, press Enter to continue...')
                input()
            screen.clear()
            curses.reset_prog_mode()
            curses.curs_set(1)
            curses.curs_set(0)

def main():
    global myMenu
    initializeMenu()
    myMenu = getJSONFromFile('config.json')
    renderMenu(myMenu)
    curses.endwin()
    os.system('clear')

main()