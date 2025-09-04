from pynput import keyboard

words = ""


def rm_junks():
    global words
    if len(words) >= 400:
        additional = len(words) - 400
        words = words[additional:]
    else:
        pass


def on_press(key):
    global words
    """Callback function executed when a key is pressed."""
    try:
        words += str(key.char)
    except AttributeError:
        words += " {" + str(key).split('.')[1] + '} '
    rm_junks()



def on_release(key):
    if key == keyboard.Key.esc:
        # Stop listener
        return False


def main():
    # Create and start the listener
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
    return words


if __name__ == "__main__":
    words = main()
    print(words)
