from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import PyPDF2
import io
import re
from typing import Dict, List


# =========================================================
# APP CONFIGURATION
# =========================================================

app = FastAPI(
    title="AI Resume Analyzer & Job Readiness Platform",
    description="AI-powered resume and job description analysis API",
    version="2.0.0"
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/")
def home():
    return {
        "status": "online",
        "message": "AI Resume Analyzer API is running"
    }


# =========================================================
# PDF TEXT EXTRACTION
# =========================================================

def extract_text_from_pdf(file_bytes: bytes) -> str:
    try:
        reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        pages = []

        for page in reader.pages:
            text = page.extract_text()
            if text:
                pages.append(text)

        return "\n".join(pages).strip()

    except Exception as e:
        raise ValueError(f"Unable to read the PDF file: {str(e)}")


# =========================================================
# TEXT NORMALIZATION
# =========================================================

def clean_text(text: str) -> str:
    text = str(text).lower()

    # Normalize common dash characters.
    text = text.replace("–", "-").replace("—", "-")

    # Make slash-separated forms easier to detect.
    text = text.replace("/", " / ")

    # Normalize whitespace.
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# =========================================================
# SKILL DATABASE
# =========================================================
#
# Key = canonical skill name returned by the API.
# Value = all common ways that skill can appear in a resume/JD.
#
# Ambiguous aliases such as standalone "ai", "ml", "c", "go",
# "bi", "js" and "ts" are intentionally not used because they
# can create false positives in normal English sentences.
# =========================================================

SKILL_ALIASES: Dict[str, List[str]] = {

    # ---------------- PROGRAMMING LANGUAGES ----------------

    "python": ["python", "python programming", "python3"],
    "java": ["java", "java programming"],
    "c": ["c programming", "c language"],
    "c++": ["c++", "cpp", "c plus plus"],
    "c#": ["c#", "c sharp", "c-sharp"],
    "javascript": ["javascript", "java script", "java-script"],
    "typescript": ["typescript", "type script", "type-script"],
    "go": ["golang", "go programming", "go language"],
    "rust": ["rust programming", "rust language"],
    "kotlin": ["kotlin", "kotlin programming"],
    "swift": ["swift programming", "swift language"],
    "php": ["php", "php programming"],
    "ruby": ["ruby programming", "ruby language"],
    "ruby on rails": ["ruby on rails", "rails", "ror"],
    "scala": ["scala programming", "scala language"],
    "perl": ["perl programming", "perl language"],
    "dart": ["dart programming", "dart language"],

    # ---------------- WEB ----------------

    "html": ["html", "html5"],
    "css": ["css", "css3"],
    "bootstrap": ["bootstrap"],
    "tailwind css": ["tailwind", "tailwind css"],
    "sass": ["sass", "scss"],
    "less": ["less css"],
    "jquery": ["jquery"],
    "ajax": ["ajax", "asynchronous javascript and xml"],
    "web development": ["web development", "web application development"],
    "responsive design": ["responsive design", "responsive web design"],

    # ---------------- FRONTEND ----------------

    "react": ["react", "react.js", "reactjs", "react js"],
    "angular": ["angular", "angularjs", "angular.js"],
    "vue.js": ["vue", "vue.js", "vuejs", "vue js"],
    "next.js": ["next.js", "nextjs", "next js"],
    "nuxt.js": ["nuxt", "nuxt.js", "nuxtjs", "nuxt js"],
    "redux": ["redux", "redux toolkit", "redux-toolkit"],
    "react native": ["react native", "react-native"],
    "flutter": ["flutter"],
    "material ui": ["material ui", "mui"],

    # ---------------- BACKEND ----------------

    "node.js": ["node.js", "nodejs", "node js", "node runtime"],
    "express.js": ["express.js", "expressjs", "express js"],
    "fastapi": ["fastapi", "fast api"],
    "flask": ["flask"],
    "django": ["django"],
    "spring": ["spring framework"],
    "spring boot": ["spring boot", "springboot"],
    "spring mvc": ["spring mvc"],
    "asp.net": ["asp.net", "asp net"],
    ".net": [".net", "dotnet", ".net framework", ".net core"],
    "asp.net core": ["asp.net core", "asp net core"],
    "entity framework": ["entity framework", "entity framework core", "ef core"],
    "graphql": ["graphql"],
    "grpc": ["grpc"],

    # ---------------- JAVA ECOSYSTEM ----------------

    "hibernate": ["hibernate"],
    "jpa": ["jpa", "java persistence api"],
    "maven": ["maven"],
    "gradle": ["gradle"],
    "jsp": ["jsp", "java server pages"],
    "jsf": ["jsf", "java server faces"],
    "wicket": ["wicket", "apache wicket"],
    "gwt": ["gwt", "google web toolkit"],

    # ---------------- DATABASE ----------------

    "sql": ["sql", "structured query language"],
    "mysql": ["mysql", "my sql"],
    "postgresql": ["postgresql", "postgres", "postgre sql"],
    "mongodb": ["mongodb", "mongo db", "mongo database"],
    "oracle": ["oracle database", "oracle db"],
    "sql server": ["sql server", "microsoft sql server", "mssql"],
    "sqlite": ["sqlite"],
    "redis": ["redis"],
    "cassandra": ["cassandra"],
    "dynamodb": ["dynamodb", "dynamo db"],
    "firebase": ["firebase"],
    "database design": ["database design", "database schema design", "db design"],
    "orm": ["orm", "object relational mapping", "object-relational mapping"],

    # ---------------- CORE CS ----------------

    "data structures": ["data structures", "data structure"],
    "algorithms": ["algorithms", "algorithm"],
    "dsa": ["dsa", "data structures and algorithms"],
    "object oriented programming": [
        "object oriented programming",
        "object-oriented programming",
        "object oriented",
        "object-oriented",
        "oops",
        "oop"
    ],
    "operating systems": ["operating systems", "operating system"],
    "computer networks": ["computer networks", "computer network"],
    "dbms": ["dbms", "database management system"],
    "system design": ["system design"],
    "low level design": ["low level design", "low-level design", "lld"],
    "high level design": ["high level design", "high-level design", "hld"],

    # ---------------- SOFTWARE ENGINEERING ----------------

    "sdlc": [
        "sdlc",
        "software development life cycle",
        "software development lifecycle"
    ],
    "software engineering": ["software engineering"],
    "software development": ["software development"],
    "agile": ["agile methodology", "agile development", "agile"],
    "scrum": ["scrum"],
    "kanban": ["kanban"],
    "waterfall": ["waterfall model", "waterfall methodology"],
    "requirements analysis": [
        "requirements analysis",
        "requirement analysis",
        "requirements gathering"
    ],
    "software architecture": ["software architecture", "application architecture"],
    "design patterns": ["design patterns", "design pattern"],
    "microservices": [
        "microservices",
        "microservices architecture",
        "microservice architecture"
    ],
    "monolithic architecture": [
        "monolithic architecture",
        "monolithic application",
        "monolith"
    ],
    "documentation": ["technical documentation", "software documentation"],
    "debugging": ["debugging", "debug"],
    "troubleshooting": ["troubleshooting", "troubleshoot"],
    "problem solving": ["problem solving", "problem-solving"],

    # ---------------- API / WEB SERVICES ----------------

    "rest api": [
        "rest api",
        "rest apis",
        "restful api",
        "restful apis",
        "rest web services"
    ],
    "soap": ["soap", "soap api", "soap web services"],
    "web services": ["web services", "web service"],
    "api development": ["api development"],
    "api integration": ["api integration", "api integrations"],
    "api testing": ["api testing", "api tests"],
    "postman": ["postman"],
    "swagger": ["swagger", "swagger ui"],
    "openapi": ["openapi", "open api"],
    "http": ["http", "http protocol"],
    "json": ["json", "json format"],
    "xml": ["xml", "xml format"],

    # ---------------- TESTING / QA ----------------

    "software testing": ["software testing"],
    "manual testing": ["manual testing"],
    "automation testing": [
        "automation testing",
        "test automation",
        "automated testing"
    ],
    "unit testing": ["unit testing", "unit tests"],
    "integration testing": ["integration testing"],
    "system testing": ["system testing"],
    "regression testing": ["regression testing"],
    "functional testing": ["functional testing"],
    "performance testing": ["performance testing"],
    "selenium": ["selenium"],
    "cypress": ["cypress"],
    "playwright": ["playwright"],
    "pytest": ["pytest", "py test"],
    "junit": ["junit", "j unit"],
    "test driven development": [
        "test driven development",
        "test-driven development",
        "tdd"
    ],
    "behavior driven development": [
        "behavior driven development",
        "behavior-driven development",
        "bdd"
    ],
    "quality assurance": ["quality assurance"],
    "test case design": [
        "test case design",
        "test case creation",
        "test cases"
    ],

    # ---------------- VERSION CONTROL ----------------

    "git": ["git", "git version control"],
    "github": ["github", "git hub"],
    "gitlab": ["gitlab"],
    "bitbucket": ["bitbucket"],
    "version control": ["version control", "version-control"],

    # ---------------- DEVOPS ----------------

    "docker": ["docker"],
    "kubernetes": ["kubernetes", "k8s"],
    "jenkins": ["jenkins"],
    "ci cd": [
        "ci/cd",
        "ci cd",
        "continuous integration",
        "continuous delivery",
        "continuous deployment"
    ],
    "terraform": ["terraform"],
    "ansible": ["ansible"],
    "nginx": ["nginx"],
    "linux": ["linux", "linux operating system"],
    "bash": ["bash", "bash scripting", "shell scripting"],
    "devops": ["devops", "dev ops"],

    # ---------------- CLOUD ----------------

    "aws": ["aws", "amazon web services"],
    "azure": ["azure", "microsoft azure"],
    "gcp": ["gcp", "google cloud", "google cloud platform"],
    "ec2": ["ec2", "amazon ec2"],
    "s3": ["s3", "amazon s3"],
    "lambda": ["aws lambda", "lambda function", "lambda functions"],
    "cloud computing": ["cloud computing"],
    "cloud deployment": ["cloud deployment", "cloud deployments"],

    # ---------------- DATA ANALYTICS ----------------

    "pandas": ["pandas"],
    "numpy": ["numpy"],
    "matplotlib": ["matplotlib"],
    "seaborn": ["seaborn"],
    "plotly": ["plotly"],
    "power bi": ["power bi", "powerbi"],
    "tableau": ["tableau"],
    "excel": ["excel", "microsoft excel"],
    "data visualization": ["data visualization", "data visualisation"],
    "data analysis": ["data analysis", "data analytics"],
    "business intelligence": ["business intelligence"],

    # ---------------- BIG DATA ----------------

    "spark": ["apache spark", "spark framework", "spark sql"],
    "pyspark": ["pyspark", "py spark"],
    "hadoop": ["hadoop", "apache hadoop"],
    "hive": ["hive", "apache hive"],
    "kafka": ["kafka", "apache kafka"],
    "airflow": ["airflow", "apache airflow"],
    "data engineering": ["data engineering"],

    # ---------------- MACHINE LEARNING ----------------

    "machine learning": ["machine learning", "machine-learning"],
    "deep learning": ["deep learning", "deep-learning"],
    "artificial intelligence": [
        "artificial intelligence",
        "artificial-intelligence"
    ],
    "natural language processing": [
        "natural language processing",
        "nlp"
    ],
    "computer vision": ["computer vision"],
    "reinforcement learning": ["reinforcement learning"],
    "scikit-learn": ["scikit-learn", "sklearn", "scikit learn"],
    "tensorflow": ["tensorflow"],
    "pytorch": ["pytorch"],
    "keras": ["keras"],
    "xgboost": ["xgboost"],
    "hugging face": ["hugging face", "huggingface"],
    "feature engineering": ["feature engineering"],
    "model evaluation": ["model evaluation", "model validation"],

    # ---------------- GENERATIVE AI ----------------

    "generative ai": [
        "generative ai",
        "generative artificial intelligence"
    ],
    "llm": [
        "llm",
        "large language model",
        "large language models"
    ],
    "rag": [
        "rag",
        "retrieval augmented generation",
        "retrieval-augmented generation"
    ],
    "prompt engineering": ["prompt engineering"],
    "langchain": ["langchain"],
    "llamaindex": ["llamaindex", "llama index"],

    # ---------------- MOBILE ----------------

    "android": ["android development", "android application development"],
    "ios": ["ios development", "ios application development"],

    # ---------------- SECURITY ----------------

    "cybersecurity": ["cybersecurity", "cyber security"],
    "oauth": ["oauth", "oauth2"],
    "jwt": ["jwt", "json web token", "json web tokens"],
    "authentication": ["authentication", "user authentication"],
    "authorization": ["authorization", "user authorization"],
    "https": ["https"],
    "ssl tls": ["ssl", "tls", "ssl/tls"],
    "owasp": ["owasp"],

    # ---------------- TOOLS ----------------

    "jira": ["jira"],
    "confluence": ["confluence"],
    "figma": ["figma"],
    "visual studio code": ["visual studio code", "vs code"],
    "intellij idea": ["intellij idea", "intellij"],
    "jupyter": ["jupyter", "jupyter notebook"],
    "anaconda": ["anaconda"],

    # ---------------- PROFESSIONAL SKILLS ----------------

    "communication": [
        "communication skills",
        "strong communication",
        "verbal communication",
        "written communication"
    ],
    "teamwork": [
        "teamwork",
        "team work",
        "collaboration skills"
    ],
    "leadership": [
        "leadership skills",
        "leadership experience"
    ],
    "analytical skills": [
        "analytical skills",
        "analytical thinking"
    ],
    "time management": ["time management"]
}


# =========================================================
# LEARNING RECOMMENDATIONS DATABASE
# =========================================================
#
# The key names exactly match SKILL_ALIASES keys.
# Therefore any detected missing skill can receive a useful
# learning recommendation without another hard-coded priority
# list.
# =========================================================

LEARNING_MAP: Dict[str, str] = {

    # Programming
    "python": "Strengthen Python fundamentals, OOP, exception handling, modules and problem-solving through practical projects.",
    "java": "Revise Java OOP, collections, exception handling, multithreading and build small backend applications.",
    "c": "Strengthen C fundamentals, pointers, arrays, structures, memory management and problem-solving.",
    "c++": "Practice C++ STL, OOP, pointers, memory management and DSA-based coding problems.",
    "c#": "Learn C# OOP, collections, exception handling, LINQ and application development with .NET.",
    "javascript": "Improve JavaScript ES6+, DOM manipulation, promises, async/await, events and API integration.",
    "typescript": "Learn TypeScript types, interfaces, generics, enums and integration with modern frontend frameworks.",
    "go": "Learn Go syntax, structs, interfaces, goroutines, channels and REST API development.",
    "rust": "Learn Rust ownership, borrowing, lifetimes, structs, enums and safe systems programming.",
    "kotlin": "Learn Kotlin syntax, OOP, collections, null safety and Android application development.",
    "swift": "Learn Swift fundamentals, optionals, protocols and iOS application development.",
    "php": "Strengthen PHP syntax, OOP, sessions, database connectivity and backend web development.",
    "ruby": "Learn Ruby syntax, OOP, collections, blocks and web development fundamentals.",
    "ruby on rails": "Learn Rails MVC, routing, ActiveRecord, controllers, views and RESTful application development.",
    "scala": "Learn Scala collections, functional programming, pattern matching and JVM application development.",
    "perl": "Learn Perl syntax, regular expressions, file handling and scripting fundamentals.",
    "dart": "Learn Dart syntax, OOP, asynchronous programming and Flutter application development.",

    # Web / Frontend
    "html": "Practice semantic HTML, forms, accessibility, tables, media and clean page structure.",
    "css": "Practice Flexbox, Grid, responsive layouts, positioning, animations and reusable CSS patterns.",
    "bootstrap": "Learn Bootstrap grid, responsive utilities, components, forms and layout customization.",
    "tailwind css": "Learn utility-first styling, responsive classes, reusable components and Tailwind configuration.",
    "sass": "Learn Sass variables, nesting, mixins, functions and modular stylesheet architecture.",
    "less": "Learn Less variables, mixins, nesting and maintainable stylesheet organization.",
    "jquery": "Practice DOM manipulation, events, AJAX requests and legacy frontend integration with jQuery.",
    "ajax": "Learn asynchronous browser requests, JSON handling and dynamic UI updates.",
    "web development": "Build complete web applications covering frontend UI, backend APIs, databases and deployment.",
    "responsive design": "Practice mobile-first layouts using CSS Grid, Flexbox and media queries.",
    "react": "Build React projects using components, props, hooks, state management, routing and API integration.",
    "angular": "Learn Angular components, services, dependency injection, routing, forms and HTTP client integration.",
    "vue.js": "Learn Vue components, reactive state, computed properties, routing and API integration.",
    "next.js": "Learn Next.js routing, server/client components, API routes, rendering strategies and deployment.",
    "nuxt.js": "Learn Nuxt routing, server-side rendering, composables and full-stack Vue development.",
    "redux": "Learn Redux state management, actions, reducers, middleware and integration with React.",
    "react native": "Build mobile applications with React Native, navigation, components, state and REST API integration.",
    "flutter": "Learn Flutter widgets, layouts, state management, navigation and REST API integration.",
    "material ui": "Learn Material UI components, theming, responsive layouts and accessible React interfaces.",

    # Backend
    "node.js": "Learn Node.js modules, asynchronous programming, REST APIs and backend architecture.",
    "express.js": "Build Express REST APIs using routing, middleware, validation, error handling and database integration.",
    "fastapi": "Learn FastAPI routing, Pydantic validation, async endpoints, error handling and API documentation.",
    "flask": "Build Flask APIs with routing, request handling, database integration and deployment.",
    "django": "Learn Django models, views, URLs, templates, ORM, authentication and REST API development.",
    "spring": "Learn Spring dependency injection, configuration, MVC architecture and REST service development.",
    "spring boot": "Build Spring Boot REST APIs using controllers, services, repositories, validation and database integration.",
    "spring mvc": "Learn Spring MVC controllers, request mapping, validation, services and view/API architecture.",
    "asp.net": "Learn ASP.NET application structure, routing, controllers, middleware and database integration.",
    ".net": "Learn .NET fundamentals, dependency injection, APIs, application architecture and backend development.",
    "asp.net core": "Build ASP.NET Core REST APIs using controllers, middleware, dependency injection and Entity Framework.",
    "entity framework": "Learn Entity Framework Core, DbContext, migrations, LINQ queries and database relationships.",
    "graphql": "Learn GraphQL schemas, queries, mutations, resolvers and API integration.",
    "grpc": "Learn gRPC services, Protocol Buffers, service contracts and client-server communication.",

    # Java ecosystem
    "hibernate": "Learn Hibernate ORM, entity mapping, relationships, HQL, transactions and database persistence.",
    "jpa": "Learn JPA entities, repositories, relationships, JPQL, transactions and persistence concepts.",
    "maven": "Learn Maven project structure, dependencies, lifecycle phases, plugins and build automation.",
    "gradle": "Learn Gradle builds, dependency management, tasks, plugins and project configuration.",
    "jsp": "Learn JSP pages, JSTL, request handling and integration with Java web applications.",
    "jsf": "Learn JSF components, managed beans, navigation and server-side Java web UI development.",
    "wicket": "Learn Apache Wicket components, models, pages and server-side Java web application patterns.",
    "gwt": "Learn GWT widgets, RPC, client-side Java development and browser-based application architecture.",

    # Databases
    "sql": "Practice SQL joins, subqueries, CTEs, window functions, aggregation, indexing and query optimization.",
    "mysql": "Practice MySQL schema design, joins, indexes, constraints, transactions and query optimization.",
    "postgresql": "Learn PostgreSQL queries, indexes, constraints, transactions, views and advanced SQL features.",
    "mongodb": "Learn MongoDB documents, collections, CRUD operations, indexes, aggregation and schema design.",
    "oracle": "Practice Oracle SQL, joins, PL/SQL basics, indexes, constraints and database optimization.",
    "sql server": "Practice T-SQL, joins, stored procedures, indexes, transactions and SQL Server database design.",
    "sqlite": "Learn SQLite schema design, CRUD operations, indexes and embedded database usage.",
    "redis": "Learn Redis data structures, caching, expiration, pub/sub and application integration.",
    "cassandra": "Learn Cassandra data modeling, partition keys, replication and distributed database concepts.",
    "dynamodb": "Learn DynamoDB tables, partition keys, indexes, queries and serverless application patterns.",
    "firebase": "Learn Firebase Authentication, Firestore, Storage and application integration.",
    "database design": "Practice ER modeling, normalization, relationships, keys, constraints and scalable schema design.",
    "orm": "Learn ORM concepts, entity mapping, relationships, transactions and ORM query optimization.",

    # Core CS
    "data structures": "Practice arrays, linked lists, stacks, queues, trees, heaps, hash tables and graphs.",
    "algorithms": "Practice searching, sorting, recursion, greedy algorithms, dynamic programming and graph algorithms.",
    "dsa": "Strengthen DSA through arrays, strings, linked lists, stacks, queues, trees, graphs and dynamic programming.",
    "object oriented programming": "Revise classes, objects, inheritance, polymorphism, abstraction, encapsulation and interfaces.",
    "operating systems": "Study processes, threads, scheduling, synchronization, deadlocks, memory management and file systems.",
    "computer networks": "Study OSI/TCP-IP, HTTP, DNS, TCP/UDP, routing, IP addressing and network security basics.",
    "dbms": "Study normalization, transactions, ACID, indexing, keys, joins, concurrency and database design.",
    "system design": "Practice scalability, load balancing, caching, databases, queues, APIs and high-level architecture.",
    "low level design": "Practice OOP-based class design, interfaces, SOLID principles and common design patterns.",
    "high level design": "Practice service decomposition, APIs, databases, caching, queues, scalability and reliability.",

    # Software engineering
    "sdlc": "Learn SDLC phases, requirements, design, development, testing, deployment and maintenance.",
    "software engineering": "Strengthen requirements, design, testing, version control, documentation and maintainable development practices.",
    "software development": "Build complete projects using clean code, version control, testing, APIs, databases and deployment.",
    "agile": "Learn Agile principles, sprint planning, backlog management, stand-ups, reviews and retrospectives.",
    "scrum": "Learn Scrum roles, events, artifacts, sprint planning and iterative product delivery.",
    "kanban": "Learn Kanban boards, work-in-progress limits, flow optimization and continuous delivery.",
    "waterfall": "Understand sequential software development phases, requirements, design, implementation and testing.",
    "requirements analysis": "Practice gathering, documenting, prioritizing and validating functional and non-functional requirements.",
    "software architecture": "Study layered architecture, modularity, scalability, reliability and architectural trade-offs.",
    "design patterns": "Learn Factory, Strategy, Observer, Adapter and other reusable software design patterns.",
    "microservices": "Learn service decomposition, API gateways, service communication, discovery, resilience and deployment.",
    "monolithic architecture": "Understand monolithic application structure, modularization, deployment and migration trade-offs.",
    "documentation": "Practice writing clear technical documentation, API documentation, setup guides and architecture notes.",
    "debugging": "Improve debugging with logs, breakpoints, stack traces, reproduction steps and root-cause analysis.",
    "troubleshooting": "Practice systematic issue diagnosis using logs, reproduction, isolation and root-cause analysis.",
    "problem solving": "Strengthen problem-solving using structured analysis, coding practice and real-world debugging exercises.",

    # APIs
    "rest api": "Learn REST principles, HTTP methods, status codes, request/response design, validation and API security.",
    "soap": "Learn SOAP envelopes, WSDL, XML messaging, services and enterprise API integration.",
    "web services": "Learn web service architecture, REST/SOAP communication, HTTP, JSON/XML and API integration.",
    "api development": "Build APIs with validation, error handling, authentication, documentation and database integration.",
    "api integration": "Practice consuming third-party APIs, authentication, error handling, JSON processing and retries.",
    "api testing": "Practice API test cases, request validation, status codes, authentication, negative testing and regression.",
    "postman": "Use Postman collections, environments, variables, assertions, scripts and API test workflows.",
    "swagger": "Learn Swagger/OpenAPI documentation, request schemas, response models and interactive API testing.",
    "openapi": "Learn OpenAPI schemas, endpoints, parameters, request bodies, responses and generated documentation.",
    "http": "Understand HTTP methods, headers, status codes, cookies, caching and request-response architecture.",
    "json": "Practice JSON structures, nested objects, arrays, serialization and API request/response handling.",
    "xml": "Learn XML structure, namespaces, schemas and XML-based API integration.",

    # Testing
    "software testing": "Learn testing lifecycle, test planning, test cases, defect lifecycle, regression and test reporting.",
    "manual testing": "Practice requirements analysis, test case design, exploratory testing, defect reporting and regression testing.",
    "automation testing": "Learn automation frameworks, locators, assertions, test suites, reporting and CI integration.",
    "unit testing": "Write unit tests using assertions, mocks, fixtures, edge cases and isolated test design.",
    "integration testing": "Practice testing interactions between modules, services, APIs and databases.",
    "system testing": "Learn end-to-end system validation against functional and non-functional requirements.",
    "regression testing": "Practice regression planning, test selection, automation and validation after software changes.",
    "functional testing": "Practice validating application behavior against functional requirements using structured test cases.",
    "performance testing": "Learn load, stress, endurance and scalability testing with performance metrics and bottleneck analysis.",
    "selenium": "Learn Selenium locators, WebDriver, waits, page objects, assertions and automated browser testing.",
    "cypress": "Learn Cypress selectors, commands, fixtures, assertions and end-to-end web testing.",
    "playwright": "Learn Playwright browser automation, locators, fixtures, assertions and cross-browser testing.",
    "pytest": "Learn pytest fixtures, parametrization, assertions, mocking and test organization.",
    "junit": "Learn JUnit test cases, assertions, lifecycle methods, parameterized tests and test suites.",
    "test driven development": "Practice TDD using the red-green-refactor cycle and small automated unit tests.",
    "behavior driven development": "Learn BDD scenarios, Given-When-Then structure and collaboration between technical and business teams.",
    "quality assurance": "Strengthen QA fundamentals including test planning, defect management, risk-based testing and quality processes.",
    "test case design": "Practice positive, negative, boundary-value, equivalence-partitioning and edge-case test design.",

    # Git / DevOps
    "git": "Practice Git commits, branches, merges, rebases, conflict resolution and clean repository workflows.",
    "github": "Practice GitHub repositories, pull requests, branches, issues, README documentation and collaboration.",
    "gitlab": "Learn GitLab repositories, merge requests, issues, CI/CD pipelines and team workflows.",
    "bitbucket": "Learn Bitbucket repositories, branches, pull requests and team collaboration workflows.",
    "version control": "Learn branching strategies, commits, merges, pull requests, code reviews and collaborative development.",
    "docker": "Learn Docker images, containers, Dockerfiles, volumes, networks and application deployment.",
    "kubernetes": "Learn Kubernetes pods, deployments, services, config maps, scaling and container orchestration.",
    "jenkins": "Learn Jenkins pipelines, jobs, triggers, build automation, testing and CI/CD workflows.",
    "ci cd": "Learn continuous integration/deployment pipelines, automated testing, builds, releases and rollback strategies.",
    "terraform": "Learn Infrastructure as Code with Terraform providers, resources, variables, state and modules.",
    "ansible": "Learn Ansible inventories, playbooks, roles, variables and server configuration automation.",
    "nginx": "Learn Nginx reverse proxying, static file serving, load balancing and web server configuration.",
    "linux": "Practice Linux commands, permissions, processes, networking, package management and shell operations.",
    "bash": "Learn Bash variables, loops, conditions, functions, pipes, redirects and automation scripts.",
    "devops": "Build CI/CD workflows combining Git, Docker, testing, cloud deployment and monitoring.",

    # Cloud
    "aws": "Learn AWS fundamentals including IAM, EC2, S3, Lambda, networking, deployment and monitoring.",
    "azure": "Learn Azure fundamentals including virtual machines, storage, identity, networking and deployment.",
    "gcp": "Learn Google Cloud fundamentals including compute, storage, IAM, networking and application deployment.",
    "ec2": "Learn EC2 instances, security groups, SSH access, deployment and basic server management.",
    "s3": "Learn S3 buckets, objects, permissions, lifecycle policies and application file storage.",
    "lambda": "Learn serverless functions, triggers, IAM permissions, event-driven architecture and deployment.",
    "cloud computing": "Learn cloud service models, virtualization, networking, storage, security and scalable deployment.",
    "cloud deployment": "Practice deploying applications to cloud platforms with environment variables, networking and monitoring.",

    # Data
    "pandas": "Practice data cleaning, transformation, grouping, merging, filtering and analysis with Pandas.",
    "numpy": "Strengthen NumPy arrays, broadcasting, indexing, vectorization and numerical operations.",
    "matplotlib": "Practice Python visualization using plots, labels, legends and data storytelling.",
    "seaborn": "Learn statistical visualization with Seaborn including distributions, categorical plots and correlations.",
    "plotly": "Build interactive visualizations and dashboards using Plotly charts and filters.",
    "power bi": "Learn Power BI data modeling, Power Query, DAX, relationships, dashboards and report design.",
    "tableau": "Learn Tableau data connections, calculated fields, filters, dashboards and interactive visual analytics.",
    "excel": "Practice Excel formulas, lookup functions, pivot tables, charts, conditional formatting and data cleaning.",
    "data visualization": "Improve data storytelling using appropriate charts, dashboard layout, filtering and clear KPI presentation.",
    "data analysis": "Practice data cleaning, exploratory analysis, statistics, visualization and insight generation.",
    "business intelligence": "Learn BI reporting, KPI design, dashboards, data modeling and business-focused analytics.",

    # Big data
    "spark": "Learn Apache Spark DataFrames, transformations, actions, Spark SQL and distributed processing.",
    "pyspark": "Learn PySpark DataFrames, transformations, actions, Spark SQL, joins and distributed processing.",
    "hadoop": "Learn Hadoop HDFS, MapReduce, YARN and distributed data processing concepts.",
    "hive": "Learn Hive tables, partitions, queries, joins and SQL-based big-data processing.",
    "kafka": "Learn Kafka topics, producers, consumers, partitions, offsets and event-driven architecture.",
    "airflow": "Learn Airflow DAGs, operators, scheduling, dependencies and data pipeline orchestration.",
    "data engineering": "Learn ETL/ELT pipelines, data modeling, orchestration, distributed processing and data quality.",

    # AI / ML
    "machine learning": "Strengthen supervised/unsupervised learning, feature engineering, model evaluation and scikit-learn.",
    "deep learning": "Learn neural networks, backpropagation, CNNs, RNNs, optimization and model evaluation.",
    "artificial intelligence": "Study core AI concepts and build practical AI-powered applications using ML and LLMs.",
    "natural language processing": "Learn text preprocessing, tokenization, embeddings, classification, transformers and NLP evaluation.",
    "computer vision": "Learn image preprocessing, CNNs, object detection, classification and computer vision pipelines.",
    "reinforcement learning": "Learn agents, states, actions, rewards, policies, value functions and RL algorithms.",
    "scikit-learn": "Practice preprocessing, pipelines, classification, regression, clustering, cross-validation and metrics.",
    "tensorflow": "Learn TensorFlow tensors, neural networks, training loops, callbacks and model deployment basics.",
    "pytorch": "Learn PyTorch tensors, datasets, neural networks, training loops and model evaluation.",
    "keras": "Build neural networks with Keras using layers, callbacks, training and evaluation workflows.",
    "xgboost": "Learn gradient boosting, feature importance, hyperparameter tuning and model evaluation with XGBoost.",
    "hugging face": "Learn transformer models, tokenizers, pipelines, fine-tuning concepts and Hugging Face tooling.",
    "feature engineering": "Practice encoding, scaling, transformations, feature selection and domain-specific feature creation.",
    "model evaluation": "Learn train/validation/test splits, cross-validation, precision, recall, F1, ROC-AUC and error analysis.",

    # GenAI
    "generative ai": "Learn LLM fundamentals, prompt design, embeddings, RAG, evaluation and AI application architecture.",
    "llm": "Learn transformer/LLM concepts, prompting, embeddings, context windows, evaluation and application integration.",
    "rag": "Build RAG pipelines using document chunking, embeddings, vector search, retrieval and grounded generation.",
    "prompt engineering": "Practice structured prompts, few-shot examples, role/task/context design and reliable output formatting.",
    "langchain": "Learn LangChain prompts, models, chains, tools, agents, document loaders and retrieval pipelines.",
    "llamaindex": "Learn LlamaIndex document ingestion, indexing, retrieval, query engines and RAG applications.",

    # Mobile
    "android": "Learn Android components, layouts, activities, lifecycle, networking and local data storage.",
    "ios": "Learn iOS application architecture, Swift integration, UI development, networking and persistence.",

    # Security
    "cybersecurity": "Learn security fundamentals, common vulnerabilities, secure coding, network security and threat awareness.",
    "oauth": "Learn OAuth 2.0 flows, access tokens, refresh tokens, scopes and secure API authorization.",
    "jwt": "Learn JWT structure, signing, validation, expiration and secure token-based authentication.",
    "authentication": "Learn secure login flows, sessions, tokens, password handling and authentication architecture.",
    "authorization": "Learn roles, permissions, access control and secure authorization patterns.",
    "https": "Understand HTTPS, TLS certificates, encryption, secure requests and browser security.",
    "ssl tls": "Learn TLS handshakes, certificates, encryption and secure client-server communication.",
    "owasp": "Study OWASP Top 10, secure coding practices, web vulnerabilities and mitigation techniques.",

    # Tools
    "jira": "Learn Jira issue tracking, workflows, sprint boards, backlog management and reporting.",
    "confluence": "Learn Confluence documentation, knowledge bases, project pages and team collaboration.",
    "figma": "Learn Figma components, auto layout, prototyping and developer handoff.",
    "visual studio code": "Learn VS Code extensions, debugging, terminals, Git integration and project workflows.",
    "intellij idea": "Learn IntelliJ debugging, refactoring, Maven/Gradle integration and Java development workflows.",
    "jupyter": "Use Jupyter notebooks for experimentation, data analysis, visualization and reproducible workflows.",
    "anaconda": "Learn Conda environments, package management and Python data-science workflows.",

    # Professional
    "communication": "Improve technical communication by practicing concise explanations, documentation and presentations.",
    "teamwork": "Practice collaborative development through Git workflows, code reviews and clear task ownership.",
    "leadership": "Develop leadership through ownership, mentoring, project coordination and measurable delivery.",
    "analytical skills": "Strengthen analytical thinking through structured problem-solving, data interpretation and root-cause analysis.",
    "time management": "Improve planning with prioritization, realistic estimates, milestones and focused execution."
}


# =========================================================
# SKILL DETECTION
# =========================================================

def contains_skill(text: str, variations: List[str]) -> bool:
    normalized_text = clean_text(text)

    for variation in variations:
        normalized_variation = clean_text(variation)

        # Special case: aliases containing "/" such as ssl/tls or ci/cd.
        if "/" in normalized_variation:
            parts = [
                part.strip()
                for part in normalized_variation.split("/")
                if part.strip()
            ]

            if parts and all(
                re.search(
                    r"(?<![a-z0-9])" + re.escape(part) + r"(?![a-z0-9])",
                    normalized_text
                )
                for part in parts
            ):
                return True

            continue

        pattern = (
            r"(?<![a-z0-9])"
            + re.escape(normalized_variation)
            + r"(?![a-z0-9])"
        )

        if re.search(pattern, normalized_text):
            return True

    return False


def extract_skills(text: str) -> List[str]:
    detected = []

    for skill, aliases in SKILL_ALIASES.items():
        if contains_skill(text, aliases):
            detected.append(skill)

    return detected


# =========================================================
# SKILL COMPARISON
# =========================================================

def compare_skills(
    resume_text: str,
    job_description: str
):
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)

    matched_skills = [
        skill for skill in job_skills
        if skill in resume_skills
    ]

    missing_skills = [
        skill for skill in job_skills
        if skill not in resume_skills
    ]

    return (
        resume_skills,
        job_skills,
        matched_skills,
        missing_skills
    )


# =========================================================
# MATCH SCORE
# =========================================================

def calculate_match_score(
    matched_skills: List[str],
    job_skills: List[str]
) -> float:

    if not job_skills:
        return 0.0

    score = (
        len(matched_skills) / len(job_skills)
    ) * 100

    return round(score, 1)


# =========================================================
# JOB READINESS SCORE
# =========================================================

def calculate_readiness_score(
    match_score: float,
    matched_skills: List[str],
    missing_skills: List[str]
) -> float:

    total = len(matched_skills) + len(missing_skills)

    if total == 0:
        return round(match_score, 1)

    skill_score = (
        len(matched_skills) / total
    ) * 100

    readiness = (
        match_score * 0.60
        + skill_score * 0.40
    )

    return round(readiness, 1)


# =========================================================
# SKILLS TO IMPROVE
# =========================================================
#
# IMPORTANT:
# There is NO separate improvement_priority list.
# The first five missing skills are the five improvement areas.
# This automatically works for every skill in the database.
# =========================================================

def get_skills_to_improve(
    missing_skills: List[str]
) -> List[str]:

    return missing_skills[:5]


# =========================================================
# LEARNING RECOMMENDATIONS
# =========================================================

def generate_learning_recommendations(
    missing_skills: List[str],
    skills_to_improve: List[str]
) -> List[str]:

    recommendations = []

    # First prioritize the five displayed improvement skills.
    for skill in skills_to_improve:
        recommendation = LEARNING_MAP.get(skill)

        if recommendation and recommendation not in recommendations:
            recommendations.append(recommendation)

    # Then cover remaining missing skills if there is room.
    for skill in missing_skills:
        recommendation = LEARNING_MAP.get(skill)

        if recommendation and recommendation not in recommendations:
            recommendations.append(recommendation)

        if len(recommendations) >= 6:
            break

    # If a future skill is added to SKILL_ALIASES but not yet to
    # LEARNING_MAP, still return a useful recommendation.
    if not recommendations and missing_skills:
        for skill in missing_skills[:3]:
            recommendations.append(
                f"Build practical projects and study the core concepts of {skill} "
                f"to improve your alignment with this role."
            )

    if not recommendations:
        recommendations.append(
            "Your detected skills already cover the main skills found in this job description. "
            "Focus on project depth, interview preparation and measurable achievements."
        )

    return recommendations[:6]


# =========================================================
# RESUME IMPROVEMENT SUGGESTIONS
# =========================================================

def generate_resume_suggestions(
    missing_skills: List[str],
    matched_skills: List[str]
) -> List[str]:

    suggestions = []

    if missing_skills:
        top_gaps = ", ".join(missing_skills[:5])

        suggestions.append(
            f"Prioritize relevant missing skills such as {top_gaps}, "
            f"but list them on your resume only if you genuinely have experience."
        )

    if "python" in matched_skills:
        suggestions.append(
            "Highlight measurable Python project outcomes instead of only listing Python as a skill."
        )

    if "sql" in matched_skills:
        suggestions.append(
            "Mention specific SQL concepts such as joins, CTEs, subqueries or window functions when applicable."
        )

    if "rest api" in matched_skills:
        suggestions.append(
            "Show the REST API work in a project bullet and mention the API's purpose, integration and outcome."
        )

    if "git" in matched_skills or "github" in matched_skills:
        suggestions.append(
            "Keep Git/GitHub visible in the technical skills and project workflow where relevant."
        )

    suggestions.append(
        "Use job-specific keywords naturally across the Skills and Projects sections."
    )

    suggestions.append(
        "Add measurable impact to projects using numbers, percentages, performance improvements or scale where applicable."
    )

    return suggestions[:5]


# =========================================================
# PERSONALIZED FEEDBACK
# =========================================================

def generate_feedback(
    match_score: float,
    matched_skills: List[str],
    missing_skills: List[str]
) -> str:

    if not matched_skills and not missing_skills:
        return (
            "No recognizable skills were detected in the job description. "
            "Try adding specific technical requirements to the JD."
        )

    if match_score >= 80:
        feedback = (
            "Your resume is strongly aligned with the job description. "
            "You have a good match across the detected required skills."
        )

    elif match_score >= 60:
        feedback = (
            "Your resume has a good foundation for this role, "
            "but there are some skill gaps that should be addressed."
        )

    elif match_score >= 40:
        feedback = (
            "Your resume shows partial alignment with the target role. "
            "Improving the missing skills and tailoring your projects can significantly strengthen your profile."
        )

    else:
        feedback = (
            "Your current resume has limited alignment with this job description. "
            "Focus on the missing skills and build relevant projects before applying."
        )

    if missing_skills:
        feedback += (
            f" The analysis detected {len(missing_skills)} skill gap(s) "
            "that you should review."
        )

    return feedback


# =========================================================
# ANALYZE ENDPOINT
# =========================================================

@app.post("/analyze")
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):

    try:
        # ---------------- FILE VALIDATION ----------------

        if not resume.filename:
            return JSONResponse(
                status_code=400,
                content={"detail": "Resume file is required."}
            )

        if not resume.filename.lower().endswith(".pdf"):
            return JSONResponse(
                status_code=400,
                content={"detail": "Only PDF files are supported."}
            )

        # ---------------- PDF ----------------

        file_bytes = await resume.read()

        if len(file_bytes) > 5 * 1024 * 1024:
            return JSONResponse(
                status_code=400,
                content={"detail": "Resume PDF must be 5 MB or smaller."}
            )

        resume_text = extract_text_from_pdf(file_bytes)

        if not resume_text:
            return JSONResponse(
                status_code=400,
                content={
                    "detail": "Could not extract text from the resume PDF."
                }
            )

        # ---------------- JD VALIDATION ----------------

        job_description = job_description.strip()

        if len(job_description) < 50:
            return JSONResponse(
                status_code=400,
                content={
                    "detail":
                    "Job description must contain at least 50 characters."
                }
            )

        if len(job_description) > 15000:
            return JSONResponse(
                status_code=400,
                content={
                    "detail":
                    "Job description must contain at most 15000 characters."
                }
            )

        # ---------------- SKILL ANALYSIS ----------------

        (
            resume_skills,
            job_skills,
            matched_skills,
            missing_skills
        ) = compare_skills(
            resume_text,
            job_description
        )

        # ---------------- IMPROVEMENT AREAS ----------------

        skills_to_improve = get_skills_to_improve(
            missing_skills
        )

        # ---------------- SCORE ----------------

        match_score = calculate_match_score(
            matched_skills,
            job_skills
        )

        # ---------------- READINESS ----------------

        job_readiness = calculate_readiness_score(
            match_score,
            matched_skills,
            missing_skills
        )

        # ---------------- LEARNING ----------------

        recommended_learning = generate_learning_recommendations(
            missing_skills,
            skills_to_improve
        )

        # ---------------- RESUME SUGGESTIONS ----------------

        resume_suggestions = generate_resume_suggestions(
            missing_skills,
            matched_skills
        )

        # ---------------- FEEDBACK ----------------

        feedback = generate_feedback(
            match_score,
            matched_skills,
            missing_skills
        )

        # ---------------- FINAL RESPONSE ----------------

        return {
            "match_score": match_score,
            "job_readiness": job_readiness,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "skills_to_improve": skills_to_improve,
            "feedback": feedback,
            "recommended_learning": recommended_learning,
            "resume_suggestions": resume_suggestions,

            # Extra debugging/transparency fields.
            # The frontend can ignore these.
            "detected_resume_skills": resume_skills,
            "detected_job_skills": job_skills
        }

    except ValueError as e:
        return JSONResponse(
            status_code=400,
            content={"detail": str(e)}
        )

    except Exception as e:
        print("SERVER ERROR:", str(e))

        return JSONResponse(
            status_code=500,
            content={
                "detail":
                "An unexpected error occurred while analyzing the resume."
            }
        )
