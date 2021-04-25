# -*- coding: utf-8 -*-
import tweepy
import json
import requests
import time
import os
"""
*******************READ ME********************
■前準備
①pipを入れる（詳細はググること）
②pip install tweepy   でtweepyを取得
③pip install requests でrequestsを取得

■設定値関連
# API用のキー
  TwitterAPIのキーをセットしてください(CK/CS/AT/AS)

# 画像取得
1 いいね取得
　res = api.favorites(screen_name = screen_name, count = 200)
　screen_name：対象のユーザのスクリーンネーム
　count：いいねの取得件数
***********************************************
"""
############################################
# ここから設定項目
# API用のキー
CUSTOMER_KEY = "FfYhUgNHZFvwtdJTcihFTkEJE"
CUSTOMER_SECRET = "fRFvuSSbY1PjiSnd5stJECSqovtuA6sZ1rMDLLzvcfYIzUBmBa"
ACCESS_TOKEN = "106067637-SFNBklOsLgDpLm4X8kkrtQr2Xlm1BhR6BFfEWX8S"
ACCESS_TOKEN_SECRET = "AHoLBIyV1V0bHwCKvJcp75XreWMppr5HfvVaNTOlnB1FH"

# 走査対象のscreen_nameとツイート数を指定
target_user = 'nesosuke'
getcount = '200'

# 保存用ディレクトリ
SAVE_DIR = "./Pictures/twitter-pics/"


# ここまで設定項目
############################################
# OAuthの準備
auth = tweepy.OAuthHandler(CUSTOMER_KEY, CUSTOMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# TwitterAPIハンドル取得
api = tweepy.API(auth)

# 画像取得
# 1 いいね取得
res = api.favorites(target_user, count=getcount)
print(len(res))

# 保存用ディレクトリがなければ作成
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

# 2 各ツイートごとに画像確認
for twi in res:
    time.sleep(1)
    # 2-1 画像の有無確認

    if 'extended_entities' in twi._json:
        for media_data in twi._json['extended_entities']['media']:
            # 複数画像対応
            if media_data['type'] == 'photo':
                filename = format(
                    twi.user._json['screen_name']) + '-' + media_data['media_url_https'].split("/")[-1]
                filepath = SAVE_DIR+filename
                req = requests.get(media_data['media_url_https'])
                if req.status_code == 200:
                    f = open(filepath, 'wb')
                    f.write(req.content)
                    f.close()

            # 動画対応
            if media_data['type'] == 'video':
                video_variants = media_data['video_info']['variants']
                bitrates = []
                for variants in video_variants:
                    if 'bitrate' in variants:
                        bitrates.append(variants['bitrate'])

                video_url = video_variants[bitrates.index(
                    max(bitrates))]['url']
                filename = format(
                    twi.user._json['screen_name']) + '-' + video_url.split("/")[-1].split('?')[-2]
                filepath = SAVE_DIR+filename
                req = requests.get(video_url)
                if req.status_code == 200:
                    f = open(filepath, 'wb')
                    f.write(req.content)
                    f.close()

            print(filename)

            # if 'media' in twi._json['entities']:
            #     # 2-2 複数画像に対応
            #     for picData in twi._json['entities']['media']:
            #         # 2-3 画像かどうか確認
            #         if picData['type'] == 'photo':
            #             # 2-4 ファイル名決定(URLの最後の「/」以降)

            #             fileName = format(
            #                 twi.user._json['screen_name']) + '-' + picData['media_url_https'].split("/")[-1]
            #             filePath = SAVE_DIR + fileName
            #             # 2-5 画像取得Req
            #             req = requests.get(picData['media_url_https'])
            #             # 2-6 200Rsp　正常時
            #             if req.status_code == 200:
            #                 # 2-7 ファイル保存
            #                 f = open(filePath, 'wb')
            #                 f.write(req.content)
            #                 f.close()
            #                 # print(picData['media_url_https'])
