from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from .utils import load_assets, get_asset_by_id
from .models import Post
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST
# from .llm import is_inappropriate  # [심화] LLM 부적절 댓글 필터링


def is_post_author(request, post):
    return request.user.is_authenticated and post.author == request.user.username


def asset_list(request):
    """금융 자산 리스트 (JSON에서 로드)"""
    assets = load_assets()
    context = {"assets": assets}
    return render(request, "community/asset_list.html", context)


def board(request, asset_id):
    """해당 자산의 토론 게시판 (게시글 목록)"""
    asset = get_asset_by_id(asset_id)
    if not asset:
        return render(request, "community/404.html", status=404)
    posts = Post.objects.filter(asset_id=asset_id)
    context = {"asset": asset, "posts": posts}
    return render(request, "community/board.html", context)


def post_detail(request, asset_id, post_id):
    """게시글 상세"""
    asset = get_asset_by_id(asset_id)
    if not asset:
        return render(request, "community/404.html", status=404)
    post = get_object_or_404(Post, id=post_id, asset_id=asset_id)
    context = {"asset": asset, "post": post}
    return render(request, "community/post_detail.html", context)


@login_required
@require_http_methods(["GET", "POST"])
def post_create(request, asset_id):
    """게시글 작성"""

    asset = get_asset_by_id(asset_id)

    if not asset:
        return render(request, "community/404.html", status=404)

    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        content = request.POST.get("content", "").strip()

        if not title or not content:
            messages.error(request, "제목과 내용을 모두 입력해 주세요.")
            context = {
                "asset": asset,
                "title": title,
                "content": content,
            }
            return render(request, "community/post_form.html", context)

        post = Post.objects.create(
            asset_id=asset_id,
            title=title,
            content=content,
            author=request.user.username,
        )

        messages.success(request, "게시글이 작성되었습니다.")
        return redirect("community:post_detail", asset_id=asset_id, post_id=post.id)

    context = {"asset": asset}
    return render(request, "community/post_form.html", context)


@login_required
@require_http_methods(["GET", "POST"])
def post_update(request, asset_id, post_id):
    """게시글 수정"""

    asset = get_asset_by_id(asset_id)

    if not asset:
        return render(request, "community/404.html", status=404)

    post = get_object_or_404(Post, id=post_id, asset_id=asset_id)

    if not is_post_author(request, post):
        messages.error(request, "본인이 작성한 게시글만 수정할 수 있습니다.")
        return redirect("community:post_detail", asset_id=asset_id, post_id=post.id)

    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        content = request.POST.get("content", "").strip()

        if not title or not content:
            messages.error(request, "제목과 내용을 모두 입력해 주세요.")
            context = {
                "asset": asset,
                "post": post,
                "title": title,
                "content": content,
                "is_edit": True,
            }
            return render(request, "community/post_form.html", context)

        post.title = title
        post.content = content

        post.save()

        messages.success(request, "게시글이 수정되었습니다.")
        return redirect("community:post_detail", asset_id=asset_id, post_id=post.id)

    context = {
        "asset": asset,
        "post": post,
        "title": post.title,
        "content": post.content,
        "is_edit": True,
    }

    return render(request, "community/post_form.html", context)


@login_required
@require_POST
def post_delete(request, asset_id, post_id):
    """게시글 삭제"""

    post = get_object_or_404(Post, id=post_id, asset_id=asset_id)

    if not is_post_author(request, post):
        messages.error(request, "본인이 작성한 게시글만 삭제할 수 있습니다.")
        return redirect("community:post_detail", asset_id=asset_id, post_id=post.id)

    post.delete()

    messages.success(request, "게시글이 삭제되었습니다.")
    return redirect("community:board", asset_id=asset_id)
