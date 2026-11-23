# Roadmap

後續工作須待前項驗收與 MAIN 授權。M0 初始為 IN_PROGRESS，完成推送及遠端核對後轉為待 Brain 驗收（READY_FOR_BRAIN_REVIEW）。實際交付狀態由 Worker 回報證據確認。M1–M5 初始皆為 NOT_STARTED。

## M0 治理與同步

- **目標** 建立治理基線並同步 GitHub。
- **輸入** 學生授權與實際確認的既有專案狀態。
- **交付物** 四份治理文件與 GitHub 同步成果。
- **責任 Brain** MAIN Brain，由 MAIN Own Worker 執行。
- **驗收** MAIN Brain 從 GitHub 實際讀取指定 Commit 和四份文件完整內容，核對公開狀態、版本與工單。
- **STOP_IF** GitHub 存取或驗證失敗、出現無法安全解決的衝突，或推送會公開未授權內容。
- **下一角色** Research Brain，待 M0 驗收及 MAIN 授權。

## M1 六筆合成資料驗證

- **目標** 用合成資料驗證派工及可重現分析。
- **輸入** 本地 `synthetic_sensor.csv`。
- **交付物** Dataset Profile、原檔 SHA-256、可重跑程式及實際輸出。Profile 包含列欄數、欄名順序、型別、缺值規則與數量、重複列，以及各數值欄有效筆數、最小值、最大值與平均值。
- **責任 Brain** Research Brain。Research Own Worker → Research Brain → MAIN Brain。
- **驗收** 實際讀取並確認六筆資料，表頭另計。重跑後核對雜湊與 Profile。
- **STOP_IF** 檔案無法讀取、解析失敗或筆數不符，附實際證據回報。
- **下一角色** Research Brain。

## M2 FD001 來源與資料定義

- **目標** 確立 FD001 資料身分、欄位及分析定義。
- **輸入** 學生指定的本地 FD001 資料夾及可取得的來源說明。
- **交付物** 檔案清單、雜湊、來源紀錄、Dataset Profile、資料字典與健康分析定義。
- **責任 Brain** Research Brain。
- **驗收** 核對資料身分、欄位、Unit／Cycle／Sensor 映射及未知事項。
- **STOP_IF** 來源或欄位無法確認，停止並回報。
- **下一角色** Engineering Brain。

## M3 可追溯查詢

- **目標** 提供可追溯至原始資料的查詢。
- **輸入** M2 已驗收資料與定義。
- **交付物** 讀取與篩選程式、趨勢資料、來源定位及啟動方式。
- **責任 Brain** Engineering Brain。
- **驗收** 核對查詢值與原始資料一致，測試首末 Cycle、不同 Unit／Sensor 及無效輸入。
- **STOP_IF** 數值不符、來源定位遺失或轉換無法重現，停止並回報。
- **下一角色** Engineering Brain。

## M4 網站與 Evidence Prompt

- **目標** 讓使用者可在本地查看資料並複製可追溯證據。
- **輸入** M3 查詢功能與 M2 分析定義。
- **交付物** 本地可啟動網站、Engine Unit／Cycle／Sensor 選擇器、趨勢圖、當前值、來源顯示及 Prompt 複製。Prompt 包含資料集、檔案雜湊、選擇條件、趨勢區間、實際摘要、來源定位、轉換及限制。
- **責任 Brain** Engineering Brain 負責網站，Research Brain 審查分析文字。
- **驗收** Engineering Brain 實際操作並核對畫面及 Prompt，Research Brain 核對分析文字及其依據。
- **STOP_IF** 畫面與資料不同步、出現無來源數值或無依據故障結論，停止並回報。
- **下一角色** MAIN Brain 統籌驗收。

## M5 端到端交付

- **目標** 交付經完整重現及版本核對的網站。
- **輸入** 網站、資料、啟動說明與驗收案例。
- **交付物** 最終版本、驗收紀錄、操作說明、已知限制及 GitHub 版本連結。
- **責任 Brain** Research Brain 核對資料與 Prompt，Engineering Brain 修復問題，MAIN Brain 最終驗收。
- **驗收** 重現啟動、選擇、趨勢、來源及 Prompt 複製全流程。MAIN 核對 GitHub 交付版本與實際驗證版本一致。
- **STOP_IF** 核心流程失敗或版本無法確認，停止並回報。
- **下一角色** 學生接收成果。
