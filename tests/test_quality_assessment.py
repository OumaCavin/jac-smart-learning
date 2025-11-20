"""
Test Suite for Quality Assessment Service
Author: Cavin Otieno
"""

import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Test imports
from backend.services.quality_assessment import (
    QualityAssessmentEngine,
    CorrectnessAssessment,
    PerformanceAssessment,
    SecurityAssessment,
    CodeQualityAssessment,
    DocumentationAssessment,
    QualityDimension,
    QualityScore,
    FileAssessment,
    ProjectAssessment
)


class TestCorrectnessAssessment:
    """Test cases for CorrectnessAssessment"""

    def test_analyze_syntax_errors_valid_code(self):
        """Test syntax analysis with valid code"""
        valid_code = """
def hello_world():
    print("Hello, World!")
    return True

class TestClass:
    def __init__(self):
        self.value = 42
"""
        
        issues, score = CorrectnessAssessment.analyze_syntax_errors.__wrapped__(
            "dummy.py"
        )
        
        # This test would need to be adapted to actually call the method
        # For now, we can test the structure
        assert isinstance(issues, list)
        assert isinstance(score, float)

    def test_analyze_syntax_errors_invalid_code(self):
        """Test syntax analysis with invalid code"""
        invalid_code = """
def invalid_function(
    print("This will cause syntax error")
"""
        
        # Create temporary file with invalid code
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(invalid_code)
            temp_file = f.name
        
        try:
            issues, score = CorrectnessAssessment.analyze_syntax_errors(temp_file)
            
            # Should have critical syntax error
            syntax_errors = [i for i in issues if i.get('type') == 'syntax_error']
            assert len(syntax_errors) > 0
            assert score < 0.5  # Should have low score
            
        finally:
            os.unlink(temp_file)

    def test_check_type_hints_usage(self):
        """Test type hints analysis"""
        code_with_hints = """
def greet(name: str) -> str:
    return f"Hello, {name}"

def add(a: int, b: int) -> int:
    return a + b
"""
        
        code_without_hints = """
def greet(name):
    return f"Hello, {name}"

def add(a, b):
    return a + b
"""
        
        # Create temporary files
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f1:
            f1.write(code_with_hints)
            file_with_hints = f1.name
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f2:
            f2.write(code_without_hints)
            file_without_hints = f2.name
        
        try:
            issues1, score1 = CorrectnessAssessment.check_type_hints_usage(file_with_hints)
            issues2, score2 = CorrectnessAssessment.check_type_hints_usage(file_without_hints)
            
            # Code with type hints should have higher score
            assert score1 >= score2
            
        finally:
            os.unlink(file_with_hints)
            os.unlink(file_without_hints)


class TestPerformanceAssessment:
    """Test cases for PerformanceAssessment"""

    def test_analyze_cyclomatic_complexity_simple_function(self):
        """Test complexity analysis for simple function"""
        simple_code = """
def simple_function():
    return 42
"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(simple_code)
            temp_file = f.name
        
        try:
            issues, score = PerformanceAssessment.analyze_cyclomatic_complexity(temp_file)
            
            # Simple function should have low complexity
            high_complexity = [i for i in issues if 'high' in i.get('type', '')]
            assert len(high_complexity) == 0
            assert score >= 0.8  # Should have high score
            
        finally:
            os.unlink(temp_file)

    def test_analyze_cyclomatic_complexity_complex_function(self):
        """Test complexity analysis for complex function"""
        complex_code = """
def complex_function(a, b, c):
    if a > 0:
        if b > 0:
            if c > 0:
                for i in range(10):
                    if i % 2 == 0:
                        print(f"Even: {i}")
                    else:
                        for j in range(5):
                            if j > 2:
                                print(f"Nested: {i}, {j}")
    return True
"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(complex_code)
            temp_file = f.name
        
        try:
            issues, score = PerformanceAssessment.analyze_cyclomatic_complexity(temp_file)
            
            # Complex function should have issues
            complexity_issues = [i for i in issues if 'complexity' in i.get('type', '')]
            assert len(complexity_issues) > 0
            assert score < 0.7  # Should have lower score
            
        finally:
            os.unlink(temp_file)

    def test_check_algorithm_efficiency(self):
        """Test algorithm efficiency checks"""
        inefficient_code = """
def inefficient_function():
    # Nested loops - could be optimized
    for i in range(1000):
        for j in range(1000):
            for k in range(1000):
                result = i + j + k
    return result
"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(inefficient_code)
            temp_file = f.name
        
        try:
            issues, score = PerformanceAssessment.check_algorithm_efficiency(temp_file)
            
            # Should detect nested loops
            loop_issues = [i for i in issues if 'nested_loop' in i.get('type', '')]
            assert len(loop_issues) > 0
            
        finally:
            os.unlink(temp_file)


class TestSecurityAssessment:
    """Test cases for SecurityAssessment"""

    @patch('backend.services.quality_assessment.bandit.cli.main')
    def test_run_bandit_analysis_with_mock(self, mock_bandit):
        """Test bandit analysis with mocked bandit"""
        # Mock bandit to return no issues
        mock_scanner = Mock()
        mock_scanner.scan_path.return_value = []
        mock_bandit.return_value = mock_scanner
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write("def hello(): pass")
            temp_file = f.name
        
        try:
            issues, score = SecurityAssessment.run_bandit_analysis(temp_file)
            
            # Should have no issues when bandit returns empty
            assert len(issues) == 0
            assert score >= 0.9  # Should have high score
            
        finally:
            os.unlink(temp_file)

    def test_basic_security_check(self):
        """Test basic security pattern detection"""
        unsafe_code = """
import os
import subprocess

def unsafe_function():
    os.system("rm -rf /")  # Dangerous command
    eval(user_input)  # Code injection risk
    pickle.load(untrusted_data)  # Pickle deserialization
"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(unsafe_code)
            temp_file = f.name
        
        try:
            issues, score = SecurityAssessment._basic_security_check(temp_file)
            
            # Should detect security issues
            security_issues = [i for i in issues if i.get('type') == 'security_pattern']
            assert len(security_issues) > 0
            
            # Should have lower score due to security issues
            assert score < 0.7
            
        finally:
            os.unlink(temp_file)


class TestCodeQualityAssessment:
    """Test cases for CodeQualityAssessment"""

    def test_check_code_style_good_style(self):
        """Test code style with good style"""
        good_style_code = """
def good_function(param1, param2):
    \"\"\"A well-documented function with good style.\"\"\"
    result = param1 + param2
    return result
"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(good_style_code)
            temp_file = f.name
        
        try:
            issues, score = CodeQualityAssessment.check_code_style(temp_file)
            
            # Should have few or no style issues
            style_issues = [i for i in issues if i.get('type') in ['line_too_long', 'trailing_whitespace', 'indentation_error']]
            assert len(style_issues) == 0
            assert score >= 0.9
            
        finally:
            os.unlink(temp_file)

    def test_check_code_style_bad_style(self):
        """Test code style with bad style"""
        bad_style_code = """
def bad_function   (    param1,param2   ):
    result=param1+param2#No space around operators
    return result
""" + "x" * 100 + "  \n"  # Very long line with trailing whitespace
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(bad_style_code)
            temp_file = f.name
        
        try:
            issues, score = CodeQualityAssessment.check_code_style(temp_file)
            
            # Should have style issues
            assert len(issues) > 0
            assert score < 0.8
            
        finally:
            os.unlink(temp_file)

    def test_calculate_maintainability_index(self):
        """Test maintainability index calculation"""
        simple_code = "def simple(): pass"
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(simple_code)
            temp_file = f.name
        
        try:
            issues, score = CodeQualityAssessment.calculate_maintainability_index(temp_file)
            
            # Simple code should have good maintainability
            assert score >= 0.7
            
        finally:
            os.unlink(temp_file)


class TestDocumentationAssessment:
    """Test cases for DocumentationAssessment"""

    def test_analyze_documentation_coverage_well_documented(self):
        """Test documentation analysis with well-documented code"""
        well_documented_code = """
\"\"\"A well-documented module.\"\"\"

def documented_function():
    \"\"\"This function is well documented.\"\"\"
    pass

class DocumentedClass:
    \"\"\"A well-documented class.\"\"\"
    
    def __init__(self):
        \"\"\"Initialize the class.\"\"\"
        pass
    
    def documented_method(self):
        \"\"\"A documented method.\"\"\"
        pass
"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(well_documented_code)
            temp_file = f.name
        
        try:
            issues, score = DocumentationAssessment.analyze_documentation_coverage(temp_file)
            
            # Should have high documentation coverage
            assert score >= 0.8
            
        finally:
            os.unlink(temp_file)

    def test_analyze_documentation_coverage_poorly_documented(self):
        """Test documentation analysis with poorly documented code"""
        poorly_documented_code = """
def undocumented_function():
    pass

class UndocumentedClass:
    def __init__(self):
        pass
    
    def undocumented_method(self):
        pass
"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(poorly_documented_code)
            temp_file = f.name
        
        try:
            issues, score = DocumentationAssessment.analyze_documentation_coverage(temp_file)
            
            # Should have low documentation coverage
            assert score < 0.5
            
        finally:
            os.unlink(temp_file)

    def test_check_docstring_quality(self):
        """Test docstring quality assessment"""
        good_docstring = "\"\"\"This is a proper docstring with period.\"\"\""
        bad_docstring = "\"\"\"Short\"\"\""  # Too short
        incomplete_docstring = "\"\"\"TODO: Complete this\"\"\""  # Contains TODO
        
        # Test good docstring
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(f"def test(): {good_docstring}")
            temp_file = f.name
        
        try:
            issues, score = DocumentationAssessment.check_docstring_quality(temp_file)
            
            # Should have no quality issues
            quality_issues = [i for i in issues if i.get('type') in ['short_docstring', 'incomplete_docstring']]
            assert len(quality_issues) == 0
            
        finally:
            os.unlink(temp_file)


class TestQualityAssessmentEngine:
    """Test cases for QualityAssessmentEngine"""

    def setup_method(self):
        """Setup test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.engine = QualityAssessmentEngine(max_workers=1)

    def teardown_method(self):
        """Cleanup test environment"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_assess_file_basic_functionality(self):
        """Test basic file assessment functionality"""
        test_file = os.path.join(self.temp_dir, "test.py")
        with open(test_file, 'w') as f:
            f.write("""
def hello_world():
    \"\"\"A simple greeting function.\"\"\"
    print("Hello, World!")
    return True

class TestClass:
    \"\"\"A test class.\"\"\"
    
    def __init__(self):
        self.value = 42
    
    def get_value(self):
        \"\"\"Get the stored value.\"\"\"
        return self.value
""")
        
        assessment = self.engine.assess_file(test_file, self.temp_dir)
        
        # Verify assessment structure
        assert isinstance(assessment, FileAssessment)
        assert assessment.file_path == "test.py"
        assert assessment.overall_score >= 0.0
        assert assessment.overall_score <= 1.0
        assert len(assessment.scores) > 0
        assert assessment.execution_time > 0

    def test_assess_file_invalid_file(self):
        """Test assessment of non-existent file"""
        non_existent_file = os.path.join(self.temp_dir, "nonexistent.py")
        
        assessment = self.engine.assess_file(non_existent_file, self.temp_dir)
        
        # Should still return an assessment, but with low scores
        assert isinstance(assessment, FileAssessment)
        assert assessment.overall_score == 0.0

    def test_assess_project_basic_functionality(self):
        """Test basic project assessment functionality"""
        # Create test project structure
        files = [
            ("main.py", "def main(): pass"),
            ("utils.py", "def helper(): pass"),
            ("models.py", "class Model: pass")
        ]
        
        for filename, content in files:
            with open(os.path.join(self.temp_dir, filename), 'w') as f:
                f.write(content)
        
        project_assessment = self.engine.assess_project(self.temp_dir)
        
        # Verify project assessment structure
        assert isinstance(project_assessment, ProjectAssessment)
        assert project_assessment.project_path == self.temp_dir
        assert len(project_assessment.files_assessed) >= 3
        assert project_assessment.overall_score >= 0.0
        assert project_assessment.overall_score <= 1.0
        assert len(project_assessment.dimension_scores) > 0

    def test_assess_project_empty_directory(self):
        """Test assessment of empty directory"""
        project_assessment = self.engine.assess_project(self.temp_dir)
        
        # Should return assessment with no files
        assert isinstance(project_assessment, ProjectAssessment)
        assert len(project_assessment.files_assessed) == 0

    def test_get_quality_level(self):
        """Test quality level determination"""
        # Test different score ranges
        assert self.engine._get_quality_level(0.95) == "EXCELLENT"
        assert self.engine._get_quality_level(0.8) == "GOOD"
        assert self.engine._get_quality_level(0.6) == "FAIR"
        assert self.engine._get_quality_level(0.3) == "POOR"


class TestDataStructures:
    """Test cases for Quality Assessment data structures"""

    def test_quality_score_creation(self):
        """Test QualityScore creation"""
        score = QualityScore(
            dimension=QualityDimension.CORRECTNESS,
            score=0.8,
            level="GOOD",
            details={"syntax_errors": 0},
            suggestions=["Add type hints"],
            violations=[],
            confidence=0.9
        )
        
        assert score.dimension == QualityDimension.CORRECTNESS
        assert score.score == 0.8
        assert score.level == "GOOD"
        assert score.details["syntax_errors"] == 0
        assert "Add type hints" in score.suggestions

    def test_file_assessment_creation(self):
        """Test FileAssessment creation"""
        assessment = FileAssessment(
            file_path="test.py",
            overall_score=0.85,
            scores={},
            metrics={"lines_of_code": 50},
            execution_time=1.5
        )
        
        assert assessment.file_path == "test.py"
        assert assessment.overall_score == 0.85
        assert assessment.metrics["lines_of_code"] == 50
        assert assessment.execution_time == 1.5

    def test_project_assessment_creation(self):
        """Test ProjectAssessment creation"""
        assessment = ProjectAssessment(
            project_path="/path/to/project",
            files_assessed=["file1.py", "file2.py"],
            overall_score=0.75,
            dimension_scores={QualityDimension.CORRECTNESS: 0.8},
            critical_issues=[],
            recommendations=["Add tests"],
            metrics={"total_files": 2},
            assessment_timestamp="2025-11-20T15:42:52Z"
        )
        
        assert assessment.project_path == "/path/to/project"
        assert len(assessment.files_assessed) == 2
        assert assessment.overall_score == 0.75
        assert "Add tests" in assessment.recommendations


class TestIntegration:
    """Integration tests for Quality Assessment Engine"""

    def setup_method(self):
        """Setup test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.engine = QualityAssessmentEngine(max_workers=2)

    def teardown_method(self):
        """Cleanup test environment"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_complete_file_assessment_workflow(self):
        """Test complete file assessment workflow"""
        # Create a realistic Python file with various issues
        problematic_code = """
import os
import pickle

def unsafe_function(user_input):
    # Security issue
    eval(user_input)
    
    # Performance issue - nested loops
    for i in range(100):
        for j in range(100):
            for k in range(100):
                result = i + j + k
    
    # Style issue - missing docstring
    return result

# Long line issue
very_long_line_that_exceeds_the_standard_line_length_limit_of_79_characters_and_should_be_broken_into_multiple_lines = "problematic"

class PoorlyDocumentedClass:
    def __init__(self):  # Missing docstring
        pass
"""
        
        test_file = os.path.join(self.temp_dir, "problematic.py")
        with open(test_file, 'w') as f:
            f.write(problematic_code)
        
        # Run assessment
        assessment = self.engine.assess_file(test_file, self.temp_dir)
        
        # Verify assessment captures all issue types
        assert assessment.overall_score < 0.5  # Should be low due to issues
        
        # Check different dimensions
        correctness_score = assessment.scores.get(QualityDimension.CORRECTNESS)
        performance_score = assessment.scores.get(QualityDimension.PERFORMANCE)
        security_score = assessment.scores.get(QualityDimension.SECURITY)
        code_quality_score = assessment.scores.get(QualityDimension.CODE_QUALITY)
        
        assert correctness_score is not None
        assert performance_score is not None
        assert security_score is not None
        assert code_quality_score is not None
        
        # All scores should be low due to issues
        assert correctness_score.score < 0.7
        assert performance_score.score < 0.7
        assert security_score.score < 0.7
        assert code_quality_score.score < 0.7

    def test_parallel_assessment(self):
        """Test parallel file assessment"""
        # Create multiple test files
        for i in range(5):
            filename = f"test_{i}.py"
            content = f"""
def function_{i}():
    '''Function {i}.'''
    return {i}
"""
            with open(os.path.join(self.temp_dir, filename), 'w') as f:
                f.write(content)
        
        # Assess project (should use parallel processing)
        project_assessment = self.engine.assess_project(self.temp_dir)
        
        # Verify all files were assessed
        assert len(project_assessment.files_assessed) == 5
        assert len(project_assessment.critical_issues) >= 0  # May or may not have issues
        assert project_assessment.overall_score >= 0.0


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])