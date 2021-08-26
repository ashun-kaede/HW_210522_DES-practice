# DES_practice

## 2021/05/20 
- 這是我的一個學校的功課項目，目前已經完成大致功能，但仍有以下bug尚在解決:
1. 部分特殊字元在轉碼(ascii to binary)過程中會不正常，目前以跳過處理
2. 已完成 ECB CBC CFB OFB。

- I made this for my homework from school. It's almost done, but it still have some bug.
1. For some reason, special characters can not be encripted. (probably is decode problem)
2. I have done 4 mode in DES (ECB CBC CFB OFB).

- このプロジェクトは学校の宿題です。もうすぐ完成ですけど、まだ問題は2つがあります：
1. 特殊文字はまだ暗号化できません、多分decodeの問題です。
  <ps.『decode』どうやって翻訳しますか？教えてください！>
2. もう４種類(ECB CBC CFB OFB)完成しました。

===============================================================================

## 零、開發環境
- 開發語言：python
- 編輯器：vscode

## 一、概述
- 此應用程式目的在於實踐DES算法，支持圖形化介面讓使用者更容易操作。程式中提供四種模式（CTR尚有問題除外）的加解密操作，以及隨機產生金鑰的功能。
- 開發上以簡潔為目標，DES算法核心部分加解密可用同一段源代碼，帶入不同參數即可分別實現加密與解密操作。
- 目前支援ACSII輸入，輸出則為HEX，不過無論輸入輸出皆可以用ASCII開啟。

## 二、程式架構
<img src="https://i.imgur.com/4aVYJOY.png" alt="Cover" width="30%"/>

本程式為階層式，分為四個py檔案：
1. UI_mian.py：圖形化介面
2. DES_mode.py：分割檔案、執行各種模式
3. DES_main.py：對單個block(64bit)進行加密
4. AllTable.py：存放各種轉換表

上圖箭頭方向為引用方向，因此從圖中可看出DES_main為本程式最核心之底層，是DES算法的核心部分。而上一層的DES_mode則包攬各種模式與拆分檔案的工作，最上層的UI_main則負責桌面應用程式的圖形化介面。以下將從最底層針對各個模塊進行細部說明。

## 三、AllTable與DES_main詳解
AllTable的部分比較簡單，單純存放各種table以供DES之用。
DES_main主要分為三個部分：編碼轉換、常用函數、主函式，細節部分程式碼中都有做註解。
- **編碼轉換**提供ASCII、binary與hex互轉。DES_main模塊支持64bits hex輸入64bits hex輸出，但DES算法需要基於binary，因此一開始會先把輸入的hex轉成binary，以便操作，輸出時再轉成hex。詳細可參考下圖：
<img src="https://i.imgur.com/5mPa1PT.png" alt="Cover" width="30%"/>

- **常用函數**包括代換函數、左移函數與XOR函數，代換函數用於各類表格轉換。

- **主函式**則主要執行DES核心算法，負責生成16個subkey與做16次迭代。

## 四、DES_mode詳解
DES_mode模塊分成兩主要部分，mode導向器與各種模式的函式。

## 五、UI_main詳解
UI_main主要生成與控制圖形介面，總共分成8個區塊，從frame1到frame8：
1. 檔案選擇
2. key輸入與隨機生成
3. 模式 與 加解密選擇
4. 預覽提示文字 與 開啟檔案夾按鈕 
5. 代處理文件預覽區
6. 執行按鈕
7. 預覽提示文字 與 開啟檔案夾按鈕
8. 已處裡文件預覽區

- 當執行按鈕被按下後，DES_go函式，此時會開啟子線程DES_main()讓DES算法執行，如此一來主UI線程就不會因為加解密操作需要時間而造成UI阻塞。

- 本模塊設有一個監聽器，監聽key輸入藍的狀態，若有文字輸入此欄位，程式會將輸入的

- 在DES算法開始後，會啟動wait_finish()，每個0.1秒會檢測一次output檔案的大小狀態，如果檢測到檔案大小沒有改變，代表output.txt不再有檔案寫入，即可判斷已經加密完成。加密完成後，輸出預覽會讀取output.txt並預覽出檔案中前1000個字元。

<img src="https://i.imgur.com/3liRCRK.png" alt="Cover" width="30%"/>

## 六、待解決問題
1. 部分特殊字元在轉碼(ascii to binary)過程中會不正常，經觀察後發現原因：一般的字元經過ascii to binary後會轉成8個位元，但特殊字元（例如『“』）會轉出14個位元，由於在最後轉回ASCII時是以8位切割，因此會出問題。目前遇到特殊字元時，強制取14位的前8位，導致在特殊字元的解碼上會出問題。
