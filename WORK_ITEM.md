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
