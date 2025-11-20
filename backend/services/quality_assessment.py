"""
Quality Assessment Engine
Multi-dimensional code quality evaluation system.
Author: Cavin Otieno
"""

import os
import ast
import json
import subprocess
import tempfile
import shutil
from typing import Dict, List, Any, Tuple, Optional, Callable
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
import radon.complexity as radon_complexity
import radon.metrics as radon_metrics
import bandit
import bandit.cli
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class QualityDimension(Enum):
    """Quality assessment dimensions"""
    CORRECTNESS = "correctness"
    PERFORMANCE = "performance"
    SECURITY = "security"
    CODE_QUALITY = "code_quality"
    DOCUMENTATION = "documentation"
    MAINTAINABILITY = "maintainability"


@dataclass
class QualityScore:
    """Quality score for a specific dimension"""
    dimension: QualityDimension
    score: float  # 0.0 to 1.0
    level: str    # EXCELLENT, GOOD, FAIR, POOR
    details: Dict[str, Any]
    suggestions: List[str]
    violations: List[Dict[str, Any]]
    confidence: float  # 0.0 to 1.0


@dataclass
class FileAssessment:
    """Quality assessment for a single file"""
    file_path: str
    overall_score: float
    scores: Dict[QualityDimension, QualityScore]
    metrics: Dict[str, Any]
    execution_time: float


@dataclass
class ProjectAssessment:
    """Overall project quality assessment"""
    project_path: str
    files_assessed: List[str]
    overall_score: float
    dimension_scores: Dict[QualityDimension, float]
    critical_issues: List[Dict[str, Any]]
    recommendations: List[str]
    metrics: Dict[str, Any]
    assessment_timestamp: str


class CorrectnessAssessment:
    """Assesses code correctness through static analysis and tests"""

    @staticmethod
    def analyze_syntax_errors(file_path: str) -> Tuple[List[Dict[str, Any]], float]:
        """Analyze Python syntax errors"""
        issues = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            ast.parse(content, filename=file_path)
            # Check for common issues
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                # Check for unreachable code
                if isinstance(node, (ast.Return, ast.Break, ast.Continue)):
                    parent = ast.get_parent(node, tree)
                    if parent and hasattr(parent, 'body'):
                        try:
                            node_index = parent.body.index(node)
                            for i in range(node_index + 1, len(parent.body)):
                                unreachable = parent.body[i]
                                if not isinstance(unreachable, (ast.Expr, ast.Pass)):
                                    issues.append({
                                        'type': 'unreachable_code',
                                        'line': unreachable.lineno,
                                        'message': 'Unreachable code detected',
                                        'severity': 'medium'
                                    })
                        except (ValueError, AttributeError):
                            pass
                
                # Check for unused variables
                if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
                    # This is a simplified check - a proper linter would do better
                    pass
            
            return issues, 0.95 if not issues else max(0.3, 0.95 - len(issues) * 0.1)
            
        except SyntaxError as e:
            issues.append({
                'type': 'syntax_error',
                'line': e.lineno,
                'message': f'Syntax error: {e.msg}',
                'severity': 'critical'
            })
            return issues, 0.0
        except Exception as e:
            issues.append({
                'type': 'analysis_error',
                'line': 0,
                'message': f'Analysis error: {str(e)}',
                'severity': 'medium'
            })
            return issues, 0.5

    @staticmethod
    def check_type_hints_usage(file_path: str) -> Tuple[List[Dict[str, Any]], float]:
        """Check type hints usage"""
        issues = []
        score = 1.0
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            total_functions = 0
            typed_functions = 0
            
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    total_functions += 1
                    # Check if function has return type annotation
                    if node.returns is not None:
                        typed_functions += 1
                    # Check if function has parameter type hints
                    has_param_hints = any(
                        arg.annotation is not None 
                        for arg in node.args.args
                    )
                    if has_param_hints:
                        typed_functions += 0.5
            
            if total_functions > 0:
                type_coverage = typed_functions / total_functions
                score = type_coverage
                
                if type_coverage < 0.3:
                    issues.append({
                        'type': 'low_type_coverage',
                        'message': f'Low type hints coverage: {type_coverage:.1%}',
                        'severity': 'medium',
                        'metrics': {'coverage': type_coverage, 'total_functions': total_functions}
                    })
            else:
                score = 1.0  # No functions to check
                
        except Exception as e:
            logger.warning(f"Error checking type hints for {file_path}: {e}")
            score = 0.5
        
        return issues, score


class PerformanceAssessment:
    """Assesses code performance through complexity and efficiency analysis"""

    @staticmethod
    def analyze_cyclomatic_complexity(file_path: str) -> Tuple[List[Dict[str, Any]], float]:
        """Analyze cyclomatic complexity"""
        issues = []
        score = 1.0
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Use radon for complexity analysis
            complexity_results = radon_complexity.cc_visit(content)
            
            for result in complexity_results:
                if isinstance(result, tuple):
                    name, complexity, lineno, colno = result[0], result[1], result[2], result[3]
                    
                    if complexity > 20:
                        issues.append({
                            'type': 'very_high_complexity',
                            'name': name,
                            'line': lineno,
                            'complexity': complexity,
                            'message': f'Very high complexity ({complexity}) - refactor required',
                            'severity': 'critical'
                        })
                        score -= 0.3
                    elif complexity > 10:
                        issues.append({
                            'type': 'high_complexity',
                            'name': name,
                            'line': lineno,
                            'complexity': complexity,
                            'message': f'High complexity ({complexity}) - consider refactoring',
                            'severity': 'medium'
                        })
                        score -= 0.15
                    elif complexity > 5:
                        issues.append({
                            'type': 'moderate_complexity',
                            'name': name,
                            'line': lineno,
                            'complexity': complexity,
                            'message': f'Moderate complexity ({complexity}) - monitor',
                            'severity': 'low'
                        })
                        score -= 0.05
            
            # Calculate average complexity
            if complexity_results:
                avg_complexity = sum(r[1] for r in complexity_results if isinstance(r, tuple)) / len(complexity_results)
                issues.append({
                    'type': 'complexity_summary',
                    'message': f'Average complexity: {avg_complexity:.1f}',
                    'metrics': {
                        'total_functions': len(complexity_results),
                        'average_complexity': avg_complexity,
                        'max_complexity': max(r[1] for r in complexity_results if isinstance(r, tuple))
                    }
                })
                
        except Exception as e:
            logger.warning(f"Error analyzing complexity for {file_path}: {e}")
            score = 0.5
        
        return issues, max(0.0, score)

    @staticmethod
    def check_algorithm_efficiency(file_path: str) -> Tuple[List[Dict[str, Any]], float]:
        """Check for inefficient algorithms and patterns"""
        issues = []
        score = 1.0
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            # Check for common inefficient patterns
            for node in ast.walk(tree):
                # Check for nested loops that could be inefficient
                if isinstance(node, ast.For):
                    # Count nested loops
                    nested_depth = PerformanceAssessment._count_nested_loops(node)
                    if nested_depth > 2:
                        issues.append({
                            'type': 'deeply_nested_loop',
                            'line': node.lineno,
                            'nested_depth': nested_depth,
                            'message': f'Deeply nested loops (depth: {nested_depth}) - consider algorithm optimization',
                            'severity': 'medium'
                        })
                        score -= 0.1
                
                # Check for list comprehensions vs explicit loops
                if isinstance(node, (ast.ListComp, ast.DictComp, ast.SetComp)):
                    # Good - comprehensions are usually efficient
                    pass
                elif isinstance(node, ast.For) and node.lineno < 100:  # Simple check for basic loops
                    # Could be optimized with comprehensions
                    pass
                    
        except Exception as e:
            logger.warning(f"Error checking algorithm efficiency for {file_path}: {e}")
            score = 0.5
        
        return issues, max(0.0, score)


class SecurityAssessment:
    """Assesses security through static security analysis"""

    @staticmethod
    def run_bandit_analysis(file_path: str) -> Tuple[List[Dict[str, Any]], float]:
        """Run bandit security analysis"""
        issues = []
        
        try:
            # Create temporary config for bandit
            with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
                config = """
                exclude_dirs:
                  - test
                  - tests
                  - __pycache__
                  - .git
                """
                f.write(config)
                config_path = f.name
            
            try:
                # Run bandit
                scanner = bandit.cli.main()
                results = scanner.scan_path(file_path)
                
                for result in results:
                    severity_mapping = {
                        'HIGH': 'critical',
                        'MEDIUM': 'medium',
                        'LOW': 'low',
                        'UNKNOWN': 'low'
                    }
                    
                    issues.append({
                        'type': 'security_vulnerability',
                        'test_id': result.test_id,
                        'filename': result.filename,
                        'line': result.lineno,
                        'message': result.issue_text,
                        'confidence': result.confidence,
                        'severity': severity_mapping.get(result.severity, 'low'),
                        'code': result.code
                    })
                
                # Calculate security score
                if issues:
                    severity_weights = {
                        'critical': 0.4,
                        'medium': 0.2,
                        'low': 0.05
                    }
                    
                    deduction = sum(
                        severity_weights.get(issue['severity'], 0.1)
                        for issue in issues
                    )
                    score = max(0.0, 1.0 - deduction)
                else:
                    score = 1.0
                    
            finally:
                os.unlink(config_path)
                
        except Exception as e:
            logger.warning(f"Error running security analysis for {file_path}: {e}")
            # Fallback to basic security checks
            issues, score = SecurityAssessment._basic_security_check(file_path)
        
        return issues, score

    @staticmethod
    def _basic_security_check(file_path: str) -> Tuple[List[Dict[str, Any]], float]:
        """Basic security checks when bandit is not available"""
        issues = []
        score = 1.0
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for common security issues
            import re
            security_patterns = [
                (r'eval\s*\(', 'Use of eval() - potential code injection', 'high'),
                (r'exec\s*\(', 'Use of exec() - potential code injection', 'high'),
                (r'shell\s*=\s*', 'Direct shell commands - consider using subprocess', 'medium'),
                (r'os\.system\s*\(', 'Direct os.system() calls - security risk', 'medium'),
                (r'subprocess\.call\s*\([^)]*shell\s*=\s*True', 'Subprocess with shell=True - security risk', 'high'),
                (r'pickle\.load', 'Pickle deserialization - potential security risk', 'medium'),
                (r'yaml\.load\s*\([^)]*Loader\s*=\s*[\'"]Loader[\'"]\)', 'yaml.load() without safe loader', 'medium')
            ]
            
            for line_num, line in enumerate(content.splitlines(), 1):
                for pattern, message, severity in security_patterns:
                    if re.search(pattern, line, re.IGNORECASE):
                        issues.append({
                            'type': 'security_pattern',
                            'line': line_num,
                            'message': message,
                            'severity': severity,
                            'code': line.strip()
                        })
                        
                        severity_weight = {'high': 0.3, 'medium': 0.15, 'low': 0.05}.get(severity, 0.1)
                        score -= severity_weight
                        
        except Exception as e:
            logger.warning(f"Error in basic security check for {file_path}: {e}")
            score = 0.5
        
        return issues, max(0.0, score)


class CodeQualityAssessment:
    """Assesses code quality through style and convention checks"""

    @staticmethod
    def check_code_style(file_path: str) -> Tuple[List[Dict[str, Any]], float]:
        """Check Python code style using PEP8 guidelines"""
        issues = []
        score = 1.0
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.splitlines()
            
            # Basic style checks
            for line_num, line in enumerate(lines, 1):
                # Line length check
                if len(line) > 79:
                    issues.append({
                        'type': 'line_too_long',
                        'line': line_num,
                        'length': len(line),
                        'message': f'Line too long ({len(line)} > 79 characters)',
                        'severity': 'low'
                    })
                    score -= 0.02
                
                # Trailing whitespace
                if line.rstrip() != line:
                    issues.append({
                        'type': 'trailing_whitespace',
                        'line': line_num,
                        'message': 'Trailing whitespace detected',
                        'severity': 'low'
                    })
                    score -= 0.01
                
                # Indentation check (basic)
                if line.strip() and not line.startswith((' ', '\t', '#', '"""', "'''")):
                    if line.startswith('    ') and not line.strip().startswith('#'):
                        # Proper indentation
                        pass
                    elif line.strip():
                        issues.append({
                            'type': 'indentation_error',
                            'line': line_num,
                            'message': 'Potential indentation error',
                            'severity': 'medium'
                        })
                        score -= 0.05
            
            # Function/class naming conventions
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    if not re.match(r'^[a-z_][a-z0-9_]*$', node.name):
                        issues.append({
                            'type': 'naming_convention',
                            'line': node.lineno,
                            'name': node.name,
                            'message': f'Function name should use snake_case: {node.name}',
                            'severity': 'low'
                        })
                        score -= 0.02
                
                elif isinstance(node, ast.ClassDef):
                    if not re.match(r'^[A-Z][A-Za-z0-9]*$', node.name):
                        issues.append({
                            'type': 'naming_convention',
                            'line': node.lineno,
                            'name': node.name,
                            'message': f'Class name should use PascalCase: {node.name}',
                            'severity': 'low'
                        })
                        score -= 0.02
                        
        except Exception as e:
            logger.warning(f"Error checking code style for {file_path}: {e}")
            score = 0.5
        
        return issues, max(0.0, score)

    @staticmethod
    def calculate_maintainability_index(file_path: str) -> Tuple[List[Dict[str, Any]], float]:
        """Calculate maintainability index"""
        issues = []
        score = 1.0
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Use radon for maintainability analysis
            mi_result = radon_metrics.mi_visit(content)
            mi_score = mi_result
            
            if mi_score < 20:
                severity = 'critical'
                score_deduction = 0.4
            elif mi_score < 50:
                severity = 'medium'
                score_deduction = 0.2
            elif mi_score < 70:
                severity = 'low'
                score_deduction = 0.1
            else:
                severity = 'none'
                score_deduction = 0.0
            
            if severity != 'none':
                issues.append({
                    'type': 'maintainability_index',
                    'score': mi_score,
                    'message': f'Low maintainability index ({mi_score:.1f})',
                    'severity': severity
                })
                score -= score_deduction
                
        except Exception as e:
            logger.warning(f"Error calculating maintainability index for {file_path}: {e}")
            score = 0.5
        
        return issues, max(0.0, score)

    @staticmethod
    def _count_nested_loops(node: ast.For) -> int:
        """Count nested loops depth"""
        depth = 1
        for child in ast.walk(node):
            if isinstance(child, ast.For) and child != node:
                depth += 1
        return depth


class DocumentationAssessment:
    """Assesses documentation completeness and quality"""

    @staticmethod
    def analyze_documentation_coverage(file_path: str) -> Tuple[List[Dict[str, Any]], float]:
        """Analyze documentation coverage"""
        issues = []
        score = 1.0
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            total_functions = 0
            documented_functions = 0
            total_classes = 0
            documented_classes = 0
            total_modules = 0
            documented_modules = 0
            
            # Module-level docstring
            docstring = ast.get_docstring(tree)
            if docstring:
                documented_modules = 1
            total_modules = 1
            
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    total_functions += 1
                    if ast.get_docstring(node):
                        documented_functions += 1
                
                elif isinstance(node, ast.ClassDef):
                    total_classes += 1
                    if ast.get_docstring(node):
                        documented_classes += 1
            
            # Calculate coverage scores
            if total_functions > 0:
                func_coverage = documented_functions / total_functions
                if func_coverage < 0.5:
                    issues.append({
                        'type': 'low_function_documentation',
                        'message': f'Low function documentation coverage: {func_coverage:.1%}',
                        'severity': 'medium',
                        'metrics': {
                            'documented': documented_functions,
                            'total': total_functions,
                            'coverage': func_coverage
                        }
                    })
                    score -= 0.2
                else:
                    issues.append({
                        'type': 'function_documentation',
                        'message': f'Function documentation coverage: {func_coverage:.1%}',
                        'metrics': {
                            'documented': documented_functions,
                            'total': total_functions,
                            'coverage': func_coverage
                        }
                    })
            
            if total_classes > 0:
                class_coverage = documented_classes / total_classes
                if class_coverage < 0.5:
                    issues.append({
                        'type': 'low_class_documentation',
                        'message': f'Low class documentation coverage: {class_coverage:.1%}',
                        'severity': 'medium',
                        'metrics': {
                            'documented': documented_classes,
                            'total': total_classes,
                            'coverage': class_coverage
                        }
                    })
                    score -= 0.2
                else:
                    issues.append({
                        'type': 'class_documentation',
                        'message': f'Class documentation coverage: {class_coverage:.1%}',
                        'metrics': {
                            'documented': documented_classes,
                            'total': total_classes,
                            'coverage': class_coverage
                        }
                    })
            
            # Module documentation check
            module_coverage = documented_modules / total_modules if total_modules > 0 else 1.0
            if module_coverage < 1.0:
                issues.append({
                    'type': 'missing_module_docstring',
                    'message': 'Module missing docstring',
                    'severity': 'low'
                })
                score -= 0.1
            
        except Exception as e:
            logger.warning(f"Error analyzing documentation for {file_path}: {e}")
            score = 0.5
        
        return issues, max(0.0, score)

    @staticmethod
    def check_docstring_quality(file_path: str) -> Tuple[List[Dict[str, Any]], float]:
        """Check docstring quality"""
        issues = []
        score = 1.0
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                docstring = ast.get_docstring(node)
                
                if docstring:
                    # Check docstring quality
                    if len(docstring) < 20:
                        issues.append({
                            'type': 'short_docstring',
                            'line': node.lineno,
                            'name': node.name if hasattr(node, 'name') else 'module',
                            'message': 'Docstring is too short - should be at least 20 characters',
                            'severity': 'low'
                        })
                        score -= 0.05
                    
                    # Check for incomplete docstrings
                    if isinstance(node, ast.FunctionDef):
                        if 'TODO' in docstring.upper() or 'FIXME' in docstring.upper():
                            issues.append({
                                'type': 'incomplete_docstring',
                                'line': node.lineno,
                                'name': node.name,
                                'message': 'Docstring contains TODO/FIXME - needs completion',
                                'severity': 'medium'
                            })
                            score -= 0.1
                    
                    # Check for proper docstring format
                    lines = docstring.split('\n')
                    if len(lines) > 1 and not lines[0].strip().endswith('.'):
                        issues.append({
                            'type': 'docstring_format',
                            'line': node.lineno,
                            'name': node.name if hasattr(node, 'name') else 'module',
                            'message': 'Docstring first line should end with a period',
                            'severity': 'low'
                        })
                        score -= 0.02
                        
        except Exception as e:
            logger.warning(f"Error checking docstring quality for {file_path}: {e}")
            score = 0.5
        
        return issues, max(0.0, score)


class QualityAssessmentEngine:
    """Main quality assessment engine orchestrator"""

    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.assessment_modules = {
            QualityDimension.CORRECTNESS: [CorrectnessAssessment.analyze_syntax_errors, 
                                         CorrectnessAssessment.check_type_hints_usage],
            QualityDimension.PERFORMANCE: [PerformanceAssessment.analyze_cyclomatic_complexity,
                                         PerformanceAssessment.check_algorithm_efficiency],
            QualityDimension.SECURITY: [SecurityAssessment.run_bandit_analysis],
            QualityDimension.CODE_QUALITY: [CodeQualityAssessment.check_code_style,
                                          CodeQualityAssessment.calculate_maintainability_index],
            QualityDimension.DOCUMENTATION: [DocumentationAssessment.analyze_documentation_coverage,
                                           DocumentationAssessment.check_docstring_quality]
        }

    def assess_file(self, file_path: str, source_dir: str) -> FileAssessment:
        """Assess a single file across all dimensions"""
        import time
        start_time = time.time()
        
        logger.info(f"Assessing file: {file_path}")
        
        scores = {}
        all_issues = []
        metrics = {}
        
        # Make file_path relative to source directory
        relative_file_path = os.path.relpath(file_path, source_dir)
        
        # Run assessments in parallel
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_dimension = {}
            
            for dimension, assessment_functions in self.assessment_modules.items():
                for assessment_func in assessment_functions:
                    future = executor.submit(assessment_func, file_path)
                    future_to_dimension[(dimension, assessment_func.__name__)] = future
            
            # Collect results
            for (dimension, func_name), future in future_to_dimension.items():
                try:
                    issues, score = future.result()
                    
                    if dimension not in scores:
                        scores[dimension] = QualityScore(
                            dimension=dimension,
                            score=0.0,
                            level="",
                            details={},
                            suggestions=[],
                            violations=[],
                            confidence=0.0
                        )
                    
                    # Aggregate issues and update score
                    all_issues.extend(issues)
                    current_score = scores[dimension].score
                    scores[dimension].score = (current_score + score) / 2
                    
                except Exception as e:
                    logger.error(f"Error in {func_name} for {file_path}: {e}")
                    
                    if dimension not in scores:
                        scores[dimension] = QualityScore(
                            dimension=dimension,
                            score=0.0,
                            level="",
                            details={},
                            suggestions=[],
                            violations=[],
                            confidence=0.0
                        )
        
        # Finalize scores and add metadata
        for dimension, score in scores.items():
            score.level = self._get_quality_level(score.score)
            score.confidence = 0.8  # Default confidence
            
            # Filter and categorize violations
            score.violations = [
                issue for issue in all_issues 
                if issue.get('severity') in ['critical', 'medium']
            ]
            
            # Generate suggestions based on issues
            score.suggestions = self._generate_suggestions(dimension, all_issues)
            
            # Add dimension-specific details
            score.details = self._get_dimension_details(dimension, all_issues)
        
        execution_time = time.time() - start_time
        
        # Calculate overall score
        overall_score = sum(score.score for score in scores.values()) / len(scores)
        
        return FileAssessment(
            file_path=relative_file_path,
            overall_score=overall_score,
            scores=scores,
            metrics=metrics,
            execution_time=execution_time
        )

    def assess_project(self, project_path: str) -> ProjectAssessment:
        """Assess entire project"""
        import time
        start_time = time.time()
        
        logger.info(f"Starting project assessment: {project_path}")
        
        # Find all Python files
        python_files = []
        for root, dirs, files in os.walk(project_path):
            # Skip common non-source directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in 
                      ['__pycache__', 'node_modules', 'venv', 'env', 'build', 'dist']]
            
            for file in files:
                if file.endswith('.py'):
                    python_files.append(os.path.join(root, file))
        
        logger.info(f"Found {len(python_files)} Python files to assess")
        
        # Assess all files
        assessments = []
        all_critical_issues = []
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_file = {
                executor.submit(self.assess_file, file_path, project_path): file_path
                for file_path in python_files
            }
            
            for future in as_completed(future_to_file):
                file_path = future_to_file[future]
                try:
                    assessment = future.result()
                    assessments.append(assessment)
                    
                    # Collect critical issues
                    for score in assessment.scores.values():
                        all_critical_issues.extend(score.violations)
                        
                except Exception as e:
                    logger.error(f"Error assessing {file_path}: {e}")
        
        # Calculate project-level metrics
        total_files = len(assessments)
        if total_files > 0:
            overall_score = sum(ass.overall_score for ass in assessments) / total_files
            
            # Dimension scores
            dimension_scores = {}
            for dimension in QualityDimension:
                dimension_scores[dimension] = sum(
                    ass.scores.get(dimension, QualityScore(
                        dimension, 0.0, "", {}, [], [], 0.0
                    )).score for ass in assessments
                ) / total_files
        else:
            overall_score = 0.0
            dimension_scores = {dim: 0.0 for dim in QualityDimension}
        
        # Generate recommendations
        recommendations = self._generate_project_recommendations(assessments)
        
        execution_time = time.time() - start_time
        
        return ProjectAssessment(
            project_path=project_path,
            files_assessed=[ass.file_path for ass in assessments],
            overall_score=overall_score,
            dimension_scores=dimension_scores,
            critical_issues=all_critical_issues,
            recommendations=recommendations,
            metrics={
                'total_files': total_files,
                'assessment_time': execution_time,
                'average_file_score': sum(ass.overall_score for ass in assessments) / max(1, total_files),
                'worst_files': sorted(assessments, key=lambda x: x.overall_score)[:5]
            },
            assessment_timestamp='2025-11-20T15:42:52Z'
        )

    def _get_quality_level(self, score: float) -> str:
        """Get quality level based on score"""
        if score >= 0.9:
            return "EXCELLENT"
        elif score >= 0.7:
            return "GOOD"
        elif score >= 0.5:
            return "FAIR"
        else:
            return "POOR"

    def _generate_suggestions(self, dimension: QualityDimension, issues: List[Dict[str, Any]]) -> List[str]:
        """Generate improvement suggestions based on issues"""
        suggestions = []
        
        issue_counts = {}
        for issue in issues:
            issue_type = issue.get('type', 'unknown')
            issue_counts[issue_type] = issue_counts.get(issue_type, 0) + 1
        
        if dimension == QualityDimension.CORRECTNESS:
            if 'syntax_error' in issue_counts:
                suggestions.append("Fix syntax errors in your code")
            if 'unreachable_code' in issue_counts:
                suggestions.append("Remove unreachable code blocks")
            if 'low_type_coverage' in issue_counts:
                suggestions.append("Add type hints to improve code correctness")
                
        elif dimension == QualityDimension.PERFORMANCE:
            if 'high_complexity' in issue_counts or 'very_high_complexity' in issue_counts:
                suggestions.append("Refactor complex functions to improve performance")
            if 'deeply_nested_loop' in issue_counts:
                suggestions.append("Optimize nested loops or consider different algorithms")
                
        elif dimension == QualityDimension.SECURITY:
            suggestions.append("Review security vulnerabilities and implement fixes")
            suggestions.append("Use secure coding practices and avoid dangerous patterns")
            
        elif dimension == QualityDimension.CODE_QUALITY:
            if 'line_too_long' in issue_counts:
                suggestions.append("Break long lines to improve readability")
            if 'naming_convention' in issue_counts:
                suggestions.append("Follow Python naming conventions (PEP 8)")
                
        elif dimension == QualityDimension.DOCUMENTATION:
            if 'low_function_documentation' in issue_counts:
                suggestions.append("Add docstrings to functions and methods")
            if 'short_docstring' in issue_counts:
                suggestions.append("Write more detailed docstrings")
        
        return suggestions[:5]  # Limit to top 5 suggestions

    def _get_dimension_details(self, dimension: QualityDimension, issues: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get dimension-specific details"""
        dimension_issues = [issue for issue in issues if True]  # Simplified for now
        
        if dimension == QualityDimension.CORRECTNESS:
            return {
                'syntax_errors': len([i for i in dimension_issues if i.get('type') == 'syntax_error']),
                'type_coverage': sum(1 for i in dimension_issues if 'coverage' in i.get('metrics', {})) / max(1, len(dimension_issues))
            }
        elif dimension == QualityDimension.PERFORMANCE:
            return {
                'high_complexity_functions': len([i for i in dimension_issues if 'complexity' in str(i)]),
                'nested_loops': len([i for i in dimension_issues if 'nested_loop' in i.get('type', '')])
            }
        elif dimension == QualityDimension.SECURITY:
            return {
                'security_vulnerabilities': len(dimension_issues),
                'high_severity_issues': len([i for i in dimension_issues if i.get('severity') == 'critical'])
            }
        else:
            return {
                'total_issues': len(dimension_issues),
                'issue_types': list(set(i.get('type', 'unknown') for i in dimension_issues))
            }

    def _generate_project_recommendations(self, assessments: List[FileAssessment]) -> List[str]:
        """Generate project-wide recommendations"""
        recommendations = []
        
        if not assessments:
            return ["No Python files found to assess"]
        
        # Analyze patterns across all files
        total_critical_issues = sum(
            len(score.violations) for ass in assessments 
            for score in ass.scores.values()
        )
        
        if total_critical_issues > len(assessments) * 3:
            recommendations.append("Address critical security and correctness issues before proceeding")
        
        # Check for consistently low-performing files
        low_score_files = [ass.file_path for ass in assessments if ass.overall_score < 0.5]
        if len(low_score_files) > len(assessments) * 0.2:
            recommendations.append("Refactor low-quality files to improve overall project quality")
        
        # Check dimension averages
        dimension_averages = {}
        for dimension in QualityDimension:
            avg_score = sum(
                ass.scores.get(dimension, QualityScore(dimension, 0.0, "", {}, [], [], 0.0)).score
                for ass in assessments
            ) / len(assessments)
            dimension_averages[dimension] = avg_score
        
        # Generate specific recommendations
        for dimension, avg_score in dimension_averages.items():
            if avg_score < 0.5:
                recommendations.append(f"Focus on improving {dimension.value} - current score: {avg_score:.1%}")
        
        # Add general recommendations
        recommendations.extend([
            "Establish code review processes to maintain quality standards",
            "Implement automated quality checks in CI/CD pipeline",
            "Regular refactoring to maintain code quality over time"
        ])
        
        return recommendations[:10]  # Limit to top 10 recommendations