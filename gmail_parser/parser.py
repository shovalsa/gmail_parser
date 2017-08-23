from email.header import decode_header

def decode(s):
    """
    For some reason I can't get the decoding to work while retrieving from gmail. This should work on the output from
    SQL, e.g.
    subject_in_hebrew = trialDB.retrieveFromDB()[2]['subject']
    decode(heb)
    :param s: string encoded in utf-8
    :return: string decoded in utf-8
    """
    try:
        header = decode_header(s)
        decoded = header[0][0].decode('utf-8')
    except AttributeError:
        decoded = s
    return decoded

