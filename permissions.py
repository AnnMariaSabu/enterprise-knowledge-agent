ROLES = ["Employee", "HR", "IT", "Admin"]


def search_filter(role):
    if role == "Employee":
        return {"access": "public"}
    elif role == "HR":
        return {"$or": [{"access": "public"}, {"department": "hr"}]}
    elif role == "IT":
        return {"$or": [{"access": "public"}, {"department": "it"}]}
    elif role == "Admin":
        return None
    else:
        raise ValueError(f"Unknown role: {role}")


def managed_departments(role):
    if role == "HR":
        return ["hr"]
    elif role == "IT":
        return ["it"]
    elif role == "Admin":
        return ["hr", "it", "travel"]
    else:
        return []


if __name__ == "__main__":
    for role in ROLES:
        print(role)
        print("   search filter:", search_filter(role))
        print("   can manage:   ", managed_departments(role))