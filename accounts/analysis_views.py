from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from openai import OpenAI

from community.models import Post
from community.utils import get_asset_by_id


MIN_ANALYSIS_TEXT_LENGTH = 80
MAX_POSTS_FOR_ANALYSIS = 10
MAX_ANALYSIS_CHARS = 4000


def _build_llm_client():
    """
    settings.MODE 값에 따라 OpenAI 또는 Upstage 클라이언트를 만든다.

    MODE=OPENAI
      - OPENAI_API_KEY 사용
      - OPENAI_MODEL 사용

    MODE=UPSTAGE
      - UPSTAGE_API_KEY 사용
      - UPSTAGE_MODEL 사용
    """

    mode = (getattr(settings, "MODE", "OPENAI") or "OPENAI").strip().upper()

    if mode == "UPSTAGE":
        api_key = (getattr(settings, "UPSTAGE_API_KEY", "") or "").strip()
        model = (getattr(settings, "UPSTAGE_MODEL", "solar-mini") or "solar-mini").strip()

        if not api_key:
            return None, None, "UPSTAGE_API_KEY가 설정되어 있지 않습니다."

        client = OpenAI(
            api_key=api_key,
            base_url="https://api.upstage.ai/v1/solar",
        )
        return client, model, None

    api_key = (getattr(settings, "OPENAI_API_KEY", "") or "").strip()
    model = (getattr(settings, "OPENAI_MODEL", "gpt-4o-mini") or "gpt-4o-mini").strip()

    if not api_key:
        return None, None, "OPENAI_API_KEY가 설정되어 있지 않습니다."

    client = OpenAI(api_key=api_key)
    return client, model, None


def _get_asset_name(asset_id):
    asset = get_asset_by_id(asset_id)

    if not asset:
        return asset_id

    return asset.get("name", asset_id)


def _build_user_activity_text(posts):
    """
    사용자가 작성한 게시글들을 LLM에 전달하기 좋은 텍스트로 정리한다.
    너무 긴 입력을 막기 위해 MAX_ANALYSIS_CHARS까지만 사용한다.
    """

    lines = []

    for index, post in enumerate(posts, start=1):
        asset_name = _get_asset_name(post.asset_id)

        lines.append(f"[게시글 {index}]")
        lines.append(f"- 자산 분류: {asset_name}")
        lines.append(f"- 제목: {post.title}")
        lines.append(f"- 내용: {post.content}")
        lines.append("")

    activity_text = "\n".join(lines).strip()

    if len(activity_text) > MAX_ANALYSIS_CHARS:
        activity_text = activity_text[:MAX_ANALYSIS_CHARS] + "\n\n[이후 내용은 길이 제한으로 생략됨]"

    return activity_text


def _analyze_investment_tendency(user, posts):
    """
    LLM을 호출해 투자 성향 분석 결과를 문자열로 반환한다.
    """

    client, model, error_message = _build_llm_client()

    if error_message:
        return None, error_message

    activity_text = _build_user_activity_text(posts)

    interest_stocks = user.interest_stocks or "등록된 관심 종목 없음"

    system_prompt = """
당신은 금융 커뮤니티 사용자의 게시글 활동을 바탕으로 투자 성향을 요약하는 분석 도우미입니다.

반드시 지켜야 할 규칙:
1. 특정 종목의 매수, 매도, 보유를 직접 권유하지 마세요.
2. 투자 조언이 아니라, 사용자의 게시글에서 드러나는 관심사와 성향을 요약하세요.
3. 과장된 수익 보장, 확정적 예측, 단정적 표현을 피하세요.
4. 한국어로 답변하세요.
5. 아래 형식을 지켜 답변하세요.

[투자 성향 요약]
- 

[관심 자산/주제]
- 

[위험 선호도 추정]
- 낮음/중간/높음 중 하나를 고르고, 이유를 설명

[투자 판단 스타일]
- 예: 안정성 중시, 성장성 중시, 단기 이슈 추종, 분산투자 선호 등

[주의할 점]
- 

[한 줄 코멘트]
- 
""".strip()

    user_prompt = f"""
사용자 정보:
- username: {user.username}
- nickname: {user.nickname}
- 관심 종목: {interest_stocks}

아래는 사용자가 금융 자산 커뮤니티에 작성한 게시글 활동입니다.

{activity_text}
""".strip()

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
        )

        result = response.choices[0].message.content

        if not result:
            return None, "LLM 분석 결과가 비어 있습니다."

        return result.strip(), None

    except Exception as error:
        return None, f"LLM 분석 중 오류가 발생했습니다: {type(error).__name__}: {error}"


@login_required
def investment_analysis(request):
    """
    프로필 투자 성향 분석 페이지

    사용자의 게시글 활동을 기반으로 LLM 투자 성향 분석 결과를 제공한다.
    게시글이 없거나 내용이 너무 부족하면 분석하지 않고 안내 메시지를 보여준다.
    """

    user = request.user

    my_posts = list(
        Post.objects.filter(author=user.username).order_by("-created_at")[:MAX_POSTS_FOR_ANALYSIS]
    )

    total_text = " ".join(
        f"{post.title} {post.content}"
        for post in my_posts
    ).strip()

    analysis_result = None
    analysis_error = None

    if not my_posts:
        analysis_error = "아직 작성한 게시글이 없어 투자 성향을 분석할 수 없습니다."
    elif len(total_text) < MIN_ANALYSIS_TEXT_LENGTH:
        analysis_error = "작성한 게시글 내용이 너무 짧아 투자 성향을 분석하기 어렵습니다."
    else:
        analysis_result, analysis_error = _analyze_investment_tendency(user, my_posts)

    context = {
        "profile_user": user,
        "my_posts": my_posts,
        "analysis_result": analysis_result,
        "analysis_error": analysis_error,
        "min_analysis_text_length": MIN_ANALYSIS_TEXT_LENGTH,
    }

    return render(request, "accounts/investment_analysis.html", context)