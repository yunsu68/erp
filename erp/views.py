from django.http import HttpResponse


def base_response(request):
    return HttpResponse("안녕하세요! 장고의 시작입니다!")