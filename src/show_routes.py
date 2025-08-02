from create_app import create_app

app = create_app()

with app.app_context():
    # In ra danh sách các route của ứng dụng
    print("Danh sách các route của ứng dụng:")
    for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint}: {rule.rule} [{', '.join(rule.methods)}]")
