import json
import os
from github import Github
import streamlit as st
import uuid
from datetime import datetime

# GitHub setup
g = Github(st.secrets["GITHUB_TOKEN"])
repo = g.get_repo(st.secrets["REPO_NAME"])

def load_data(file_path):
    if file_path not in ("checklist.json", "change_log.json"):
        return None
    try:
        content = repo.get_contents(file_path)
        data = json.loads(content.decoded_content.decode())
    except:
        data = {"records": []} if file_path == "checklist.json" else {"logs": []}
    return data

def save_data(file_path, data):
    try:
        content = repo.get_contents(file_path)
        repo.update_file(file_path, f"Update {file_path}", json.dumps(data, indent=2), content.sha)
    except:
        repo.create_file(file_path, f"Create {file_path}", json.dumps(data, indent=2))

# Checklist CRUD operations
def create_checklist_record(record):
    data = load_data("checklist.json")
    new_record = {
        "id": str(len(data["records"]) + 1),
        "location": record.get("location", ""),
        "element": record.get("element", ""),
        "eventDetectorName": record.get("eventDetectorName", ""),
        "date": record.get("date", datetime.now().isoformat()),
        "rating": record.get("rating", ""),
        "responsiblePerson": record.get("responsiblePerson", ""),
        "expectedRepairDate": record.get("expectedRepairDate", ""),
        "actualRepairDate": record.get("actualRepairDate", ""),
        "image": record.get("image", ""),
        "comment": record.get("comment", ""),
        "highRisk": record.get("highRisk", "")
    }
    data["records"].append(new_record)
    save_data("checklist.json", data)
    return new_record

def update_checklist_record(record_id, updated_data):
    data = load_data("checklist.json")
    for record in data["records"]:
        if record["id"] == record_id:
            record.update(updated_data)
            save_data("checklist.json", data)
            return record
    return None

def delete_checklist_record(record_id):
    data = load_data("checklist.json")
    data["records"] = [record for record in data["records"] if record["id"] != record_id]
    save_data("checklist.json", data)

# Change Log CRUD operations
def create_change_log_entry(entry):
    data = load_data("change_log.json")
    new_entry = {
        "id": str(len(data["logs"]) + 1),
        "modifierName": entry.get("modifierName", ""),
        "modificationDate": entry.get("modificationDate", datetime.now().isoformat()),
        "modificationType": entry.get("modificationType", ""),
        "newDate": entry.get("newDate", "")
    }
    data["logs"].append(new_entry)
    save_data("change_log.json", data)
    return new_entry

def update_change_log_entry(entry_id, updated_data):
    data = load_data("change_log.json")
    for entry in data["logs"]:
        if entry["id"] == entry_id:
            entry.update(updated_data)
            save_data("change_log.json", data)
            return entry
    return None

def delete_change_log_entry(entry_id):
    data = load_data("change_log.json")
    data["logs"] = [entry for entry in data["logs"] if entry["id"] != entry_id]
    save_data("change_log.json", data)