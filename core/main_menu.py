from pynput import keyboard

class MainMenu :
    def __init__(self):
        self.kl = keyboard.GlobalHotKeys({
            '<ctrl>+<right>': self.on_activate_r,
            '<ctrl>+<left>': self.on_activate_l})
        self.kl.start()

    def on_activate_r():
        print('freccia dx')
    def on_activate_l():
        print('freccia lx')


    import os
    rows, columns = os.popen('stty size', 'r').read().split()
    print(f'Rows {rows}')
    print(f'Columns {columns}')
    while True:
        print('Sleeping')
        time.sleep(5)

    ### stop the key parser!!
    self.kl.stop()
    exit()