# 113-1 資料庫管理 - LISTEN!! 專案Readme

## 專案簡介

LISTEN!! 是一個提供數位音樂播放服務的平台，致力於為使用者打造一個即時、便利的音樂世界。使用者可隨時隨地瀏覽並播放全球數百萬首音樂，根據個人喜好創建自訂播放清單，並接收個性化推薦，發現更多喜愛的歌曲和歌手。

平台支援多種會員方案，包括免費基本服務及高級會員訂閱，享受無廣告播放和離線下載等進階功能。我們的資料庫精心設計，確保資料的一致性與查詢效率，為用戶提供最佳體驗。


## 使用者功能

#### Listener (一般使用者)

*基本功能*

1. 瀏覽與播放音樂： 可瀏覽歌曲、專輯和歌手資訊，選擇播放喜愛的音樂。

2. 搜尋音樂： 輸入關鍵字查詢特定歌曲、專輯或歌手。

3. 播放清單管理： 建立播放清單，將歌曲加入或移除，檢視公開播放清單。

4. 播放紀錄與推薦： 自動記錄播放紀錄，系統根據喜好推薦音樂。

5. 捐贈與支持： 支援喜愛的歌手，進行金額捐贈。

6. 訂閱與追蹤活動： 關注歌手並查看歌曲與活動。

#### Artist (音樂創作者)

*創作者功能*

1. 音樂管理： 上傳與管理歌曲與專輯，編輯內容和描述。

2. 播放數據分析： 檢視播放次數與收入報告，瞭解個人影響力。

3. 活動管理： 創建演唱會與活動，與粉絲保持互動。

#### Admin (管理員)

*平台管理功能*

1. 帳戶管理： 新增、修改或刪除使用者與創作者帳號。

2. 使用者行為查詢： 檢視使用者的播放與捐款紀錄。

3. 內容審核： 管理平台上的歌曲與活動資訊。

## 使用方法

1. 安裝需求模組
    bash'''
        pip install -r requirements.txt
    '''

2. 資料庫復原： 使用 backup 檔案進行資料庫復原。

3. 連線設定： 預設連線為 127.0.0.1:5432，可修改 .env進行設定。
    DB_PASSWORD = ""
    DB_PORT = ""

4. 啟動伺服器
    bash'''
        python server.py
    '''
    啟動用戶端
    bash'''
        python client.py
    '''

## 技術細節

1. 資料庫： PostgreSQL，操作工具為 Psycopg2。

2. 網路連線： 使用 Socket 建立 Client-Server 連線，支援多人同時連線。

3. 交易管理： 自動交易控制，資料寫入錯誤時回滾操作，確保資料完整性。

4. 併行控制： 避免資料競爭，防止多重預約與交易衝突。

## 程式結構

1. server.py： 伺服器主程序，管理用戶連線與伺服器運行。

2. client.py： 用戶端應用，接收伺服器訊息並執行操作。

3. DB_utils.py： 資料庫操作封裝，包含資料查詢與交易管理。

4. action 資料夾： 功能動作模組，支援動態擴展。

5. role 資料夾： 使用者角色模組，定義各角色行為與權限。

## 開發環境

作業系統： mac os

程式語言與工具：

Python 3.10.9

PostgreSQL 16.4

套件：Psycopg2 2.9.10, Pandas 2.2.2, Tabulate 0.9.0

## 參考資料

專案說明文件與報告內容來自 113-1 資料庫管理。