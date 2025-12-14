import json
from pathlib import Path

# --------------------------------------------------
# CONFIG
# --------------------------------------------------
BASE_DIR = Path(__file__).parent
MANIFEST_PATH = BASE_DIR / "manifest.json"

RUN_DIR = Path(r"C:\Users\Aditya Shastri\run\my_new_project\models")

# --------------------------------------------------
# LOAD MANIFEST
# --------------------------------------------------
with MANIFEST_PATH.open(encoding="utf-8") as f:
    manifest = json.load(f)

nodes = manifest.get("nodes", {})

if not RUN_DIR.exists():
    raise FileNotFoundError(f"Run directory not found: {RUN_DIR}")

print(f"Using run directory: {RUN_DIR}\n")

# --------------------------------------------------
# GENERATE DDL
# --------------------------------------------------
for node_id, node in nodes.items():

    # Only dbt models
    if node.get("resource_type") != "model":
        continue

    model_name = node["name"]
    materialized = node.get("config", {}).get("materialized", "view")

    # MySQL object name (schema.table)
    schema = node.get("schema")
    alias = node.get("alias") or model_name

    mysql_relation = f"{schema}.{alias}" if schema else alias

    # Find compiled SQL file
    original_path = Path(node["original_file_path"])
    compiled_sql_path = RUN_DIR / original_path.with_suffix(".sql").name

    if not compiled_sql_path.exists():
        print(f"Skipping {model_name}: compiled SQL not found")
        continue

    sql = compiled_sql_path.read_text(encoding="utf-8").strip()

    if not sql:
        print(f"Skipping {model_name}: empty SQL")
        continue

    # --------------------------------------------------
    # MySQL DDL
    # --------------------------------------------------
    if materialized == "view":
        ddl = f"""
CREATE OR REPLACE VIEW {mysql_relation} AS
{sql};
""".strip()
    else:
        ddl = f"""
CREATE TABLE {mysql_relation} AS
{sql};
""".strip()

    print("=" * 80)
    print(f"Model        : {model_name}")
    print(f"Materialized : {materialized}")
    print(f"MySQL Object : {mysql_relation}")
    print("-" * 80)
    print(ddl)
    print()
