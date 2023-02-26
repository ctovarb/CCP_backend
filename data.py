import random
import string

user_ids = list(range(1, 101))
recipient_ids = list(range(1, 101))


def generate_message() -> dict:
    random_user_id = random.choice(user_ids)

    # Copia de arreglo de receptores
    recipient_ids_copy = recipient_ids.copy()

    # No se puede enviar mensaje a si mismo
    recipient_ids_copy.remove(random_user_id)
    random_recipient_id = random.choice(recipient_ids_copy)

    # Generar un mensaje
    message = ''.join(random.choice(string.ascii_letters) for i in range(32))

    return {
        'user_id': random_user_id,
        'recipient_id': random_recipient_id,
        'message': message
    }
