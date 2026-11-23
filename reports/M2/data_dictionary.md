# FD001 資料字典與 M3 資料契約

資料來源及版本辨識見 [來源與資料品質](source_and_profile.md)。NASA 入口與 ZIP README 都定義 26 個數字欄位，依序為 Unit、Cycle、三項設定與感測器。兩份說明末欄的感測器編號寫成 26，與位置 6 = Sensor 1、位置 7 = Sensor 2 及總欄數矛盾。經比對官方檔案的 26 欄結構，本契約採 `sensor_index = position - 5`，因此最後一欄是位置 26、Sensor 21。證據支持位置映射；目前無可核對的逐位置物理名稱與單位對照，故標記 UNKNOWN。

| 位置（1 起） | 識別名 | 型別 | 語意／依據 | 單位 |
| ---: | --- | --- | --- | --- |
| 1 | unit | 正整數 | 檔內引擎編號，NASA 入口及 ZIP README | 識別碼 |
| 2 | cycle | 正整數 | 引擎運行週期索引，NASA 入口及 ZIP README | Cycle |
| 3 | setting_1 | 有限十進位 | 操作設定 1，NASA 入口及 ZIP README。物理名稱 UNKNOWN | UNKNOWN |
| 4 | setting_2 | 有限十進位 | 操作設定 2，NASA 入口及 ZIP README。物理名稱 UNKNOWN | UNKNOWN |
| 5 | setting_3 | 有限十進位 | 操作設定 3，NASA 入口及 ZIP README。物理名稱 UNKNOWN | UNKNOWN |
| 6 | sensor_01 | 有限十進位 | 第 1 個感測器位置，見位置規則。物理名稱 UNKNOWN | UNKNOWN |
| 7 | sensor_02 | 有限十進位 | 第 2 個感測器位置，見位置規則。物理名稱 UNKNOWN | UNKNOWN |
| 8 | sensor_03 | 有限十進位 | 第 3 個感測器位置，見位置規則。物理名稱 UNKNOWN | UNKNOWN |
| 9 | sensor_04 | 有限十進位 | 第 4 個感測器位置，見位置規則。物理名稱 UNKNOWN | UNKNOWN |
| 10 | sensor_05 | 有限十進位 | 第 5 個感測器位置，見位置規則。物理名稱 UNKNOWN | UNKNOWN |
| 11 | sensor_06 | 有限十進位 | 第 6 個感測器位置，見位置規則。物理名稱 UNKNOWN | UNKNOWN |
| 12 | sensor_07 | 有限十進位 | 第 7 個感測器位置，見位置規則。物理名稱 UNKNOWN | UNKNOWN |
| 13 | sensor_08 | 有限十進位 | 第 8 個感測器位置，見位置規則。物理名稱 UNKNOWN | UNKNOWN |
| 14 | sensor_09 | 有限十進位 | 第 9 個感測器位置，見位置規則。物理名稱 UNKNOWN | UNKNOWN |
| 15 | sensor_10 | 有限十進位 | 第 10 個感測器位置，見位置規則。物理名稱 UNKNOWN | UNKNOWN |
| 16 | sensor_11 | 有限十進位 | 第 11 個感測器位置，見位置規則。物理名稱 UNKNOWN | UNKNOWN |
| 17 | sensor_12 | 有限十進位 | 第 12 個感測器位置，見位置規則。物理名稱 UNKNOWN | UNKNOWN |
| 18 | sensor_13 | 有限十進位 | 第 13 個感測器位置，見位置規則。物理名稱 UNKNOWN | UNKNOWN |
| 19 | sensor_14 | 有限十進位 | 第 14 個感測器位置，見位置規則。物理名稱 UNKNOWN | UNKNOWN |
| 20 | sensor_15 | 有限十進位 | 第 15 個感測器位置，見位置規則。物理名稱 UNKNOWN | UNKNOWN |
| 21 | sensor_16 | 有限十進位 | 第 16 個感測器位置，見位置規則。物理名稱 UNKNOWN | UNKNOWN |
| 22 | sensor_17 | 有限十進位 | 第 17 個感測器位置，見位置規則。物理名稱 UNKNOWN | UNKNOWN |
| 23 | sensor_18 | 有限十進位 | 第 18 個感測器位置，見位置規則。物理名稱 UNKNOWN | UNKNOWN |
| 24 | sensor_19 | 有限十進位 | 第 19 個感測器位置，見位置規則。物理名稱 UNKNOWN | UNKNOWN |
| 25 | sensor_20 | 有限十進位 | 第 20 個感測器位置，見位置規則。物理名稱 UNKNOWN | UNKNOWN |
| 26 | sensor_21 | 有限十進位 | 第 21 個感測器位置，見位置規則。物理名稱 UNKNOWN | UNKNOWN |

`RUL_FD001.txt` 的位置 1 為非負整數 `endpoint_rul`，單位 Cycle，代表 test Unit 最後觀測 Cycle 之後到模擬失效的剩餘週期。此向量沒有顯式 Unit 欄。本契約採官方向量行序對齊 test Unit 1–100，並驗證兩者數量與連續 ID。此對齊依資料排列及官方向量用途推定，逐列無獨立 Unit 標籤。

## 資料選擇與查詢

- 先選 FD001 train 或 test，再選 Unit、Cycle、Sensor。資料分組鍵為 `(dataset, split, unit)`；觀測鍵再加 Cycle。同號 train/test Unit 各自獨立。RUL 是 test 標籤，不是觀測序列。PDF 僅為來源文件。
- 以所選檔案實際存在的 Unit 和指定 Unit 已觀測的 Cycle 為選項，皆數字升冪；Sensor 按位置 1–21 升冪。切換 split 或 Unit 後重新驗證選項。非法或不存在的組合回傳無對應資料，禁止替補或插值。
- 趨勢預設顯示該 Unit 首末觀測 Cycle 的閉區間。指定視窗使用實際存在的上下界、包含兩端，按 Cycle 升冪，只畫已觀測點，缺口不跨線補值。所選 Cycle 加標記。若指定區間未含所選 Cycle，要求修正區間或選擇。
- 當前值與趨勢點應可重現原始欄位字串與其解析數值。摘要可用指定區間內觀測點的筆數、最小值、最大值與算術平均，明列區間、分母、排除與顯示精度，標示為衍生值。
- 每個觀測點來源需保存資料集、split、檔案相對路徑、原始位元組 SHA-256、原始實體行號（1 起）、原始欄位位置（1 起）、Unit、Cycle。RUL 若呈現則另列其來源檔行號與欄位位置，以及對齊的 test Unit 與末端 Cycle。

## 健康分析與 RUL

本階段以原始感測器趨勢和描述性摘要作為健康分析。感測器變化或常數性不足以單獨確定故障起點、健康分數或即時 RUL。NASA 論文的模擬健康指標涉及運行裕度，公開觀測欄位的逐位置物理映射及完整裕度未經核證，因此本契約未定義健康分數。

如後續授權使用回顧性 RUL 標籤，train 的 `RUL(c) = max_observed_cycle - c`，以 NASA 說明訓練軌跡到模擬失效為依據；末端為 0，需完整未來軌跡。test 的 `RUL(c) = endpoint_rul[unit] + max_observed_cycle - c`，以官方向量和觀測終點反推先前標籤；它使用測試終點與真值，僅供事後驗證，不用於即時推論或未來未知資料。向量與軌跡須依上述對齊方法及來源定位同時留存。

## Evidence Prompt 欄位

資料集與官方來源、split、檔案相對路徑與 SHA-256、Unit/Cycle/Sensor 選擇與欄位置、閉區間、觀測原始值、摘要與計算規則、各點與標籤來源定位、轉換及精度、物理名稱及單位的 UNKNOWN、模擬資料與回顧性標籤限制。
