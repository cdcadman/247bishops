# Contributing to 247 bishops

By contributing to 247 bishops, you agree that your contributions will be licensed under its GNU AGPL 3.
If you are adding something to this web app which is not your own, it must either in the public domain or have
a license which is compatible with the GNU AGPL 3.

## Guidelines

To contribute code changes to this repo, create a pull request into the main branch.
The following checks have to pass before it can merge (defined in `code_checks.yml`).

* licensecheck - confirms that all python packages in requirements.txt are compatible with this project's license.
* pip_audit - confirms that no python packages used by this project (including in `requirements-dev.txt`) have reported vulnerabilities.
  * If any vulnerabilities are reported and if there is a fix version, update `requirements.txt` by running `calc_deterministic.sh`.
* bandit - checks for unsafe python code in this repo.
  * To ignore a reported issue, please use the code.  For example, putting `# nosec B608` on a line will ignore a potential SQL injection issue.
  * If you have to insert the value of a variable into a query string, please ensure that the variable is trusted or checked.  For example:

```python
# `positions` is an untrusted list of strings.  The values are passed as parameters, but the right number of markers needs to be inserted into the query.
result = conn.exec_driver_sql(
    f"select * from position_data where position in ({', '.join('%s' for _ in positions)})",  # nosec B608
    tuple(positions),
)
```

* black - enforces black formatting.  Please run `python -m black .` before creating a pull request.
* isort - enforces import sorting.  Please run `python -m isort .` before creating a pull request.
* pylint - checks for errors or warnings.  If you have to ignore a message, please include the code.
For example: `from webapp_python import app  # pylint:disable=unused-import`
* pytest - fails on warnings and checks for 100% code coverage.
  * If you are unable to prevent a warning, please ignore it in `pyproject.toml` in `filterwarnings` using the precise line number.
  For example: `"ignore:Use list:DeprecationWarning:msal.token_cache:164",`
  * If you are unable to ensure 100% code coverage, please use `# pragma: no cover` sparingly, preferably only in tests.  For example:

```python
# expected_condition() should return True, possibly after a brief delay
while True:
    if expected_condition():
        break
    time.sleep(0.1) # pragma: no cover
```

## Adding python packages

To add a python package, place it in `base_reqs.txt` with no version specifier.  Then run `calc_deterministic.sh` to update `requirements.txt`.

## Adding front end 3rd party dependencies (javascript/css/images)

This project uses its own python code to manage front end 3rd party dependencies.

* Dependencies are saved in the `front_end_deps` folder, which is ignored by git.
* Installation is performed by the `install_front_end_deps` local python package, which is run as part of the testing and deployment workflows.

To add or update a dependency, edit the `install_front_end_deps` local python package.  Whenever you run the package (`python -m install_front_end_deps`),
it should delete the contents of the `front_end_deps` folder, if any, and reinstall everything.  `install_front_end_deps` should not depend on any 3rd party python packages.

Licenses for the dependencies are saved in the `install_front_end_deps` folder.  They are checked
against the source when the source is downloaded, mainly as a form of documentation.

Attribution for front end dependencies should be added to the `About 24/7 Bishops` popup box on the landing webpage.

Hashes for the files should be checked each time they are downloaded, to ensure that
the source has not been replaced with a malicious version.

## Website security

Since this website hosts information provided by users, XSS attacks pose a
significant risk.  Recommendations for improving its security are welcomed.
The current strategy is as follows.

* Incorporate all recommendations of the
[HTTP Observatory project](https://developer.mozilla.org/en-US/observatory).  This is
[automatically](.github/workflows/http_obs.yml) checked every week.
* Host all 3rd party front end dependencies in the webapp.
Check their hashes when they are downloaded during the deployment workflow.
* Check all python dependencies for vulnerabilities using `pip-audit`.
* Check all python code for vulneravbilities using `bandit`.
* Avoid allowing arbitrary path traversal in flask routes.
* Take care to avoid SQL injections and HTML injections from user-provided data.
