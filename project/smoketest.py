# smoketest.py
import requests

def run_smoketest():
    base_url = "http://localhost:5001"
    username = "smoketestuser"
    password = "smokepass"
    new_password = "newsmokepass"

    session = requests.Session()

    # 1. Healthcheck
    health = requests.get(f"{base_url}/healthcheck")
    assert health.status_code == 200
    assert health.json()["status"] == "ok"
    print("✅ Healthcheck passed")

    # 2. Create user
    user_data = {"username": username, "password": password}
    create_user = session.post(f"{base_url}/create-account", json=user_data)
    assert create_user.status_code in [201, 400]
    print("✅ Account creation attempted (success or already exists)")

    # 3. Login
    login = session.post(f"{base_url}/login", json=user_data)
    assert login.status_code == 200, f"Login failed: {login.text}"
    assert login.json()["message"] == "Login successful"
    print("✅ Login passed")

    # 4. Update password
    update_resp = session.post(f"{base_url}/update-password", json={"new_password": new_password})
    assert update_resp.status_code == 200, f"Update failed: {update_resp.text}"
    print("✅ Password update passed")

    # 5. Logout
    logout = session.post(f"{base_url}/logout")
    assert logout.status_code == 200
    print("✅ Logout passed")

    # 6. Login with new password
    relogin = session.post(f"{base_url}/login", json={"username": username, "password": new_password})
    assert relogin.status_code == 200, f"Relogin failed: {relogin.text}"
    print("✅ Relogin with new password passed")

    # 7. Delete account
    delete_resp = session.delete(f"{base_url}/delete-account")
    assert delete_resp.status_code == 200
    print("✅ Account deletion passed")


if __name__ == "__main__":
    run_smoketest()