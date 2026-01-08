# 個人化生產力工具開發計畫

這是一個為個人使用而設計的生產力應用程式，結合了待辦事項、日曆和看板功能，旨在幫助您管理工作任務、客戶會議和每日行程。

## 1. 核心功能

*   **任務管理**:
    *   建立、編輯、刪除任務。
    *   任務應包含：標題、詳細說明、截止日期、完成狀態。
    *   可為任務設定分類，例如「工作」、「個人」或「會議」。

*   **看板視圖 (Kanban Board)**:
    *   以視覺化的方式呈現您的任務流程。
    *   看板分為三個主要欄位：「今天要做」、「本週要做」、「未來規劃」。
    *   任務卡片可以在欄位之間拖曳（進階功能），或根據截止日期自動歸類。

*   **日曆視圖 (Calendar View)**:
    *   以月曆或週曆的形式顯示所有有截止日期的任務和會議。
    *   可以快速查看每天的行程安排。

*   **客戶會議追蹤**:
    *   建立任務時，可選擇「會議」分類。
    *   為會議類型的任務額外增加「客戶名稱」和「開會地點」的欄位。

## 2. 專案架構與技術選型

專案將維持前後端分離的架構。

*   **後端**: Python Flask
    *   負責處理所有業務邏輯和資料庫操作。
    *   提供 RESTful API 給前端使用。
*   **前端**: Vue.js
    *   打造互動式的使用者介面，包含看板和日曆。
*   **資料庫**: SQLite
    *   一個輕量級的單一檔案資料庫，非常適合個人應用。

## 3. 資料庫模型 (Backend)

我們需要一個更詳細的 `Task` 模型來儲存所有資訊。

```python
# models.py
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    due_date = db.Column(db.DateTime, nullable=True)
    completed = db.Column(db.Boolean, default=False)
    category = db.Column(db.String(50), default='工作') # 例如: '工作', '會議', '個人'

    # 會議相關的額外欄位
    client_name = db.Column(db.String(100), nullable=True)
    location = db.Column(db.String(200), nullable=True)
```

## 4. API 設計 (Backend)

後端 API 需要擴充以支援新的查詢需求。

| 方法   | URL                | 描述                           |
|--------|--------------------|--------------------------------|
| `GET`  | `/api/tasks`       | 獲取所有任務                   |
| `POST` | `/api/tasks`       | 新增一個任務或會議             |
| `GET`  | `/api/tasks/<id>`  | 獲取單一任務的詳細資訊         |
| `PUT`  | `/api/tasks/<id>`  | 更新一個任務（包含標記為完成） |
| `DELETE`| `/api/tasks/<id>`| 刪除一個任務                   |
| `GET`  | `/api/tasks/board` | 獲取看板所需的所有任務（已分類） |
| `GET`  | `/api/tasks/calendar`| 獲取日曆所需的所有任務         |


## 5. 開發階段

### 階段一：後端基礎建設

1.  **環境與模型**: 設定好 Flask 環境，並根據上面的設計建立 `Task` 資料庫模型。
2.  **核心 API**: 實作針對任務 (Task) 的基本增、刪、改、查 (CRUD) API。
3.  **進階查詢 API**: 實作 `/api/tasks/board` 和 `/api/tasks/calendar` 的端點，這兩個端點需要後端幫忙處理日期的篩選和分類邏輯。
4.  **測試**: 使用工具 (如 Postman) 確保所有 API 都能正常運作。

### 階段二：前端開發 - 看板視圖

1.  **環境設定**: 建立 Vue 專案，安裝 `axios` 用於 API 請求。
2.  **主畫面**: 建立一個看板視圖 (`BoardView.vue`)。
3.  **API 串接**: 呼叫 `/api/tasks/board` API，獲取「今天」、「本週」、「未來」的任務列表。
4.  **元件開發**:
    *   `TaskCard.vue`: 用於顯示單一任務的卡片。
    *   `AddTaskForm.vue`: 用於新增任務的表單，需包含客戶會議所需的額外欄位。
5.  **互動功能**: 實作標記完成和刪除任務的功能。

### 階段三：前端開發 - 日曆視圖

1.  **路由設定**: 在 Vue 中新增一個 `/calendar` 路由。
2.  **日曆元件**: 引入一個現成的 Vue 日曆元件（例如 `v-calendar`），這樣可以節省開發時間。
3.  **API 串接**: 建立 `CalendarView.vue`，並呼叫 `/api/tasks/calendar` API 來獲取所有任務，然後將它們顯示在日曆上。
4.  **視圖切換**: 在 UI 中提供一個可以在「看板」和「日曆」視圖之間切換的導覽列或按鈕。

### 階段四：整合與優化

1.  **端對端測試**: 同時運行前後端，完整測試所有功能流程。
2.  **UI/UX 優化**: 調整樣式，讓應用程式更好看、更好用。
3.  **細節完善**: 例如，點擊日曆上的事件或看板上的卡片，可以彈出一個視窗來編輯任務詳情。