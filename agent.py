import re
import pandas as pd
from typing import Optional, Dict, Any, List

class CoddyAgent:
    def __init__(self):
        self.current_df: Optional[pd.DataFrame] = None
        self.file_history: List[str] = []
        self.current_file_name: Optional[str] = None
        self.last_query: Optional[str] = None
        self.last_result: Any = None

    def extract_file_id(self, url_or_id: str) -> str:
        match = re.search(r'/file/d/([a-zA-Z0-9_-]+)', url_or_id)
        if match:
            return match.group(1)
        match_open = re.search(r'id=([a-zA-Z0-9_-]+)', url_or_id)
        if match_open:
            return match_open.group(1)
        return url_or_id.strip()

    def load_csv(self, source: str, df: Optional[pd.DataFrame] = None, file_name: str = "dataset.csv") -> str:
        if df is not None:
            self.current_df = df.copy()
        else:
            # Simulated load or actual read
            try:
                self.current_df = pd.read_csv(source)
            except Exception as e:
                # If source is a file ID or path simulation
                raise ValueError(f"Could not load CSV from {source}: {e}")
        
        self.current_file_name = file_name
        self.file_history.append(file_name)
        rows, cols = self.current_df.shape
        return f"✅ Loaded '{file_name}' with {rows:,} rows and {cols} columns"

    def describe_columns(self) -> str:
        if self.current_df is None:
            return "❌ No CSV file loaded. Please load a file first using: 'Load [Google Drive URL]'"
        
        lines = ["Column Profile:"]
        for col in self.current_df.columns:
            dtype = str(self.current_df[col].dtype)
            non_null = self.current_df[col].count()
            samples = self.current_df[col].dropna().unique()[:3]
            sample_str = ", ".join(map(str, samples))
            lines.append(- f"- {col} ({dtype}): {non_null} non-null | Samples: [{sample_str}]")
        return "\n".join(lines)

    def filter_rows(self, condition: str) -> str:
        if self.current_df is None:
            return "❌ No CSV file loaded. Please load a file first."
        try:
            filtered = self.current_df.query(condition, engine="python")
            self.current_df = filtered
            return f"✅ Filtered to {len(filtered):} rows where {condition}"
        except Exception as e:
            return f"❌ Invalid filter condition: {e}"

    def group_by_aggregate(self, group_col: str, agg_col: str, func: str) -> str:
        if self.current_df is None:
            return "❌ No CSV file loaded."
        if group_col not in self.current_df.columns or agg_col not in self.current_df.columns:
            return f"❌ Column(s) not found. Available: {list(self.current_df.columns)}"
        try:
            res = self.current_df.groupby(group_col)[agg_col].agg(func).reset_index()
            self.last_result = res
            return res.to_string(index=False)
        except Exception as e:
            return f"❌ Aggregation error: {e}"

def main():
    agent = CoddyAgent()
    print("🤖 Coddy Data Analyst Agent v0.1.0 initialized.")
    print("Type 'exit' to quit.")
    while True:
        try:
            user_input = input("\nUser: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ("exit", "quit"):
                print("Goodbye!")
                break
            if user_input.lower().startswith("load "):
                url = user_input[5:].strip()
                # For demo CLI, check if it's a local path or URL
                try:
                    df = pd.read_csv(url) if ',' not in url else None
                    print("Coddy:", agent.load_csv(url, df=df, file_name=url.split("/")[-1]))
                except Exception:
                    # Create dummy df for testing if path doesn't exist
                    dummy = pd.DataFrame({
                        "date": ["2024-01-01", "2024-01-02", "2024-01-03"],
                        "product": ["Widget A", "Widget B", "Widget A"],
                        "price": [19.99, 29.99, 49.99],
                        "quantity": [1, 2, 5],
                        "region": ["North", "South", "East"]
                    })
                    print("Coddy:", agent.load_csv(url, df=dummy, file_name="sales_data.csv"))
            elif user_input.lower() in ("describe", "what columns are in this file?"):
                print("Coddy:\n" + agent.describe_columns())
            elif user_input.lower().startswith("filter "):
                cond = user_input[7:].strip()
                print("Coddy:", agent.filter_rows(cond))
            else:
                print("Coddy: I understand commands like 'Load [URL]', 'describe', or 'filter [condition]'.")
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break
