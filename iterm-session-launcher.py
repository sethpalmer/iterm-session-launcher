#!/usr/bin/env python3

import iterm2
import sys

SESSIONS = {
    'session-1': {
        'path': '~/',
        'panes': [
            ['echo Hello', 'echo World'],
            ['echo Hello World!']
        ],
        'console': True
    }
}

async def main(connection):
    app = await iterm2.async_get_app(connection)
    window = app.current_terminal_window

    if window is not None:
        tab = await window.async_create_tab()
        service = SESSIONS[sys.argv[1]]
        await tab.async_set_title(service['path'])

        for i in range(len(service['panes']) - 1):
            split = await tab.current_session.async_split_pane(vertical=True)

        if service['console']:
            split = await tab.current_session.async_split_pane(vertical=False)

        for i in range(len(tab.sessions)):
            if service['path']:
                await tab.sessions[i].async_send_text(f"cd {service['path']}\n")
            if i < len(tab.sessions) - 1:
                for line in service['panes'][i]:
                   await tab.sessions[i].async_send_text(line + "\n")

if len(sys.argv) == 2 and sys.argv[1] in SESSIONS.keys():
    iterm2.run_until_complete(main, True)
else:
    print("Invalid arguments! Options:")
    for session in SESSIONS.keys():
        print("    " + session)
