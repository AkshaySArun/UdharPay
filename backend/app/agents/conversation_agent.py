def classify(text:str)->str:
    t=text.lower()
    if any(x in t for x in ("stop","मत भेज","opt out","बंद करो")): return "OPT_OUT"
    if any(x in t for x in ("dispute","गलत","wrong","कम है")): return "DISPUTE_AMOUNT"
    if any(x in t for x in ("later","कल","बाद में","pay later")): return "PAY_LATER"
    if any(x in t for x in ("paid","दे दिया","already paid")): return "ALREADY_PAID"
    if any(x in t for x in ("link","pay","भेजो","भुगतान","हाँ","haan")): return "REQUEST_PAYMENT_LINK"
    if any(x in t for x in ("partial","थोड़ा","कुछ")): return "PAY_PARTIALLY"
    return "REQUEST_HUMAN_HELP"
