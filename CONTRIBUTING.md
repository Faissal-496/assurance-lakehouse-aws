# Contributing

## Guidelines

- Code follows PEP 8
- Use type hints for all functions
- Max line length: 100 characters
- Add docstrings to modules and functions
- Use structured logging

## Development Setup

```bash
git clone <repo>
cd assurance-lakehouse-aws
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Submitting Changes

1. Create feature branch: `git checkout -b feature/name`
2. Write code with clear commits
3. Test: `make run-pipeline`
4. Submit pull request with description

## Code Standards

- Error handling with try-except
- Appropriate log levels (INFO, WARN, ERROR)
- Update documentation if adding features
- Test with different configurations
   - Reference related issues
   - Ensure CI checks pass
   - Be responsive to review feedback

### Example Contribution: Adding a New Transformation

#### Step 1: Create Module

Create `src/lakehouse/transformation/custom_transform.py`:

```python
from pyspark.sql import SparkSession, DataFrame
from lakehouse.paths import PathResolver

def run(spark: SparkSession, resolver: PathResolver) -> DataFrame:
    """
    Custom transformation step.
    
    Processes data with business-specific logic.
    
    Args:
        spark: SparkSession instance
        resolver: PathResolver for S3 paths
        
    Returns:
        Transformed DataFrame
    """
    logger.info("Starting custom transformation")
    
    try:
        # Read from silver layer
        silver_path = resolver.s3_layer_path("silver", "data")
        df = spark.read.parquet(silver_path)
        
        # Apply transformation logic
        result = df.filter("status = 'active'")
        
        # Write to gold layer
        output_path = resolver.s3_layer_path("gold", "custom_output")
        result.write.mode("overwrite").parquet(output_path)
        
        logger.info(f"Custom transformation completed: {output_path}")
        return result
        
    except Exception as e:
        logger.error(f"Custom transformation failed: {str(e)}", exc_info=True)
        raise
```

#### Step 2: Update Main Orchestrator

Add to `src/lakehouse/main.py`:

```python
from lakehouse.transformation import custom_transform

# In main() function:
try:
    custom_transform.run(spark, resolver)
    logger.info("Custom transformation succeeded")
except Exception as e:
    logger.error(f"Custom transformation failed: {str(e)}")
    raise
```

#### Step 3: Update Configuration (if needed)

Add to `config/paths.yaml` if new layer needed:

```yaml
paths:
  custom_output: custom_output
```

## Code Review Process

All contributions go through code review:

1. Automated checks must pass
2. Code review by maintainers
3. Feedback and iterations
4. Approval and merge

### Review Criteria

- Code quality and standards
- Functionality correctness
- Documentation completeness
- Test coverage
- Performance impact

## Git Workflow

### Commit Messages

Write clear commit messages:

```
Add short description (50 chars)

More detailed explanation if needed.
- Point 1
- Point 2

Fixes #123
```

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation
- [ ] Performance improvement

## Testing
Describe testing performed

## Related Issues
Fixes #123

## Configuration Changes
List any new config variables needed
```

## Documentation Contributions

### Updating README

When updating documentation:

1. Keep information accurate and current
2. Use professional tone
3. Remove outdated sections
4. Add examples when helpful
5. Proofread before submitting

### Adding Examples

Good examples should:

- Be concise and practical
- Include expected output
- Handle common scenarios
- Include error cases

## Testing Guidelines

### Manual Testing

```bash
# Test full pipeline
export APP_ENV=dev
make run-pipeline

# Test individual stage
python3 run_bronze.py

# Check specific functionality
python3 -c "from lakehouse.paths import PathResolver; PathResolver()"
```

### Configuration Testing

Test with different configurations:

```bash
# Dev environment
export APP_ENV=dev
make run-pipeline

# Production environment
export APP_ENV=prod
export SPARK_DRIVER_MEMORY=8g
make run-pipeline

# Custom settings
export SPARK_SHUFFLE_PARTS=8
make run-pipeline
```

## Deployment

When changes are ready for deployment:

1. Tag the release
2. Update version in documentation
3. Create release notes
4. Deploy to production following safe deployment practices

## Questions?

- Open an issue with your question
- Check existing discussions
- Review PIPELINE_GUIDE.md for technical details
- Check CONFIG_USAGE.md for configuration help

## License

By contributing, you agree that your contributions will be licensed under the project's license.

---

Thank you for contributing to making this project better!
