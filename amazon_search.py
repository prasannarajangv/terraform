# coding: shift-jis
from bs4 import BeautifulSoup
import requests
import pandas as pd
import csv

__author__ = "SakaiEiji"
__version__ = "1.0.0"
__date__    = "2019/05/25"

# アマゾンで検索したい言葉を引数に 検索結果の「商品名」と「値段」をCSVに保存する
def search_amazon(search_word):
    """
    入力されたキーワードの検索結果ページからHTMLを解析して
    商品名、値段をCSV出力する
    なお、検索するページはサイトの負荷を踏まえ「5ページ」までとする

    @param search_word : this is a first param
    @raise keyError: raises an exception
    """

    # アマゾンのベースとなるURL
    amazon = "https://www.amazon.co.jp"

    # 空白で分割
    words = search_word.split(" ")
    # 先頭キーワード取得
    serch_words = words[0]
    # 分割で2個目以降のキーワードを+で連結
    for i in range(1, len(words)):
        serch_words = serch_words + "+" + words[i]

    # スクレイピングするサイトのURLを作成
    url =  amazon + "/s/ref=nb_sb_noss_2?__mk_ja_JP=カタカナ&url=search-alias%3Daps&field-keywords=" + serch_words + "&rh=i%3Aaps%2Ck%3A" + serch_words

    # CSVのヘッダーに書込みする項目をリストで作成
    columns = ["Name",  "Price"]
    # 配列名を指定する
    df = pd.DataFrame(columns=columns)

    # ページ番号(1ページ目から)
    page = 1

    #　6ページ未満は「except」処理へ
    try:

        #　サイトの負荷を考慮し、1?5ページ分だけ繰り返す
        while page < 6:

            # 作成したURLからHTMLを取得
            response = requests.get(url).text
            # BeautifulSoupの初期化
            soup = BeautifulSoup(response, 'html.parser')

            # htmlのどの部分を取得するか指定
            items = soup.find_all(attrs={'class':'s-result-item'})

            # 取得したタグ郡を1つずつ処理
            for item in items:

                # 商品名のタグ取得
                name = item.find("span", {"class":"a-size-base-plus a-color-base a-text-normal"})
                # 値段のタグ取得
                price = item.find("span", {"class":"a-offscreen"})

                # 商品名、値段の片方しかない場合はCSV出力せず、次のループへ(エラーとなるため)
                if name == None or price == None:
                    continue

                # 商品名取得
                nameTitle = name.string
                # 商品の値段取得
                priceText = price.string

                # 商品名、値段をリストに追加
                se = pd.Series([nameTitle, priceText], columns)
                #リストを追加
                df = df.append(se, columns)

            # 「次のページ」ボタンのタグを取得
            nextButton = soup.find("li", {"class":"a-last"})

            # 「次のページ」ボタンのURLを取得
            nextUrl = nextButton.a.get("href")

            # アマゾンのベースとなるURL + 次ページのURL
            url = amazon + nextUrl
            # 次のページに行くので+1する
            page += 1

    except:

             # 検索結果が2ページ等、5ページまでない場合は以下が出力
             print(page +1 + "以降のページはありませんでした")

    finally:

        # 保存するcsvのファイル名を決める
        filename = "amazon_" + search_word + ".csv"
        # 作成したリストをcsvへ
        df.to_csv(filename, encoding = 'utf-8-sig')
        # 終了した旨を出力
        print("終了しました")



# 検索キーワードを入力する
print('Amazonの商品を検索します\n検索ワードを入力してください')
key_word = input('検索ワード:')

# 検索キーワードで検索を実施(serch_amazonメソッド呼出)
search_amazon(key_word)