"""Member management (owner: Member 3).

A member is a dict:
    {"id": 1, "name": "...", "email": "...", "phone": "..."}
"""
from library.storage import next_id


def _find(data, member_id):
    for member in data["members"]:
        if member["id"] == member_id:
            return member
    raise ValueError(f"No member with id {member_id}.")


def _valid_email(email):
    return "@" in email and "." in email.split("@")[-1]


def register_member(data, name, email, phone=""):
    """Register a new member with a unique id and return it."""
    name, email, phone = name.strip(), email.strip().lower(), phone.strip()
    if not name:
        raise ValueError("Name is required.")
    if not _valid_email(email):
        raise ValueError("Please enter a valid email address.")
    if any(m["email"] == email for m in data["members"]):
        raise ValueError(f"A member with email {email} already exists.")
    member = {"id": next_id(data["members"]), "name": name,
              "email": email, "phone": phone}
    data["members"].append(member)
    return member


def edit_member(data, member_id, **changes):
    """Update name, email or phone. Empty/None values are ignored."""
    member = _find(data, member_id)
    for field, value in changes.items():
        if field not in ("name", "email", "phone"):
            raise ValueError(f"Cannot edit field '{field}'.")
        if value is None or value == "":
            continue
        if field == "email":
            value = value.strip().lower()
            if not _valid_email(value):
                raise ValueError("Please enter a valid email address.")
            if any(m["email"] == value and m["id"] != member_id
                   for m in data["members"]):
                raise ValueError(f"A member with email {value} already exists.")
        member[field] = value
    return member


def remove_member(data, member_id):
    """Remove a member. Refuses if they still have unreturned books."""
    member = _find(data, member_id)
    if any(l["member_id"] == member_id and l["returned"] is None
           for l in data["loans"]):
        raise ValueError("Cannot remove a member who still has books on loan.")
    data["members"].remove(member)
    return member


def find_member(data, keyword):
    """Return members whose name or email contains keyword (case-insensitive)."""
    kw = keyword.strip().lower()
    return [m for m in data["members"]
            if kw in m["name"].lower() or kw in m["email"]]


def list_members(data):
    """Return all members."""
    return list(data["members"])
