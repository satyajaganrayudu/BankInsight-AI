const questionInput =
    document.getElementById("question");

const chat =
    document.getElementById("chat");

const sendButton =
    document.getElementById("sendButton");


async function sendQuestion() {

    const question =
        questionInput.value.trim();

    if (!question) {
        return;
    }

    addUserMessage(question);

    questionInput.value = "";

    addLoadingMessage();

    sendButton.disabled = true;

    try {

        const response = await fetch(
            "/api/ask",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    question: question
                })
            }
        );

        const data =
            await response.json();

        removeLoadingMessage();

        if (!response.ok) {

            addAIMessage(
                "Error: " +
                (data.error || "Something went wrong.")
            );

            return;
        }

        addAIMessage(
            data.answer,
            data.sources
        );

    }

    catch (error) {

        removeLoadingMessage();

        addAIMessage(
            "Unable to connect to the BankInsight AI server."
        );

        console.error(error);

    }

    finally {

        sendButton.disabled = false;

        questionInput.focus();

    }
}


function addUserMessage(message) {

    const div =
        document.createElement("div");

    div.className =
        "message user-message";

    div.innerHTML = `
        <div class="message-content">
            ${escapeHtml(message)}
        </div>
    `;

    chat.appendChild(div);

    scrollToBottom();
}


function addAIMessage(answer, sources = []) {

    const div =
        document.createElement("div");

    div.className =
        "message ai-message";

    let sourcesHTML = "";

    if (sources && sources.length > 0) {

        sourcesHTML = `
            <div class="sources">

                <h4>Sources</h4>

                ${sources.map(source => `
                    <div class="source-card">
                        <span>📄</span>
                        <div>
                            <strong>
                                Page ${source.page}
                            </strong>

                            <small>
                                ${escapeHtml(
                                    source.section || ""
                                )}
                            </small>
                        </div>
                    </div>
                `).join("")}

            </div>
        `;
    }

    div.innerHTML = `
        <div class="ai-avatar">
            🏦
        </div>

        <div class="message-content">

            <div class="answer">
                ${formatAnswer(answer)}
            </div>

            ${sourcesHTML}

        </div>
    `;

    chat.appendChild(div);

    scrollToBottom();
}


function addLoadingMessage() {

    const div =
        document.createElement("div");

    div.id = "loading";

    div.className =
        "message ai-message";

    div.innerHTML = `
        <div class="ai-avatar">
            🏦
        </div>

        <div class="typing">
            <span></span>
            <span></span>
            <span></span>
        </div>
    `;

    chat.appendChild(div);

    scrollToBottom();
}


function removeLoadingMessage() {

    const loading =
        document.getElementById("loading");

    if (loading) {
        loading.remove();
    }
}


function askExample(button) {

    questionInput.value =
        button.textContent;

    sendQuestion();
}


function scrollToBottom() {

    chat.scrollTop =
        chat.scrollHeight;
}


function formatAnswer(text) {

    return escapeHtml(text)
        .replace(/\n/g, "<br>")
        .replace(
            /\*\*(.*?)\*\*/g,
            "<strong>$1</strong>"
        );
}


function escapeHtml(text) {

    const div =
        document.createElement("div");

    div.textContent =
        text;

    return div.innerHTML;
}


questionInput.addEventListener(
    "keydown",
    function(event) {

        if (
            event.key === "Enter" &&
            !event.shiftKey
        ) {

            event.preventDefault();

            sendQuestion();
        }

    }
);