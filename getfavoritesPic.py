# -*- coding: utf-8 -*-
import tweepy
import json
import requests
"""
*******************READ ME********************
■前準備
①pipを入れる（詳細はググること）
②pip install tweepy   でtweepyを取得
③pip install requests でrequestsを取得
④コードを動かすディレクトリに
  ./pic/ を作成する。

■設定値関連
# API用のキー
  TwitterAPIのキーをセットしてください(CK/CS/AT/AS)

# 画像取得
1 いいね取得
　res = api.favorites(screen_name = 'nesosuke',count = 200)
　screen_name：対象のユーザのスクリーンネーム
　count：いいねの取得件数
***********************************************
"""
# API用のキー
CUSTOMER_KEY = "XXXXXXXXXXXXXXXX"
CUSTOMER_SECRET = "XXXXXXXXXXXXXXXX"
ACCESS_TOKEN = "XXXXXXXXXXXXXXXX-XXXXXXXXXXXXXXXX"
ACCESS_TOKEN_SECRET = "XXXXXXXXXXXXXXXX"

# OAuthの準備
auth = tweepy.OAuthHandler(CUSTOMER_KEY,CUSTOMER_SECRET)
auth.set_access_token(ACCESS_TOKEN,ACCESS_TOKEN_SECRET)

# TwitterAPIハンドル取得
api = tweepy.API(auth)

# 画像取得
# 1 いいね取得
res = api.favorites('nesosuke',count=200)
print(len(res))
# 2 各ツイートごとに画像確認
for twi in res:
    #2-1 画像の有無確認
    if 'media' in twi._json['entities']: 
        # 2-2 複数画像に対応
        for  picData in twi._json['entities']['media']: 
            # 2-3 画像かどうか確認
            if picData['type'] == 'photo':
                # 2-4 ファイル名決定(URLの最後の「/」以降)
                fileName = picData['media_url_https'].split("/")[-1]
                filePath = './pic/' + fileName
                # 2-5 画像取得Req
                req = requests.get(picData['media_url_https'])
                # 2-6 200Rsp　正常時
                if req.status_code == 200:
                    # 2-7 ファイル保存
                    f = open(filePath, 'wb')
                    f.write(req.content)
                    f.close()
                    print(picData['media_url_https'])
    