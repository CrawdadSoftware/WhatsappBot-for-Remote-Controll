import time
from twilio.rest import Client
from datetime import datetime, timedelta, timezone
import pygame

accound_sid = 'account_sid'
auth_token = 'auth_token'

client = Client(accound_sid, auth_token)

pygame.init()

processed_messages = set()

messages_to_sounds = {
    "cheese" : "cheese.mp3",
    # Dodaj więcej par wiadomość-plik dźwiękowy tutaj
}

def get_last_check_time():
    try:
        with open('last_check.txt', 'r') as file:
            return datetime.fromisoformat(file.read().strip())
    except (FileNotFoundError, ValueError):
        # Zwraca czas 24 godziny wcześniej, używając obiektów świadomych strefy czasowej
        return datetime.now(timezone.utc) - timedelta(days=1)

def set_last_check_time():
    with open('last_check.txt', 'w') as file:
        # Zapisuje bieżący czas w UTC, używając obiektów świadomych strefy czasowej
        file.write(datetime.now(timezone.utc).isoformat())

def check_messages(last_check_time):
    # Pobierz wiadomości od ostatniego sprawdzenia
    messages = client.messages.list(date_sent_after=last_check_time)
    for message in messages:
        msg_body = message.body.lower().strip()
        if message.direction == "inbound" and msg_body in messages_to_sounds:
            mp3_file = messages_to_sounds[msg_body]
            print(f"Odtwarzam '{mp3_file}'")
            try:
                pygame.mixer.music.load(mp3_file)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
            except Exception as e:
                print(f'Wystąpił błąd przy odtwarzaniu pliku: {e}')
            break

if __name__ == "__main__":
    last_check_time = get_last_check_time()
    check_messages(last_check_time)
    set_last_check_time()