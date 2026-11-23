# M2 Research 驗收證據

Research 驗收維持 **PENDING_BRAIN_REVIEW**，MAIN 最終驗收 **PENDING**。

在專案根目錄使用 Python 3.15.2 或相容版本，保有原始 `data/FD001` 三個數據檔及 PDF，並將 NASA 參考 ZIP 下載至本地 `reports/M2/nasa-reference.zip`。在終端執行：

```powershell
python scripts/m2_fd001_profile.py --data-dir data/FD001 --output reports/M2/dataset_profile.json
python reports/M2/verify_profile.py data/FD001 reports/M2/dataset_profile.json reports/M2/nasa-reference.zip
```

獨立驗證以 bytes 讀取與 regex 切分欄位，使用 Fraction 與 statistics.mean 比對 Profile 的精確分數。驗證涵蓋尺寸、欄位置、空白行、缺值、重複、所有欄位摘要、Unit/Cycle 唯一性、順序、缺口、每個 Unit 的範圍與常數欄。train/test 各抽查 Unit 1、51、100 的首末 Cycle，涵蓋 Sensor 2、9、21，核對 Cycle 端點及以實體行號和欄位置重讀的原始值。命令、時間、退出碼、完整 stdout/stderr、樣本及前後雜湊見 [執行證據](execution_evidence.json)。

Research Brain 需要本機原始檔重算統計、前後雜湊及抽樣資料；需 NASA 參考 ZIP 獨立核對來源位元組。請從 GitHub 固定交付 Commit 讀回治理文件及報告，核對來源、資料契約、UNKNOWN 與公開提交範圍。

## 公開交付清單

- `scripts/m2_fd001_profile.py`
- `reports/M2/dataset_profile.json`
- `reports/M2/source_and_profile.md`
- `reports/M2/data_dictionary.md`
- `reports/M2/execution_evidence.json`
- `reports/M2/verify_profile.py`
- `reports/M2/research_verification.md`
- `ROADMAP.md`、`WORK_ITEM.md`、`DECISIONS.md`

Git 提交及推送後證據由 Worker Return 提供。原始檔與參考 ZIP 留在本地。
