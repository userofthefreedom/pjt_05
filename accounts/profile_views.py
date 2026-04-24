from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from community.models import Post


@login_required
def profile(request):
    """
    내 프로필 페이지

    - 프로필 이미지
    - 닉네임
    - 관심 종목 목록
    - 내가 작성한 게시글 목록
    """

    user = request.user

    # interest_stocks는 DB에 "삼성전자,네이버,카카오" 같은 문자열로 저장된다.
    # 화면에서는 리스트처럼 보여주기 위해 쉼표 기준으로 나눈다.
    interest_stocks = []

    if user.interest_stocks:
        interest_stocks = [
            stock.strip()
            for stock in user.interest_stocks.split(",")
            if stock.strip()
        ]

    # 명세서 요구사항:
    # 내가 작성한 게시글 목록은 username을 기반으로 검색한다.
    my_posts = Post.objects.filter(author=user.username)

    context = {
        "profile_user": user,
        "interest_stocks": interest_stocks,
        "my_posts": my_posts,
    }

    return render(request, "accounts/profile.html", context)