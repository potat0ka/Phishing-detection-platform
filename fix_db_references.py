#!/usr/bin/env python3
"""
Fix Database Reference Utility
Adds proper MongoDB manager imports to all files
"""

import re
import os

def fix_file_db_references(filepath):
    """Add get_mongodb_manager() calls where db_manager is used"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Pattern to find functions that use db_manager but don't have get_mongodb_manager()
        lines = content.split('\n')
        modified = False
        
        for i, line in enumerate(lines):
            # If line uses db_manager but no get_mongodb_manager in function
            if 'db_manager.' in line and 'get_mongodb_manager()' not in line:
                # Look backwards for function start
                func_start = i
                while func_start > 0 and not lines[func_start].strip().startswith('def '):
                    func_start -= 1
                
                if func_start >= 0:
                    # Check if function already has get_mongodb_manager
                    has_manager = False
                    for j in range(func_start, i + 5):
                        if j < len(lines) and 'get_mongodb_manager()' in lines[j]:
                            has_manager = True
                            break
                    
                    if not has_manager:
                        # Find appropriate place to insert db_manager = get_mongodb_manager()
                        insert_line = i
                        indent = len(line) - len(line.lstrip())
                        if indent > 0:
                            # Insert before current db_manager usage
                            manager_line = ' ' * indent + 'db_manager = get_mongodb_manager()'
                            lines.insert(i, manager_line)
                            modified = True
                            break
        
        if modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write('\n'.join(lines))
            print(f"Fixed {filepath}")
            return True
        
    except Exception as e:
        print(f"Error fixing {filepath}: {e}")
    
    return False

def main():
    """Fix all Python files with database references"""
    files_to_fix = [
        'auth_routes.py',
        'routes.py', 
        'admin_routes.py'
    ]
    
    fixed_count = 0
    for filepath in files_to_fix:
        if os.path.exists(filepath):
            if fix_file_db_references(filepath):
                fixed_count += 1
    
    print(f"Fixed {fixed_count} files")

if __name__ == "__main__":
    main()