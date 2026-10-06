/* =========================================================
AI RESUME ANALYZER & JOB READINESS PLATFORM
FRONTEND LOGIC
   ========================================================= */


/* =========================================================
CONFIGURATION
   ========================================================= */

const API_URL = "https://ai-resume-analyzer-api-mbmr.onrender.com/analyze";

const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5 MB
const MIN_JD_LENGTH = 50;
const MAX_JD_LENGTH = 15000;


/* =========================================================
DOM ELEMENTS
   ========================================================= */

const resumeInput = document.getElementById("resume");
const fileName = document.getElementById("file-name");

const jobDescription = document.getElementById("job-description");
const characterCount = document.getElementById("character-count");

const analyzeButton = document.getElementById("analyze-btn");

const loading = document.getElementById("loading");
const results = document.getElementById("results");

const scoreElement = document.getElementById("score");
const readinessElement = document.getElementById("readiness-score");

const matchedCount = document.getElementById("matched-count");
const missingCount = document.getElementById("missing-count");
const improveCount = document.getElementById("improve-count");

const matchedSkills = document.getElementById("matched-skills");
const missingSkills = document.getElementById("missing-skills");
const improveSkills = document.getElementById("skills-to-improve");

const feedbackElement = document.getElementById("feedback-text");
const recommendationsList =
    document.getElementById("recommendation-list");

const suggestionsList =
    document.getElementById("suggestions-list");


/* =========================================================
INITIAL STATE
   ========================================================= */

document.addEventListener("DOMContentLoaded", () => {

    if (loading) {
        loading.classList.add("hidden");
    }

    if (results) {
        results.classList.add("hidden");
    }

    updateCharacterCount();

});


/* =========================================================
FILE UPLOAD
   ========================================================= */

if (resumeInput) {

    resumeInput.addEventListener("change", () => {

        const file = resumeInput.files[0];

        if (!file) {
            if (fileName) {
                fileName.textContent = "No file selected";
            }
            return;
        }


        /* Validate file type */

        const isPDF =
            file.type === "application/pdf" ||
            file.name.toLowerCase().endsWith(".pdf");

        if (!isPDF) {

            showError(
                "Please upload your resume in PDF format only."
            );

            resumeInput.value = "";

            if (fileName) {
                fileName.textContent = "No file selected";
            }

            return;
        }


        /* Validate file size */

        if (file.size > MAX_FILE_SIZE) {

            showError(
                "Resume file size must be less than 5 MB."
            );

            resumeInput.value = "";

            if (fileName) {
                fileName.textContent = "No file selected";
            }

            return;
        }


        /* Display selected filename */

        if (fileName) {

            fileName.textContent =
                `✓ ${file.name}`;

            fileName.style.color = "#4ade80";
        }


        clearError();
    });

}


/* =========================================================
JOB DESCRIPTION CHARACTER COUNTER
   ========================================================= */

if (jobDescription) {

    jobDescription.addEventListener(
        "input",
        updateCharacterCount
    );

}


function updateCharacterCount() {

    if (!jobDescription || !characterCount) {
        return;
    }

    const length = jobDescription.value.length;

    characterCount.textContent =
        `${length.toLocaleString()} / ${MAX_JD_LENGTH.toLocaleString()}`;


    /* Remove previous states */

    characterCount.classList.remove(
        "warning",
        "good"
    );


    /* Character status */

    if (length >= MIN_JD_LENGTH) {

        characterCount.classList.add("good");

    } else if (length > 0) {

        characterCount.classList.add("warning");

    }

}


/* =========================================================
ANALYZE BUTTON
   ========================================================= */

if (analyzeButton) {

    analyzeButton.addEventListener(
        "click",
        analyzeResume
    );

}


/* =========================================================
MAIN ANALYSIS FUNCTION
   ========================================================= */

async function analyzeResume() {

    clearError();


    /* -----------------------------------------------------
    Validate Resume
       ----------------------------------------------------- */

    if (!resumeInput || !resumeInput.files.length) {

        showError(
            "Please upload your resume PDF before starting the analysis."
        );

        return;
    }


    const resumeFile = resumeInput.files[0];


    /* -----------------------------------------------------
    Validate PDF
       ----------------------------------------------------- */

    const isPDF =
        resumeFile.type === "application/pdf" ||
        resumeFile.name.toLowerCase().endsWith(".pdf");

    if (!isPDF) {

        showError(
            "Only PDF resumes are supported."
        );

        return;
    }


    /* -----------------------------------------------------
    Validate File Size
       ----------------------------------------------------- */

    if (resumeFile.size > MAX_FILE_SIZE) {

        showError(
            "Resume file size must be less than 5 MB."
        );

        return;
    }


    /* -----------------------------------------------------
    Validate Job Description
       ----------------------------------------------------- */

    if (!jobDescription) {
        showError(
            "Job description field is unavailable."
        );
        return;
    }


    const jdText = jobDescription.value.trim();


    if (!jdText) {

        showError(
            "Please paste the job description."
        );

        jobDescription.focus();

        return;
    }


    if (jdText.length < MIN_JD_LENGTH) {

        showError(
            `Job description should contain at least ${MIN_JD_LENGTH} characters.`
        );

        jobDescription.focus();

        return;
    }


    if (jdText.length > MAX_JD_LENGTH) {

        showError(
            "Job description exceeds the maximum allowed length."
        );

        return;
    }


    /* -----------------------------------------------------
    Start Loading State
       ----------------------------------------------------- */

    setLoadingState(true);


    /* -----------------------------------------------------
    Prepare Form Data
       ----------------------------------------------------- */

    const formData = new FormData();

    formData.append(
        "resume",
        resumeFile
    );

    formData.append(
        "job_description",
        jdText
    );


    try {

        /* -------------------------------------------------
        Send Request To Backend
           ------------------------------------------------- */

        const response = await fetch(
            API_URL,
            {
                method: "POST",
                body: formData
            }
        );


        /* -------------------------------------------------
        Parse Response
           ------------------------------------------------- */

        let data;

        try {

            data = await response.json();

        } catch (jsonError) {

            throw new Error(
                "The server returned an invalid response."
            );

        }


        /* -------------------------------------------------
        Handle Backend Errors
           ------------------------------------------------- */

        if (!response.ok) {

            const backendMessage =
                data.detail ||
                data.message ||
                "Unable to analyze the resume.";

            throw new Error(
                backendMessage
            );
        }


        /* -------------------------------------------------
        Validate Response
           ------------------------------------------------- */

        if (!data) {

            throw new Error(
                "No analysis data was returned by the server."
            );
        }


        /* -------------------------------------------------
        Display Results
           ------------------------------------------------- */

        displayResults(data);


    } catch (error) {

        console.error(
            "Analysis Error:",
            error
        );


        let message =
            "Something went wrong while analyzing your resume.";


        /* Backend unavailable */

        if (
            error.message.includes("Failed to fetch") ||
            error.name === "TypeError"
        ) {

            message =
                "Unable to connect to the analysis server. Please make sure the Python backend is running.";

        } else if (error.message) {

            message =
                error.message;
        }


        showError(message);


    } finally {

        setLoadingState(false);

    }

}


```javascript```
function displayResults(data) {

    /* -----------------------------------------------------
    DEBUG — Check API response
    ----------------------------------------------------- */

    console.log("API RESPONSE:", data);


    /* -----------------------------------------------------
    Extract Scores
    ----------------------------------------------------- */

    const matchScore = Number(
        data.match_score ??
        data.resume_match_score ??
        0
    );

    const readinessScore = Number(
        data.job_readiness ??
        data.readiness_score ??
        0
    );


    /* -----------------------------------------------------
    Extract Skills
    ----------------------------------------------------- */

    const matched = normalizeArray(
        data.matched_skills
    );

    const missing = normalizeArray(
        data.missing_skills
    );

    const improve = normalizeArray(
        data.skills_to_improve
    );


    /* -----------------------------------------------------
    Extract Feedback
    ----------------------------------------------------- */

    const feedback =
        data.feedback ||
        data.personalized_feedback ||
        "Your profile has been analyzed successfully.";


    /* -----------------------------------------------------
    Extract Recommendations
    ----------------------------------------------------- */

    const recommendations = normalizeArray(
        data.recommended_learning ||
        data.recommendations
    );


    /* -----------------------------------------------------
    Extract Resume Suggestions
    ----------------------------------------------------- */

    const suggestions = normalizeArray(
        data.resume_suggestions ||
        data.suggestions
    );


    /* =====================================================
]SCORES
    ===================================================== */

    updateScore(
        scoreElement,
        matchScore
    );

    updateScore(
        readinessElement,
        readinessScore
    );


    /* =====================================================
    SUMMARY COUNTS
    ===================================================== */

    setText(
        matchedCount,
        matched.length
    );

    setText(
        missingCount,
        missing.length
    );

    setText(
        improveCount,
        improve.length
    );


    /* =====================================================
    MATCHED SKILLS
    ===================================================== */

    if (matchedSkills) {

        renderSkillTags(
            matchedSkills,
            matched,
            "matched"
        );

    }


    /* =====================================================
    MISSING SKILLS
    ===================================================== */

    if (missingSkills) {

        if (missing.length > 0) {

            renderSkillTags(
                missingSkills,
                missing,
                "missing"
            );

        } else {

            missingSkills.innerHTML = `
                <span class="empty-state">
                    No missing skills identified.
                </span>
            `;

        }

    }


    /* =====================================================
    SKILLS TO IMPROVE
    ===================================================== */

    if (improveSkills) {

        if (improve.length > 0) {

            renderSkillTags(
                improveSkills,
                improve,
                "improve"
            );

        } else {

            improveSkills.innerHTML = `
                <span class="empty-state">
                    No specific improvement areas identified.
                </span>
            `;

        }

    }


    /* =====================================================
    PERSONALIZED FEEDBACK
    ===================================================== */

    if (feedbackElement) {

        feedbackElement.textContent =
            feedback;

    }


    /* =====================================================
    RECOMMENDED LEARNING
    ===================================================== */

    if (recommendationsList) {

        renderRecommendations(
            recommendationsList,
            recommendations
        );

    }


    /* =====================================================
    RESUME IMPROVEMENT SUGGESTIONS
    ===================================================== */

    if (suggestionsList) {

        renderSuggestions(
            suggestionsList,
            suggestions
        );

    }


    /* =====================================================
    SHOW RESULTS
    ===================================================== */

    if (results) {

        results.classList.remove(
            "hidden"
        );


        /* Smooth scroll to results */

        setTimeout(() => {

            results.scrollIntoView({
                behavior: "smooth",
                block: "start"
            });

        }, 150);

    }

}




/* =========================================================
UPDATE SCORE
   ========================================================= */

function updateScore(
    element,
    score
) {

    if (!element) {
        return;
    }


    /* Keep score between 0 and 100 */

    score =
        Math.max(
            0,
            Math.min(
                100,
                score
            )
        );


    /* Display one decimal only when required */

    const formattedScore =
        Number.isInteger(score)
            ? score
            : score.toFixed(1);


    element.textContent =
        `${formattedScore}%`;


    /* Dynamic score styling */

    element.style.background =
        getScoreGradient(score);

    element.style.webkitBackgroundClip =
        "text";

    element.style.webkitTextFillColor =
        "transparent";

}


/* =========================================================
SCORE GRADIENT
   ========================================================= */

function getScoreGradient(score) {

    if (score >= 80) {

        return "linear-gradient(135deg, #22c55e, #4ade80)";

    }

    if (score >= 60) {

        return "linear-gradient(135deg, #38bdf8, #60a5fa)";

    }

    if (score >= 40) {

        return "linear-gradient(135deg, #f59e0b, #fbbf24)";

    }

    return "linear-gradient(135deg, #ef4444, #f87171)";
}


/* =========================================================
RENDER SKILL TAGS
   ========================================================= */

function renderSkillTags(
    container,
    skills,
    type
) {

    if (!container) {
        return;
    }


    container.innerHTML = "";


    if (!skills.length) {

        const empty =
            document.createElement("span");

        empty.className =
            "empty-state";


        if (type === "matched") {

            empty.textContent =
                "No matched skills detected.";

        } else if (type === "missing") {

            empty.textContent =
                "No major missing skills detected.";

        } else {

            empty.textContent =
                "No additional improvement areas detected.";
        }


        container.appendChild(
            empty
        );

        return;
    }


    skills.forEach(skill => {

        const tag =
            document.createElement("span");

        tag.className =
            "skill-tag";


        tag.textContent =
            skill;


        container.appendChild(
            tag
        );

    });

}


/* =========================================================
RENDER RECOMMENDATIONS
   ========================================================= */

function renderRecommendations(
    container,
    recommendations
) {

    if (!container) {
        return;
    }


    container.innerHTML = "";


    if (!recommendations.length) {

        const item =
            document.createElement("li");

        item.className =
            "recommendation-item";


        item.textContent =
            "No personalized learning recommendations available.";

        container.appendChild(
            item
        );

        return;
    }


    recommendations.forEach(
        (recommendation, index) => {

            const item =
                document.createElement("li");

            item.className =
                "recommendation-item";


            const number =
                document.createElement("span");

            number.className =
                "recommendation-number";

            number.textContent =
                index + 1;


            const text =
                document.createElement("span");

            text.textContent =
                recommendation;


            item.appendChild(
                number
            );

            item.appendChild(
                text
            );


            container.appendChild(
                item
            );

        }
    );

}


/* =========================================================
RENDER RESUME SUGGESTIONS
   ========================================================= */

function renderSuggestions(
    container,
    suggestions
) {

    if (!container) {
        return;
    }


    container.innerHTML = "";


    if (!suggestions.length) {

        const item =
            document.createElement("li");

        item.textContent =
            "No additional resume improvement suggestions.";

        container.appendChild(
            item
        );

        return;
    }


    suggestions.forEach(
        suggestion => {

            const item =
                document.createElement("li");

            item.textContent =
                suggestion;


            container.appendChild(
                item
            );

        }
    );

}


/* =========================================================
NORMALIZE ARRAY
   ========================================================= */

function normalizeArray(value) {

    if (Array.isArray(value)) {

        return value
            .filter(item => item !== null && item !== undefined)
            .map(item => String(item).trim())
            .filter(Boolean);

    }


    if (typeof value === "string") {

        return value
            .split(",")
            .map(item => item.trim())
            .filter(Boolean);

    }


    return [];

}


/* =========================================================
SET TEXT SAFELY
   ========================================================= */

function setText(
    element,
    value
) {

    if (!element) {
        return;
    }

    element.textContent =
        value;
}


/* =========================================================
LOADING STATE
   ========================================================= */

function setLoadingState(
    isLoading
) {

    if (!analyzeButton) {
        return;
    }


    if (isLoading) {

        analyzeButton.disabled =
            true;

        analyzeButton.dataset.originalText =
            analyzeButton.textContent;

        analyzeButton.textContent =
            "⏳ Analyzing Resume...";

        analyzeButton.style.opacity =
            "0.75";

        analyzeButton.style.cursor =
            "not-allowed";


        if (loading) {

            loading.classList.remove(
                "hidden"
            );
        }


        if (results) {

            results.classList.add(
                "hidden"
            );
        }

    } else {

        analyzeButton.disabled =
            false;

        analyzeButton.textContent =
            analyzeButton.dataset.originalText ||
            "🔍 Analyze Resume";

        analyzeButton.style.opacity =
            "1";

        analyzeButton.style.cursor =
            "pointer";


        if (loading) {

            loading.classList.add(
                "hidden"
            );
        }

    }

}


/* =========================================================
ERROR HANDLING
   ========================================================= */

function showError(
    message
) {

    clearError();


    const error =
        document.createElement("div");

    error.id =
        "frontend-error";

    error.className =
        "error-message";

    error.textContent =
        message;


    if (analyzeButton) {

        analyzeButton.insertAdjacentElement(
            "afterend",
            error
        );

    }


    /* Auto remove after 7 seconds */

    setTimeout(() => {

        if (error) {

            error.remove();

        }

    }, 7000);

}


/* =========================================================
CLEAR ERROR
   ========================================================= */

function clearError() {

    const existingError =
        document.getElementById(
            "frontend-error"
        );

    if (existingError) {

        existingError.remove();

    }

}


/* =========================================================
KEYBOARD SHORTCUT
   ========================================================= */

if (jobDescription) {

    jobDescription.addEventListener(
        "keydown",
        event => {

            /*
            Ctrl/Cmd + Enter
            = Analyze Resume
            */

            if (
                (event.ctrlKey || event.metaKey) &&
                event.key === "Enter"
            ) {

                event.preventDefault();

                analyzeResume();

            }

        }
    );

}


/* =========================================================
END
   ========================================================= */