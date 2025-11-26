"""Query service: analysis planning via playbooks (no SQL generation)."""
import logging
from typing import Dict, Any
from app.core.llm import LLMClient
from app.utils.schema_parser import build_schema_context


class QueryService:
    """Service for planning which analysis playbook to run."""

    def __init__(self):
        self.llm = LLMClient()
        self.logger = logging.getLogger(__name__)

    async def select_analysis(
        self,
        user_query: str,
        schema_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Use the LLM to select an analysis playbook and fill in high-level slots.

        The LLM does NOT write SQL. It only chooses which playbook to use and
        which columns (target/measures) to focus on.
        """
        schema_context = build_schema_context(schema_info)
        lower_query = user_query.lower()

        playbook_descriptions = """
Available analysis INTENTS (high-level goals):
- "overview": High-level description of the dataset (size, key numeric features, ranges, missingness).
- "drivers": What features are most strongly related to an outcome/target overall.
- "distribution": Explore the distribution and outliers for a single numeric feature.
- "relationship": Show how two numeric features relate to each other (scatter / curve).
- "compare_groups": Compare two or more cohorts/groups on a key metric.
- "outcome_breakdown": Show how often each outcome/target class occurs (class balance).
- "segment_drilldown": Zoom into a particular segment (e.g. only Outcome=1, or Age>60) and summarize it.

These intents are implemented using the following PLAYBOOKS (deterministic Python code):
- "overview": dataset_overview_playbook
- "correlation": drivers_playbook (top-N correlations with a target)
- "distribution": distribution_playbook (histograms)
- "relationship": relationship_playbook (scatter)
- "segment_comparison": segment_comparison_playbook (compare_groups)
- "outcome_breakdown": outcome_breakdown_playbook
- "feature_outcome_profile": feature_outcome_profile_playbook (risk curve)
- "segmented_distribution": segmented_distribution_playbook

You can also set numeric detail parameters when relevant:
- "top_n": how many top items to show (e.g. top 10 correlated features).
- "bins": how many bins to use for histograms / profiles (e.g. 20 bins).

You may optionally request SECONDARY playbooks when they clearly add value.
Examples:
- For "correlation" you might also request "feature_outcome_profile" for the most important feature.
- For "outcome_breakdown" you might also request "distribution" for a key feature by outcome.
Never add secondary playbooks just to show more charts; only add them if they help answer the question.
"""

        prompt = f"""You are an analysis planner. Your job is to choose ONE analysis playbook
for the user's question, based on the dataset schema.

{playbook_descriptions}

Dataset schema:
{schema_context}

User question: "{user_query}"

Return a JSON object ONLY, with this structure:
{{
  "intent": "overview" | "drivers" | "distribution" | "relationship" | "compare_groups" | "outcome_breakdown" | "segment_drilldown",
  "playbook": "overview" | "correlation" | "distribution" | "segment_comparison" | "outcome_breakdown" | "feature_outcome_profile" | "relationship" | "segmented_distribution",
  "target": "column_name or null",              // for correlation, outcome_breakdown & feature_outcome_profile
  "feature": "column_name or null",             // for distribution & feature_outcome_profile (numeric)
  "segment_column": "column_name or null",      // for segment_comparison (categorical/boolean)
  "feature_x": "column_name or null",           // for relationship (numeric)
  "feature_y": "column_name or null",           // for relationship (numeric)
  "top_n": number or null,                      // for correlation or any ranking-style output
  "bins": number or null,                       // for distribution / feature_outcome_profile
  "filter_segment": {{ "column": string, "value": string | number | boolean }} | null,
  "focus_range": {{ "feature": string, "min": number, "max": number }} | null,
  "secondary_playbooks": string[] | null,       // names of additional playbooks to run, or null
  "mode": "quick" | "deep"
}}

Rules:
- Choose INTENT first based on the user question, then choose an appropriate PLAYBOOK.
- Use "overview" intent when the user asks to describe or summarize the dataset or data overall.
- Use "drivers" intent when the user asks which features/columns are most related to an outcome or target overall.
- Use "distribution" intent when the user asks about the spread, range, outliers, or histogram of a single numeric column.
- Use "relationship" intent when the user asks how two specific numeric features relate to each other (e.g. pregnancies vs age).
- Use "compare_groups" intent when the user asks to compare two groups or cohorts (e.g. outcome=1 vs outcome=0, men vs women).
- Use "outcome_breakdown" intent when the user asks how often the outcome/target occurs, or for class balance / base rate.
- Use "segment_drilldown" intent when the user restricts analysis to a group (e.g. only Outcome=1, or only Age > 60) and wants that segment summarized.
- When the user mentions a specific count like "top 3" or "top 10", set "top_n" accordingly (within 3-20).
- When the user asks for more or fewer "buckets" / "ranges" / "granularity", adjust "bins" between 5 and 30.
- Use "filter_segment" when the user restricts analysis to a group (e.g. only Outcome=1, or only Age > 60).
- Use "focus_range" when the user specifies a value range of interest for a numeric feature (e.g. glucose between 80 and 200).
- Only set "secondary_playbooks" when clearly useful; otherwise omit or set it to null.
- For "drivers"/correlation, choose a numeric column that looks like the outcome/target (e.g., a binary label) if possible.
- Default mode is "quick" unless the user clearly asks for very detailed or deep analysis.
- If you are unsure of a column to use for a given playbook, set its field to null and let the backend fall back safely.
"""

        messages = [
            {
                "role": "system",
                "content": "You are a careful analysis planner. Always return valid JSON and never invent columns that are not in the schema.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ]

        response = await self.llm.generate_json(messages, temperature=0.2)

        # Ensure we got a dictionary back; fall back to a safe default otherwise
        if not isinstance(response, dict):
            self.logger.error(f"select_analysis: LLM returned non-dict: {response!r}")
            return {
                "playbook": "overview",
                "target": None,
                "mode": "quick",
            }

        intent = response.get("intent", "overview")
        playbook = response.get("playbook")  # may be None; we'll map from intent if needed
        target = response.get("target")
        feature = response.get("feature")
        segment_column = response.get("segment_column")
        feature_x = response.get("feature_x")
        feature_y = response.get("feature_y")
        top_n = response.get("top_n")
        bins = response.get("bins")
        filter_segment = response.get("filter_segment")
        focus_range = response.get("focus_range")
        secondary_playbooks = response.get("secondary_playbooks") or []
        mode = response.get("mode", "quick")

        # Basic validation and fallbacks
        allowed_intents = {
            "overview",
            "drivers",
            "distribution",
            "relationship",
            "compare_groups",
            "outcome_breakdown",
            "segment_drilldown",
        }
        if intent not in allowed_intents:
            intent = "overview"

        allowed_playbooks = {
            "overview",
            "correlation",
            "distribution",
            "segment_comparison",
            "outcome_breakdown",
            "feature_outcome_profile",
            "relationship",
            "segmented_distribution",
        }

        # Map INTENT → default PLAYBOOK if playbook is missing or invalid
        intent_to_playbook = {
            "overview": "overview",
            "drivers": "correlation",
            "distribution": "distribution",
            "relationship": "relationship",
            "compare_groups": "segment_comparison",
            "outcome_breakdown": "outcome_breakdown",
            "segment_drilldown": "overview",  # for now, a filtered overview
        }

        if playbook not in allowed_playbooks:
            playbook = intent_to_playbook.get(intent, "overview")

        # Common candidate names for "outcome-like" targets
        candidate_names = {"outcome", "target", "label", "y"}

        # Heuristic: if drivers/correlation or outcome_breakdown was requested but target is missing,
        # try to infer a reasonable default from schema table names / columns.
        if playbook in {"correlation", "outcome_breakdown"} and not target:
            for table in schema_info.get("tables", []):
                for col in table.get("columns", []):
                    if col["name"].lower() in candidate_names:
                        target = col["name"]
                        break
                if target:
                    break

        # Collect any mentioned columns in the user's question
        mentioned_columns: list[str] = []
        for table in schema_info.get("tables", []):
            for col in table.get("columns", []):
                col_name = col["name"]
                col_lower = col_name.lower()
                if col_lower in lower_query:
                    mentioned_columns.append(col_name)

        # Additional heuristic for correlation:
        # If the user clearly mentions a specific column name (e.g. "Pregnancies") and
        # target is still empty or points to a generic outcome column, treat that
        # mentioned column as the correlation target instead.
        if playbook == "correlation":
            non_outcome_mentions = [
                c for c in mentioned_columns if c.lower() not in candidate_names
            ]
            if non_outcome_mentions and (not target or target.lower() in candidate_names):
                target = non_outcome_mentions[0]

        # Heuristic for relationship: if two columns are clearly mentioned,
        # prefer them as feature_x and feature_y.
        if playbook == "relationship":
            numeric_columns = {
                col["name"]
                for table in schema_info.get("tables", [])
                for col in table.get("columns", [])
                if col.get("type") == "number"
            }
            # Filter mentioned columns to numerics
            numeric_mentions = [c for c in mentioned_columns if c in numeric_columns]
            if len(numeric_mentions) >= 2:
                feature_x = feature_x or numeric_mentions[0]
                feature_y = feature_y or numeric_mentions[1]

        # Clamp numeric detail parameters to reasonable ranges
        if isinstance(top_n, (int, float)):
            # allow between 3 and 50
            top_n = max(3, min(int(top_n), 50))
        else:
            top_n = None

        if isinstance(bins, (int, float)):
            # allow between 5 and 50
            bins = max(5, min(int(bins), 50))
        else:
            bins = None

        # Normalize secondary_playbooks to a list of allowed names
        if not isinstance(secondary_playbooks, list):
            secondary_playbooks = []
        secondary_playbooks = [
            p
            for p in secondary_playbooks
            if isinstance(p, str) and p in allowed_playbooks and p != playbook
        ]

        # Final, fully validated analysis request
        return {
            "intent": intent,
            "playbook": playbook,
            "target": target,
            "feature": feature,
            "segment_column": segment_column,
            "feature_x": feature_x,
            "feature_y": feature_y,
            "top_n": top_n,
            "bins": bins,
            "filter_segment": filter_segment,
            "focus_range": focus_range,
            "secondary_playbooks": secondary_playbooks,
            "mode": mode,
        }

