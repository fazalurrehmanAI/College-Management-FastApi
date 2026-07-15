from college_api.main import app   # Change if needed

for route in app.routes:
    if hasattr(route, "methods"):
        print("=" * 60)
        print("Endpoint :", route.path)
        print("Methods  :", ", ".join(route.methods))
        print("Name     :", route.name)

        if route.endpoint.__annotations__:
            print("Parameters:")
            for k, v in route.endpoint.__annotations__.items():
                print(f"  {k}: {v}")

        print()