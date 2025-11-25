# CSV Upload Guide

## How to Upload CSV Files

### Quick Steps

1. **Create a dataset** (if you haven't already)
   - Click "New Dataset" in the UI
   - Enter a name (e.g., "my_data")

2. **Upload CSV file**
   - Click "Upload CSV" button on your dataset card
   - Select a CSV file from your computer
   - Wait for confirmation message

3. **Query your data!**
   - Select the dataset
   - Ask questions in natural language

## CSV File Requirements

### Format
- **File extension**: `.csv`
- **Encoding**: UTF-8 (default)
- **Delimiter**: Comma (`,`)
- **First row**: Should contain column headers

### Example CSV

```csv
region,product,amount,quarter,date
North,Product A,50000,Q4,2024-10-01
South,Product A,45000,Q4,2024-10-15
East,Product B,60000,Q4,2024-11-01
```

### Column Name Rules

- Column names are automatically sanitized:
  - Spaces → underscores
  - Special characters → removed or replaced
  - Must start with letter or underscore

**Example:**
- `Sales Amount` → `Sales_Amount`
- `Product-Name` → `Product_Name`
- `2024 Sales` → `_2024_Sales`

## Data Type Detection

The system automatically detects data types:

- **INTEGER**: Whole numbers (1, 2, 100)
- **REAL**: Decimal numbers (1.5, 99.99)
- **TEXT**: Text strings
- **DATE**: Dates (YYYY-MM-DD format)

## Table Creation

- **Table name**: Defaults to filename (without .csv)
- **Custom name**: Can be specified (future feature)
- **Re-upload**: Replaces existing table with same name

## Sample CSV File

A sample CSV is available at: `backend/data/sample_sales.csv`

You can use this to test the upload functionality.

## Troubleshooting

### "CSV file is empty"
- Make sure your CSV has data rows (not just headers)
- Check file encoding (should be UTF-8)

### "Failed to import CSV"
- Check CSV format (comma-separated)
- Ensure first row has column headers
- Verify file isn't corrupted

### "Table already exists"
- Re-uploading replaces the existing table
- This is expected behavior

## Tips

1. **Large files**: CSV upload works best with files under 10MB
2. **Date formats**: Use YYYY-MM-DD format for best date detection
3. **Headers**: Always include column headers in first row
4. **Empty cells**: Will be imported as NULL values

## Next Steps After Upload

Once your CSV is uploaded:

1. The table is automatically created
2. All data is imported
3. You can immediately query it:
   - "Show me all data"
   - "What are the totals by region?"
   - "Show me trends over time"

