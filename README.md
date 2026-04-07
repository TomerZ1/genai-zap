# GenAI-Zap — אוטומציית אונבורדינג לקוחות עסקיים

---

## חלק א׳ — גישה, חשיבה ועיצוב הפתרון

### הבנת האתגר

קיבלתי משימה לבנות אוטומציה לתהליך אונבורדינג של לקוח עסקי חדש בזאפ — ספציפית טכנאי מזגנים שרכש אתר אינטרנט ומיניסייט בדפי זהב.

הנחת המוצא שלי: הלקוח הגיע עם מינימום מידע (שם, טלפון, אזור), אך קיים מידע ציבורי נרחב עליו ברשת שיכול להפוך את שיחת האונבורדינג לאפקטיבית בהרבה. המטרה היא לחסוך למפיק בזאפ את עבודת המחקר הידנית ולספק לו כרטיס לקוח מוכן לפני השיחה.

---

### הנחות שהנחתי

- הלקוח **לא בהכרח** בעל אתר קיים — הוא רוכש אחד. לכן ה-URL הוא שדה אופציונלי (יכול להיות אתר ישן, מיניסייט קיים, או כלום).
- מספיק מידע זמין ברשת (דפי זהב, B144, פייסבוק, גוגל מפות) כדי לבנות פרופיל עסקי מבלי שהלקוח מספק אותו בעצמו.
- המפיק בזאפ זקוק למידע **מוכן לפעולה**, לא לדאמפ גולמי — לכן הפורמט מובנה ומודגשות נקודות פעולה.

---

### ארכיטקטורת הפתרון — למה pipeline ולא agent מלא?

הפתרון בנוי כ-**pipeline של שלושה שלבים** עוקבים:

```
קלט מהמשתמש → סריקת URL (אם קיים) → מחקר AI + חיפוש ברשת → כרטיס לקוח → תסריט אונבורדינג → CRM
```

**למה לא agent מלא עם לולאת חשיבה?**
Agent "אמיתי" מחליט בעצמו מה הצעד הבא בכל איטרציה. כאן הזרימה ידועה מראש — מחקר → כרטיס → תסריט — ולכן pipeline מובנה הוא הפתרון הנכון: פשוט יותר, צפוי יותר, קל יותר להסביר ולתחזק.

**אבל**: שלב המחקר **הוא** בעצם chain-of-thought סמוי — Claude מקבל כלי חיפוש ברשת ומחליט בעצמו כמה פעמים לחפש, במה לחפש, ואיך לשלב את התוצאות. זו חשיבה אגנטית, רק בתוך קריאת API אחת.

---

### החלטות עיצוב חכמות

**1. מודל כפול — Sonnet למחקר, Haiku לייצור**
שלב המחקר דורש יכולת חשיבה ושימוש בכלים — השתמשתי ב-`claude-sonnet-4-6`. שלבי הכרטיס והתסריט הם ייצור טקסט מובנה בלבד — השתמשתי ב-`claude-haiku-4-5-20251001`. כך מקסמתי איכות מול עלות.

**2. גילוי אוטומטי של אי-התאמות**
המערכת השוותה את מספר הטלפון שהלקוח סיפק לפני הרכישה מול המספרים שנמצאו ברשת. כשנמצאה אי-התאמה — זה הופיע כ"דגל אדום" בכרטיס הלקוח. זה בדיוק סוג המידע שמפיק לא ידע לחפש, אבל יכול לחסוך אי-הבנות בשיחה.

**3. שקיפות מקורות**
הכרטיס כולל סעיף "מקורות מידע" המפרט מה נמצא ומה לא — ב-B144, בגוגל, בפייסבוק וכו'. המפיק יודע בדיוק על מה מבוסס המידע ומה עדיין דורש אימות ידני.

**4. Scrape + AI במקביל**
אם סופק URL — המערכת סורקת אותו עם BeautifulSoup **וגם** נותנת ל-Claude לבקר בו עם כלי החיפוש. שתי נקיבות על אותו מקור, מה שמגדיל את כמות המידע הנחלץ.

**5. Fallback חכם**
אם החיפוש נכשל או לא מחזיר JSON תקין — המערכת בונה פרופיל מינימלי מהקלט הגולמי ומסמנת אותו לעדכון ידני. הפייפליין לא קורס.

---

### הפרונטאנד — למה?

הפרונטאנד הוא HTML פשוט, ללא פריימוורק. המטרה היחידה שלו היא להדגים את הפייפליין בצורה ויזואלית — הצגת הכרטיס והתסריט בממשק נקי, ב-RTL עברית, בצבעי זאפ. בפרויקט אמיתי זה יחליף ממשק ב-CRM הקיים.

---

### מה היה שונה בפרודקשן?

- **CRM אמיתי** — במקום `crm_log.json`, קריאת API ל-HubSpot / Salesforce
- **שליחת הודעה אוטומטית** — במקום הצגת התסריט בלבד, שליחה אוטומטית ב-WhatsApp Business API או SMS
- **גילוי אוטומטי של נכסים** — בהינתן רק מספר טלפון, מצא את כל הנכסים הדיגיטליים של הלקוח
- **תמיכה בסוגי עסקים נוספים** — כרגע מותאם לבעלי מקצוע, ניתן להרחיב לחנויות, מסעדות וכו׳
- **לוגינג ומוניטורינג** — במקום `print()`, מערכת לוגים מסודרת עם Sentry / CloudWatch

---

---

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
- **קישור** *(optional)* — Existing website or Dapei Zahav minisite URL

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
