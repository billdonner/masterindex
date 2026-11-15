"""Non-destructive checks for the Project Intake capture/confirmation boundary."""

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from project_intake import IntakeError, ProjectIntakeStore  # noqa: E402


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding="utf-8")


def main():
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        write(root / "current" / "index.json", {"entities": [{"id": "existing-app", "name": "Existing"}], "repos": []})
        write(root / "tasks" / "index.json", {"entryTasks": {}})
        (root / "current" / "inventory.md").write_text("# Inventory\n", encoding="utf-8")
        write(root / "intake" / "index.json", {
            "generatedAt": "2026-01-01T00:00:00Z", "schemaVersion": "1.0",
            "defaults": {"githubOwner": "billdonner", "visibility": "private", "workspaceParent": "~", "entityKind": "project", "entityStatus": "incubating"}, "projects": []
        })
        store = ProjectIntakeStore(root, root / "projects")
        project = store.capture(name="Pantry Pal", purpose="A shared household pantry and shopping-list app.")
        assert project["id"] == "pantry-pal-project"
        assert store.list_projects()[0]["state"] == "captured"
        assert store.provisioning_plan(project["id"])["confirmationRequired"] == "Pantry Pal"
        try:
            store.provision(project_id=project["id"], confirmation="not the name", create_github=False)
        except IntakeError as error:
            assert "exactly match" in str(error)
        else:
            raise AssertionError("Provisioning should require exact confirmation")
        try:
            store.capture(name="Pantry Pal", purpose="Another description that is long enough.")
        except IntakeError as error:
            assert "already uses" in str(error)
        else:
            raise AssertionError("Duplicate project slugs must be refused")
    print("Project Intake tests passed")


if __name__ == "__main__":
    main()
