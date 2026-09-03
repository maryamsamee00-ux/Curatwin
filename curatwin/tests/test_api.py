from tests.conftest import client, register_user, get_token, auth_header


# ============= AUTH TESTS =============

class TestAuth:
    def test_register_success(self):
        res = register_user()
        assert res.status_code == 200
        data = res.json()
        assert "access_token" in data
        assert data["user"]["name"] == "Test Student"
        assert data["user"]["email"] == "test@university.edu"

    def test_register_duplicate_email(self):
        register_user()
        res = register_user()
        assert res.status_code == 400
        assert "already exists" in res.json()["detail"]

    def test_register_password_mismatch(self):
        res = client.post("/api/auth/register", json={
            "name": "Test", "email": "test2@uni.edu",
            "password": "SecurePass123", "confirm_password": "DifferentPass"
        })
        assert res.status_code == 400
        assert "do not match" in res.json()["detail"]

    def test_register_short_password(self):
        res = client.post("/api/auth/register", json={
            "name": "Test", "email": "test2@uni.edu",
            "password": "short", "confirm_password": "short"
        })
        assert res.status_code == 400
        assert "8 characters" in res.json()["detail"]

    def test_register_invalid_email(self):
        res = client.post("/api/auth/register", json={
            "name": "Test", "email": "not-an-email",
            "password": "SecurePass123", "confirm_password": "SecurePass123"
        })
        assert res.status_code == 422

    def test_login_success(self):
        register_user()
        res = client.post("/api/auth/login", json={
            "email": "test@university.edu", "password": "SecurePass123"
        })
        assert res.status_code == 200
        assert "access_token" in res.json()

    def test_login_wrong_password(self):
        register_user()
        res = client.post("/api/auth/login", json={
            "email": "test@university.edu", "password": "WrongPassword"
        })
        assert res.status_code == 401

    def test_login_nonexistent_user(self):
        res = client.post("/api/auth/login", json={
            "email": "nobody@uni.edu", "password": "anything"
        })
        assert res.status_code == 401

    def test_logout(self):
        register_user()
        token = get_token()
        res = client.post("/api/auth/logout", headers=auth_header(token))
        assert res.status_code == 200

    def test_me_endpoint(self):
        register_user()
        token = get_token()
        res = client.get("/api/auth/me", headers=auth_header(token))
        assert res.status_code == 200
        assert res.json()["email"] == "test@university.edu"


# ============= SECURITY TESTS =============

class TestSecurity:
    def test_protected_endpoint_without_auth(self):
        res = client.get("/api/users/profile")
        assert res.status_code == 403 or res.status_code == 401

    def test_cross_user_isolation(self):
        register_user("Alice", "alice@uni.edu", "Pass12345678")
        register_user("Bob", "bob@uni.edu", "Pass12345678")

        token_a = get_token("alice@uni.edu", "Pass12345678")
        token_b = get_token("bob@uni.edu", "Pass12345678")

        client.post("/api/mood/checkin", json={
            "mood": 0.9, "perceived_stress": 0.1, "sleep_quality": 0.8,
            "energy_level": 0.85, "notes": "Alice's private note"
        }, headers=auth_header(token_a))

        res_b = client.get("/api/mood/checkins", headers=auth_header(token_b))
        assert res_b.status_code == 200
        assert len(res_b.json()) == 0

        res_a = client.get("/api/mood/checkins", headers=auth_header(token_a))
        assert len(res_a.json()) == 1
        assert res_a.json()[0]["notes"] == "Alice's private note"

    def test_invalid_token_rejected(self):
        res = client.get("/api/users/profile", headers={"Authorization": "Bearer invalid-token"})
        assert res.status_code == 401


# ============= PROFILE TESTS =============

class TestProfile:
    def test_get_profile(self):
        register_user()
        token = get_token()
        res = client.get("/api/users/profile", headers=auth_header(token))
        assert res.status_code == 200
        assert res.json()["age_range"] == "21-24"

    def test_update_profile(self):
        register_user()
        token = get_token()
        res = client.put("/api/users/profile", json={
            "university": "LUMS", "onboarding_complete": 1
        }, headers=auth_header(token))
        assert res.status_code == 200
        assert res.json()["university"] == "LUMS"
        assert res.json()["onboarding_complete"] == 1


# ============= WELLNESS/TELEMETRY TESTS =============

class TestWellness:
    def test_ingest_telemetry(self):
        register_user()
        token = get_token()
        res = client.post("/api/wellness/telemetry", json={
            "ppg_hrv": 60, "gsr_amplitude": 4.5, "skin_temp": 36.6,
            "imu_activity": 0.4, "heart_rate": 72, "source": "simulator"
        }, headers=auth_header(token))
        assert res.status_code == 200
        assert res.json()["ppg_hrv"] == 60

    def test_get_telemetry(self):
        register_user()
        token = get_token()
        client.post("/api/wellness/telemetry", json={"ppg_hrv": 55}, headers=auth_header(token))
        client.post("/api/wellness/telemetry", json={"ppg_hrv": 65}, headers=auth_header(token))
        res = client.get("/api/wellness/telemetry", headers=auth_header(token))
        assert res.status_code == 200
        assert len(res.json()) == 2


# ============= STRESS PREDICTION TESTS =============

class TestStress:
    def test_stress_prediction_low(self):
        register_user()
        token = get_token()
        res = client.post("/api/stress/predict", json={
            "ppg_hrv": 80, "gsr_amplitude": 2, "skin_temp": 36.5,
            "imu_activity": 0.2, "self_report_stress": 0.1
        }, headers=auth_header(token))
        assert res.status_code == 200
        data = res.json()
        assert data["stress_level"] in ["low", "moderate", "high"]
        assert 0 <= data["confidence"] <= 1
        assert data["model_version"] == "1.0.0"

    def test_stress_prediction_high(self):
        register_user()
        token = get_token()
        res = client.post("/api/stress/predict", json={
            "ppg_hrv": 15, "gsr_amplitude": 9, "skin_temp": 37.5,
            "imu_activity": 0.9, "self_report_stress": 0.95
        }, headers=auth_header(token))
        assert res.status_code == 200
        data = res.json()
        assert data["stress_level"] == "high"
        assert data["confidence"] > 0.5

    def test_stress_prediction_moderate(self):
        register_user()
        token = get_token()
        res = client.post("/api/stress/predict", json={
            "ppg_hrv": 50, "gsr_amplitude": 5, "skin_temp": 36.7,
            "imu_activity": 0.5, "self_report_stress": 0.5
        }, headers=auth_header(token))
        assert res.status_code == 200
        assert res.json()["stress_level"] in ["low", "moderate", "high"]

    def test_stress_history(self):
        register_user()
        token = get_token()
        for _ in range(3):
            client.post("/api/stress/predict", json={
                "ppg_hrv": 50, "gsr_amplitude": 5, "skin_temp": 36.5,
                "imu_activity": 0.3, "self_report_stress": 0.5
            }, headers=auth_header(token))
        res = client.get("/api/stress/history", headers=auth_header(token))
        assert res.status_code == 200
        assert len(res.json()) == 3

    def test_current_stress_empty(self):
        register_user()
        token = get_token()
        res = client.get("/api/stress/current", headers=auth_header(token))
        assert res.status_code == 200
        assert res.json()["stress_level"] == "unknown"


# ============= DIGITAL TWIN TESTS =============

class TestDigitalTwin:
    def test_twin_state_no_data(self):
        register_user()
        token = get_token()
        res = client.get("/api/digital-twin/state", headers=auth_header(token))
        assert res.status_code == 200
        data = res.json()
        assert "digital_twin" in data
        assert "affective_state" in data
        assert data["digital_twin"]["state"] == "moderate"
        assert data["affective_state"]["affective_state"] == "insufficient_data"

    def test_twin_state_with_data(self):
        register_user()
        token = get_token()
        # Add wellness data
        client.post("/api/wellness/telemetry", json={
            "ppg_hrv": 80, "gsr_amplitude": 2, "skin_temp": 36.5,
            "imu_activity": 0.2, "heart_rate": 65
        }, headers=auth_header(token))
        # Add mood checkin
        client.post("/api/mood/checkin", json={
            "mood": 0.8, "perceived_stress": 0.2, "sleep_quality": 0.9, "energy_level": 0.85
        }, headers=auth_header(token))
        # Add stress prediction
        client.post("/api/stress/predict", json={
            "ppg_hrv": 80, "gsr_amplitude": 2, "skin_temp": 36.5,
            "imu_activity": 0.2, "self_report_stress": 0.1
        }, headers=auth_header(token))

        res = client.get("/api/digital-twin/state", headers=auth_header(token))
        assert res.status_code == 200
        twin = res.json()["digital_twin"]
        assert twin["data_points_wellness"] >= 1
        assert twin["data_points_mood"] >= 1


# ============= MOOD CHECKIN TESTS =============

class TestMood:
    def test_create_checkin(self):
        register_user()
        token = get_token()
        res = client.post("/api/mood/checkin", json={
            "mood": 0.7, "perceived_stress": 0.3, "sleep_quality": 0.8,
            "energy_level": 0.75, "symptoms": "mild headache",
            "notes": "Feeling okay today"
        }, headers=auth_header(token))
        assert res.status_code == 200
        data = res.json()
        assert data["mood"] == 0.7
        assert data["notes"] == "Feeling okay today"

    def test_get_checkins(self):
        register_user()
        token = get_token()
        for i in range(3):
            client.post("/api/mood/checkin", json={
                "mood": 0.5 + i * 0.1, "perceived_stress": 0.5,
                "sleep_quality": 0.5, "energy_level": 0.5
            }, headers=auth_header(token))
        res = client.get("/api/mood/checkins", headers=auth_header(token))
        assert res.status_code == 200
        assert len(res.json()) == 3


# ============= CYCLE TESTS =============

class TestCycle:
    def test_add_cycle_record(self):
        register_user()
        token = get_token()
        res = client.post("/api/cycle/records", json={
            "cycle_start": "2026-08-15", "cycle_length": 28,
            "symptoms": "cramps, fatigue", "mood_observations": "irritable"
        }, headers=auth_header(token))
        assert res.status_code == 200
        data = res.json()
        assert data["cycle_length"] == 28
        assert data["estimated_phase"] != ""
        assert data["symptoms"] == "cramps, fatigue"

    def test_get_cycle_records(self):
        register_user()
        token = get_token()
        client.post("/api/cycle/records", json={
            "cycle_start": "2026-08-01", "cycle_length": 28
        }, headers=auth_header(token))
        res = client.get("/api/cycle/records", headers=auth_header(token))
        assert res.status_code == 200
        assert len(res.json()) == 1

    def test_update_cycle_record(self):
        register_user()
        token = get_token()
        create_res = client.post("/api/cycle/records", json={
            "cycle_start": "2026-08-01", "cycle_length": 28
        }, headers=auth_header(token))
        record_id = create_res.json()["id"]

        res = client.put(f"/api/cycle/records/{record_id}", json={
            "symptoms": "updated symptoms"
        }, headers=auth_header(token))
        assert res.status_code == 200
        assert res.json()["symptoms"] == "updated symptoms"

    def test_current_cycle_empty(self):
        register_user()
        token = get_token()
        res = client.get("/api/cycle/current", headers=auth_header(token))
        assert res.status_code == 200
        assert "message" in res.json()


# ============= COPING TESTS =============

class TestCoping:
    def test_get_recommendations(self):
        register_user()
        token = get_token()
        res = client.get("/api/coping/recommendations", headers=auth_header(token))
        assert res.status_code == 200
        data = res.json()
        assert "recommendations" in data
        assert len(data["recommendations"]) >= 1

    def test_get_library(self):
        register_user()
        token = get_token()
        res = client.get("/api/coping/library", headers=auth_header(token))
        assert res.status_code == 200
        cats = res.json()["categories"]
        assert "breathing" in cats
        assert "mindfulness" in cats
        assert "cbt_reframing" in cats
        assert len(cats) == 9

    def test_coping_history(self):
        register_user()
        token = get_token()
        client.get("/api/coping/recommendations", headers=auth_header(token))
        res = client.get("/api/coping/history", headers=auth_header(token))
        assert res.status_code == 200
        assert len(res.json()) >= 1


# ============= INSIGHTS TESTS =============

class TestInsights:
    def test_overview_no_data(self):
        register_user()
        token = get_token()
        res = client.get("/api/insights/overview", headers=auth_header(token))
        assert res.status_code == 200
        assert res.json()["has_data"] is False

    def test_overview_with_data(self):
        register_user()
        token = get_token()
        client.post("/api/mood/checkin", json={
            "mood": 0.7, "perceived_stress": 0.3, "sleep_quality": 0.8, "energy_level": 0.75
        }, headers=auth_header(token))
        client.post("/api/stress/predict", json={
            "ppg_hrv": 60, "gsr_amplitude": 4, "skin_temp": 36.5,
            "imu_activity": 0.3, "self_report_stress": 0.3
        }, headers=auth_header(token))

        res = client.get("/api/insights/overview", headers=auth_header(token))
        assert res.status_code == 200
        data = res.json()
        assert data["has_data"] is True
        assert "avg_mood" in data
        assert "stress_distribution" in data

    def test_stress_trend(self):
        register_user()
        token = get_token()
        client.post("/api/stress/predict", json={
            "ppg_hrv": 50, "gsr_amplitude": 5, "skin_temp": 36.5,
            "imu_activity": 0.3, "self_report_stress": 0.5
        }, headers=auth_header(token))
        res = client.get("/api/insights/stress-trend", headers=auth_header(token))
        assert res.status_code == 200
        assert res.json()["count"] >= 1


# ============= GUARDIAN & CONSENT TESTS =============

class TestGuardianConsent:
    def test_add_guardian(self):
        register_user()
        token = get_token()
        res = client.post("/api/guardians/", json={
            "guardian_name": "Mother", "guardian_contact": "mother@email.com",
            "relationship": "parent"
        }, headers=auth_header(token))
        assert res.status_code == 200
        data = res.json()
        assert data["guardian_name"] == "Mother"
        assert data["verification_status"] == "pending"
        assert len(data["verification_code"]) == 6

    def test_verify_guardian(self):
        register_user()
        token = get_token()
        create_res = client.post("/api/guardians/", json={
            "guardian_name": "Father", "guardian_contact": "father@email.com",
            "relationship": "parent"
        }, headers=auth_header(token))
        gid = create_res.json()["id"]
        code = create_res.json()["verification_code"]

        res = client.post(f"/api/guardians/{gid}/verify", json={
            "verification_code": code
        }, headers=auth_header(token))
        assert res.status_code == 200
        assert res.json()["verification_status"] == "verified"

    def test_verify_wrong_code(self):
        register_user()
        token = get_token()
        create_res = client.post("/api/guardians/", json={
            "guardian_name": "Sister", "guardian_contact": "sis@email.com",
            "relationship": "sibling"
        }, headers=auth_header(token))
        gid = create_res.json()["id"]

        res = client.post(f"/api/guardians/{gid}/verify", json={
            "verification_code": "000000"
        }, headers=auth_header(token))
        assert res.status_code == 400

    def test_consent_flow(self):
        register_user()
        token = get_token()
        # Add and verify guardian
        create_res = client.post("/api/guardians/", json={
            "guardian_name": "Mom", "guardian_contact": "mom@email.com",
            "relationship": "parent"
        }, headers=auth_header(token))
        gid = create_res.json()["id"]
        code = create_res.json()["verification_code"]
        client.post(f"/api/guardians/{gid}/verify", json={
            "verification_code": code
        }, headers=auth_header(token))

        # Grant consent
        res = client.post("/api/consent/", json={
            "guardian_id": gid, "permission_type": "stress_level", "enabled": 1
        }, headers=auth_header(token))
        assert res.status_code == 200
        consent_id = res.json()["id"]
        assert res.json()["enabled"] == 1

        # Revoke consent
        res = client.put(f"/api/consent/{consent_id}", json={
            "enabled": 0
        }, headers=auth_header(token))
        assert res.status_code == 200
        assert res.json()["enabled"] == 0

    def test_delete_guardian(self):
        register_user()
        token = get_token()
        create_res = client.post("/api/guardians/", json={
            "guardian_name": "Friend", "guardian_contact": "friend@email.com",
            "relationship": "friend"
        }, headers=auth_header(token))
        gid = create_res.json()["id"]

        res = client.delete(f"/api/guardians/{gid}", headers=auth_header(token))
        assert res.status_code == 200

        list_res = client.get("/api/guardians/", headers=auth_header(token))
        assert len(list_res.json()) == 0


# ============= EMERGENCY ALERT TESTS =============

class TestEmergency:
    def test_emergency_no_guardians(self):
        register_user()
        token = get_token()
        res = client.post("/api/alerts/emergency", headers=auth_header(token))
        assert res.status_code == 400
        assert "No verified guardians" in res.json()["detail"]

    def test_emergency_with_verified_guardian(self):
        register_user()
        token = get_token()
        # Setup verified guardian with consent
        create_res = client.post("/api/guardians/", json={
            "guardian_name": "Mom", "guardian_contact": "mom@email.com",
            "relationship": "parent"
        }, headers=auth_header(token))
        gid = create_res.json()["id"]
        code = create_res.json()["verification_code"]
        client.post(f"/api/guardians/{gid}/verify", json={
            "verification_code": code
        }, headers=auth_header(token))
        client.post("/api/consent/", json={
            "guardian_id": gid, "permission_type": "stress_level", "enabled": 1
        }, headers=auth_header(token))

        # Trigger emergency
        res = client.post("/api/alerts/emergency", headers=auth_header(token))
        assert res.status_code == 200
        data = res.json()
        assert len(data["alerts"]) == 1
        assert data["alerts"][0]["status"] == "triggered"

    def test_alert_history(self):
        register_user()
        token = get_token()
        # Setup + trigger
        create_res = client.post("/api/guardians/", json={
            "guardian_name": "Dad", "guardian_contact": "dad@email.com",
            "relationship": "parent"
        }, headers=auth_header(token))
        gid = create_res.json()["id"]
        code = create_res.json()["verification_code"]
        client.post(f"/api/guardians/{gid}/verify", json={
            "verification_code": code
        }, headers=auth_header(token))
        client.post("/api/alerts/emergency", headers=auth_header(token))

        res = client.get("/api/alerts/history", headers=auth_header(token))
        assert res.status_code == 200
        assert len(res.json()["alerts"]) >= 1


# ============= AI MODEL TESTS =============

class TestAIModel:
    def test_model_version_tracked(self):
        register_user()
        token = get_token()
        res = client.post("/api/stress/predict", json={
            "ppg_hrv": 50, "gsr_amplitude": 5, "skin_temp": 36.5,
            "imu_activity": 0.3, "self_report_stress": 0.5
        }, headers=auth_header(token))
        assert res.json()["model_version"] == "1.0.0"

    def test_multiple_scenarios(self):
        register_user()
        token = get_token()
        scenarios = [
            {"ppg_hrv": 85, "gsr_amplitude": 1.5, "skin_temp": 36.3, "imu_activity": 0.1, "self_report_stress": 0.05},
            {"ppg_hrv": 50, "gsr_amplitude": 5.0, "skin_temp": 36.6, "imu_activity": 0.4, "self_report_stress": 0.5},
            {"ppg_hrv": 12, "gsr_amplitude": 9.5, "skin_temp": 37.8, "imu_activity": 0.95, "self_report_stress": 0.98},
        ]
        results = []
        for s in scenarios:
            res = client.post("/api/stress/predict", json=s, headers=auth_header(token))
            assert res.status_code == 200
            results.append(res.json()["stress_level"])

        assert results[2] == "high"

    def test_confidence_score(self):
        register_user()
        token = get_token()
        res = client.post("/api/stress/predict", json={
            "ppg_hrv": 10, "gsr_amplitude": 10, "skin_temp": 38,
            "imu_activity": 1.0, "self_report_stress": 1.0
        }, headers=auth_header(token))
        assert res.json()["confidence"] > 0.7


# ============= END-TO-END WORKFLOW TEST =============

class TestEndToEnd:
    def test_full_workflow(self):
        # Register
        res = register_user("Sara", "sara@uni.edu", "MySecurePass1")
        assert res.status_code == 200
        token = get_token("sara@uni.edu", "MySecurePass1")

        # Complete profile
        client.put("/api/users/profile", json={
            "university": "NUST", "onboarding_complete": 1
        }, headers=auth_header(token))

        # Submit telemetry
        client.post("/api/wellness/telemetry", json={
            "ppg_hrv": 65, "gsr_amplitude": 4, "skin_temp": 36.5,
            "imu_activity": 0.3, "heart_rate": 70
        }, headers=auth_header(token))

        # Get stress prediction
        stress_res = client.post("/api/stress/predict", json={
            "ppg_hrv": 65, "gsr_amplitude": 4, "skin_temp": 36.5,
            "imu_activity": 0.3, "self_report_stress": 0.4
        }, headers=auth_header(token))
        assert stress_res.status_code == 200

        # Daily checkin
        client.post("/api/mood/checkin", json={
            "mood": 0.6, "perceived_stress": 0.4, "sleep_quality": 0.7,
            "energy_level": 0.65, "notes": "Exams coming up"
        }, headers=auth_header(token))

        # Add cycle record
        client.post("/api/cycle/records", json={
            "cycle_start": "2026-08-20", "cycle_length": 28,
            "symptoms": "mild cramps"
        }, headers=auth_header(token))

        # Get Digital Twin state
        twin_res = client.get("/api/digital-twin/state", headers=auth_header(token))
        assert twin_res.status_code == 200
        twin = twin_res.json()
        assert twin["digital_twin"]["data_points_wellness"] >= 1
        assert twin["digital_twin"]["data_points_mood"] >= 1

        # Get insights
        insights_res = client.get("/api/insights/overview", headers=auth_header(token))
        assert insights_res.status_code == 200
        assert insights_res.json()["has_data"] is True

        # Get coping recommendations
        coping_res = client.get("/api/coping/recommendations", headers=auth_header(token))
        assert coping_res.status_code == 200
        assert len(coping_res.json()["recommendations"]) >= 1

        # Setup guardian
        g_res = client.post("/api/guardians/", json={
            "guardian_name": "Amma", "guardian_contact": "amma@email.com",
            "relationship": "parent"
        }, headers=auth_header(token))
        gid = g_res.json()["id"]
        code = g_res.json()["verification_code"]
        client.post(f"/api/guardians/{gid}/verify", json={
            "verification_code": code
        }, headers=auth_header(token))

        # Grant consent
        client.post("/api/consent/", json={
            "guardian_id": gid, "permission_type": "wellness_summary", "enabled": 1
        }, headers=auth_header(token))

        # Trigger emergency
        alert_res = client.post("/api/alerts/emergency", headers=auth_header(token))
        assert alert_res.status_code == 200
        assert len(alert_res.json()["alerts"]) == 1

        # Verify alert history
        history_res = client.get("/api/alerts/history", headers=auth_header(token))
        assert len(history_res.json()["alerts"]) == 1
