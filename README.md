# ibs_log

ibisPaint の特定ユーザーの投稿データを一括で取得するスクリプトです。自己責任にてご利用ください。


## How To Use

### Install

```
pip3 install -r requirements.txt
```

### Run

```
python3 ibs_log --service-id=twitter $ARTIST_ID
```

$ARTIST_ID は ibisPaint のサイト上から確認できます。

Facebook 連携の場合は service_id を twitter でなく facebook にしてください(未検証)。

とりあえず投稿タイムスタンプ(ms)、PV、制作時間(s) が取れます。