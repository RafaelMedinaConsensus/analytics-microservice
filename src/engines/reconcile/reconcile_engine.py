"""
Reconciliation Engine for Analytics Microservice

This module provides core logic for cross-referencing two datasets
to find discrepancies, missing records, or intersections.
Designed for fiscal reconciliation between SAP and DIAN data.
"""

from typing import List, Dict, Any, Optional


def find_column(dataset: List[Dict[str, Any]], target_name: str) -> str:
    """
    Find a column name in the dataset using case-insensitive search.
    
    Args:
        dataset: List of dictionaries representing the dataset
        target_name: Name of the column to find (case-insensitive)
        
    Returns:
        The actual column name as it appears in the dataset
        
    Raises:
        ValueError: If the column is not found in the dataset
    """
    if not dataset or len(dataset) == 0:
        raise ValueError("Dataset is empty, cannot find columns")
    
    # Get column names from the first record
    sample_record = dataset[0]
    
    # Case-insensitive search
    for column_name in sample_record.keys():
        if column_name.lower() == target_name.lower():
            return column_name
    
    # Column not found
    available_columns = ", ".join(sample_record.keys())
    raise ValueError(
        f"Column '{target_name}' not found in dataset. "
        f"Available columns: {available_columns}"
    )


def normalize_key_value(value: Any) -> str:
    """
    Normalize a key value for comparison.
    Converts to string, strips whitespace, and converts to lowercase.
    
    Args:
        value: The value to normalize
        
    Returns:
        Normalized string value
    """
    return str(value).strip().lower()


def build_key_index(
    dataset: List[Dict[str, Any]], 
    key_column: str
) -> Dict[str, Dict[str, Any]]:
    """
    Build a hash map index for efficient lookups.
    
    Args:
        dataset: List of dictionaries to index
        key_column: The actual column name to use as the key
        
    Returns:
        Dictionary mapping normalized key values to original records
    """
    index = {}
    
    for record in dataset:
        # Get the key value from this record
        key_value = record.get(key_column)
        
        # Skip records that don't have this field or have None/empty values
        if key_value is None or key_value == "":
            continue
            
        # Normalize the key and add to index
        normalized_key = normalize_key_value(key_value)
        
        # Add source information to the record for tracking
        record_with_source = record.copy()
        index[normalized_key] = record_with_source
    
    return index


def reconcile_datasets(
    data_a: List[Dict[str, Any]],
    data_b: List[Dict[str, Any]],
    key_column_a: Optional[str] = None,
    key_column_b: Optional[str] = None,
    key_column: str = "CUFE",
    mode: str = "missing_in_a"
) -> Dict[str, Any]:
    """
    Reconcile two datasets to find differences or intersections.
    
    Args:
        data_a: First dataset (e.g., SAP invoices)
        data_b: Second dataset (e.g., DIAN documents)
        key_column_a: Column name in dataset A (optional, fallback to key_column)
        key_column_b: Column name in dataset B (optional, fallback to key_column)
        key_column: Fallback column name if specific columns not provided
        mode: Operation mode - "missing_in_a", "missing_in_b", or "intersection"
        
    Returns:
        Dictionary with reconciliation results including summary and matched records
        
    Raises:
        ValueError: If datasets are invalid or columns not found
    """
    # ========================================
    # 1. INPUT VALIDATION
    # ========================================
    if not data_a or not isinstance(data_a, list):
        raise ValueError("data_a must be a non-empty list of dictionaries")
    
    if not data_b or not isinstance(data_b, list):
        raise ValueError("data_b must be a non-empty list of dictionaries")
    
    if len(data_a) == 0:
        raise ValueError("data_a is empty")
    
    if len(data_b) == 0:
        raise ValueError("data_b is empty")
    
    # Validate mode
    valid_modes = ["missing_in_a", "missing_in_b", "intersection"]
    if mode not in valid_modes:
        raise ValueError(
            f"Invalid mode '{mode}'. Must be one of: {', '.join(valid_modes)}"
        )
    
    # ========================================
    # 2. DYNAMIC COLUMN RESOLUTION
    # ========================================
    # Use specific column names if provided, otherwise fall back to key_column
    actual_key_column_a = key_column_a if key_column_a else key_column
    actual_key_column_b = key_column_b if key_column_b else key_column
    
    # Find actual column names in datasets (case-insensitive)
    try:
        resolved_column_a = find_column(data_a, actual_key_column_a)
    except ValueError as e:
        raise ValueError(f"Error in dataset A: {str(e)}")
    
    try:
        resolved_column_b = find_column(data_b, actual_key_column_b)
    except ValueError as e:
        raise ValueError(f"Error in dataset B: {str(e)}")
    
    # ========================================
    # 3. BUILD HASH MAP INDEXES (O(1) Lookup)
    # ========================================
    index_a = build_key_index(data_a, resolved_column_a)
    index_b = build_key_index(data_b, resolved_column_b)
    
    keys_a = set(index_a.keys())
    keys_b = set(index_b.keys())
    
    # ========================================
    # 4. SET OPERATIONS
    # ========================================
    if mode == "missing_in_a":
        # Records in B that are NOT in A
        diff_keys = keys_b - keys_a
        source_index = index_b
        source_name = "B"
    elif mode == "missing_in_b":
        # Records in A that are NOT in B
        diff_keys = keys_a - keys_b
        source_index = index_a
        source_name = "A"
    else:  # intersection
        # Records that exist in BOTH datasets
        diff_keys = keys_a & keys_b
        source_index = index_a
        source_name = "Both"
    
    # ========================================
    # 5. BUILD RESULT SET
    # ========================================
    result_records = []
    for key in diff_keys:
        record = source_index[key]
        result_records.append(record)
    
    # ========================================
    # 6. GENERATE SUMMARY
    # ========================================
    count = len(result_records)
    
    if mode == "missing_in_a":
        summary = (
            f"Reconciliación completada. Se encontraron {count} documentos "
            f"en el conjunto B (DIAN/Externo) que NO están en el conjunto A (SAP/Base)."
        )
    elif mode == "missing_in_b":
        summary = (
            f"Reconciliación completada. Se encontraron {count} documentos "
            f"en el conjunto A (SAP/Base) que NO están en el conjunto B (DIAN/Externo)."
        )
    else:  # intersection
        summary = (
            f"Reconciliación completada. Se encontraron {count} documentos "
            f"que coinciden en AMBOS conjuntos."
        )
    
    # ========================================
    # 7. RETURN STRUCTURED RESULT
    # ========================================
    return {
        "summary": summary,
        "match_count": count,
        "mode_used": mode,
        "key_column_a": resolved_column_a,
        "key_column_b": resolved_column_b,
        "data": result_records,
        "metadata": {
            "total_records_a": len(data_a),
            "total_records_b": len(data_b),
            "valid_keys_a": len(keys_a),
            "valid_keys_b": len(keys_b)
        }
    }
