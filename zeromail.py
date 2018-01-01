import sqlite3, cryptlib, os

current_directory = os.path.dirname(os.path.realpath(__file__))

pubkey = None
privkey = None

conn = None
c = None
def connect(zeronet_directory, pub, priv):
    global pubkey, privkey
    pubkey = pub
    privkey = priv

    global conn, c
    conn = sqlite3.connect(zeronet_directory + 'data/1MaiL5gfBM1cyb4a8e3iiL8L5gXmoAJu27/data/users/zeromail.db')
    c = conn.cursor()

def get_secrets(from_date_added=0):
    secrets = []
    for row in c.execute('SELECT encrypted, json_id, date_added FROM secret WHERE date_added > %s ORDER BY date_added DESC' % from_date_added):
        aes_key, json_id, date_added = cryptlib.eciesDecrypt(row[0], privkey), row[1], row[2]
        if aes_key != None:
            secrets.append([aes_key, json_id])
        from_date_added = max(from_date_added, date_added)
    return (secrets, from_date_added)
def update_secrets():
    import json

    old_secrets = []
    from_date_added = 0
    try:
        with open(current_directory + "/secrets.cache.json", "r") as f:
            cache = json.loads(f.read())
            old_secrets = cache["secrets"]
            from_date_added = cache["date_added"]
    except:
        pass

    new_secrets, date_added = get_secrets(from_date_added)
    secrets = old_secrets + new_secrets

    with open(current_directory + "/secrets.cache.json", "w") as f:
        cache = dict(secrets=secrets, date_added=date_added)
        f.write(json.dumps(cache))

    return secrets

def get_messages(secrets, from_date_added=0):
    date_added = 0

    res = []
    for s in secrets:
        aes_key, json_id = s[0], s[1]
        messages = c.execute('SELECT encrypted, date_added FROM message WHERE json_id = ? AND date_added > %s ORDER BY date_added DESC' % from_date_added, (json_id,))
        for m in messages:
            message = m[0].split(',')
            iv, encrypted_text = message[0], message[1]
            result = cryptlib.aesDecrypt(iv, encrypted_text, aes_key)
            if result != None:
                res.append(result)
            date_added = max(date_added, m[1])

    return (res, date_added)
def update_messages(secrets):
    import json

    old_messages = []
    from_date_added = 0
    try:
        with open(current_directory + "/messages.cache.json", "r") as f:
            cache = json.loads(f.read())
            old_messages = cache["messages"]
            from_date_added = cache["date_added"]
    except:
        pass

    new_messages, date_added = get_messages(secrets, from_date_added)
    messages = old_messages + new_messages

    with open(current_directory + "/messages.cache.json", "w") as f:
        cache = dict(messages=messages, date_added=date_added)
        f.write(json.dumps(cache))

    return messages