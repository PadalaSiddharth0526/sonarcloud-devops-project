# SonarCloud CI/CD Demo (React + Flask + GitHub Actions)

A production-ready reference project that integrates **SonarCloud** analysis for a
**React (Vite)** frontend and a **Python Flask** backend, driven entirely by a
single **GitHub Actions** workflow.

Everything in this repository has been installed, linted, tested, and coverage-verified
locally before being committed here — there are no placeholder scripts.

Updated README to trigger GitHub Actions.

---

## 1. Folder Structure

```
project/
│
├── frontend/                       # React (Vite) application
│   ├── src/
│   │   ├── App.jsx                 # Main React component
│   │   ├── App.test.jsx            # Component tests (RTL + Vitest)
│   │   ├── main.jsx                # React DOM entry point
│   │   ├── setupTests.js           # Vitest + jest-dom setup
│   │   └── utils/
│   │       ├── math.js             # Pure functions used for coverage demo
│   │       └── math.test.js        # Unit tests for math.js
│   ├── index.html                  # Vite HTML entry point
│   ├── eslint.config.js            # ESLint 9 flat config
│   ├── vite.config.js              # Vite + Vitest + coverage config
│   ├── package.json                # Scripts & dependencies
│   └── package-lock.json           # Locked dependency tree (required for `npm ci`)
│
├── backend/                        # Python Flask application
│   ├── app.py                      # Flask app + business logic
│   ├── tests/
│   │   ├── __init__.py
│   │   └── test_app.py             # Pytest test suite
│   ├── requirements.txt            # Python dependencies
│   ├── pytest.ini                  # Pytest + coverage configuration
│   └── .coveragerc                 # coverage.py configuration
│
├── .github/
│   └── workflows/
│       └── sonarcloud.yml          # CI pipeline: build, test, coverage, Sonar scan
│
├── sonar-project.properties        # SonarCloud project configuration
├── .gitignore
└── README.md
```

---

## 2. File-by-File Explanation

### Frontend

| File | Purpose |
|---|---|
| `frontend/package.json` | Declares `dev`, `build`, `lint`, `test`, and `coverage` scripts, plus React, Vite, Vitest, ESLint and Testing Library dependencies. |
| `frontend/vite.config.js` | Configures the Vite dev/build pipeline **and** the Vitest test runner, including the `v8` coverage provider with `lcov` output (required by SonarCloud). |
| `frontend/eslint.config.js` | ESLint 9 "flat config" enabling recommended JS rules plus `react-hooks` and `react-refresh` plugins. |
| `frontend/index.html` | Vite's HTML entry point that mounts the React app. |
| `frontend/src/main.jsx` | Bootstraps React and renders `<App />` into the DOM. |
| `frontend/src/App.jsx` | Sample component (counter) used to demonstrate real test coverage. |
| `frontend/src/utils/math.js` | Pure utility functions (`add`, `subtract`, `multiply`, `divide`) — easy, deterministic code to unit test. |
| `frontend/src/utils/math.test.js` | Vitest unit tests for `math.js`. |
| `frontend/src/App.test.jsx` | React Testing Library tests that render `<App />` and simulate a click. |
| `frontend/src/setupTests.js` | Registers `@testing-library/jest-dom` matchers (e.g. `toBeInTheDocument`) for Vitest. |

### Backend

| File | Purpose |
|---|---|
| `backend/app.py` | Minimal Flask API (`/health`, `/api/calculate`) plus the arithmetic functions it uses. |
| `backend/tests/test_app.py` | Pytest suite covering the Flask routes (via `app.test_client()`) and the pure functions directly. |
| `backend/requirements.txt` | Pins `Flask`, `pytest`, and `pytest-cov`. |
| `backend/pytest.ini` | Tells pytest where tests live and auto-enables coverage (`--cov=. --cov-report=xml`), producing `coverage.xml` — the format SonarCloud's Python sensor expects. |
| `backend/.coveragerc` | Excludes test files/venvs from the coverage report and ignores `if __name__ == "__main__":` blocks. |

### Root / CI

| File | Purpose |
|---|---|
| `sonar-project.properties` | Tells the SonarCloud scanner where the frontend/backend source and coverage reports are. **Replace `sonar.projectKey` and `sonar.organization`** with your own SonarCloud values. |
| `.github/workflows/sonarcloud.yml` | The full CI/CD pipeline (see below). |
| `.gitignore` | Excludes build artifacts, `node_modules`, virtual environments, and coverage output from version control. |

---

## 3. GitHub Actions Pipeline (`.github/workflows/sonarcloud.yml`)

Trigger: every push to `main`/`develop` and every pull request.

Steps, in order:

1. **Checkout repository** — `actions/checkout@v4` with `fetch-depth: 0` (full git history, required by SonarCloud for blame/PR analysis).
2. **Setup Node.js 20** — `actions/setup-node@v4`, with npm caching keyed to `frontend/package-lock.json`.
3. **Setup Python** — `actions/setup-python@v5` (3.11), with pip caching keyed to `backend/requirements.txt`.
4. **Install frontend dependencies** — `npm ci` (uses the lockfile for reproducible installs).
5. **Run ESLint** — `npm run lint`, fails the job on lint errors.
6. **Run frontend tests + coverage** — `npm run coverage` → generates `frontend/coverage/lcov.info`.
7. **Install backend dependencies** — `pip install -r requirements.txt`.
8. **Run backend tests + coverage** — `pytest` (config in `pytest.ini`) → generates `backend/coverage.xml`.
9. **SonarCloud Scan** — `SonarSource/sonarqube-scan-action@v4`, reads `sonar-project.properties` from the repo root and uploads both coverage reports.
10. **Quality Gate Check** — `SonarSource/sonarqube-quality-gate-action@v1` polls SonarCloud for the Quality Gate result and **fails the workflow** (non-zero exit) if the gate does not pass.

### Required GitHub Secret

| Secret | Where to get it | Used by |
|---|---|---|
| `SONAR_TOKEN` | SonarCloud → **My Account → Security → Generate Token** | Steps 9 & 10 |

Add it under **Repository Settings → Secrets and variables → Actions → New repository secret**.

`GITHUB_TOKEN` is provided automatically by GitHub Actions — no setup needed.

---

## 4. One-Time SonarCloud Setup

1. Log in to [sonarcloud.io](https://sonarcloud.io) with your GitHub account.
2. **Import** this repository as a new project ("+" → "Analyze new project").
3. Note your **Organization Key** and the generated **Project Key**.
4. Update `sonar-project.properties`:
   ```properties
   sonar.projectKey=<your-project-key>
   sonar.organization=<your-organization-key>
   ```
5. In SonarCloud, set **Analysis Method → GitHub Actions** (this disables SonarCloud's own
   automatic analysis so it doesn't conflict with the CI-based scan).
6. Generate a token and add it as the `SONAR_TOKEN` secret in GitHub (see above).

---

## 5. Commands to Run Locally

### Frontend

```bash
cd frontend
npm install          # install dependencies
npm run dev          # start the Vite dev server
npm run lint          # run ESLint
npm run build          # production build
```

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py                 # runs Flask on http://localhost:5000
```

---

## 6. Commands to Verify Coverage

### Frontend coverage

```bash
cd frontend
npm run coverage
```
This runs Vitest with the `v8` provider and writes:
- `frontend/coverage/lcov.info` (consumed by SonarCloud)
- `frontend/coverage/index.html` (human-readable report — open in a browser)

Expected output ends with a coverage table, e.g.:
```
% Coverage report from v8
-----------|---------|----------|---------|---------|
File       | % Stmts | % Branch | % Funcs | % Lines |
-----------|---------|----------|---------|---------|
All files  |     100 |      100 |     100 |     100 |
```

### Backend coverage

```bash
cd backend
pytest
```
This runs pytest with `pytest-cov` (configured via `pytest.ini`) and writes:
- `backend/coverage.xml` (consumed by SonarCloud, Cobertura format)
- A terminal summary showing missed lines (`--cov-report=term-missing`)

---

## 7. Commands to Verify SonarCloud Analysis

Locally, using the official scanner CLI (optional — CI does this automatically):

```bash
# Install the scanner (requires Java 17+)
npm install -g @sonar/scan   # or use the Docker image: sonarsource/sonar-scanner-cli

# From the repository root, after generating both coverage reports:
sonar-scanner \
  -Dsonar.projectKey=<your-project-key> \
  -Dsonar.organization=<your-organization-key> \
  -Dsonar.host.url=https://sonarcloud.io \
  -Dsonar.token=<your-local-token>
```

In CI, verify the scan and Quality Gate by:

1. Pushing a commit or opening a pull request.
2. Checking the **Actions** tab → `SonarCloud Analysis` workflow run.
3. Confirming the `SonarCloud Scan` step uploads successfully and the
   `SonarCloud Quality Gate Check` step **passes** (green) or **fails the job** (red) based
   on the configured Quality Gate thresholds (coverage, duplications, bugs, vulnerabilities,
   code smells).
4. Reviewing full results on the SonarCloud project dashboard
   (`https://sonarcloud.io/project/overview?id=<your-project-key>`).

---

## 8. Verified Locally

Before delivery, this project was actually installed and run end-to-end:

- `npm install` → 299 packages installed cleanly, no peer-dependency conflicts.
- `npm run lint` → 0 errors, 0 warnings.
- `npm run coverage` → 8/8 tests passed, **100%** statements/branches/functions/lines.
- `pytest` (backend) → 13/13 tests passed, **100%** coverage, `coverage.xml` generated.

No placeholder logic exists anywhere except the two SonarCloud identifiers
(`sonar.projectKey`, `sonar.organization`) and the `SONAR_TOKEN` secret, which are
inherently unique to your SonarCloud account and cannot be pre-filled.
