# -*- coding: utf-8 -*-
# import numpy as np
import random

def pick_up():
    messages = [
        u"こんにちは",
        u"こんばんは",
        u"おはようございます"
    ]
    return random.choice(messages)
