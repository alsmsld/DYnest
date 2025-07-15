import re

BAD_WORDS = [
    'ㅅㅂ', 'ㅂㅅ', 'ㅄ', '씨발', '시발', '좆', '새끼', '미친놈', '미친년',
    '애미', '미친년', '지랄', '시발년', '미친년', 'ㅅ ㅂ', 'ㅆㅂ', 'ㅗ','존나','어매','시발년','ㅈㄴ','븅신','등신','장애','개같은', '병신'
    # 여기에 더 추가 가능
]

def censor_text(text):
    pattern = '|'.join([re.escape(word) for word in BAD_WORDS])
    return re.sub(pattern, '***', text, flags=re.IGNORECASE)
