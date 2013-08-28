#!/usr/bin/env python
# -*- coding: utf-8 -*-
# from http://d.hatena.ne.jp/mohayonao/20091129/1259505966

import re

"""かな⇔ローマ字を変換する"""

def _make_kana_convertor():
    """ひらがな⇔カタカナ変換器を作る"""
    kata = {
        u'ア':u'あ', u'イ':u'い', u'ウ':u'う', u'エ':u'え', u'オ':u'お',
        u'カ':u'か', u'キ':u'き', u'ク':u'く', u'ケ':u'け', u'コ':u'こ',
        u'サ':u'さ', u'シ':u'し', u'ス':u'す', u'セ':u'せ', u'ソ':u'そ',
        u'タ':u'た', u'チ':u'ち', u'ツ':u'つ', u'テ':u'て', u'ト':u'と',
        u'ナ':u'な', u'ニ':u'に', u'ヌ':u'ぬ', u'ネ':u'ね', u'ノ':u'の',
        u'ハ':u'は', u'ヒ':u'ひ', u'フ':u'ふ', u'ヘ':u'へ', u'ホ':u'ほ',
        u'マ':u'ま', u'ミ':u'み', u'ム':u'む', u'メ':u'め', u'モ':u'も',
        u'ヤ':u'や', u'ユ':u'ゆ', u'ヨ':u'よ', u'ラ':u'ら', u'リ':u'り',
        u'ル':u'る', u'レ':u'れ', u'ロ':u'ろ', u'ワ':u'わ', u'ヲ':u'を',
        u'ン':u'ん',

        u'ガ':u'が', u'ギ':u'ぎ', u'グ':u'ぐ', u'ゲ':u'げ', u'ゴ':u'ご',
        u'ザ':u'ざ', u'ジ':u'じ', u'ズ':u'ず', u'ゼ':u'ぜ', u'ゾ':u'ぞ',
        u'ダ':u'だ', u'ヂ':u'ぢ', u'ヅ':u'づ', u'デ':u'で', u'ド':u'ど',
        u'バ':u'ば', u'ビ':u'び', u'ブ':u'ぶ', u'ベ':u'べ', u'ボ':u'ぼ',
        u'パ':u'ぱ', u'ピ':u'ぴ', u'プ':u'ぷ', u'ペ':u'ぺ', u'ポ':u'ぽ',

        u'ァ':u'ぁ', u'ィ':u'ぃ', u'ゥ':u'ぅ', u'ェ':u'ぇ', u'ォ':u'ぉ',
        u'ャ':u'ゃ', u'ュ':u'ゅ', u'ョ':u'ょ',
        u'ヴ':u'&#12436;', u'ッ':u'っ', u'ヰ':u'ゐ', u'ヱ':u'ゑ',
    }

    # ひらがな → カタカナ のディクショナリをつくる
    hira = dict([(v, k) for k, v in kata.items() ])

    re_hira2kata = re.compile("|".join(map(re.escape, hira)))
    re_kata2hira = re.compile("|".join(map(re.escape, kata)))

    def _hiragana2katakana(text):
        return re_hira2kata.sub(lambda x: hira[x.group(0)], text)

    def _katakana2hiragana(text):
        return re_kata2hira.sub(lambda x: kata[x.group(0)], text)

    return (_hiragana2katakana, _katakana2hiragana)


hiragana2katakana, katakana2hiragana = _make_kana_convertor()

################################################################################

def _make_romaji_convertor():
    """ローマ字⇔かな変換器を作る"""
    master = {
        u'a'  :u'ア', u'i'  :u'イ', u'u'  :u'ウ', u'e'  :u'エ', u'o'  :u'オ',
        u'ka' :u'カ', u'ki' :u'キ', u'ku' :u'ク', u'ke' :u'ケ', u'ko' :u'コ',
        u'sa' :u'サ', u'shi':u'シ', u'su' :u'ス', u'se' :u'セ', u'so' :u'ソ',
        u'ta' :u'タ', u'chi':u'チ', u'tu' :u'ツ', u'te' :u'テ', u'to' :u'ト',
        u'na' :u'ナ', u'ni' :u'ニ', u'nu' :u'ヌ', u'ne' :u'ネ', u'no' :u'ノ',
        u'ha' :u'ハ', u'hi' :u'ヒ', u'fu' :u'フ', u'he' :u'ヘ', u'ho' :u'ホ',
        u'ma' :u'マ', u'mi' :u'ミ', u'mu' :u'ム', u'me' :u'メ', u'mo' :u'モ',
        u'ya' :u'ヤ', u'yu' :u'ユ', u'yo' :u'ヨ',
        u'ra' :u'ラ', u'ri' :u'リ', u'ru' :u'ル', u're' :u'レ', u'ro' :u'ロ',
        u'wa' :u'ワ', u'wo' :u'ヲ', u'n'  :u'ン', u'vu' :u'ヴ',
        u'ga' :u'ガ', u'gi' :u'ギ', u'gu' :u'グ', u'ge' :u'ゲ', u'go' :u'ゴ',
        u'za' :u'ザ', u'ji' :u'ジ', u'zu' :u'ズ', u'ze' :u'ゼ', u'zo' :u'ゾ',
        u'da' :u'ダ', u'di' :u'ヂ', u'du' :u'ヅ', u'de' :u'デ', u'do' :u'ド',
        u'ba' :u'バ', u'bi' :u'ビ', u'bu' :u'ブ', u'be' :u'ベ', u'bo' :u'ボ',
        u'pa' :u'パ', u'pi' :u'ピ', u'pu' :u'プ', u'pe' :u'ペ', u'po' :u'ポ',

        u'kya':u'キャ', u'kyi':u'キィ', u'kyu':u'キュ', u'kye':u'キェ', u'kyo':u'キョ',
        u'gya':u'ギャ', u'gyi':u'ギィ', u'gyu':u'ギュ', u'gye':u'ギェ', u'gyo':u'ギョ',
        u'sha':u'シャ',
        u'shu':u'シュ', u'she':u'シェ', u'sho':u'ショ',
        u'ja' :u'ジャ',
        u'ju' :u'ジュ', u'je' :u'ジェ', u'jo' :u'ジョ',
        u'cha':u'チャ',
        u'chu':u'チュ', u'che':u'チェ', u'cho':u'チョ',
        u'dya':u'ヂャ', u'dyi':u'ヂィ', u'dyu':u'ヂュ', u'dhe':u'デェ', u'dyo':u'ヂョ',
        u'nya':u'ニャ', u'nyi':u'ニィ', u'nyu':u'ニュ', u'nye':u'ニェ', u'nyo':u'ニョ',
        u'hya':u'ヒャ', u'hyi':u'ヒィ', u'hyu':u'ヒュ', u'hye':u'ヒェ', u'hyo':u'ヒョ',
        u'bya':u'ビャ', u'byi':u'ビィ', u'byu':u'ビュ', u'bye':u'ビェ', u'byo':u'ビョ',
        u'pya':u'ピャ', u'pyi':u'ピィ', u'pyu':u'ピュ', u'pye':u'ピェ', u'pyo':u'ピョ',
        u'mya':u'ミャ', u'myi':u'ミィ', u'myu':u'ミュ', u'mye':u'ミェ', u'myo':u'ミョ',
        u'rya':u'リャ', u'ryi':u'リィ', u'ryu':u'リュ', u'rye':u'リェ', u'ryo':u'リョ',
        u'fa' :u'ファ', u'fi' :u'フィ',
        u'fe' :u'フェ', u'fo' :u'フォ',
        u'wi' :u'ウィ', u'we' :u'ウェ', 
        u'va' :u'ヴァ', u'vi' :u'ヴィ', u've' :u'ヴェ', u'vo' :u'ヴォ',

        u'kwa':u'クァ', u'kwi':u'クィ', u'kwu':u'クゥ', u'kwe':u'クェ', u'kwo':u'クォ',
        u'kha':u'クァ', u'khi':u'クィ', u'khu':u'クゥ', u'khe':u'クェ', u'kho':u'クォ',
        u'gwa':u'グァ', u'gwi':u'グィ', u'gwu':u'グゥ', u'gwe':u'グェ', u'gwo':u'グォ',
        u'gha':u'グァ', u'ghi':u'グィ', u'ghu':u'グゥ', u'ghe':u'グェ', u'gho':u'グォ',
        u'swa':u'スァ', u'swi':u'スィ', u'swu':u'スゥ', u'swe':u'スェ', u'swo':u'スォ',
        u'swa':u'スァ', u'swi':u'スィ', u'swu':u'スゥ', u'swe':u'スェ', u'swo':u'スォ',
        u'zwa':u'ズヮ', u'zwi':u'ズィ', u'zwu':u'ズゥ', u'zwe':u'ズェ', u'zwo':u'ズォ',
        u'twa':u'トァ', u'twi':u'トィ', u'twu':u'トゥ', u'twe':u'トェ', u'two':u'トォ',
        u'dwa':u'ドァ', u'dwi':u'ドィ', u'dwu':u'ドゥ', u'dwe':u'ドェ', u'dwo':u'ドォ',
        u'mwa':u'ムヮ', u'mwi':u'ムィ', u'mwu':u'ムゥ', u'mwe':u'ムェ', u'mwo':u'ムォ',
        u'bwa':u'ビヮ', u'bwi':u'ビィ', u'bwu':u'ビゥ', u'bwe':u'ビェ', u'bwo':u'ビォ',
        u'pwa':u'プヮ', u'pwi':u'プィ', u'pwu':u'プゥ', u'pwe':u'プェ', u'pwo':u'プォ',
        u'phi':u'プィ', u'phu':u'プゥ', u'phe':u'プェ', u'pho':u'フォ',
    }


    romaji_asist = {
        u'si' :u'シ'  , u'ti' :u'チ'  , u'hu' :u'フ' , u'zi':u'ジ',
        u'sya':u'シャ', u'syu':u'シュ', u'syo':u'ショ',
        u'tya':u'チャ', u'tyu':u'チュ', u'tyo':u'チョ',
        u'cya':u'チャ', u'cyu':u'チュ', u'cyo':u'チョ',
        u'jya':u'ジャ', u'jyu':u'ジュ', u'jyo':u'ジョ', u'pha':u'ファ', 
        u'qa' :u'クァ', u'qi' :u'クィ', u'qu' :u'クゥ', u'qe' :u'クェ', u'qo':u'クォ',

        u'ca' :u'カ', u'ci':u'シ', u'cu':u'ク', u'ce':u'セ', u'co':u'コ',
        u'la' :u'ラ', u'li':u'リ', u'lu':u'ル', u'le':u'レ', u'lo':u'ロ',

        u'mb' :u'ム', u'py':u'パイ', u'tho': u'ソ', u'thy':u'ティ', u'oh':u'オウ',
        u'by':u'ビィ', u'cy':u'シィ', u'dy':u'ディ', u'fy':u'フィ', u'gy':u'ジィ',
        u'hy':u'シー', u'ly':u'リィ', u'ny':u'ニィ', u'my':u'ミィ', u'ry':u'リィ',
        u'ty':u'ティ', u'vy':u'ヴィ', u'zy':u'ジィ',

        u'b':u'ブ', u'c':u'ク', u'd':u'ド', u'f':u'フ'  , u'g':u'グ', u'h':u'フ', u'j':u'ジ',
        u'k':u'ク', u'l':u'ル', u'm':u'ム', u'p':u'プ'  , u'q':u'ク', u'r':u'ル', u's':u'ス',
        u't':u'ト', u'v':u'ヴ', u'w':u'ゥ', u'x':u'クス', u'y':u'ィ', u'z':u'ズ',

        u'-':u'ー', u'~':u'〜', u'!':u'！', u'?':u'？', u'&':u'＆', u'[':u'「', u']':u'」', u'(':u'（', u')':u'）',
    }


    kana_asist = { u'a':u'ァ', u'i':u'ィ', u'u':u'ゥ', u'e':u'ェ', u'o':u'ォ', }


    def __romaji2kana():
        romaji_dict = {}
        for tbl in master, romaji_asist:
            for k, v in tbl.items(): romaji_dict[k] = v
        
        romaji_keys = romaji_dict.keys()
        romaji_keys.sort(key=lambda x:len(x), reverse=True)
        
        re_roma2kana = re.compile("|".join(map(re.escape, romaji_keys)))
        # m の後ろにバ行、パ行のときは "ン" と変換
        rx_mba = re.compile("m(b|p)([aiueo])")
        # 子音が続く時は "ッ" と変換
        rx_xtu = re.compile(r"([bcdfghjklmpqrstvwxyz])\1")
        # 母音が続く時は "ー" と変換
        rx_a__ = re.compile(r"([aiueo])\1")
        
        def _romaji2katakana(text):
            result = text.lower()
            result = rx_mba.sub(ur"ン\1\2", result)
            result = rx_xtu.sub(ur"ッ\1"  , result)
            result = rx_a__.sub(ur"\1ー"  , result)
            return re_roma2kana.sub(lambda x: romaji_dict[x.group(0)], result)
        
        def _romaji2hiragana(text):
            result = _romaji2katakana(text)
            return katakana2hiragana(result)
        
        return _romaji2katakana, _romaji2hiragana


    def __kana2romaji():
        kana_dict = {}
        for tbl in master, kana_asist:
            for k, v in tbl.items(): kana_dict[v] = k

        kana_keys = kana_dict.keys()
        kana_keys.sort(key=lambda x:len(x), reverse=True)
        
        re_kana2roma = re.compile("|".join(map(re.escape, kana_keys)))
        rx_xtu = re.compile("ッ(.)") # 小さい "ッ" は直後の文字を２回に変換
        rx_ltu = re.compile("ッ$"  ) # 最後の小さい "ッ" は消去(?)
        rx_er  = re.compile("(.)ー") # "ー"は直前の文字を２回に変換
        rx_n   = re.compile(r"n(b|p)([aiueo])") # n の後ろが バ行、パ行 なら m に修正
        rx_oo  = re.compile(r"([aiueo])\1")      # oosaka → osaka
        
        def _kana2romaji(text):
            result = hiragana2katakana(text)
            result = re_kana2roma.sub(lambda x: kana_dict[x.group(0)], result)
            result = rx_xtu.sub(r"\1\1" , result)
            result = rx_ltu.sub(r""     , result)
            result = rx_er.sub (r"\1\1" , result)
            result = rx_n.sub  (r"m\1\2", result)
            result = rx_oo.sub (r"\1"   , result)
            return result
        return _kana2romaji

    a, b = __romaji2kana()
    c = __kana2romaji()

    return  a, b, c


romaji2katakana, romaji2hiragana, kana2romaji = _make_romaji_convertor()

################################################################################


if __name__ == "__main__":
    for s in ("mohayonao", "twitter", "ukulele", "monthy python", "spam!", "lambda"):
        print s, "\t>\t", romaji2katakana(s)
    print "=" * 20

    for s in ("nambda", "maitta", "ping pong"):
        print s, "\t>\t", romaji2hiragana(s)
    print "=" * 20

    for s in ("ぎょぎょっ", "こまったな", "おおさか", "ニッポン", "ジャパン"):
        print s, "\t>\t", kana2romaji(s)



    for word in ("mohayonao", "dendenmushi", "namba", "Dan Kogai"):
        print word, ">", romaji2katakana(word)

    for word in ("モハヨナオ", "なんば", "こんにちは", "マイッタ", "とうばんじゃん"):
        print word, ">", kana2romaji(word)

    def amasakas(text):
        s = kana2romaji(text)
        s = s[::-1]
        return romaji2hiragana(s)

    print amasakas("さかさま")
