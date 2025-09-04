import json
import os


def save_text(text: str, file_name: str) -> None:
    with open(f'Records\\{file_name}.txt', 'w') as text_file:
        text_file.write(text)
        text_file.close()


lines = ['nigga', 'are', 'you', 'okay']
tuple_txt = '\n'.join(lines)

save_text(tuple_txt, 'testing')