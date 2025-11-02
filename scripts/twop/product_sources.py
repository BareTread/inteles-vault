from typing import List, Dict


def curated_queries_by_program_slug() -> Dict[str, List[str]]:
    return {
        "libris.ro": ["dictionar de vise", "c.g. jung vise", "freud vise", "psihologia viselor"],
        "springfarma.com": ["magneziu glicinat", "melatonina 5 mg", "ceai lavanda n146"],
        "manukashop.ro": ["manuka mgo 550", "manuka mgo 850"],
        "evomag.ro": ["beurer wl 50"],
        "flanco.ro": ["umidificator ecg ah d501"],
        "librex.ro": ["jurnal vise", "jurnal mindfulness"],
    }


def curated_product_urls() -> Dict[str, List[str]]:
    return {
        "libris.ro": [
            "https://www.libris.ro/dictionar-de-vise-a120422--p27597066.html",
            "https://www.libris.ro/dictionar-de-vise-C98691--p27455015.html",
            "https://www.libris.ro/analiza-viselor-c-g-jung-TRE978-606-40-0393-5--p1258533.html",
        ],
        "springfarma.com": [
            "https://www.springfarma.com/magneziu-glicinat-60-capsule-nutrific.html",
            "https://www.springfarma.com/ceai-de-lavanda-n-146-20-plicuri-fares.html",
            "https://www.springfarma.com/melatonina-pura-5-mg-60-tablete.html",
        ],
        "manukashop.ro": [
            "https://manukashop.ro/miere-de-manuka-mgo-550-500g.html",
            "https://manukashop.ro/miere-de-manuka-mgo-850-250g.html",
        ],
        "evomag.ro": [
            "https://www.evomag.ro/electronice/alarme/ceas-beurer-wl-50.html",
        ],
        "flanco.ro": [
            "https://www.flanco.ro/umidificator-ecg-ah-d501-t.html",
        ],
        "librex.ro": [],
    }

