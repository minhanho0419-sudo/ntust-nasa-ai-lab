# WO-M0-001

| 欄位 | 值 |
| --- | --- |
| TYPE | BOUNDED_WORK_ORDER |
| WORK_ITEM_ID | WO-M0-001 |
| TO | MAIN Own Worker (Codex) |
| STATUS | COMMAND_DISPATCHED |
| FROM | STUDENT-MAIN Brain |
| PROJECT | NTUST_SYNTHETIC_AGENT_LAB |
| MILESTONE | M0_GOVERNANCE |
| AUTHORIZATION | 學生正式批准建立 M0 治理文件、初始化 Git、Commit、建立公開 GitHub 儲存庫及 Push |
| RETURN_TO | STUDENT-MAIN Brain |
| WORKER 完成狀態 | READY_FOR_BRAIN_REVIEW，須有推送及遠端核對證據 |
| Brain 驗收 | PENDING |
| 下一階段 MAIN 授權 | PENDING |

## INPUT

學生派發的工單及實際確認的本機和 GitHub 狀態。本機專案根目錄為 `C:\Users\User\Desktop\20261123_AI\20261123_AI`。檢查時該目錄及上層沒有適用的既有 `AGENTS.md`，Git 回傳「not a git repository」（128）。

GitHub MCP 回傳登入帳號 `minhanho0419-sudo`。在該認證下查詢 `minhanho0419-sudo/ntust-nasa-ai-lab` 回傳 HTTP 404 `Not Found`，記作 BOOTSTRAP 查詢證據。指定目標為 `https://github.com/minhanho0419-sudo/ntust-nasa-ai-lab` 的 `main` 分支，公開狀態須於交付時讀回確認。

## EXPECTED_OUTPUT 與範圍

可寫範圍為根目錄的 `AGENTS.md`、`ROADMAP.md`、`WORK_ITEM.md`、`DECISIONS.md`，以及同步所需的本專案 Git 設定與指定 GitHub 儲存庫。所有其他檔案及原始資料唯讀。本次公開提交只含上述四份文件。

## 執行與驗收

1. 檢查本機根目錄、適用治理規範、Git 狀態、登入帳號及遠端。若遠端已有 `main` 上的 `AGENTS.md`，先讀取並記錄版本。首次建立保留 BOOTSTRAP 證據。
2. 初始化或沿用 `main`。保留學生修改與無關暫存內容，檢查文件及 staged diff。以 `chore(M0): initialize AI team governance and roadmap` Commit 四份治理文件。
3. 確認完整推送歷史僅公開授權內容，建立或沿用已確認的指定公開儲存庫，設定 `origin` 並執行 `git push -u origin main`。
4. Worker 從 GitHub 讀回公開狀態、`main` 完整 Commit ID 與四份文件，逐一比對本機。Brain 另行從 GitHub 讀取同一 Commit 的完整文件並驗收。
5. 完成回報提供關鍵命令 Exit Code、完整本機及遠端 Commit ID、Git 物件格式、原始 Commit 內容 SHA-256 與方法、儲存庫及 Commit 連結、四份文件連結、驗證結果與阻塞。每次回報附 M0 狀態、證據及驗收狀態、下一角色及派工狀態。Commit ID 與實際推送證據記於完成回報。

## 後續工單及 STOP_IF

每張後續工單須列 INPUT、EXPECTED_OUTPUT、可寫範圍、唯讀範圍、驗收、STOP_IF、RETURN_TO。真實阻塞經診斷仍無法在授權範圍內恢復，或必要操作涉及破壞性修改、未授權公開與越界時，停止並附實際錯誤與最小解決條件回報 BLOCKED。M0 推送及核對完成後，回報 READY_FOR_BRAIN_REVIEW 並停止，等候 STUDENT-MAIN Brain 驗收及下一階段授權。

## M2-FD001-PROFILE-001

- **TYPE／PROJECT／MILESTONE** BOUNDED_WORK_ORDER／NTUST_SYNTHETIC_AGENT_LAB／M2_FD001_SOURCE_AND_DATA_DEFINITION。
- **FROM／TO／RETURN_TO** STUDENT-RESEARCH／Research Own Worker (Codex)／STUDENT-RESEARCH。
- **授權與派發** 學生於 2026-11-23 將工單貼入 Worker 介面，轉為 COMMAND_DISPATCHED。依該工單，學生指示且 MAIN 授權直接啟動 M2，M1 為 DEFERRED、驗收未完成。M3 待 MAIN 另行授權。
- **治理基線** 從 origin 擷取的 main 為 `fb8ffc1ba186cd147d58a44c91ce77cb8261ef53`，已讀取完整 AGENTS.md，blob `dcba9f2e66cf648d2924718f1f2e245ade337dc1`，與 Brain 提供版本一致。
- **INPUT** 本地 `data/FD001` 的 train/test/RUL、來源論文及 NASA 官方參考資料。
- **EXPECTED_OUTPUT** 可重跑程式、來源對照、品質報告、資料字典與 M3 查詢契約、兩次執行及獨立核對證據。證據位置見 `reports/M2/research_verification.md`。
- **可寫範圍** `scripts/m2_fd001_profile.py`、`reports/M2/`、本次階段調整與進度所需的 ROADMAP.md、WORK_ITEM.md、DECISIONS.md。
- **唯讀與公開範圍** 原始資料、AGENTS.md、既有 M1 成果與其他未授權檔案唯讀。原始資料與 NASA 參考 ZIP 保留本地。公開提交限工單授權程式、衍生報告、驗證證據及治理更新。
- **驗收** 確認來源與欄位映射、輸入雜湊不變、Profile 可重跑、抽查一致、契約及 UNKNOWN 明確、GitHub main 已推送且可讀回。Worker 已完成本機兩次 Profile、來源位元組比對及獨立統計核對；推送與遠端證據載於 Worker Return。
- **STOP_IF** 無法定位或確認檔案、來源或必要映射，解析不可靠、輸入改變、核對不一致且無法修復、GitHub 無法存取或驗證，或必要操作越界時停止。
- **交付狀態** 推送及遠端核對完成後為 READY_FOR_BRAIN_REVIEW。Research 驗收為 PENDING_BRAIN_REVIEW，MAIN 最終驗收為 PENDING。
