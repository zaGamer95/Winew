# -*- coding: utf-8 -*-
"""wine_review_crawling_code.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1r9rDonGAq1oH2zuOXn1hfdjpGY1vKLeP
"""

import requests
import numpy as np
import pandas as pd
import json

from google.colab import drive
drive.mount('/content/drive')

from google.colab import files
wine_csv = '/content/drive/MyDrive/tobigs14_conference/data/무필요/vintages.csv'
wine_data = pd.read_csv(wine_csv)

wine_ids=list(wine_data['vintage.wine.id'].unique())

# wine_id 별로 year & vintage_id 10개씩 가져오기 -> 10개가 다 안가져와지고 개수가 다 다른 상태..!

vintage_year = []

headers = {
  'Cookie': 'first_time_visit=nOpHhXsBHwQaz8ZxE%2FAZvbOm1UXriuJxKS6JkDZo%2B1ZC6dBaXPF3C5ksPg3gvZoElbp%2BJhjQVhWoMqO3ud5MbXEEgvCqWpH1Bg%3D%3D--yEwhYjoFJkmz0uTr--UpOtwJX6YYIEVeI7i6Lt4w%3D%3D; eeny_meeny_test_checkout_login_v1=C9T2VzusNxYl2uL96O6xo%2FoQb%2FLOG%2BbwXgoV%2Fq4Vp53JDf12oAaUACCmyEf2UEPB5vejhjp4mBBHFqGl%2BAC7fQ%3D%3D; recently_viewed=r0ESLAJYpHx%2FzdK9PtQuv334%2Bt8j6h4JaS0L8HT2%2FtBzh0ZlPoLnszYuawAWhxMxfNLSn4qzGFe62cuJi396L79TOPWEfy9fNa2YiIojkZ%2BWwSlP7e0bsUb3s8eA%2FgQaoUufONQYMupNIam6L%2FG64pwy3htYoumhIWpE%2BDjr0XHEi%2B7fZ54CDWCbQ6jowdLi5uRegt9K7Y%2Biy30P2lDRl6E5tfRaaa80MJCJrfYW7KJzn0AVVttj1pFe%2FOwMbb4zDI4aF3aWkgIdG%2FAs7LWuJsoOXZzzZMLxpQYkAx5vqQ0BLNjgkFtFrjPzAOiTT7dBJjurafheWER5xtMWCPnsBSxIwh46MabkF7am40YkkWYxlisHcvu6TbCE4YbJPZl8WDbVvNNqHRKvtTe7PJV2kjAHYm7ir8QsTkhrXfeevBeeYnWtUgTULDA%2BGrRHYW0HoVKH9NE%3D--RP4y%2F5nMgMlbf9Uc--xZDrj35krcKjzF6zvt0Iag%3D%3D; eeny_meeny_test_forced_merchant_filter_v1=1%2FOkhWrQZ2YZgTpjZGJ7A9lDr1xIqcuNJKg5T9aPX%2Bio%2FKeZ6t%2F2ZFcqvQVmNDI5C9%2BIpAy1gSrBi37NsAR0yA%3D%3D; _ruby-web_session=SKTSodxzYZl9PS3ObbQSLKv11E5UUZ0nctZILbxUpsgqMQtxO5f27wb99PxKFs5dwepymBYfjKqZxOHrQdt53M3FqIOfTC6URokMXbx0%2FHz5YOgm7YjVrO7kba4WzdQA6qjyfI6hdxSFnEY%2Ft8fo64H4%2F7Yj6GSrsFHNDvzcWgcbe%2Fxzs3C1obqTS%2FGaQz9SUttjs3NbtPG9Whb7oL4%2BSy1ujh9cuQ6X%2FgCJSV0WLj%2BhUekwHgzof0mDUqO9oDb7%2F0kHn60nGleIG9bFEyW5HhkK0VUSO0XJZt9cWsMlB66qkfnIPxMQHaCXVmoFM5c7%2Bunb7PmrFVhMEhzcINNb9UTKM1nsZ3aK%2BHd71UVOldXemWVAJBXk0eYnL9J0%2FfbVhJ2uBMXXzOE9GTZfYCMDYqSSQFbFRHQMTHi9qXxl2hiRrMnnqjLLqu%2FLlMHVOYSXA0ZY8Y09vefVt7I3wg1F0or7Ec4lfwMfHBZUrv6Jtb%2BPNUmXg3GAXSZn6DNCgY5eMEc71Mk%3D--OSMVFLjM8A9jA3b1--HGFvfWGHKyuyTVoTRaicsg%3D%3D',
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'
}

for i in wine_ids:
    url = "https://www.vivino.com/api/wines/{}/highlights?per_page=10".format(i)
    response = requests.request("GET", url, headers=headers).json()['highlights']
    for highlight in response:
        year = highlight['metadata']['vintage_year']
        vintage_id = highlight['vintage_id']
        vintage_type=highlight['highlight_type']
        vintage_year.append([i,year,vintage_id, vintage_type])
vintage_year = pd.DataFrame(vintage_year, columns=['wine_id','year','vintage_id', 'vintage_type'])

#vintage_year별로 리뷰 가져오기
wine_review_dataFrame = pd.DataFrame(columns=['wine_id', 'vintage_id', 'vintage_type','vintage_year','userID', 'rating_per_user', 'user_note', 'user_follower_count', 'user_following_count', 'user_rating_count',
                                                                'user_rating_sum', 'reviews_count', 'user_like_count', 'user_comments_count', 'review_time', 'review_language', 'review_year'])

headers = {
        'accept': 'application/json',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/json',
        'Cookie': 'first_time_visit=XTJGtS0FCF9wLuAbu62fCafZGTpMEBmq7oH9qIBNeExMAX%2BbzkfYkUl0Lx%2BszIUnpWdJ%2BAn0VNeA7cAXUjpH8g5GTo9SoPw9Cg%3D%3D--sMDXKb7f5LyU%2BACy--BRN%2BSjIjTTJdMxjZmPKBwQ%3D%3D; eeny_meeny_test_checkout_login_v1=1Zk2r0Bm9U4dbab5RXW3cy4GTo95liDfrj5aaHl%2FXYX9od99aZYC9NJ2GNi807pgp4DJ16RiuxJAP2%2F8at9FBg%3D%3D; _ruby-web_session=RtaZZyz7U1uT%2B17T8R3Txn61SChDKGdvZDEav4L4uMY1tLddoIzeFrWYe%2BcEjFnFmLOFlWCeAfaE30fqLh7T5w5Kx0d0RsT3nw2ygTM0rxArilhO48zBiMtJi9h220Wt9XJLL6T%2B76ozsILk%2Bmtsg1sr2f8JT8OtWkgoGTWb1RlE%2Fn2eUQD2rKFh1wqjFcpw%2FPMAVj2hFP3oBLfvOxSru8B2mnm2I%2FXqjUHvuXVYyHGexdfS%2FixhqUIt2T%2FMPEeWZmAYRfNZ4Z4YycA9pZi6Sxc1WlB%2BbGP%2FuxdbMYEgQXIeG3%2F%2FDWJIIf0LDq95eTuBztd9xOllDURYRQUiHtkrZ78G9ofyAme9zT7WJUh3ZckWwF6xPptDoep1312K3a%2FK0XK2jCYmZ6hn1Ln5P2PgcI6EaQ4L2VX%2BKYAAZXhJqtnEGusDVRk8jb13pDpA0MlQcLPmpgEt1oPfua6XzkFO1FuGH1l%2F2gNRGwXqJLwmLRW7RWSZ%2BrkjST8xN%2Bqsjq8YGrPIS0w%3D--JB7wCxUQHIoDHoXG--yx192j3fhxp27Tt58CNeig%3D%3D; eeny_meeny_test_forced_merchant_filter_v1=pjAoKTJFxvftq%2B4y%2FO9nc%2FPAaO3aOF3RKeAphoBvkKK3gyFV4Bgxrqlxdq0dISH1CAsIOsWypUTJy55hp%2B0S0Q%3D%3D',
        'referer' : 'https://www.vivino.com/FR/en/domaine-de-grangeneuve-la-truffiere/w/1805893?year=2017',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Mobile Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
        }

for i in vintage_year.index:
    url = "https://www.vivino.com/api/wines/{}/reviews?year={}&per_page=50&page=2".format(vintage_year.loc[i,'wine_id'], vintage_year.loc[i,'year'])
    response = requests.request("GET", url, headers=headers).json()

    for review in response['reviews']:

        save_list = []
        save_list.append(vintage_year.loc[i,'wine_id'])
        save_list.append(vintage_year.loc[i,'vintage_id'])
        save_list.append(vintage_year.loc[i,'vintage_type'])
        save_list.append(vintage_year.loc[i,'year'])

        try:
            save_list.append(review.get('user').get('id')) #유저 id
        except:
            save_list.append(np.nan)
        try:
            save_list.append(review.get('rating')) #유저의 와인 평점
        except:
            save_list.append(np.nan)
        try:
            save_list.append(review.get('note')) #유저의 리뷰
        except:
            save_list.append(np.nan)
        try:
            save_list.append(review.get('user').get('statistics').get('followers_count')) #유저의 팔로워 수
        except:
            save_list.append(np.nan)
        try:
            save_list.append(review.get('user').get('statistics').get('followings_count')) #유저의 팔로잉 수
        except:
            save_list.append(np.nan)
        try:    
            save_list.append(review.get('user').get('statistics').get('ratings_count')) # 유저의 평점 count
        except:
            save_list.append(np.nan)
        try:    
            save_list.append(review.get('user').get('statistics').get('ratings_sum')) # 평점 합
        except:
            save_list.append(np.nan)
        try:
            save_list.append(review.get('user').get('statistics').get('reviews_count')) # 리뷰 횟수
        except:
            save_list.append(np.nan)
        try:
            save_list.append(review.get('activity').get('statistics').get('likes_count')) # 좋아요 수
        except:
            save_list.append(np.nan)
        try:        
            save_list.append(review.get('activity').get('statistics').get('comments_count')) # 코멘트 수
        except:
            save_list.append(np.nan)
        try:        
            save_list.append(review.get('created_at')) # 리뷰 남긴 시간
        except:
            save_list.append(np.nan)
        try:        
            save_list.append(review.get('language')) # 리뷰 언어
        except:
            save_list.append(np.nan)
        try:        
            save_list.append(review.get('vintage').get('year')) # 리뷰남긴 와인의 년도
        except:
            save_list.append(np.nan)

        finally:
            wine_review_dataFrame = wine_review_dataFrame.append(pd.Series(save_list, index=wine_review_dataFrame.columns), ignore_index=True)


wine_review_dataFrame

wine_review_dataFrame

wine_review_dataFrame.to_json('review_vintage_id.json')

wine_review_dataFrame.to_csv('review_vintage_id.csv')

