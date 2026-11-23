# FD001 來源與資料品質

查閱日期 2026-11-23（Asia/Taipei）。[NASA Open Data Portal — CMAPSS Jet Engine Simulated Data](https://data.nasa.gov/dataset/cmapss-jet-engine-simulated-data) 說明 FD001 是單一海平面工況、單一 HPC 退化模式的模擬資料。訓練與測試各有 100 條軌跡。訓練延續到模擬失效，測試在失效前截斷，另附測試末端 RUL 向量。[NASA NTRS — Damage Propagation Modeling for Aircraft Engine Prognostics](https://ntrs.nasa.gov/citations/20090029214) 說明模擬、退化及健康指標背景。感測器物理映射的採用界線見資料字典。

## 本機候選與官方比對

在 Git 專案根目錄內搜尋 FD001、C-MAPSS、README 與來源檔名後，找到唯一一組 `data/FD001`。實際目錄為 `C:\Users\User\Desktop\20261123_AI\20261123_AI\data\FD001`。表內每個檔名皆相對於此目錄。

| 檔名 | 位元組 | 本機 SHA-256 | 與 NASA ZIP 同名項目 |
| --- | ---: | --- | --- |
| train_FD001.txt | 3515356 | `963b5e22825b34d8b21c69e1aeb4af3e647050eb672ee8834ba4b5d91d2de0f8` | 位元組一致 |
| test_FD001.txt | 2228855 | `3cda7109ce17bafb5443f2ac926cfcf88154b941b8c4cf95eb55d1ddd6f52851` | 位元組一致 |
| RUL_FD001.txt | 429 | `a19c8ec94931949d0485bdc35118206e9c81c4547b422efb9cf86f4ceddbceca` | 位元組一致 |
| Damage Propagation Modeling.pdf | 434158 | `e7aaef80c177333f400a4c1099fe76e67d244569b9397c937ec4cd3ed5b44a27` | 位元組一致，來源文件 |

官方參考下載命令為 `curl.exe -fsSL --max-time 40 https://data.nasa.gov/docs/legacy/CMAPSSData.zip -o reports/M2/nasa-reference.zip`，退出碼 0。驗證程式用 Python `zipfile` 讀取 ZIP 內部項目、逐位元組比對並計算 SHA-256。官方封存及 README 的完整雜湊與實際結果見執行證據。NASA ZIP 內的 `readme.txt` 以嚴格 ASCII 解碼時遇到 0x96（退出碼 1），改以 Windows-1252 解碼成功（0）。資料檔仍使用嚴格 ASCII。ZIP 僅供本地核對。

確認程度分三層。**名稱**為上述本機檔名與官方 ZIP 同名。**結構**為 train/test 皆 26 欄、各 100 個 Unit，RUL 為 100 筆單欄整數且可按 test Unit 對齊。**內容**為四檔逐位元組相等，確認本機輸入與此次下載的 NASA 參考檔一致。

## Dataset Profile

| 檔案 | 資料列 × 欄位 | Unit | 缺值 | 重複列 | 重複 Unit/Cycle | 逆序 | Cycle 缺口 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| train | 20,631 × 26 | 100 | 0 | 0 | 0 | 0 | 0 |
| test | 13,096 × 26 | 100 | 0 | 0 | 0 | 0 | 0 |
| RUL | 100 × 1 | 不適用 | 0 | 29 | 不適用 | 不適用 | 不適用 |

兩個軌跡檔的全檔常數 Sensor 相同，為 01、05、10、16、18、19。各 Unit 的列數、Cycle 端點、缺口和常數 Sensor，以及逐欄有效筆數、排除、最小值、最大值、平均值均在 [Dataset Profile](dataset_profile.json)。RUL 的 29 筆整列重複計數是相同壽命值的後續出現，全部保留。

三個數據檔均以嚴格 ASCII 解碼，依實體換行分列、以連續空白切分並忽略行首尾空白，無表頭。每列驗證欄位寬度及有限十進位數字格式。Unit/Cycle 為正整數，RUL 為非負整數。變寬空白屬分隔符，無欄位缺值標記。缺欄、多欄、無效字串或非有限值會使該次執行失敗，回報異常數及前 20 個行號。空白行記錄行號後略過。此次三檔均有 0 空白行、0 解析異常、0 非有限值、0 排除列。重複列以切分後、轉成型別前的字串序列比較，每組扣除首次出現。統計保留重複資料。

使用 Decimal 轉換，80 位十進位精度覆蓋這批輸入的加總；平均另記精確分數與 40 位有效數字顯示值。常數判定採精確數值相等，無容差。Unit/Cycle 逆序為相鄰有效列的鍵下降；同鍵重複另計。缺口按各 Unit 的 1 至最大觀測 Cycle 計算。RUL 無 Unit、Cycle 或 Sensor 欄。
