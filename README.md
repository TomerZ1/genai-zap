<div dir="rtl">
הסבר בעברית (הוראות הרצה באנגלית למטה):

- ## הבנת האתגר:

  קיבלתי משימה לבנות אוטומציה לתהליך אונבורדינג של לקוח עסקי חדש בזאפ (ספציפית טכנאי מזגנים מהקריות שרכש אתר אינטרנט ומיניסייט בדפי זהב). הנחת המוצא שלי היא שהלקוח מגיע לזאפ עם מינימום מידע (שם, טלפון, אזור) אך יכול להיות שיש עליו מידע ציבורי ברשת שיכול להפוך את שיחת האונבורדינג לאפקטיבית בהרבה. המטרה שלי היא לחסוך לעובד בזאפ את עבודת המחקר הידנית ולספק לו כרטיס לקוח מוכן לפני השיחה.

- ## הנחות שהנחתי:
  - הלקוח לא בהכרח בעל אתר קיים שכן הוא רוכש אחד. לכן ה- URL הוא שדה אופציונלי (יכול להיות שיש לו אתר ישן, מיניסייט קיים).
  - לא בהכרח יש מספיק מידע ברשת (דפי זהב, B144, פייסבוק, גוגל מפות) כדי לבנות פרופיל עסקי מבלי שהלקוח מספק אותו בעצמו (הסבר על טיפול במקרה קצה זה בהמשך).
  - העובד בזאפ זקוק למידע **מוכן לפעולה** ולא לסתם טקסט ולכן הפורמט מובנה ומודגשות נקודות פעולה וטמפלייטים מוכנים.

- ## ארכיטקטורת פתרון (Pipeline ולא Agent מלא):

  הפתרון בנוי כ- pipeline באופן הבא:

  ```
  קלט מהמשתמש (שם, טלפון, אזור, URL אופציונלי)
          ↓
  סריקה של האתר (אם סופק) בעזרת BeautifulSoup
          ↓
  מחקר ברשת על העסק באמצעות AI (Claude)
          ↓
  יצירת כרטיס לקוח בעברית (לעובד זאפ)
          ↓
  יצירת תסריט אונבורדינג בעברית (ללקוח)
          ↓
  שמירה ב- CRM + קובץ markdown
  ```

  - למה לא agent מלא עם chain of thought? סוכן ״אמיתי״ מחליט בעצמו מה הצעד הבא בכל איטרציה. כאן הזרימה היא קבועה וידועה מראש (מחקר, כרטיס לקוח, אונבורדינג) ולכן pipeline מובנה הוא הפתרון המתאים: פשוט יותר, צפוי יותר, קל להסבר ותחזוקה וחשוב מאוד- **זול יותר**. כן אציין ששלב המחקר ברשת הוא סוג של chain of thought סמוי, שכן Claude מקבל כלי חיפוש ברשת ומחליט בעצמו כמה לחפש, איפה ואיך לשלב את התוצאה על ידי ״חשיבה״. אנחנו בעצם ״נהנים״ כאן משני העולמות כאשר אנחנו מקבלים צורת חשיבה וכוח של Agent בקריאת API חסכונית אחת.

- ## החלטות עיצוב:
  - **מודל כפול:** Sonnet למחקר, Haiku לייצור. שלב המחקר דורש יכולת חשיבה ושימוש בכלי חיפוש ולכן השתמשתי ב-claude-sonnet-4-6. שלבי הכרטיס והתסריט הם ייצור טקסט מובנה בלבד - השתמשתי ב-claude-haiku-4-5-20251001. כך מקסמתי איכות מול עלות.

  - **גילוי אוטומטי של אי-התאמות:** המערכת השוותה את מספר הטלפון שהלקוח סיפק לפני הרכישה מול המספרים שנמצאו ברשת. כשנמצאה אי-התאמה - זה הופיע כ"דגל אדום" בכרטיס הלקוח. זוהי דוגמה למידע שעובד זאפ יכול לא לשים לב בחיפוש ידני, אבל יכול לחסוך אי הבנות בשיחה.

  - **שקיפות מקורות:** הכרטיס כולל סעיף "מקורות מידע" המפרט מה נמצא ומה לא (ב-B144, בגוגל, בפייסבוק וכו׳). העובד בזאפ יודע בדיוק על מה מבוסס המידע ומה עדיין דורש אימות ידני.

  - **חיפוש כפול (Scrape + AI במקביל אם סופק URL):** המערכת סורקת אותו עם BeautifulSoup וגם נותנת ל-Claude לבקר בו עם כלי החיפוש, מה שמגדיל את כמות המידע שהמערכת מוצאת.

  - **מקרה קצה של Fallback חכם:** אם החיפוש נכשל או לא מחזיר שום דבר, המערכת בונה פרופיל מינימלי מהקלט שניתן ומסמנת שצריך לעדכן מידע ידנית. הפחיפליין לא קורס.

- ## Frontend:

  הפרונטאנד הוא HTML פשוט, ללא פריימוורק. המטרה היחידה שלו היא להדגים את הפייפליין בצורה ויזואלית הצגת הכרטיס והתסריט בממשק נקי בעברית. בפרויקט אמיתי זה יוחלף ב- CRM וה- JSON הנשמר יכתב לשם.

- ## מה יהיה שונה בפרודקשן:
  - **CRM אמיתי** - במקום `crm_log.json`, קריאת API ל-HubSpot / Salesforce
  - **שליחת הודעה אוטומטית** - במקום הצגת התסריט בלבד, שליחה אוטומטית ב-WhatsApp Business API או SMS
  - **גילוי אוטומטי של נכסים** - בהינתן רק מספר טלפון, מצא את כל הנכסים הדיגיטליים של הלקוח

- ## דוגמת הרצה:

  למען פשטות ההסבר, אציג דוגמת הרצה באמצעות ממשק Frontend שיצרתי באמצעות קלוד-קוד כדי להנגיש את הכלי.
  1. תחת ההנחה שלאחר הרכישה של בעל העסק יש לזאפ את הפרטים הבסיסיים שלו (וגם אולי אתר ישן) נמלא אותם בטופס. לשם הדוגמה השתמשתי בעסק מיזוג אוויר שמצאתי בגוגל.

  ![pic 1](assets/pic%201.png)

  ![pic 2](assets/pic%202.png) 2. לאחר הפעלת הכלי, יתבצע מחקר באינטרנט אודות בית העסק. אם הייתי ממלא גם קישור לאתר ישן, הייתה מתבצעת סריקה של האתר **ללא** כלי AI (Scraping) והתוצאות היו עוברות לכלי המחקר (ה- AI) בתור context. הסריקה הראשונית יעילה באמצעות ספריית BeautifulSoup שסורקת את קוד המקור של האתר, מנקה את הדאטה ומחזירה פלט מסודר. השימוש ב- AI בשלב הסריקה הראשונית מיותר בגלל ש- BeautifulSoup הוא כלי מוכח וחינמי. 3. הכלי פונה דרך API KEY לקלוד עם פרומפטים מוכנים מראש (ניתן למצוא אותם בתיקיה המתאימה) שמגדירים לו איך לחקור את הרשת, מה לחפש ואיך לבנות כרטיס לקוח + תסריט שיחה + JSON מתאים ל- CRM. על מנת לאזן בין יעילות למחיר, בחרתי להשתמש ב- Claude Sonnet 4.6 לחיפוש ברשת (שכן לאחר בדיקה המודלים החלשים יותר לא נותנים תוצאות מספקות), וב- Claude Haiku 4.5 לכתיבת הטקסט שכן זו משימה די פשוטה למודל שפה ואין צורך לשלם פי כמה על מודל חזק יותר. אציין שכתיבת הפרומפטים ודיוקם הייתה באמצעות Claude ושם יש טמפלייטים מפורטים של הפלט המצופה, ודגשים חשובים שיחסכו לעובדי זאפ עבודה (למשל, בדוגמה למטה ניתן לראות כי בעת מחקר ברשת התגלו בשני מקומות שונים מספרי טלפון שונים, ולכן יש דגש על בדיקה של העניין מול הלקוח).

  ![pic 3](assets/pic%203.png)

  ![pic 4](assets/pic%204.png)

  ![pic 5](assets/pic%205.png)

  ![pic 6](assets/pic%206.png)

  המידע יישמר למערכת CRM וכאן מוצג לדוגמה JSON עבור הכרטיס הנ״ל:

  ![pic 7](assets/pic%207.png)

</div>

<div>
## Part B — Setup & Run Guide

### Prerequisites

- Python 3.10+
- An [Anthropic API key](https://console.anthropic.com/)

---

### Installation

```bash
# Clone the repo
git clone https://github.com/TomerZ1/genai-zap.git
cd genai-zap

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

### Environment Setup

Create a `.env` file in the project root (use `.env.example` as a reference):

```bash
cp .env.example .env
```

Then open `.env` and add your Anthropic API key:

```
ANTHROPIC_API_KEY=your_api_key_here
```

---

### Running the App

**1. Start the backend:**

```bash
uvicorn backend.main:app --reload
```

**2. Serve the frontend** (in a separate terminal):

```bash
cd frontend
python3 -m http.server 3000
```

**3. Open the UI:**  
Go to [http://localhost:3000](http://localhost:3000) in your browser.

---

### Usage

Fill in the client form:

- **שם העסק** — Business name
- **שם בעל העסק** — Owner name
- **טלפון** — Phone number
- **אזור פעילות** — Service area
- **קישור** _(optional)_ — Existing website or Dapei Zahav minisite URL

Click **הפעל אונבורדינג** and wait ~30 seconds for the AI to research and generate the outputs.

---

### Output

Each run produces:

- A **client card** (Hebrew) displayed in the UI — for the Zap account manager
- An **onboarding script** (Hebrew) displayed in the UI — ready to send to the client
- A timestamped **markdown file** saved to `/outputs`
- A record appended to **`crm_log.json`** (simulated CRM log)

---

### Project Structure

```
genai-zap/
├── backend/
│   ├── main.py           # FastAPI app + pipeline orchestration
│   ├── scraper.py        # URL scraping with BeautifulSoup
│   ├── claude_client.py  # All Claude API calls
│   ├── crm.py            # CRM logging to JSON
│   └── prompts/
│       ├── research.md   # Prompt: web research phase
│       ├── client_card.md  # Prompt: Hebrew client card
│       └── onboarding.md   # Prompt: Hebrew onboarding message
├── frontend/
│   └── index.html        # Single-page UI
├── outputs/              # Generated markdown files (gitignored)
├── .env.example          # Environment variable template
└── requirements.txt      # Python dependencies
```

<div/>
