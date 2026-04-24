# 05 PJT - 금융 자산 정보 토론 게시판 2

## 1. 프로젝트 개요

이 프로젝트는 Django 기반의 금융 자산 커뮤니티 서비스입니다.

기존 금융 자산별 토론 게시판 기능에 사용자 인증 기능을 확장하고, Django 기본 사용자 모델을 커스텀 유저 모델로 대체하여 사용자별 닉네임, 관심 종목, 프로필 이미지를 관리할 수 있도록 구현했습니다.

또한 게시글 작성자 권한을 로그인 사용자 기준으로 제어하여, 게시글 작성·수정·삭제 흐름이 사용자 인증 시스템과 연결되도록 구성했습니다.

심화 기능으로는 사용자가 작성한 게시글을 기반으로 LLM API를 호출하여 투자 성향을 분석하는 기능을 구현했습니다.

---

## 2. 프로젝트 목표

이번 프로젝트의 주요 목표는 다음과 같습니다.

- Django 기본 User 모델을 커스텀 User 모델로 확장하기
- 회원가입, 로그인, 로그아웃, 비밀번호 변경 기능 구현하기
- 로그인 사용자만 게시글을 작성할 수 있도록 제한하기
- 게시글 작성 시 현재 로그인 사용자의 username을 작성자로 자동 저장하기
- 게시글 수정과 삭제는 작성자 본인만 가능하도록 제어하기
- 프로필 페이지에서 사용자 정보와 내가 작성한 게시글 목록 보여주기
- 사용자의 게시글 활동을 기반으로 LLM 투자 성향 분석 기능 제공하기
- 구현 기능, 학습 내용, 어려웠던 점을 README에 정리하기

---

## 3. 개발 환경 및 사용 기술

### 3.1 개발 언어 및 프레임워크

- Python
- Django
- HTML
- CSS
- SQLite

### 3.2 주요 라이브러리

- Django
- Pillow
- python-dotenv
- openai

### 3.3 외부 API

- OpenAI API
- Upstage API

LLM 투자 성향 분석 기능은 OpenAI API 또는 Upstage API 중 하나를 선택하여 사용할 수 있도록 구성했습니다.

---

## 4. 프로젝트 구조

```text
pjt_05/
├── accounts/
│   ├── migrations/
│   ├── templates/
│   │   ├── base.html
│   │   └── accounts/
│   │       ├── login.html
│   │       ├── signup.html
│   │       ├── profile.html
│   │       ├── password_change.html
│   │       ├── password_change_done.html
│   │       └── investment_analysis.html
│   ├── admin.py
│   ├── analysis_views.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── profile_views.py
│   ├── urls.py
│   └── views.py
│
├── community/
│   ├── migrations/
│   ├── templates/
│   │   └── community/
│   │       ├── 404.html
│   │       ├── asset_list.html
│   │       ├── base.html
│   │       ├── board.html
│   │       ├── post_detail.html
│   │       └── post_form.html
│   ├── admin.py
│   ├── apps.py
│   ├── llm.py
│   ├── models.py
│   ├── urls.py
│   ├── utils.py
│   └── views.py
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── data/
│   └── assets.json
│
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 5. 주요 기능

## 5.1 금융 자산 목록 조회

메인 페이지에서는 `data/assets.json` 파일에 저장된 금융 자산 목록을 불러와 화면에 표시합니다.

사용자는 각 자산을 클릭하여 해당 자산에 대한 토론 게시판으로 이동할 수 있습니다.

구현 위치:

```text
community/utils.py
community/views.py
community/templates/community/asset_list.html
```

주요 흐름:

```text
1. load_assets() 함수로 JSON 파일을 읽는다.
2. asset_list view에서 assets 데이터를 템플릿에 전달한다.
3. asset_list.html에서 금융 자산 목록을 카드 형태로 출력한다.
4. 사용자가 자산을 클릭하면 해당 자산 게시판으로 이동한다.
```

---

## 5.2 커스텀 유저 모델

Django 기본 User 모델을 그대로 사용하지 않고, `AbstractUser`를 상속한 커스텀 User 모델을 구현했습니다.

구현 위치:

```text
accounts/models.py
```

추가한 필드는 다음과 같습니다.

| 필드명 | 설명 |
|---|---|
| nickname | 사용자의 닉네임 |
| interest_stocks | 사용자의 관심 종목 목록 |
| profile_image | 사용자의 프로필 이미지 |

현재 `interest_stocks`는 여러 관심 종목을 쉼표로 연결한 문자열 형태로 저장합니다.

예시:

```text
SAMSUNG,NAVER,BTC
```

커스텀 유저 모델을 사용하기 위해 `settings.py`에 다음 설정을 추가했습니다.

```python
AUTH_USER_MODEL = "accounts.User"
```

프로필 이미지 업로드를 위해 다음 설정도 추가했습니다.

```python
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
```

개발 환경에서 업로드된 이미지를 확인할 수 있도록 `config/urls.py`에 media URL 설정도 추가했습니다.

```python
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

## 5.3 회원가입

회원가입 기능은 `SignupForm`을 사용하여 구현했습니다.

구현 위치:

```text
accounts/forms.py
accounts/views.py
accounts/templates/accounts/signup.html
```

회원가입 시 입력받는 정보는 다음과 같습니다.

- 아이디
- 비밀번호
- 비밀번호 확인
- 닉네임
- 관심 종목
- 프로필 이미지

관심 종목은 체크박스 다중 선택 방식으로 입력받습니다.

`forms.py`에서는 `MultipleChoiceField`와 `CheckboxSelectMultiple`을 사용했습니다.

```python
interest_stocks = forms.MultipleChoiceField(
    choices=User.STOCK_CHOICES,
    widget=forms.CheckboxSelectMultiple,
    required=False,
)
```

폼에서 선택된 관심 종목은 리스트 형태로 전달되므로, 저장 시 쉼표로 연결해 문자열로 변환했습니다.

```python
stocks = self.cleaned_data.get("interest_stocks")
user.interest_stocks = ",".join(stocks)
```

회원가입이 성공하면 생성된 사용자를 즉시 로그인 처리합니다.

```python
user = form.save()
login(request, user)
return redirect("/")
```

이를 통해 회원가입 완료 후 사용자는 바로 로그인된 상태로 메인 페이지에 접근할 수 있습니다.

---

## 5.4 로그인

로그인 기능은 Django의 `AuthenticationForm`을 사용하여 구현했습니다.

구현 위치:

```text
accounts/views.py
accounts/templates/accounts/login.html
```

로그인 흐름은 다음과 같습니다.

```text
1. 로그인 페이지에서 아이디와 비밀번호를 입력한다.
2. AuthenticationForm으로 인증 정보를 검증한다.
3. 인증 성공 시 login(request, user)를 호출한다.
4. next 파라미터가 있으면 원래 접근하려던 페이지로 이동한다.
5. next 파라미터가 없으면 메인 페이지로 이동한다.
```

`next` 처리를 추가하여, 비로그인 사용자가 글쓰기 페이지에 접근했다가 로그인한 경우 다시 원래 글쓰기 페이지로 돌아갈 수 있도록 했습니다.

```python
next_url = request.GET.get("next") or request.POST.get("next")

if form.is_valid():
    user = form.get_user()
    login(request, user)

    if next_url:
        return redirect(next_url)

    return redirect("/")
```

로그인 템플릿에는 hidden input으로 `next` 값을 유지하도록 했습니다.

```html
<input type="hidden" name="next" value="{{ next|default:'' }}">
```

---

## 5.5 로그아웃

로그아웃 기능은 Django의 `logout()` 함수를 사용했습니다.

구현 위치:

```text
accounts/views.py
accounts/urls.py
community/templates/community/base.html
```

로그아웃은 POST 요청으로 처리하도록 구성했습니다.

```python
def logout_view(request):
    if request.method == "POST":
        logout(request)

    return redirect("/")
```

메인 페이지와 게시판에서 사용하는 `community/base.html`의 상단 네비게이션에는 로그아웃 버튼을 form 형태로 배치했습니다.

```html
<form action="{% url 'accounts:logout' %}" method="post" class="logout-form">
  {% csrf_token %}
  <button type="submit" class="nav-logout-button">로그아웃</button>
</form>
```

POST 방식으로 로그아웃을 처리한 이유는 사용자의 로그인 상태를 변경하는 요청을 단순 링크 클릭인 GET 요청으로 처리하지 않기 위해서입니다.

---

## 5.6 비밀번호 변경

비밀번호 변경 기능은 Django의 `PasswordChangeForm`을 사용하여 구현했습니다.

구현 위치:

```text
accounts/views.py
accounts/templates/accounts/password_change.html
accounts/templates/accounts/password_change_done.html
```

비밀번호 변경 페이지에서는 다음 값을 입력받습니다.

- 현재 비밀번호
- 새 비밀번호
- 새 비밀번호 확인

비밀번호 변경 성공 후에는 `update_session_auth_hash()`를 호출하여 비밀번호 변경 이후에도 현재 로그인 세션이 유지되도록 했습니다.

```python
user = form.save()
update_session_auth_hash(request, user)
return redirect("accounts:password_change_done")
```

비밀번호 변경이 완료되면 완료 페이지로 이동합니다.

```python
@login_required
def password_change_done(request):
    return render(request, "accounts/password_change_done.html")
```

이를 통해 비밀번호 변경 페이지와 완료 페이지를 모두 제공했습니다.

---

## 5.7 게시글 작성

게시글 작성은 로그인한 사용자만 가능합니다.

구현 위치:

```text
community/views.py
community/templates/community/post_form.html
```

`post_create` view에 `@login_required`를 적용하여 비로그인 사용자가 게시글 작성 페이지에 접근할 수 없도록 했습니다.

```python
@login_required
@require_http_methods(["GET", "POST"])
def post_create(request, asset_id):
    ...
```

게시글 작성 시 작성자 입력칸은 제공하지 않습니다.

대신 현재 로그인한 사용자의 username을 `Post.author`에 자동 저장합니다.

```python
post = Post.objects.create(
    asset_id=asset_id,
    title=title,
    content=content,
    author=request.user.username,
)
```

이를 통해 사용자가 임의로 작성자명을 입력하거나 다른 사람의 이름으로 게시글을 작성하는 것을 막았습니다.

---

## 5.8 게시글 수정

게시글 수정은 작성자 본인만 가능합니다.

구현 위치:

```text
community/views.py
community/templates/community/post_detail.html
community/templates/community/post_form.html
```

작성자 확인은 다음 함수로 처리했습니다.

```python
def is_post_author(request, post):
    return request.user.is_authenticated and post.author == request.user.username
```

수정 요청이 들어오면 먼저 현재 로그인 사용자가 게시글 작성자인지 확인합니다.

```python
if not is_post_author(request, post):
    messages.error(request, "본인이 작성한 게시글만 수정할 수 있습니다.")
    return redirect("community:post_detail", asset_id=asset_id, post_id=post.id)
```

작성자가 아닌 사용자는 수정 페이지에 접근할 수 없고, 상세 페이지로 되돌아가며 오류 메시지를 확인하게 됩니다.

템플릿에서도 작성자 본인에게만 수정 버튼이 보이도록 처리했습니다.

```django
{% if user.is_authenticated and user.username == post.author %}
  <a href="{% url 'community:post_update' asset.id post.id %}" class="btn">수정</a>
{% endif %}
```

단, 템플릿에서 버튼을 숨기는 것은 사용자 경험을 위한 처리일 뿐이고, 실제 권한 검사는 view 함수에서 수행합니다.

---

## 5.9 게시글 삭제

게시글 삭제도 작성자 본인만 가능합니다.

구현 위치:

```text
community/views.py
community/templates/community/post_detail.html
```

삭제 view에는 `@login_required`와 `@require_POST`를 적용했습니다.

```python
@login_required
@require_POST
def post_delete(request, asset_id, post_id):
    ...
```

삭제 요청도 수정과 동일하게 작성자 확인을 거칩니다.

```python
if not is_post_author(request, post):
    messages.error(request, "본인이 작성한 게시글만 삭제할 수 있습니다.")
    return redirect("community:post_detail", asset_id=asset_id, post_id=post.id)
```

작성자 본인인 경우에만 게시글이 삭제됩니다.

삭제 버튼은 form으로 구성하고 CSRF 토큰을 포함했습니다.

```html
<form action="{% url 'community:post_delete' asset.id post.id %}" method="post" class="form-inline">
  {% csrf_token %}
  <button type="submit" class="btn btn-danger">삭제</button>
</form>
```

---

## 5.10 프로필 페이지

프로필 페이지에서는 로그인한 사용자의 정보를 확인할 수 있습니다.

구현 위치:

```text
accounts/profile_views.py
accounts/templates/accounts/profile.html
```

표시하는 정보는 다음과 같습니다.

- 프로필 이미지
- 아이디
- 닉네임
- 관심 종목 목록
- 내가 작성한 게시글 목록
- 비밀번호 변경 페이지 이동 버튼
- 투자 성향 분석 페이지 이동 버튼

프로필 페이지는 로그인한 사용자만 접근할 수 있도록 `@login_required`를 적용했습니다.

```python
@login_required
def profile(request):
    ...
```

관심 종목은 DB에 쉼표로 연결된 문자열로 저장되어 있기 때문에, 화면에서는 split을 사용해 리스트로 변환했습니다.

```python
interest_stocks = []

if user.interest_stocks:
    interest_stocks = [
        stock.strip()
        for stock in user.interest_stocks.split(",")
        if stock.strip()
    ]
```

내가 작성한 게시글 목록은 username을 기준으로 조회했습니다.

```python
my_posts = Post.objects.filter(author=user.username)
```

프로필 페이지에서 게시글 제목을 클릭하면 해당 게시글 상세 페이지로 이동할 수 있습니다.

---

## 5.11 LLM 투자 성향 분석

심화 기능으로 LLM 기반 투자 성향 분석 기능을 구현했습니다.

구현 위치:

```text
accounts/analysis_views.py
accounts/templates/accounts/investment_analysis.html
```

분석 흐름은 다음과 같습니다.

```text
1. 로그인한 사용자의 username을 기준으로 작성 게시글을 조회한다.
2. 최근 게시글 최대 10개를 분석 대상으로 사용한다.
3. 게시글이 없으면 분석하지 않고 안내 메시지를 출력한다.
4. 게시글 제목과 내용의 전체 길이가 너무 짧으면 분석하지 않고 안내 메시지를 출력한다.
5. 분석 가능한 경우 OpenAI 또는 Upstage API 클라이언트를 생성한다.
6. 사용자의 게시글 활동을 프롬프트로 구성한다.
7. LLM에 투자 성향 분석을 요청한다.
8. 분석 결과를 화면에 출력한다.
```

분석에 사용하는 게시글 수와 길이는 상수로 제한했습니다.

```python
MIN_ANALYSIS_TEXT_LENGTH = 80
MAX_POSTS_FOR_ANALYSIS = 10
MAX_ANALYSIS_CHARS = 4000
```

게시글이 없는 경우에는 다음 메시지를 출력합니다.

```text
아직 작성한 게시글이 없어 투자 성향을 분석할 수 없습니다.
```

게시글 내용이 너무 짧은 경우에는 다음 메시지를 출력합니다.

```text
작성한 게시글 내용이 너무 짧아 투자 성향을 분석하기 어렵습니다.
```

API 키가 설정되어 있지 않은 경우에도 예외가 발생하지 않도록 사용자에게 안내 메시지를 보여줍니다.

```python
if not api_key:
    return None, None, "OPENAI_API_KEY가 설정되어 있지 않습니다."
```

LLM 응답은 다음 형식으로 요청했습니다.

```text
[투자 성향 요약]
-

[관심 자산/주제]
-

[위험 선호도 추정]
-

[투자 판단 스타일]
-

[주의할 점]
-

[한 줄 코멘트]
-
```

LLM 분석은 투자 조언이 아니라, 사용자의 게시글에서 드러나는 관심사와 성향을 요약하는 용도로 제한했습니다.

---

## 6. URL 구조

## 6.1 community 앱 URL

| URL | 이름 | 설명 |
|---|---|---|
| `/` | `community:asset_list` | 금융 자산 목록 |
| `/asset/<asset_id>/` | `community:board` | 특정 자산 게시판 |
| `/asset/<asset_id>/post/new/` | `community:post_create` | 게시글 작성 |
| `/asset/<asset_id>/post/<post_id>/` | `community:post_detail` | 게시글 상세 |
| `/asset/<asset_id>/post/<post_id>/edit/` | `community:post_update` | 게시글 수정 |
| `/asset/<asset_id>/post/<post_id>/delete/` | `community:post_delete` | 게시글 삭제 |

## 6.2 accounts 앱 URL

| URL | 이름 | 설명 |
|---|---|---|
| `/accounts/signup/` | `accounts:signup` | 회원가입 |
| `/accounts/login/` | `accounts:login` | 로그인 |
| `/accounts/logout/` | `accounts:logout` | 로그아웃 |
| `/accounts/profile/` | `accounts:profile` | 프로필 |
| `/accounts/password/change/` | `accounts:password_change` | 비밀번호 변경 |
| `/accounts/password/change/done/` | `accounts:password_change_done` | 비밀번호 변경 완료 |
| `/accounts/profile/analysis/` | `accounts:investment_analysis` | 투자 성향 분석 |

---

## 7. 실행 방법

## 7.1 가상환경 생성

```bash
python -m venv venv
```

## 7.2 가상환경 활성화

Windows Git Bash 사용 시:

```bash
source venv/Scripts/activate
```

Windows PowerShell 또는 CMD 사용 시:

```bash
venv\Scripts\activate
```

macOS 또는 Linux 사용 시:

```bash
source venv/bin/activate
```

## 7.3 패키지 설치

```bash
pip install -r requirements.txt
```

## 7.4 데이터베이스 생성

```bash
python manage.py migrate
```

## 7.5 개발 서버 실행

```bash
python manage.py runserver
```

서버 실행 후 브라우저에서 아래 주소로 접속합니다.

```text
http://127.0.0.1:8000/
```

---

## 8. 환경 변수 설정

LLM 투자 성향 분석 기능을 사용하려면 프로젝트 루트에 `.env` 파일을 생성해야 합니다.

`.env` 파일은 `manage.py`와 같은 위치에 둡니다.

## 8.1 OpenAI 사용 시

```env
MODE=OPENAI
OPENAI_API_KEY=발급받은_OPENAI_API_KEY
OPENAI_MODEL=gpt-4o-mini
```

## 8.2 Upstage 사용 시

```env
MODE=UPSTAGE
UPSTAGE_API_KEY=발급받은_UPSTAGE_API_KEY
UPSTAGE_MODEL=solar-mini
```

## 8.3 환경 변수 보안

`.env` 파일에는 API 키가 들어가기 때문에 Git에 업로드하면 안 됩니다.

현재 `.gitignore`에는 다음 항목을 추가하여 `.env` 파일이 Git에 포함되지 않도록 했습니다.

```gitignore
.env
```

만약 실수로 API 키가 포함된 `.env` 파일을 GitHub에 업로드했다면, 해당 API 키는 폐기하고 새 키를 발급받아야 합니다.

---

## 9. 테스트 시나리오

## 9.1 회원가입 테스트

```text
1. /accounts/signup/ 접속
2. 아이디, 비밀번호, 비밀번호 확인, 닉네임 입력
3. 관심 종목 선택
4. 프로필 이미지 선택
5. 가입하기 클릭
6. 회원가입 성공 후 메인 페이지로 이동
7. 상단에 로그인 상태 메뉴가 표시되는지 확인
```

기대 결과:

```text
회원가입 성공 후 자동 로그인된다.
```

## 9.2 로그인 테스트

```text
1. /accounts/login/ 접속
2. 아이디와 비밀번호 입력
3. 로그인 클릭
```

기대 결과:

```text
인증 성공 시 메인 페이지로 이동한다.
잘못된 정보 입력 시 로그인 페이지에 오류 메시지가 표시된다.
```

## 9.3 로그아웃 테스트

```text
1. 로그인 상태에서 상단 메뉴의 로그아웃 클릭
2. 메인 페이지로 이동
```

기대 결과:

```text
로그아웃 처리 후 상단 메뉴가 로그인/회원가입 상태로 변경된다.
```

## 9.4 비밀번호 변경 테스트

```text
1. 로그인 상태에서 프로필 페이지 접속
2. 비밀번호 변경 클릭
3. 현재 비밀번호 입력
4. 새 비밀번호 입력
5. 새 비밀번호 확인 입력
6. 비밀번호 변경 클릭
```

기대 결과:

```text
정상 입력 시 비밀번호 변경 완료 페이지로 이동한다.
현재 비밀번호가 틀리거나 새 비밀번호 확인이 일치하지 않으면 오류 메시지가 표시된다.
비밀번호 변경 후에도 로그인 상태가 유지된다.
```

## 9.5 게시글 작성 권한 테스트

```text
1. 로그아웃 상태에서 글쓰기 페이지 접근
2. 로그인 페이지로 이동하는지 확인
3. 로그인 후 글쓰기 페이지로 돌아오는지 확인
4. 제목과 내용을 입력하고 게시글 작성
```

기대 결과:

```text
비로그인 사용자는 글쓰기 페이지에 직접 접근할 수 없다.
로그인 사용자는 게시글을 작성할 수 있다.
작성자는 현재 로그인 사용자의 username으로 자동 저장된다.
```

## 9.6 게시글 수정 권한 테스트

```text
1. A 계정으로 게시글 작성
2. A 계정으로 게시글 상세 페이지 접속
3. 수정 버튼이 보이는지 확인
4. B 계정으로 같은 게시글 상세 페이지 접속
5. 수정 버튼이 보이지 않는지 확인
6. B 계정으로 수정 URL에 직접 접근
```

기대 결과:

```text
작성자 본인에게만 수정 버튼이 보인다.
작성자가 아닌 사용자가 수정 URL에 직접 접근하면 차단된다.
오류 메시지가 표시되고 게시글 상세 페이지로 이동한다.
```

## 9.7 게시글 삭제 권한 테스트

```text
1. A 계정으로 게시글 작성
2. A 계정으로 게시글 상세 페이지 접속
3. 삭제 버튼이 보이는지 확인
4. B 계정으로 같은 게시글 상세 페이지 접속
5. 삭제 버튼이 보이지 않는지 확인
6. B 계정으로 삭제 요청 시도
```

기대 결과:

```text
작성자 본인에게만 삭제 버튼이 보인다.
삭제는 POST 요청으로만 처리된다.
작성자가 아닌 사용자는 삭제할 수 없다.
```

## 9.8 프로필 페이지 테스트

```text
1. 로그인 상태에서 /accounts/profile/ 접속
2. 프로필 이미지 확인
3. 아이디와 닉네임 확인
4. 관심 종목 목록 확인
5. 내가 작성한 게시글 목록 확인
```

기대 결과:

```text
현재 로그인한 사용자의 정보가 표시된다.
내가 작성한 게시글 목록은 username 기준으로 조회된다.
```

## 9.9 투자 성향 분석 테스트

```text
1. 로그인 상태에서 게시글을 작성한다.
2. 프로필 페이지로 이동한다.
3. 투자 성향 분석 보기 버튼을 클릭한다.
4. 분석 결과 또는 안내 메시지를 확인한다.
```

기대 결과:

```text
게시글이 없으면 분석 불가 메시지가 표시된다.
게시글 내용이 너무 짧으면 내용 부족 메시지가 표시된다.
API 키가 없으면 API 키 설정 안내 메시지가 표시된다.
분석 가능한 경우 LLM이 생성한 투자 성향 분석 결과가 표시된다.
```

---

## 10. 구현 과정에서 학습한 점

## 10.1 커스텀 유저 모델

Django에서 기본 User 모델을 프로젝트 중간에 변경하는 것은 복잡할 수 있기 때문에, 사용자 정보를 확장해야 하는 경우 프로젝트 초기에 커스텀 유저 모델을 설정하는 것이 중요하다는 점을 학습했습니다.

이번 프로젝트에서는 `AbstractUser`를 상속하여 기본 인증 기능은 유지하면서 `nickname`, `interest_stocks`, `profile_image` 필드를 추가했습니다.

이를 통해 Django 인증 시스템을 그대로 활용하면서도 프로젝트 요구사항에 맞는 사용자 정보를 저장할 수 있었습니다.

## 10.2 회원가입 폼 커스터마이징

`UserCreationForm`을 상속하여 회원가입 폼을 커스터마이징했습니다.

특히 관심 종목은 여러 개를 선택할 수 있어야 했기 때문에 `MultipleChoiceField`와 `CheckboxSelectMultiple`을 사용했습니다.

폼에서 선택된 값은 리스트 형태였지만, 모델에서는 문자열 필드로 저장해야 했기 때문에 `save()` 메서드를 오버라이드하여 쉼표로 연결한 문자열로 변환했습니다.

## 10.3 로그인 사용자 기반 권한 제어

게시글 작성, 수정, 삭제 기능에서 가장 중요한 점은 템플릿에서 버튼만 숨기는 것이 아니라 view 함수에서 실제 권한 검사를 수행해야 한다는 것이었습니다.

템플릿에서 수정/삭제 버튼을 숨기더라도 사용자가 URL을 직접 입력하면 view에 접근할 수 있기 때문입니다.

따라서 `is_post_author()` 함수를 만들고, 수정/삭제 view에서 작성자 여부를 반드시 확인하도록 구현했습니다.

## 10.4 login_required와 next 처리

`@login_required`를 사용하면 비로그인 사용자의 접근을 로그인 페이지로 보낼 수 있습니다.

하지만 로그인 후 항상 메인 페이지로 이동하면 사용자가 원래 접근하려던 페이지로 돌아가지 못합니다.

이를 해결하기 위해 로그인 view에서 `next` 파라미터를 처리했습니다.

덕분에 비로그인 사용자가 글쓰기 페이지에 접근했다가 로그인하면 다시 글쓰기 페이지로 돌아갈 수 있습니다.

## 10.5 비밀번호 변경 후 세션 유지

Django에서 비밀번호를 변경하면 기존 세션이 무효화될 수 있습니다.

비밀번호 변경 후에도 현재 사용자가 계속 로그인 상태를 유지하도록 `update_session_auth_hash()`를 사용했습니다.

이를 통해 비밀번호 변경 직후 다시 로그인해야 하는 불편함을 줄일 수 있었습니다.

## 10.6 프로필 이미지 업로드

프로필 이미지를 저장하기 위해 `ImageField`를 사용했고, 이를 위해 `Pillow` 패키지가 필요했습니다.

또한 업로드 파일을 저장하고 조회하기 위해 `MEDIA_URL`, `MEDIA_ROOT`를 설정하고, 개발 환경에서는 `static()`을 사용해 media 파일을 제공했습니다.

## 10.7 LLM API 연동

LLM 투자 성향 분석 기능에서는 OpenAI SDK를 사용했습니다.

OpenAI와 Upstage를 선택적으로 사용할 수 있도록 `MODE` 환경 변수를 두었고, Upstage 사용 시에는 `base_url`을 별도로 지정했습니다.

API 키를 코드에 직접 작성하지 않고 `.env`로 분리하면서 보안상 중요한 정보를 코드 저장소에 올리지 않는 방식도 학습했습니다.

또한 게시글이 부족하거나 API 키가 없는 경우에도 서버 오류가 나지 않도록 예외 처리와 안내 메시지를 함께 구현했습니다.

---

## 11. 어려웠던 점

## 11.1 기존 게시글 작성자 구조 변경

초기 게시글 작성 폼은 작성자를 사용자가 직접 입력하는 방식이었습니다.

하지만 명세서에서는 게시글 작성 시 현재 로그인 사용자의 username을 작성자로 자동 저장해야 했습니다.

따라서 작성자 입력칸을 제거하고, view에서 `request.user.username`을 저장하도록 구조를 바꾸어야 했습니다.

## 11.2 작성자 권한 처리

수정/삭제 버튼을 작성자에게만 보여주는 것과 실제 수정/삭제 권한을 제한하는 것은 다른 문제였습니다.

처음에는 템플릿 조건문만으로 충분해 보였지만, URL 직접 접근을 막으려면 view 함수에서 권한 검사가 반드시 필요했습니다.

이 점을 반영하여 템플릿과 view 양쪽에 모두 권한 처리를 적용했습니다.

## 11.3 협업 중 파일 충돌 가능성

회원가입, 로그인, 프로필, 투자 성향 분석 기능이 모두 accounts 앱에 속하다 보니 하나의 `views.py` 파일을 여러 명이 동시에 수정할 가능성이 있었습니다.

이를 줄이기 위해 프로필 기능은 `profile_views.py`, 투자 성향 분석 기능은 `analysis_views.py`로 분리했습니다.

기능별 view 파일을 분리하니 역할별 작업 범위가 더 명확해졌고, merge conflict 가능성도 줄일 수 있었습니다.

## 11.4 관심 종목 저장 방식

명세서에서는 관심 종목을 여러 개 선택할 수 있도록 요구했지만, 모델 필드는 문자열 필드였습니다.

따라서 체크박스로 여러 종목을 선택받고, 저장할 때는 쉼표로 연결한 문자열로 변환했습니다.

반대로 프로필 페이지에서는 쉼표로 저장된 문자열을 다시 split하여 목록 형태로 보여주었습니다.

## 11.5 로그인/로그아웃 템플릿 분리

로그인과 회원가입 페이지는 `accounts/templates/base.html`을 상속하고, 메인 페이지와 게시판은 `community/templates/community/base.html`을 상속했습니다.

처음에는 accounts 쪽 base 템플릿만 수정하면 모든 화면의 네비게이션이 바뀔 것으로 생각할 수 있었지만, 실제로는 community 화면이 별도의 base 템플릿을 사용하고 있었습니다.

그래서 메인 페이지와 게시판 상단에도 로그인, 회원가입, 프로필, 로그아웃 링크가 보이도록 `community/base.html`을 별도로 수정했습니다.

## 11.6 LLM 분석 조건 처리

LLM은 입력이 너무 적어도 그럴듯한 답변을 만들어낼 수 있습니다.

하지만 게시글이 없거나 내용이 너무 짧은 상황에서 투자 성향을 분석하는 것은 신뢰도가 낮다고 판단했습니다.

그래서 최소 텍스트 길이를 설정하고, 조건을 만족하지 못하면 LLM을 호출하지 않고 안내 메시지를 출력하도록 구현했습니다.

---

## 12. 보완하고 싶은 점

이번 프로젝트에서 필수 요구사항과 심화 요구사항을 구현했지만, 다음과 같은 점은 추가로 개선할 수 있습니다.

- 관심 종목을 문자열이 아니라 별도 모델 또는 ManyToMany 관계로 관리하기
- 게시글 작성자의 username만 저장하는 대신 User 모델과 ForeignKey로 연결하기
- 댓글 모델을 추가하여 게시글 상세 페이지에서 댓글 작성, 삭제 기능 제공하기
- 프로필 페이지에서 내가 작성한 댓글 목록도 함께 보여주기
- 비밀번호 변경 폼의 오류 메시지를 더 명확한 문장으로 커스터마이징하기
- LLM 분석 결과를 매번 새로 호출하지 않고 캐싱하거나 저장하기
- 투자 성향 분석 결과에 분석 시각과 사용된 게시글 수를 함께 표시하기
- API 호출 실패 유형에 따라 사용자 메시지를 더 세분화하기
- 테스트 코드를 작성하여 권한 처리와 인증 흐름을 자동 검증하기

---

## 13. 마무리

이번 프로젝트를 통해 Django의 사용자 인증 흐름과 커스텀 유저 모델 확장 방식을 학습했습니다.

또한 로그인 사용자 기반으로 게시글 권한을 제어하고, 프로필 페이지와 LLM 분석 기능을 연결하면서 하나의 커뮤니티 서비스가 사용자별 데이터를 어떻게 관리하는지 경험할 수 있었습니다.

특히 작성자 권한 제어는 템플릿 처리만으로는 충분하지 않고, view에서 반드시 검증해야 한다는 점을 확인했습니다.

마지막으로 LLM API를 사용할 때는 API 키 관리, 입력 데이터 부족 상황 처리, 결과의 표현 방식까지 함께 고려해야 한다는 점을 배웠습니다.