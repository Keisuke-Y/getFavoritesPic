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

# 検索条件作成(関数)
# ①RT or Favが引数の値以上（規定値：20）
# ②メディア有無の確認
def target_pic_judge(twi_status,fav_count=20,rt_count=20):
    # 取得条件(いいね OR RT が20より大きい)
    if twi_status._json['retweet_count'] > rt_count or twi_status._json['favorite_count'] > fav_count:
        # メディア有無確認
        if 'media' in  twi_status._json['entities']:
            # メディアあり→保存確認要
            return True
        else:
            # メディアなし→保存不要
            return False
    else:
        # RT Fav条件未達
        return False


# 画像保存処理
# req_data：取得データ
# target_path：保存先
def get_pic_onReq(req_data, target_path):
    f = open(target_path, 'wb')
    f.write(req_data.content)
    f.close()


# 画像取得
# 1 いいね取得
res = api.favorites('nesosuke',count=200)
# 2 各ツイートごとに画像確認
for twi in res:
    # 2-1 条件確認
    if target_pic_judge(twi):
        # 2-2 複数画像に対応
        for picData in twi._json['entities']['media']: 
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
                    get_pic_onReq(req,filePath)
                    # 2-8 不適切画像はさらにほかのフォルダへ
                    if twi._json['possibly_sensitive'] == True:
                        get_pic_onReq(req,'./target/'+fileName)
