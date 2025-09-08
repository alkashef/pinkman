"""
Cleanup script for removing temporary and cache files from a codebase.

This script recursively searches for and removes:
- Backup files (*.bak, *.new, *.fixed, *.old, *.tmp, *.backup)
- Python cache files and directories (__pycache__, *.pyc, *.pyo)
- Other common temporary files and directories

Usage:
    python cleanup.py [root_dir] [-y/--yes]
"""
import os
import glob
import shutil
import logging
from pathlib import Path
from typing import List, Set, Tuple
import argparse

# Configure logging with f-strings
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def get_temp_patterns() -> List[str]:
    """Get list of file patterns to clean up."""
    return [
        "*.bak", "*.new", "*.fixed", "*.old", "*.tmp", "*.backup",
        "*.pyc", "*.pyo", "*.pyd", "*.so", "*.dll",
        "*.log", "*.cache", "*.swp", "*.swo",
        "*~", ".DS_Store", "Thumbs.db"
    ]

def get_temp_dirs() -> List[str]:
    """Get list of directory names to clean up."""
    return [
        "__pycache__",
        ".pytest_cache",
        ".coverage",
        ".mypy_cache",
        ".ruff_cache",
        ".hypothesis",
        "build",
        "dist",
        "*.egg-info",
        ".ipynb_checkpoints",
        ".tox",
        ".env",
        ".venv",
        "node_modules"
    ]

def find_cleanup_targets(root_dir: str) -> Tuple[Set[str], Set[str]]:
    """
    Find all files and directories that should be cleaned up.
    
    Args:
        root_dir: Root directory to start search from
        
    Returns:
        Tuple of (files to delete, directories to delete)
    """
    files_to_delete: Set[str] = set()
    dirs_to_delete: Set[str] = set()
    root_path = Path(root_dir).resolve()
    
    logger.info(f"Scanning directory: {root_path}")
    
    try:
        # Get the patterns
        file_patterns = get_temp_patterns()
        dir_patterns = get_temp_dirs()
        
        # Walk through directory tree
        for current_dir, subdirs, files in os.walk(root_path, topdown=False):
            current_path = Path(current_dir)
            
            # Check for matching directories
            for dir_pattern in dir_patterns:
                matching_dirs = current_path.glob(dir_pattern)
                dirs_to_delete.update(str(d) for d in matching_dirs if d.is_dir())
            
            # Check for matching files
            for pattern in file_patterns:
                matching_files = current_path.glob(pattern)
                files_to_delete.update(str(f) for f in matching_files if f.is_file())
                
    except Exception as e:
        logger.error(f"Error while scanning directory: {e}")
        raise
            
    return files_to_delete, dirs_to_delete

def format_size(size_bytes: int) -> str:
    """Format file size in human readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"

def calculate_total_size(paths: List[str]) -> int:
    """Calculate total size of files and directories."""
    total = 0
    for path in paths:
        try:
            if os.path.isfile(path):
                total += os.path.getsize(path)
            elif os.path.isdir(path):
                for dirpath, _, filenames in os.walk(path):
                    for f in filenames:
                        fp = os.path.join(dirpath, f)
                        if os.path.exists(fp):  # Check if file still exists
                            total += os.path.getsize(fp)
        except (OSError, PermissionError) as e:
            logger.warning(f"Error calculating size for {path}: {e}")
            continue
    return total

def delete_paths(paths: Set[str], is_dir: bool = False) -> List[str]:
    """
    Delete files or directories and return list of successfully deleted paths.
    
    Args:
        paths: Set of paths to delete
        is_dir: True if paths are directories, False if files
        
    Returns:
        List of successfully deleted paths
    """
    deleted = []
    for path in paths:
        try:
            if is_dir:
                shutil.rmtree(path)
            else:
                os.remove(path)
            deleted.append(path)
            logger.debug(f"Successfully deleted: {path}")
        except OSError as e:
            logger.error(f"Error deleting {path}: {e}")
    return deleted

def main() -> None:
    """Main entry point for the cleanup script."""
    parser = argparse.ArgumentParser(
        description="Clean up temporary and cache files from a codebase"
    )
    parser.add_argument(
        "root_dir",
        nargs="?",
        default=".",
        help="Root directory to clean (default: current directory)"
    )
    parser.add_argument(
        "-y", "--yes",
        action="store_true",
        help="Skip confirmation and delete files immediately"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    root_dir = os.path.abspath(args.root_dir)
    logger.info(f"Starting cleanup in: {root_dir}")
    
    try:
        # Find all targets
        files_to_delete, dirs_to_delete = find_cleanup_targets(root_dir)
        
        if not files_to_delete and not dirs_to_delete:
            logger.info("No files or directories to clean up!")
            return
        
        # Calculate total size
        all_paths = list(files_to_delete) + list(dirs_to_delete)
        total_size = calculate_total_size(all_paths)
        
        # Show what will be deleted
        if files_to_delete:
            print("\nFiles to be deleted:")
            for f in sorted(files_to_delete):
                print(f"  - {f}")
        
        if dirs_to_delete:
            print("\nDirectories to be deleted:")
            for d in sorted(dirs_to_delete):
                print(f"  - {d}")
            
        print(f"\nTotal space to be freed: {format_size(total_size)}")
        
        # Get confirmation
        if not args.yes:
            response = input("\nDelete these files/directories? [y/N] ").lower()
            if response != 'y':
                logger.info("Operation cancelled by user")
                return
        
        # Delete files and directories
        deleted_files = delete_paths(files_to_delete)
        deleted_dirs = delete_paths(dirs_to_delete, is_dir=True)
        
        # Print summary
        logger.info("Cleanup completed!")
        logger.info(f"Deleted {len(deleted_files)} files and {len(deleted_dirs)} directories")
        logger.info(f"Freed up approximately: {format_size(total_size)}")
        
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise

if __name__ == "__main__":
    main()
