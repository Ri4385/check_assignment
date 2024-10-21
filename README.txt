### スマホでもpandaにある課題を確認できるアプリを作りたい

非公式の課題取得アプリです。
なんかusernameとかpasswordとか暗号化できてるのか知らないけど、もし情報漏洩があったとしても製作者は一切の責任を負いません。
というか、何かあったとしても製作者はいかなる責任も負いません^^ おまえが負うんだよ^^

username, passwordでログインしてget assignmentを押すと課題が見れるよ^^

DUEのやつ見れるけど見れないようにするか悩み中
遅延提出ができるかどうかと、その期限を表示したいかも
授業資料見れるようにしたい

なんでREADME.mdじゃなくて.txtかって？？？僕の環境だと.md保存時にpdf exportされるからです。
なんか仮想環境とか設定とかで変えられると思うけどめんどいのでやりません。

sakai apiの仕様？
https://sakaiproject.atlassian.net/wiki/spaces/CONF/overview?mode=global

pandaをhackするという記事
https://kmconner.net/posts/2019/12/23-panda-console/

comfortable pandaのapi呼び出しの主要部分
https://github.com/comfortable-panda/ComfortablePandATS/blob/master/src/features/api/fetch.ts#L20

https://panda.ecs.kyoto-u.ac.jp/direct/content/resources/2024-110-7403-000.json
これで授業資料とれた
https://panda.ecs.kyoto-u.ac.jp/direct/content/resources/2024-110-7302-000/%E3%83%99%E3%82%AF%E3%83%88%E3%83%AB%E8%A7%A3%E6%9E%90%E8%87%AA%E7%BF%92%E5%95%8F%E9%A1%8C%E3%81%A8%E8%A7%A3%E7%AD%94%E4%BE%8B.json
みたいにやれば行けるわ、
folderなら~/name.jsonでリクエスト送る、fileUploadならnameとurlメモでいいかもね

https://panda.ecs.kyoto-u.ac.jp/access/content/group/2024-110-7302-000/
apiよりこれでスクレイピングしたほうが多分早い。

