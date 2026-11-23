# 專案治理

NTUST_SYNTHETIC_AGENT_LAB 的最終交付是本地 NASA C-MAPSS FD001 健康分析網站。使用者可選 Engine Unit、Cycle、Sensor，查看原始資料來源、數值與趨勢，並產生可追溯的 Evidence Prompt。M1 先用本地 `synthetic_sensor.csv` 練習派工，預期六筆資料（表頭另計），實際內容與筆數須執行確認。

## 權責與回報

- 學生擁有最終決策與授權權限。
- MAIN Brain 負責 Roadmap、跨 Brain 協調與最終驗收。MAIN Own Worker 執行 MAIN 工單授權的治理與整合。
- Research Brain 負責資料來源、Dataset Profile、分析定義及驗收 Research Own Worker 成果。
- Engineering Brain 負責資料查詢程式、網站及驗收 Engineering Own Worker 成果。
- 各 Brain 的本地 Own Worker 可使用 Codex 或 Claude。Worker 先回報所屬 Brain，由該 Brain 驗收後回報 MAIN。MAIN 透過 Research Brain 與 Engineering Brain 協調各自工作。

## 工單與證據

每張工單必須明列 INPUT、EXPECTED_OUTPUT、可寫範圍、唯讀範圍、驗收、STOP_IF、RETURN_TO。原始資料與未授權檔案唯讀。資料衍生處理須保留來源定位及可重現的轉換紀錄。檔案讀取、執行、推送及完成聲明都須有實際證據。遇到無法恢復的阻塞、必要操作超出授權或可能公開未授權內容時，依 STOP_IF 停止並附證據回報。

## Git 治理

1. 每次派工前，Brain 必須實際讀取 GitHub `main` 最新的 `AGENTS.md`，並要求 Own Worker 遵守。
2. 首次建立若遠端或該檔案尚不存在，須用實際查詢證據記錄 BOOTSTRAP，依學生已批准的 WO-M0-001 建立。認證、權限及連線失敗須與不存在區分。
3. 專案採單一 `main` 分支、循序開發。Worker 完成後必須 Commit 並 Push 到 GitHub `main`。推送前須檢查將公開的完整歷史及授權範圍。
4. Brain 必須從 GitHub 實際讀取並審查結果，確認符合工單才能回報 PASS。Brain 須記錄所讀取的完整 Commit ID，並以該版本核對 `AGENTS.md`、`ROADMAP.md`、`WORK_ITEM.md`、`DECISIONS.md` 的完整內容。
5. 前一項工作取得 Brain 驗收及 MAIN 授權後，下一個 Worker 才可開始。
6. GitHub 無法存取或無法完成驗證時，回報 BLOCKED 並附實際證據。Worker 完成推送與核對後回報 READY_FOR_BRAIN_REVIEW，由 STUDENT-MAIN Brain 獨立完成 M0 驗收。
7. WO-M0-001 執行至 M0 交付為止。
