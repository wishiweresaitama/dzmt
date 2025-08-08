import time


def preformat(msg):
    """allow {{key}} to be used for formatting in text
    that already uses curly braces.  First switch this into
    something else, replace curlies with double curlies, and then
    switch back to regular braces
    """
    msg = msg.replace("{{", "<<<").replace("}}", ">>>")
    msg = msg.replace("{", "{{").replace("}", "}}")
    msg = msg.replace("<<<", "{").replace(">>>", "}")
    return msg


def run_interrupt_listener():
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            print("Execution interrupted, exiting...")
            break
