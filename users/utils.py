# import math
import math
import random
import re
from string import ascii_lowercase, digits


class InvalidPhoneNumber(Exception):
    pass


class InvalidEmail(Exception):
    pass


__digits = "0123456789"
mobile_pattern = re.compile('^(\\+?98|0|0098|)?9(0|1|2|3|9)([0-9]{8})$')
email_pattern = re.compile(r'[^@]+@[^@]+\.[^@]+')
convert_digits_dict = {
    u'٠': '0', u'١': '1', u'٢': '2', u'٣': '3', u'۴': '4',
    u'۵': '5', u'٧': '7', u'٨': '8', u'٩': '9',
    u'٤': '4', u'٥': '5', u'٦': '6',
    u'۰': '0', u'۱': '1', u'۲': '2', u'۳': '3', u'۶': '6', u'۷': '7', u'۸': '8', u'۹': '9',
}


def normalize_digits(digits):
    input_digits = str(digits)
    result = ''
    for ltr in input_digits:
        if ltr in convert_digits_dict:
            result += convert_digits_dict[ltr]
        else:
            result += ltr
    return result


def validate_phone_number(phone_number):
    if mobile_pattern.match(phone_number):
        return (phone_number)
    else:
        raise InvalidPhoneNumber("Invalid phone number {}".format(phone_number))


def validate_email(email):
    if email_pattern.match(email):
        return (email)
    else:
        raise InvalidEmail("Invalid Email {}".format(email))


def normalaize_phone_number(phone_number: str):
    eng_phone_number = normalize_digits(phone_number)
    return '989%s%s'\
        % (mobile_pattern.search(eng_phone_number).group(2),
            mobile_pattern.search(eng_phone_number).group(3))


def generate_random_username(length=8, chars=ascii_lowercase + digits, split=8, delimiter='-'):
    from users.models import User
    username = ''.join([random.choice(chars) for i in range(length)])

    if split:
        username = delimiter.join([username[start:start + split] for start in range(0, len(username), split)])
    username = 'user-' + username
    try:
        User.objects.get(username=username)
        return generate_random_username(length=length, chars=chars, split=split, delimiter=delimiter)
    except User.DoesNotExist:
        return username
    except:
        return ''


def generate_otp(length=6):
    otp = ""
    for i in range(length):
        otp += __digits[math.floor(random.random() * 10)]
    return otp
