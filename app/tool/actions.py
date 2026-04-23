def subscribe_user(name, email, plan, platform):
    print("🔥 SUBSCRIBING USER:")
    print(f"Name: {name}")
    print(f"Email: {email}")
    print(f"Plan: {plan}")
    print(f"Platform: {platform}")

    return {
        "status": "success",
        "message": f"{name} subscribed to {plan} plan 🎉"
    }