from _thread import interrupt_main
# noinspection PyProtectedMember
from os import _exit as osexit
from threading import Thread

from controllers import datactl
from controllers.messagectl import MessageController
from controllers.socketctl import SocketController
from interface import printing
from interface.header import print_header
from interface.logger import log
from strat import summarize


def main():
    global data_controller
    log('server.main', '+' * 20)
    log('server.main', 'Server started')

    print_header()

    datactl.makefile()
    data_controller = datactl.DataController()
    msgctl = MessageController(data_controller)

    printing.printf('Waiting for connections', style=printing.STATUS, log=True, logtag='server.main')

    Thread(target=handleinput).start()

    socketctl = SocketController(msgctl.handle_msg)
    socketctl.start_connecting()

    while True:
        try:
            data_controller.update()
        except KeyboardInterrupt:
            # Make sure everything made it into the data file
            data_controller.update()

            socketctl.close()

            log('server.main', 'Server stopped')
            log('server.main', '-' * 20)

            # Quit everything (closes all the many threads)
            osexit(1)


def handleinput():
    global data_controller
    i = input()
    ii = i.split()
    if i in ('q', 'quit'):
        printing.printf('Are you sure you want to quit? (y/n)', style=printing.QUIT, end=' ')
        q = input()
        if q == 'y':
            interrupt_main()

    elif i in ('d', 'data', 'drive', 'flash drive', 'u', 'update', 'dump', 'data dump'):
        data_controller.driveupdaterequest()

    elif i in ('s', 'strat', 'match strat', 'strategy', 'match strategy'):
        # noinspection PyUnusedLocal
        teams = [input("Our alliance: ") for i in range(3)] + [input("Other alliance: ") for i in range(3)]
        printing.printf(summarize.strategy(teams), style=printing.DATA_OUTPUT)

    elif i in ('missing', 'm', 'count', 'msng'):
        datactl.findmissing()

    elif len(ii):
        if ii[0] in ('sum', 'summary', 'detail', 'info', 'detailed', 'full', 'ds', 'dcomp', 'dc'):
            [printing.printf(q) for q in summarize.detailed_summary(ii[1:])]

        elif ii[0] in ('qsum', 'quick', 'brief', 'qsummary', 'qinfo', 'qk', 'qs', 'comp', 'c'):
            [printing.printf(q) for q in summarize.quick_summary(ii[1:])]

        # elif ii[0] == 'send':
        #     socketctl.blanket_send(ii[1])

    Thread(target=handleinput).start()


if __name__ == '__main__':
    main()
