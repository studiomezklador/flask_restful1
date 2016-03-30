import string
import random 

alpha_low = list(string.ascii_lowercase)
alpha_up = list(string.ascii_uppercase)
numb = map(str, list(range(0,9)))

alphanum = alpha_low
alphanum.extend(alpha_up)
alphanum.extend(numb)


def rnd(length=61):
    """ Alphanumeric generator key, with recursion if > 61 char.  """
    random.shuffle(alphanum, random.random)
    if length > len(alphanum):
       nu_len = length - len(alphanum)
       alphanum.append(rnd(nu_len))

    result = alphanum[:length]
    return "".join(result)


if __name__ == '__main__':
    rndk = rnd()
    print(rndk, len(rndk))
