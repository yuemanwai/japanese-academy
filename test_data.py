"""
Seed test data into database.
This script only inserts data, does NOT create tables.
Tables should be created by check_db.py first.
"""
from app import db, app
from app.models import User, Post, Level, Lesson, ChatSettings

app_context = app.app_context()
app_context.push()

print("🌱 Seeding database with initial data...")

# Mock Admin account
admin = User.query.filter_by(username='admin').first()
if not admin:
    admin = User(username='admin', email='admin@example.com', is_admin=True)
    admin.set_password("admin")
    db.session.add(admin)
    db.session.commit()
    print("✅ Admin user created")
else:
    print("ℹ️  Admin user already exists")

# Mock users Account
users_data = [
    ('u1', 'u1@example.com', '1'),
    ('u2', 'u2@example.com', '2'),
    ('u3', 'u3@example.com', '3'),
    ('alice', 'alice@example.com', '4'),
    ('bob', 'bob@example.com', '5'),
    ('charlie', 'charlie@example.com', '6'),
    ('david', 'david@example.com', '7'),
    ('eve', 'eve@example.com', '8'),
    ('frank', 'frank@example.com', '9'),
    ('grace', 'grace@example.com', '10'),
]

created_users = []
for username, email, password in users_data:
    user = User.query.filter_by(username=username).first()
    if not user:
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        created_users.append(user)

if created_users:
    db.session.commit()
    print(f"✅ Created {len(created_users)} users")
else:
    print("ℹ️  Users already exist")

# Get users for later use (whether newly created or existing)
u1 = User.query.filter_by(username='u1').first()
u2 = User.query.filter_by(username='u2').first()
u3 = User.query.filter_by(username='u3').first()
u4 = User.query.filter_by(username='alice').first()
u5 = User.query.filter_by(username='bob').first()
u6 = User.query.filter_by(username='charlie').first()
u7 = User.query.filter_by(username='david').first()
u8 = User.query.filter_by(username='eve').first()
u9 = User.query.filter_by(username='frank').first()
u10 = User.query.filter_by(username='grace').first()

# Mock levels
levels_data = [
    ('Beginner', 'l1'),
    ('Intermediate', 'l2'),
    ('Advanced', 'l3')
]

level_objects = {}
for level_name, var_name in levels_data:
    level = Level.query.filter_by(name=level_name).first()
    if not level:
        level = Level(name=level_name)
        db.session.add(level)
        db.session.flush()  # Get the ID without committing
    level_objects[var_name] = level

if any(level.id is None for level in level_objects.values()):
    db.session.commit()
    print("✅ Created levels")
else:
    print("ℹ️  Levels already exist")

l1 = level_objects['l1']
l2 = level_objects['l2']
l3 = level_objects['l3']

# Mock posts
posts_data = [
    ('My first post', 'This is the body of my first post', 'u1'),
    ('A day in the life', 'Today I went to the park and had a great time.', 'u2'),
    ('Learning Python', 'Python is a versatile programming language.', 'u3'),
    ('Traveling to Japan', 'Japan is a beautiful country with rich culture.', 'alice'),
    ('My favorite recipes', 'I love cooking and trying out new recipes.', 'bob'),
    ('Fitness journey', 'Staying fit and healthy is important.', 'charlie'),
    ('Book recommendations', 'Here are some books I recommend reading.', 'david'),
    ('Photography tips', 'Photography is a great hobby to capture moments.', 'eve'),
    ('Gardening 101', 'Gardening is a relaxing and rewarding activity.', 'frank'),
    ('Tech trends', 'Keeping up with the latest in technology.', 'grace'),
    ('Music I love', 'Sharing my favorite music tracks.', 'u1'),
    ('Movie reviews', 'My thoughts on the latest movies.', 'u2'),
    ('DIY projects', 'Do-it-yourself projects are fun and creative.', 'u3'),
    ('Mindfulness and meditation', 'Practicing mindfulness for a better life.', 'alice'),
    ('Career advice', 'Tips and advice for advancing your career.', 'bob'),
    ('Learning new languages', 'The benefits of learning new languages.', 'charlie'),
    ('Home decor ideas', 'Ideas to decorate your home beautifully.', 'david'),
    ('Pet care tips', 'Taking care of your pets.', 'eve'),
    ('Outdoor adventures', 'Exploring the great outdoors.', 'frank'),
    ('Healthy eating', 'Tips for maintaining a healthy diet.', 'grace'),
    ('Personal finance', 'Managing your personal finances effectively.', 'u1'),
    ('Hiking trails', 'Best hiking trails to explore.', 'u2'),
    ('Yoga for beginners', 'Starting your yoga journey.', 'u3'),
]

# Only create posts if none exist
if Post.query.count() == 0:
    for title, body, username in posts_data:
        user = User.query.filter_by(username=username).first()
        if user:
            post = Post(title=title, body=body, user_id=user.id)
            db.session.add(post)
    db.session.commit()
    print(f"✅ Created {len(posts_data)} posts")
else:
    print("ℹ️  Posts already exist")

# Mock lessons
lessons = [
    {"name": "平假名、片假名的學習和練習", "level_id": l1.id, "description": "學習如何讀寫平假名和片假名，打好日語基礎。"},
    {"name": "發音練習：母音、清音、濁音、拗音、促音、長音", "level_id": l1.id, "description": "練習正確的日語發音，提升聽說能力。"},
    {"name": "基本句型結構 (SOV)", "level_id": l1.id, "description": "掌握日語的基本句型結構，學會組織簡單句子。"},
    {"name": "基本詞彙 (挨拶、物品名稱、數字等)", "level_id": l1.id, "description": "擴展基本詞彙量，學會常用的問候語和物品名稱。"},
    {"name": "助詞的使用 (が、を、は、に、へ、で、の)", "level_id": l1.id, "description": "理解並正確使用日語中的常用助詞。"},
    {"name": "基本問候語", "level_id": l1.id, "description": "學習日常生活中的基本問候語，提升交流能力。"},
    {"name": "自我介紹", "level_id": l1.id, "description": "學會用日語進行自我介紹，增強自信心。"},
    {"name": "日常對話練習 (購物、餐飲、問路)", "level_id": l2.id, "description": "練習在日常生活中的對話，如購物、餐飲和問路。"},
    {"name": "五段動詞、一段動詞、不規則動詞", "level_id": l2.id, "description": "學習並掌握日語中的各類動詞變化。"},
    {"name": "動詞變化 (ます形、て形、ない形等)", "level_id": l2.id, "description": "深入了解動詞的各種變化形式，提升語法知識。"},
    {"name": "時態 (過去形、否定形等)", "level_id": l2.id, "description": "學習日語中的各種時態，能夠描述不同時間的動作。"},
    {"name": "基礎漢字的介紹與練習", "level_id": l2.id, "description": "認識並練習基礎漢字，提升閱讀和書寫能力。"},
    {"name": "常用漢字的寫法與讀法", "level_id": l2.id, "description": "學習常用漢字的正確寫法和讀法，增強漢字知識。"},
    {"name": "漢字的組詞與運用", "level_id": l2.id, "description": "學會組合漢字並在日常交流中運用。"},
    {"name": "簡單的短文和對話", "level_id": l2.id, "description": "閱讀和理解簡單的短文和對話，提升閱讀能力。"},
    {"name": "理解與翻譯練習", "level_id": l2.id, "description": "練習翻譯日語文本，提升理解和表達能力。"},
    {"name": "簡單對話與段落的聆聽", "level_id": l2.id, "description": "練習聆聽簡單的對話和段落，提升聽力水平。"},
    {"name": "答題與摘要", "level_id": l3.id, "description": "練習回答問題和撰寫摘要，提升綜合能力。"},
    {"name": "自我表達練習", "level_id": l3.id, "description": "練習用日語進行自我表達，增強口語能力。"},
    {"name": "模擬場景對話練習", "level_id": l3.id, "description": "在模擬場景中進行對話練習，提升實戰能力。"},
    {"name": "節日與習俗", "level_id": l3.id, "description": "了解日本的節日和習俗，增強文化知識。"},
    {"name": "飲食文化", "level_id": l3.id, "description": "學習日本的飲食文化，增強文化理解。"},
        {"name": "日常生活與社交禮儀", "level_id": l3.id, "description": "了解日本的日常生活和社交禮儀，提升文化素養。"}
]

created_lessons = 0
for lesson in lessons:
    if not Lesson.query.filter_by(name=lesson["name"]).first():
        db.session.add(Lesson(name=lesson["name"], level_id=lesson["level_id"], description=lesson["description"]))
        created_lessons += 1

if created_lessons > 0:
    db.session.commit()
    print(f"✅ Created {created_lessons} lessons")
else:
    print("ℹ️  Lessons already exist")

# Mock chat settings
chat_settings = ChatSettings.query.first()
if not chat_settings:
    chat_settings = ChatSettings(
        debug=False,
        headless=True,
        word_limit=100,
        condition="answer using only text and in simple japanese(and explain what you mean in short eng)"
    )
    db.session.add(chat_settings)
    db.session.commit()
    print("✅ Chat settings created")
else:
    print("ℹ️  Chat settings already exist")

print("\n✅ Database initialization completed!\n")
app_context.pop()