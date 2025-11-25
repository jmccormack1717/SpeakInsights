"""Analysis service: Generate textual insights"""
from typing import Dict, Any, List
from app.core.llm import LLMClient


class AnalysisService:
    """Service for generating textual analysis and insights"""
    
    def __init__(self):
        self.llm = LLMClient()
    
    async def generate_insights(
        self,
        user_query: str,
        query_results: List[Dict[str, Any]],
        sql: str,
        data_structure: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate textual analysis of query results
        
        Args:
            user_query: Original user query
            query_results: Query results
            sql: Executed SQL query
            data_structure: Data structure analysis
            
        Returns:
            Textual analysis with summary, findings, and insights
        """
        # Prepare results summary for LLM
        results_summary = self._prepare_results_summary(query_results, data_structure)
        
        prompt = f"""You are helping a non-technical business user understand their data.
The user will never see any mention of SQL, queries, or technical implementation details.
Speak in clear, friendly business language.

User Question: "{user_query}"

Data Summary:
{results_summary}

Please provide a concise, easy-to-understand analysis with:
1. Executive summary (2-3 sentences describing the key findings)
2. Key findings (3-5 bullet points highlighting important patterns or numbers)
3. Notable patterns or anomalies (if any)
4. Recommendations (if applicable, 1-2 actionable insights)

Formatting rules:
- Do NOT mention SQL, queries, tables, columns, or code.
- When you mention numbers, round them to at most 2 decimal places.
- Prefer percentages and simple ranges over raw long decimals.

Return JSON format only:
{{
  "summary": "Executive summary text",
  "key_findings": ["finding 1", "finding 2", ...],
  "patterns": ["pattern 1", "pattern 2", ...],
  "recommendations": ["recommendation 1", ...]
}}"""

        messages = [
            {
                "role": "system",
                "content": "You are a data analyst expert. Analyze query results and provide clear, actionable insights. Always return valid JSON."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
        
        try:
            response = await self.llm.generate_json(messages, temperature=0.5)
            
            return {
                "summary": response.get("summary", ""),
                "key_findings": response.get("key_findings", []),
                "patterns": response.get("patterns", []),
                "recommendations": response.get("recommendations", [])
            }
        except Exception as e:
            # Fallback to basic analysis if LLM fails
            return self._generate_fallback_analysis(query_results, data_structure)
    
    def _prepare_results_summary(
        self,
        results: List[Dict[str, Any]],
        data_structure: Dict[str, Any]
    ) -> str:
        """Prepare a summary of results for LLM"""
        if not results:
            return "No results returned from query."
        
        summary_parts = [
            f"Total rows: {len(results)}",
            f"Columns: {', '.join(data_structure.get('columns', {}).keys())}"
        ]
        
        # Add sample data
        summary_parts.append("\nSample data (first 5 rows):")
        for i, row in enumerate(results[:5], 1):
            summary_parts.append(f"Row {i}: {row}")
        
        # Add statistics for numeric columns
        numeric_cols = data_structure.get("numeric_columns", [])
        for col in numeric_cols:
            stats = data_structure.get("columns", {}).get(col, {}).get("statistics", {})
            if stats:
                summary_parts.append(
                    f"\n{col} statistics: "
                    f"min={stats.get('min')}, max={stats.get('max')}, "
                    f"mean={stats.get('mean'):.2f}, median={stats.get('median'):.2f}"
                )
        
        return "\n".join(summary_parts)
    
    def _generate_fallback_analysis(
        self,
        results: List[Dict[str, Any]],
        data_structure: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate basic analysis without LLM"""
        row_count = len(results)
        
        summary = f"Query returned {row_count} result{'s' if row_count != 1 else ''}."
        
        findings = []
        if row_count > 0:
            findings.append(f"Total records: {row_count}")
        
        numeric_cols = data_structure.get("numeric_columns", [])
        for col in numeric_cols:
            stats = data_structure.get("columns", {}).get(col, {}).get("statistics", {})
            if stats:
                findings.append(
                    f"{col} ranges from {stats.get('min')} to {stats.get('max')} "
                    f"(average: {stats.get('mean'):.2f})"
                )
        
        return {
            "summary": summary,
            "key_findings": findings,
            "patterns": [],
            "recommendations": []
        }

