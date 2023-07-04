from django.urls import reverse


def assert_view_requires_login(client, *, view_name: str, params_dict: dict = None):
    client.logout()
    path = reverse(view_name, kwargs=params_dict) if params_dict else reverse(view_name)
    response = client.get(path)
    print(response.content.decode('utf-8'))
    assert response.status_code == 302
    assert 'accounts/login' in response.url


def assert_view_renders_template(client, *, view_name: str, template_name: str, params_dict: dict = None, user: object = None):
    path = reverse(view_name, kwargs=params_dict) if params_dict else reverse(view_name)
    client.logout()  # logging out so I log in right user
    client.force_login(user)
    response = client.get(path)
    assert response.status_code == 200
    names = (t.name for t in response.templates)
    print(*names)
    assert template_name in (t.name for t in response.templates)
