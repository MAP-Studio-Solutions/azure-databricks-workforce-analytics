from __future__ import annotations
from pathlib import Path
from datetime import date, datetime, timedelta
import random
import pandas as pd
from faker import Faker
import argparse

# Initialize Faker for fake company names and set random seed for reproducibility
fake = Faker()
random.seed(42)


def ensure_dirs(out: Path):
    # Create output directories for each data type if they don't exist
    (out / "hr_events").mkdir(parents=True, exist_ok=True)
    (out / "headcount").mkdir(parents=True, exist_ok=True)
    (out / "org").mkdir(parents=True, exist_ok=True)


# Generate n org units, each with a possible parent (first 3 are top-level)
def gen_org(n=25):
    orgs = [f"ORG{str(i+1).zfill(3)}" for i in range(n)]
    rows = []
    for org_id in orgs:
        parent = None if org_id in orgs[:3] else random.choice(orgs[:3])
        rows.append(
            {"org_id": org_id, "org_name": f"{fake.company()} Dept", "parent_org_id": parent}
        )
    return pd.DataFrame(rows)


# Generate n employee IDs
def gen_employees(n=500):
    return [f"E{str(i+1).zfill(6)}" for i in range(n)]


# Generate HR events (hire, org change, termination) for each employee
def gen_hr_events(emps, orgs, start_dt=date(2023, 1, 1), end_dt=date(2025, 12, 31)):
    job_profiles = ["Analyst", "Engineer", "Manager", "Director", "Specialist"]
    locations = ["Remote", "Nashville", "Chattanooga", "Knoxville", "Memphis"]
    rows = []
    for emp in emps:
        hire_dt = start_dt + timedelta(days=random.randint(0, 365))
        current_org = random.choice(orgs)
        # HIRE event
        rows.append(
            {
                "employee_id": emp,
                "event_ts": datetime.combine(hire_dt, datetime.min.time()).isoformat(),
                "event_type": "HIRE",
                "org_id": current_org,
                "job_profile": random.choice(job_profiles),
                "location": random.choice(locations),
                "manager_id": random.choice(emps),
            }
        )
        # 0-2 ORG_CHANGE events
        for _ in range(random.randint(0, 2)):
            move_dt = hire_dt + timedelta(days=random.randint(30, 500))
            if move_dt > end_dt:
                continue
            current_org = random.choice(orgs)
            rows.append(
                {
                    "employee_id": emp,
                    "event_ts": datetime.combine(move_dt, datetime.min.time()).isoformat(),
                    "event_type": "ORG_CHANGE",
                    "org_id": current_org,
                    "job_profile": random.choice(job_profiles),
                    "location": random.choice(locations),
                    "manager_id": random.choice(emps),
                }
            )
        # Optional TERMINATION event (15% chance)
        if random.random() < 0.15:
            term_dt = hire_dt + timedelta(days=random.randint(120, 900))
            if term_dt <= end_dt:
                rows.append(
                    {
                        "employee_id": emp,
                        "event_ts": datetime.combine(term_dt, datetime.min.time()).isoformat(),
                        "event_type": "TERMINATION",
                        "org_id": current_org,
                        "job_profile": random.choice(job_profiles),
                        "location": random.choice(locations),
                        "manager_id": random.choice(emps),
                    }
                )
    return pd.DataFrame(rows)


# Generate monthly headcount snapshots for each employee, with a small chance of termination each month
def gen_headcount_snapshots(emps, orgs, start_month=date(2023, 1, 1), months=36):
    rows = []
    d = start_month
    active = set(emps)
    for _ in range(months):
        snap_date = date(d.year, d.month, 1)
        # Randomly remove some employees to simulate attrition
        for emp in list(active):
            if random.random() < 0.005:
                active.remove(emp)
        # Assign each active employee to a random org for the snapshot
        for emp in active:
            rows.append(
                {
                    "snapshot_date": snap_date.isoformat(),
                    "employee_id": emp,
                    "org_id": random.choice(orgs),
                }
            )
        d = date(d.year + (1 if d.month == 12 else 0), 1 if d.month == 12 else d.month + 1, 1)
    return pd.DataFrame(rows)


def generate_synth_data(out_dir: str) -> None:
    out = Path(out_dir)
    ensure_dirs(out)

    # Generate dataframes for orgs, employees, events, and headcount
    org_df = gen_org()
    orgs = org_df["org_id"].tolist()
    emps = gen_employees()
    events_df = gen_hr_events(emps, orgs)
    hc_df = gen_headcount_snapshots(emps, orgs)

    # Write dataframes to CSV files in appropriate directories
    org_df.to_csv(out / "org" / "org.csv", index=False)
    events_df.to_csv(out / "hr_events" / "hr_events.csv", index=False)
    hc_df.to_csv(out / "headcount" / "headcount_snapshots.csv", index=False)

    # Print summary of generated files and row counts
    print("Generated:")
    print(f"- {out/'org'/'org.csv'} ({len(org_df)} rows)")
    print(f"- {out/'hr_events'/'hr_events.csv'} ({len(events_df)} rows)")
    print(f"- {out/'headcount'/'headcount_snapshots.csv'} ({len(hc_df)} rows)")


def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        "--out", type=str, default="data", help="Output directory for generated CSVs"
    )
    args, _ = parser.parse_known_args()

    generate_synth_data(args.out)

if __name__ == "__main__": 
    main()