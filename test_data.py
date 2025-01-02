from app import db, app
from app.models import User, Post, Level, Lesson

app_context = app.app_context()
app_context.push()
db.drop_all()
db.create_all()

# Mock Admin account
admin = User(username='admin', email='admin@example.com', is_admin=True)
admin.set_password("a")
db.session.add(admin)
db.session.commit()
db.session.close()

# Mock users Account
u1 = User(username='u1', email='u1@example.com')
u2 = User(username='u2', email='u2@example.com')
u3 = User(username='u3', email='u3@example.com')
u4 = User(username='alice', email='alice@example.com')
u5 = User(username='bob', email='bob@example.com')
u6 = User(username='charlie', email='charlie@example.com')
u7 = User(username='david', email='david@example.com')
u8 = User(username='eve', email='eve@example.com')
u9 = User(username='frank', email='frank@example.com')
u10 = User(username='grace', email='grace@example.com')
u1.set_password("1")
u2.set_password("2")
u3.set_password("3")
u4.set_password("4")
u5.set_password("5")
u6.set_password("6")
u7.set_password("7")
u8.set_password("8")
u9.set_password("9")
u10.set_password("10")
db.session.add_all([u1, u2, u3, u4, u5, u6, u7, u8, u9, u10])
db.session.commit()
db.session.close()

# Mock levels
l1 = Level(name='Beginner')
l2 = Level(name='Intermediate')
l3 = Level(name='Advanced')
db.session.add_all([l1, l2, l3])
db.session.commit()
db.session.close()

# Mock posts
p1 = Post(title='My first post', body='This is the body of my first post', user_id=u1.id)
p2 = Post(title='A day in the life', body='Today I went to the park and had a great time.', user_id=u2.id)
p3 = Post(title='Learning Python', body='Python is a versatile programming language.', user_id=u3.id)
p4 = Post(title='Traveling to Japan', body='Japan is a beautiful country with rich culture.', user_id=u4.id)
p5 = Post(title='My favorite recipes', body='I love cooking and trying out new recipes.', user_id=u5.id)
p6 = Post(title='Fitness journey', body='Staying fit and healthy is important.', user_id=u6.id)
p7 = Post(title='Book recommendations', body='Here are some books I recommend reading.', user_id=u7.id)
p8 = Post(title='Photography tips', body='Photography is a great hobby to capture moments.', user_id=u8.id)
p9 = Post(title='Gardening 101', body='Gardening is a relaxing and rewarding activity.', user_id=u9.id)
p10 = Post(title='Tech trends', body='Keeping up with the latest in technology.', user_id=u10.id)
p11 = Post(title='Music I love', body='Sharing my favorite music tracks.', user_id=u1.id)
p12 = Post(title='Movie reviews', body='My thoughts on the latest movies.', user_id=u2.id)
p13 = Post(title='DIY projects', body='Do-it-yourself projects are fun and creative.', user_id=u3.id)
p14 = Post(title='Mindfulness and meditation', body='Practicing mindfulness for a better life.', user_id=u4.id)
p15 = Post(title='Career advice', body='Tips and advice for advancing your career.', user_id=u5.id)
p16 = Post(title='Learning new languages', body='The benefits of learning new languages.', user_id=u6.id)
p17 = Post(title='Home decor ideas', body='Ideas to decorate your home beautifully.', user_id=u7.id)
p18 = Post(title='Pet care tips', body='Taking care of your pets.', user_id=u8.id)
p19 = Post(title='Outdoor adventures', body='Exploring the great outdoors.', user_id=u9.id)
p20 = Post(title='Healthy eating', body='Tips for maintaining a healthy diet.', user_id=u10.id)
p21 = Post(title='Personal finance', body='Managing your personal finances effectively.', user_id=u1.id)
p22 = Post(title='Hiking trails', body='Best hiking trails to explore.', user_id=u2.id)
p23 = Post(title='Yoga for beginners', body='Starting your yoga journey.', user_id=u3.id)

db.session.add_all([p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15, p16, p17, p18, p19, p20, p21, p22, p23])
db.session.commit()
db.session.close()

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

for lesson in lessons:
    db.session.add(Lesson(name=lesson["name"], level_id=lesson["level_id"], description=lesson["description"]))
db.session.commit()
db.session.close()

app_context.pop()