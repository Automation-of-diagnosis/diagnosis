# безопасное использование request.referrer
from urllib.parse import urlparse, urljoin
from flask import redirect, request, url_for


def is_safe_url(target):
    # ref_url = urlparse(request.host_url) - получить URL сайта
    ref_url = urlparse(request.host_url)
    # test_url = urlparse(urljoin(request.host_url, target)) - проверить не происходит ли перенаправление пользователя
    # на внешний сайт
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def get_redirect_target():
    # Проверяет есть ли в запросе параметр 'next'
    for target in request.values.get('next'), request.referrer:
        if not target:
            redirect(url_for('gsc.index'))
        if is_safe_url(target):
            return target
